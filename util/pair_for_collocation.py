#!/usr/bin/env python
import glob
import time
import os,sys
import shutil
import netCDF4 as nc4
import json
from datetime import datetime
import os
import stat

ext = '.nc'

# --------------------------------------
def pair_create_dataset(cris_files, viirs_files, output_dir_root):

  for f1 in cris_files:
    ### print ('f1: ', f1)
    basename1 = os.path.splitext(os.path.basename(f1))[0]
    dir1 = os.path.join(output_dir_root, basename1)
    print ('dir1: ', dir1)

    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.mkdir(dir1)
    shutil.copyfile(f1, os.path.join(dir1, basename1+ext))

    f = nc4.Dataset(f1, 'r')
    ### print ('starttime: ', f.time_coverage_start)
    ### print ('endtime: ', f.time_coverage_end)
    ### print ('bounds: ', f.geospatial_bounds)

    # 2017-10-01T00:00:00Z
    starttime = datetime.strptime(f.time_coverage_start, '%Y-%m-%dT%H:%M:%SZ')
    endtime = datetime.strptime(f.time_coverage_end, '%Y-%m-%dT%H:%M:%SZ')
    print ('starttime: ', starttime)
    print ('endtime: ', endtime)

    print ('---------------')
    for f2 in viirs_files:
      ff = nc4.Dataset(f2, 'r')
      ### print ('v starttime: ', ff.time_coverage_start)
      ### print ('v endtime: ', ff.time_coverage_end)
      ### print ('v south bound: ', ff.SouthBoundingCoordinate)

      v_starttime = datetime.strptime(ff.time_coverage_start, '%Y-%m-%dT%H:%M:%S.000Z')
      v_endtime = datetime.strptime(ff.time_coverage_end, '%Y-%m-%dT%H:%M:%S.000Z')

      ### print ('v starttime: ', v_starttime)
      ### print ('v endtime: ', v_endtime)

      if starttime <= v_endtime and endtime >= v_starttime:
        print ('v starttime: ', v_starttime)
        print ('v endtime: ', v_endtime)
        shutil.copyfile(f2, os.path.join(dir1, os.path.basename(f2)))

    ### sys.exit()



if __name__ == '__main__':

  pair_dir_root = '/raid15/leipan/pair/20211126/'
  if os.path.exists(pair_dir_root) == False:
    os.makedirs(pair_dir_root)

  # two months for Qing
  ### dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2017/10/'
  ### dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2020/08/'
  dataDir4='/raid15/leipan/VIIRS/VNP03MOD/2017/010/'
  viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD.*'+ext))
  ### print ('viirs_geo_files: ', viirs_geo_files)
 
  # get CrIS files
  dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2017/10/'
  ### cris_geo_files = sorted(glob.glob(dataDir2+'SNDR*1809042004*'))
  cris_geo_files = sorted(glob.glob(dataDir2+'**/**/SNDR.SNPP.CRIS*L1B_NSR*'+ext))
  ### print ('cris_geo_files: ', cris_geo_files)

  pair_create_dataset(cris_geo_files, viirs_geo_files, pair_dir_root)

  # get VIIRS files
  ### viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD*201726106455*'))
  """
  viirs_geo_files = sorted(glob.glob(dataDir4+'/VNP03MOD*'+ext))
  print ('viirs_geo_files: ', viirs_geo_files)
  create_dataset(viirs_geo_files, pair_dir_root, scriptfile1)
  """


