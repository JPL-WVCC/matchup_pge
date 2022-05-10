#!/usr/bin/python

import os,sys
import fnmatch
import netCDF4 as nc4
import datetime
import shlex, subprocess, shutil
import numpy as np

### root_dir = './test_output/'
### root_dir = '/raid15/leipan/products/20220504/'
### root_dir = '/raid15/leipan/products/20220117/'
root_dir = 'tmp/'
year1 = '2015'
month1 = '11'
### year1 = '2020'
### month1 = '08'
root_dir += year1 + '/' + month1 + '/'

### root_dir = './tmp/'

print ('------------- root_dir: ' + root_dir)
### sys.exit()

nc_fname = ''
manifest_fname = ''

for root, dir, files in os.walk(root_dir):
  if 'SNDR.SNPP.' in root:
    ### print ('------------- ' + root)
    ### print ("")

    for items in fnmatch.filter(files, '*'):

      # look for nc file
      if '.nc' in items:
        nc_fname = os.path.join(root, items)
        ### print ("... nc ... " + nc_fname)

    # found nc file
    if nc_fname != '':
      print ("--- got it ---")
      print (nc_fname)
      nc_basename = os.path.basename(nc_fname)
      nc_dir = nc_fname.replace(nc_basename, '')
      print ('nc_basename: ', nc_basename)
      print ('nc_dir: ', nc_dir)
      tmp_file = os.path.join(nc_dir, 'tmp.nc')
      cmd = 'h5repack -i ' + nc_fname + ' -o ' + tmp_file + ' -f GZIP=5'
      print ('cmd: ', cmd)

      args = shlex.split(cmd)
      p = subprocess.Popen(args)
      rc=p.wait()
      print('rc: ', rc)

      dest = shutil.move(tmp_file, nc_fname)
      print('dest: ', dest)

      # h5repack -i IND_CrIS_VIIRSMOD_SNDR.SNPP.20171129T2106.g212.nc -o test.nc -f GZIP=5
      print ("-----------------------------------------")
      print ("")
