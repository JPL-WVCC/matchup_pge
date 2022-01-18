#!/usr/bin/env python
from multiprocessing import Process
import multiprocessing
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
import argparse


ext = '.nc'

# --------------------------------------
def colocate_one_cris_granual(cris_file, viirs_dir, output_dir_root, day1):

  print (' --------- viirs_dir: ', viirs_dir)

  if True:
    cris_files = []
    cris_files.append(cris_file)
    ### print('type(cris_files): ', type(cris_files))
    print('cris_files: ', cris_files)

    f1 = cris_file
    ### print ('f1: ', f1)
    basename1 = os.path.splitext(os.path.basename(f1))[0]
    dir1 = os.path.join(output_dir_root, day1, basename1)
    ### print ('dir1: ', dir1)

    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.makedirs(dir1)

    ### shutil.copyfile(f1, os.path.join(dir1, basename1+ext))

    f = nc4.Dataset(f1, 'r')
    # 2017-10-01T00:00:00Z
    starttime = datetime.strptime(f.time_coverage_start, '%Y-%m-%dT%H:%M:%SZ')
    endtime = datetime.strptime(f.time_coverage_end, '%Y-%m-%dT%H:%M:%SZ')
    print ('starttime: ', starttime, ' , endtime: ', endtime)

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
    """
    print('type(viirs_files): ', type(viirs_files))
    """
    print('len(viirs_files): ', len(viirs_files))
    ### print('viirs_files: ', viirs_files)

    viirs_files_selected = []

    for f2 in viirs_files:
      ### print ('f2: ', f2)
      ff = nc4.Dataset(f2, 'r')
      v_starttime = datetime.strptime(ff.time_coverage_start, '%Y-%m-%dT%H:%M:%S.000Z')
      v_endtime = datetime.strptime(ff.time_coverage_end, '%Y-%m-%dT%H:%M:%S.000Z')
      """
      print ('v starttime: ', v_starttime)
      print ('v endtime: ', v_endtime)
      """

      if starttime <= v_endtime and endtime >= v_starttime:
        print ('v starttime: ', v_starttime, ' , v endtime: ', v_endtime)
        ### shutil.copyfile(f2, os.path.join(dir1, os.path.basename(f2)))
        viirs_files_selected.append(f2)

    print('viirs_files_selected: ', viirs_files_selected)

    ### sys.exit(0)

    # spawn co-location child process
    """
    cmd = '/home/leipan/anaconda3/bin/python /home/leipan/code_test_QY.py'
    p1 = subprocess.Popen(cmd, shell=True, cwd=dir1, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    out, err = p1.communicate()
    print('out: ', out)
    print('err: ', err)
    """

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

  start_time = time.time()

  parser = argparse.ArgumentParser(description='Process co-location of CrIS and VIIRS.')
  parser.add_argument('--y', metavar='YEAR', type=int, required=True, help='year')
  parser.add_argument('--m', metavar='MONTH', type=int, required=True, help='month')
  parser.add_argument('--d1', metavar='START DAY', type=int, required=True, help='start day')
  parser.add_argument('--d2', metavar='END DAY', type=int, required=True, help='end day')
  parser.add_argument('--cr', metavar='CrIS Root Dir', type=str, const='/peate_archive/NPPOps/snpp/gdisc/2/', help='CrIS root dir', nargs='?')
  parser.add_argument('--vr', metavar='VIIRS Root Dir', type=str, const='/raid15/leipan/VIIRS/VNP03MOD/', help='VIIRS root dir', nargs='?')
  parser.add_argument('--pr', metavar='Product Root Dir', type=str, const='/raid15/leipan/pair/20220116/', help='product root dir', nargs='?')
  parser.add_argument('--c', metavar='CPU COUNT', type=int, const=36, help='CPU count', nargs='?')
  args = parser.parse_args()

  print('year: ', args.y)
  print('month: ', args.m)
  print('start day: ', args.d1)
  print('end day: ', args.d2)
  print('CrIS root dir: ', args.cr)
  print('VIIRS root dir: ', args.vr)
  print('product root dir: ', args.pr)
  print('CPU count: ', args.c)


  # how many total cores to use for parallel processing
  chunk_size = multiprocessing.cpu_count()
  if chunk_size > args.c:
    chunk_size = args.c

  if args.pr == None:
    args.pr = '/raid15/leipan/products/20210116/'
  if args.cr == None:
    args.cr = '/peate_archive/NPPOps/snpp/gdisc/2/'
  if args.vr == None:
    args.vr = '/raid15/leipan/VIIRS/VNP03MOD/'

  print('CrIS root dir: ', args.cr)
  print('VIIRS root dir: ', args.vr)
  print('product root dir: ', args.pr)

  if os.path.exists(args.pr) == False:
    os.makedirs(args.pr)

  ### viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD.*'+ext))
  ### print ('viirs_geo_files: ', viirs_geo_files)
 
  """
  cris_geo_files = sorted(glob.glob(args.cr+str(args.y)+'/**/**/crisl1b/SNDR.SNPP.CRIS*L1B.std*'+ext))
  print ('cris_geo_files: ', cris_geo_files)
  print ('len(cris_geo_files): ', len(cris_geo_files))
  """

  print("done in --- %.2f seconds --- " % (float(time.time() - start_time)))

  month1 = str(args.m).zfill(2)

  for day in range (args.d1, args.d2+1):
    day1 = str(day).zfill(2)
    print('day1: ', day1)
    print(args.cr+str(args.y)+'/'+month1+'/'+day1+'/'+'crisl1b/SNDR.SNPP.CRIS')
    cris_geo_files = sorted(glob.glob(args.cr+str(args.y)+'/'+month1+'/'+day1+'/'+'crisl1b/SNDR.SNPP.CRIS*L1B.std*'+ext))
    ### print ('cris_geo_files: ', cris_geo_files)
    print ('len(cris_geo_files): ', len(cris_geo_files))

    ### sys.exit()

    chunks = [cris_geo_files[x:x+chunk_size] for x in range(0, len(cris_geo_files), chunk_size)]
    for cris_files in chunks:
      processes = []
      for cris_file in cris_files:
        ### colocate_one_cris_granual(cris_file, args.vr+str(args.y)+'/', args.pr, day1)

        p1 = Process(target=colocate_one_cris_granual, args=(cris_file, args.vr+str(args.y)+'/', args.pr, day1))
        processes.append(p1)

      for p in processes:
        p.start()

      for p in processes:
        p.join()

