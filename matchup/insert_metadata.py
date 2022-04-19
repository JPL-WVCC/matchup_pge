#!/usr/bin/python

import os
import fnmatch
import netCDF4 as nc4
import datetime
import shlex, subprocess
import numpy as np

### root_dir = './test_output/'
root_dir = './tmp/'
nc_fname = ''
manifest_fname = ''

for root, dir, files in os.walk(root_dir):
  if 'SNDR.SNPP.' in root:
    ### print ('------------- ' + root)
    ### print ("")

    for items in fnmatch.filter(files, '*'):
      # look for mf file
      if 'manifest.mf' in items:
        manifest_fname = os.path.join(root, items)
        ### print ("... manifest ... " + manifest_fname)

      # look for nc file
      if '.nc' in items:
        nc_fname = os.path.join(root, items)
        ### print ("... nc ... " + nc_fname)

    # found both files under the same root
    if nc_fname != '' and manifest_fname != '':
      print ("--- got it ---")
      print (manifest_fname)
      print (nc_fname)

      # open manifest file for input
      cris_filename = ''
      viirs_filenames = ''
      with open(manifest_fname) as f:
        lines = f.readlines()

      for line1 in lines:
        if 'CrIS granule' in line1:
          cris_filename = line1
        if 'VIIRS granules' in line1:
          viirs_filenames = line1

      cris_filename = cris_filename.split(':')[1]
      cris_filename = os.path.basename(cris_filename)
      cris_filename = cris_filename.replace('\n', '')
      print('cris_filename: ', cris_filename)

      viirs_filenames = viirs_filenames.split(':')[1]
      viirs_filenames = viirs_filenames.split(',')
      for i, fn in enumerate(viirs_filenames):
        fn = os.path.basename(fn)
        viirs_filenames[i] = fn
 
      print('viirs_filenames: ', viirs_filenames)

      # insert global attributes into nc file using info from manifest file
      f = nc4.Dataset(nc_fname, 'r+', format='NETCDF4')

      f.VERSION = '1.0'
      f.IDENTIFIER_PRODUCT_DOI_AUTHORITY = "http://dx.doi.org/"
      f.IDENTIFIER_PRODUCT_DOI = "10.5067/MEASURES/WVCC/DATA211"

      ct = datetime.datetime.now()
      f.PRODUCTIONDATE = ct.isoformat()

      f.CRIS_FILE = cris_filename
      f.VIIRS_FILE1 = viirs_filenames[0]
      f.VIIRS_FILE2 = viirs_filenames[1]
      f.VIIRS_FILE3 = viirs_filenames[2]
      nf = np.int32(3)
      f.VIIRS_FILES_COUNT = nf

      # start/end times
      cris_startt = f.cris_start_time
      cris_endt = f.cris_end_time

      f.RANGEBEGINNINGDATE = cris_startt.split('T')[0]
      f.RANGEBEGINNINGTIME = cris_startt.split('T')[1].replace('Z', '')
      f.RANGEENDINGDATE = cris_endt.split('T')[0]
      f.RANGEENDINGTIME = cris_endt.split('T')[1].replace('Z', '')

      f.NORTHBOUNDINGCOORDINATE = f.cris_max_lat.item()
      f.SOUTHBOUNDINGCOORDINATE = f.cris_min_lat.item()
      f.EASTBOUNDINGCOORDINATE  = f.cris_max_lon.item()
      f.WESTBOUNDINGCOORDINATE  = f.cris_min_lon.item()

      f.TIME_TOLERANCE = "900 seconds"
      f.DISTANCE_TOLERANCE = "CrIS FOV size angle 0.963 deg divided by 2"

      f.description = "Version-1 SNPP VIIRS-CrIS collocation index product by the project of Multidecadal Satellite Record of Water Vapor, Temperature, and Clouds (PI: Eric Fetzer) funded by NASA’s Making Earth System Data Records for Use in Research Environments (MEaSUREs) Program following Wang et al. (2016, https://doi.org/10.3390/rs8010076) and Yue et al. (2022, https://doi.org/10.5194/amt-15-2099-2022)."

      f.close()

      # now remove the following global attributes
      attr_list = ['cris_start_time', 'cris_end_time', 'viirs_file_names', 'cris_file_name', 'cris_min_lat', 'cris_min_lon', 'cris_max_lat', 'cris_max_lon']
      # sample command: ncatted -O -h -a cris_min_lat,global,d,, -a cris_min_lon,global,d,, -a cris_max_lat,global,d,, -a cris_max_lon,global,d,, IND_CrIS_VIIRSMOD_SNDR.SNPP.20180301T0100.g011.nc
      cli1 = 'ncatted -O -h '
      for at1 in attr_list:
        cli1 += '-a ' + at1 + ',global,d,, '
      cli1 += nc_fname
      print ('cli1: ', cli1)

      args = shlex.split(cli1)
      p = subprocess.Popen(args)
      rc=p.wait()
      ### print(p)

      # reset filenames
      nc_fname = ''
      manifest_fname = ''

      print ("-----------------------------------------")
      print ("")
