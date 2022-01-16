#!/usr/bin/env python
from multiprocessing import Process
import subprocess
import glob
import time
import os,sys
import shutil
import netCDF4 as nc4
import json
from datetime import datetime,timedelta
import os
import stat

ext = '.nc'

# --------------------------------------
def pair_one_cris(cris_file, viirs_dir, output_dir_root, day1):

  if True:
    f1 = cris_file
    ### print ('f1: ', f1)
    basename1 = os.path.splitext(os.path.basename(f1))[0]
    dir1 = os.path.join(output_dir_root, day1, basename1)
    ### print ('dir1: ', dir1)

    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.makedirs(dir1)
    shutil.copyfile(f1, os.path.join(dir1, basename1+ext))

    f = nc4.Dataset(f1, 'r')
    # 2017-10-01T00:00:00Z
    starttime = datetime.strptime(f.time_coverage_start, '%Y-%m-%dT%H:%M:%SZ')
    endtime = datetime.strptime(f.time_coverage_end, '%Y-%m-%dT%H:%M:%SZ')
    ### print ('starttime: ', starttime)
    ### print ('endtime: ', endtime)

    # get the 3 consecutive days that span the cris date
    # get all the viirs files in those 3 days
    delta1 = timedelta(days=1)
    starttime_m1 = starttime - delta1
    starttime_p1 = starttime + delta1
    day_of_year_m1 = starttime_m1.timetuple().tm_yday 
    day_of_year = starttime.timetuple().tm_yday 
    day_of_year_p1 = starttime_p1.timetuple().tm_yday 

    """
    print ('day_of_year_m1: ', day_of_year_m1)
    print ('day_of_year: ', day_of_year)
    print ('day_of_year_p1: ', day_of_year_p1)
    """

    viirs_geo_files1 = sorted(glob.glob(viirs_dir+str(day_of_year_m1).zfill(3)+'/'+'VNP03MOD.*'+ext))
    viirs_geo_files2 = sorted(glob.glob(viirs_dir+str(day_of_year).zfill(3)+'/'+'VNP03MOD.*'+ext))
    viirs_geo_files3 = sorted(glob.glob(viirs_dir+str(day_of_year_p1).zfill(3)+'/'+'VNP03MOD.*'+ext))

    viirs_files = viirs_geo_files1+viirs_geo_files2+viirs_geo_files3
    ### print('viirs_files: ', viirs_files)

    ### print ('---------------')

    for f2 in viirs_files:
      ### print ('f2: ', f2)
      ff = nc4.Dataset(f2, 'r')
      v_starttime = datetime.strptime(ff.time_coverage_start, '%Y-%m-%dT%H:%M:%S.000Z')
      v_endtime = datetime.strptime(ff.time_coverage_end, '%Y-%m-%dT%H:%M:%S.000Z')
      ### print ('v starttime: ', v_starttime)
      ### print ('v endtime: ', v_endtime)

      if starttime <= v_endtime and endtime >= v_starttime:
        """
        print ('v starttime: ', v_starttime)
        print ('v endtime: ', v_endtime)
        """
        shutil.copyfile(f2, os.path.join(dir1, os.path.basename(f2)))

    # spawn co-location child process
    cmd = '/home/leipan/anaconda3/bin/python /home/leipan/code_test_QY.py'
    p1 = subprocess.Popen(cmd, shell=True, cwd=dir1, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p1.communicate()
    print('out: ', out)
    print('err: ', err)

    # check to make sure that under dir1 there are 4 files
    """
    cnt = len([name for name in os.listdir(dir1) if os.path.isfile(name)])
    if cnt != 4:
      print('Warning: there are {0} files under {1}, not 4 as expected!'.format(cnt, dir1))

    for name in os.listdir(dir1):
      if os.path.isdir(name):
        cnt = len([name for name in os.listdir(os.path.join(dir1, name)) if os.path.isfile(name)])
        if cnt != 3:
          print('Warning: there are {0} files under {1}, not 4 as expected!'.format(cnt, os.path.join(dir1, name)))
    """



if __name__ == '__main__':

  chunk_size = 30

  ### pair_dir_root = '/raid15/leipan/pair/202008/'
  pair_dir_root = '/raid15/leipan/pair/201710/'

  if os.path.exists(pair_dir_root) == False:
    os.makedirs(pair_dir_root)

  # two months for Qing
  # 2017/10
  dataDir4='/raid15/leipan/VIIRS/VNP03MOD/2017/'
  dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2017/10/'

  # 2020/08
  ### dataDir4='/raid15/leipan/VIIRS/VNP03MOD/2020/'
  ### dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2020/08/'

  ### viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD.*'+ext))
  ### print ('viirs_geo_files: ', viirs_geo_files)
 
  # get CrIS files
  ### cris_geo_files = sorted(glob.glob(dataDir2+'SNDR*1809042004*'))
  ### cris_geo_files = sorted(glob.glob(dataDir2+'**/**/SNDR.SNPP.CRIS*L1B_NSR*'+ext))
  ### print ('cris_geo_files: ', cris_geo_files)

  for day in range (1, 32):
    day1 = str(day).zfill(2)
    ### print('day1: ', day1)
    cris_geo_files = sorted(glob.glob(dataDir2+day1+'/'+'**/SNDR.SNPP.CRIS*L1B_NSR*'+ext))
    ### print ('cris_geo_files: ', cris_geo_files)
    ### print ('len(cris_geo_files): ', len(cris_geo_files))

    chunks = [cris_geo_files[x:x+chunk_size] for x in range(0, len(cris_geo_files), chunk_size)]
    for cris_files in chunks:
      processes = []
      for cris_file in cris_files:
        p1 = Process(target=pair_one_cris, args=(cris_file, dataDir4, pair_dir_root, day1))
        processes.append(p1)

      for p in processes:
        p.start()

      for p in processes:
        p.join()

