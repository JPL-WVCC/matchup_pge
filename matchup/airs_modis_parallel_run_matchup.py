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
import logging

sys.path.append('/home/leipan/pge/CrIS_VIIRS_collocation-master/')
sys.path.append('/home/leipan/pge/AIRS_MODIS_collocation-master/')
from code_test_QY import call_match_cris_viirs
from geo_airs_modis_ncloud import call_match_airs_modis
from geo import read_airs_time, read_modis_time


module_logger = logging.getLogger("airs_modis_parallel_run_matchup.airs_modis_parallel_run_matchup")

ext = '.nc'
ext1 = '.hdf'

# --------------------------------------
def colocate_one_airs_granual(airs_file, modis_dir, output_dir_root):
  
  print (' --------- modis_dir: ', modis_dir)
  
  if True:
    airs_files = []
    airs_files.append(airs_file)
    print('airs_files: ', airs_files)
    
    # example: AIRS.2016.01.30.240.L1B.AIRS_Rad.v5.0.23.0.G16031113544.hdf
    f1 = airs_file
    ### print ('f1: ', f1)
    basename1 = os.path.splitext(os.path.basename(f1))[0]
    basename1_split = basename1.split('.')
    year1 = basename1_split[1]
    month1 = basename1_split[2]
    day1 = basename1_split[3]

    pos1 = basename1.find('.L1B')
    subdir1 = basename1[:pos1]
    print('subdir1: ', subdir1)

    ### dir1 = os.path.join(output_dir_root, str(year1), str(month1), str(day1), basename1)
    dir1 = os.path.join(output_dir_root, str(year1), str(month1), str(day1), subdir1)
    ### print ('dir1: (if exists delete it)', dir1)
    print ('dir1: (if exists skip it)', dir1)

    """
    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.makedirs(dir1)
    """

    # open f1 the AIRS hdf file and get start/end time
    time1 = read_airs_time(airs_files)
    print('time1: ', time1)
    starttime = time1[0][0]
    starttime = datetime(1993,1,1,0,0) + timedelta(seconds=starttime)
    endtime = time1[-1][-1]
    endtime = datetime(1993,1,1,0,0) + timedelta(seconds=endtime)

    ### starttime = datetime.strptime(starttime, '%Y-%m-%dT%H:%M:%SZ')
    ### endtime = datetime.strptime(endtime, '%Y-%m-%dT%H:%M:%SZ')
    print ('starttime: ', starttime, ' , endtime: ', endtime)

    # get the 3 consecutive days that span the AIRS date
    # get all the MODIS files in those 3 days
    delta1 = timedelta(days=1)
    starttime_minus1 = starttime - delta1
    starttime_plus1 = starttime + delta1
    ### day_of_year_minus1 = starttime_minus1.timetuple().tm_yday 

    year_minus1 = starttime_minus1.year
    month_minus1 = starttime_minus1.month
    day_minus1 = starttime_minus1.day

    year_plus1 = starttime_plus1.year
    month_plus1 = starttime_plus1.month
    day_plus1 = starttime_plus1.day

    ### day_of_year = starttime.timetuple().tm_yday 
    ### day_of_year_plus1 = starttime_plus1.timetuple().tm_yday 

    ### print ('day_of_year_minus1: ', day_of_year_minus1)
    print ('year_minus1: ', year_minus1)
    print ('month_minus1: ', month_minus1)
    print ('day_minus1: ', day_minus1)
    ### print ('day_of_year: ', day_of_year)
    ### print ('day_of_year_plus1: ', day_of_year_plus1)

    dir11 = modis_dir+str(year_minus1).zfill(4)+'/'+str(month_minus1).zfill(2)+'/'+str(day_minus1).zfill(2)+'/'+'aqua_modis_myd03/'
    print('dir11: ', dir11)
    modis_geo_files1 = sorted(glob.glob(dir11+'MYD03.*'+ext1))
    ### print('modis_geo_files1: ', modis_geo_files1)
    print('len(modis_geo_files1): ', len(modis_geo_files1))

    dir2 = modis_dir+str(year1).zfill(4)+'/'+str(month1).zfill(2)+'/'+str(day1).zfill(2)+'/'+'aqua_modis_myd03/'
    print('dir2: ', dir2)
    modis_geo_files2 = sorted(glob.glob(dir2+'MYD03.*'+ext1))
    print('len(modis_geo_files2): ', len(modis_geo_files2))

    dir3 = modis_dir+str(year_plus1).zfill(4)+'/'+str(month_plus1).zfill(2)+'/'+str(day_plus1).zfill(2)+'/'+'aqua_modis_myd03/'
    print('dir3: ', dir3)
    modis_geo_files3 = sorted(glob.glob(dir3+'MYD03.*'+ext1))
    print('len(modis_geo_files3): ', len(modis_geo_files3))

    modis_geo_files = modis_geo_files1 + modis_geo_files2 + modis_geo_files3
    ### print('modis_geo_files: ', modis_geo_files)
    print('len(modis_geo_files): ', len(modis_geo_files))

    modis_files_selected = []
    v_times = []

    for f2 in modis_geo_files:
      l2 = []
      l2.append(f2)
      ### print('f2: ', f2)
      ### print('l2: ', l2)
      time2 = read_modis_time(l2)
      if len(time2) > 0:
        ### print('time2: ', time2)
        v_starttime = time2[0]
        v_starttime = datetime(1993,1,1,0,0) + timedelta(seconds=v_starttime)
        v_endtime = time2[-1]
        v_endtime = datetime(1993,1,1,0,0) + timedelta(seconds=v_endtime)

        if starttime <= v_endtime and endtime >= v_starttime:
          modis_files_selected.append(f2)
          v_times.append(v_starttime)
          v_times.append(v_endtime)

    print('modis_files_selected: ', modis_files_selected)

    if len(modis_files_selected) > 0:

      # if exists, assume the product is good, either from a previous run (that is, this is a restart run),
      # or from a redundent AIRS granule, such as
      # /archive/AIRSOps/airs/gdaac/v5/2020/08/01/airibrad/AIRS.2020.08.01.189.L1B.AIRS_Rad.v5.0.23.0.G20215141841.hdf
      # /archive/AIRSOps/airs/gdaac/v5/2020/08/01/airibrad/AIRS.2020.08.01.007.L1B.AIRS_Rad.v5.0.25.0.G20307183952.hdf
      if os.path.exists(dir1):
        print('****** INFO: product already produced from previous run: ', dir1)
        return
      else:
        try:
          os.makedirs(dir1)
        except FileExistsError: # dir1 could be made by another parallel process
          return

      # write to manifest file
      mfile_name = os.path.join(dir1, 'manifest.mf')
      with open(mfile_name, 'w') as f:
        f.write('AIRS granule:')
        f.write(airs_files[0])
        f.write('\nAIRS time duration:')
        f.write(str(starttime))
        f.write(',')
        f.write(str(endtime))
        f.write('\nMODIS granules:')
        for vf in modis_files_selected:
          f.write(vf)
          f.write(',')
        f.write('\nMODIS time durations:')
        for t1 in v_times:
          f.write(str(t1))
          f.write(',')
        f.write('\n')

      ### sys.exit(0)

      # call colocation func
      call_match_airs_modis(airs_files, modis_files_selected, day1, 1, dir1)




# end of colocate_one_airs_granual()



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
    v_times = []

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
        v_times.append(v_starttime)
        v_times.append(v_endtime)

    print('viirs_files_selected: ', viirs_files_selected)

    # write to manifest file
    mfile_name = os.path.join(dir1, 'manifest.mf')
    with open(mfile_name, 'w') as f:
      f.write('CrIS granule:')
      f.write(cris_files[0])
      f.write('\nCrIS time duration:')
      f.write(str(starttime))
      f.write(',')
      f.write(str(endtime))
      f.write('\nVIIRS granules:')
      for vf in viirs_files_selected:
        f.write(vf)
        f.write(',')
      f.write('\nVIIRS time durations:')
      for t1 in v_times:
        f.write(str(t1))
        f.write(',')
      f.write('\n')

    ### sys.exit(0)

    # call colocation func
    call_match_cris_viirs(cris_files, viirs_files_selected, dir1)

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

# end of colocate_one_cris_granual()



if __name__ == '__main__':

  start_time = time.time()

  parser = argparse.ArgumentParser(description='Process co-location of CrIS and VIIRS.')
  parser.add_argument('--y', metavar='YEAR', type=int, required=True, help='year')
  parser.add_argument('--m', metavar='MONTH', type=int, required=True, help='month')
  parser.add_argument('--d1', metavar='START DAY', type=int, required=True, help='start day')
  parser.add_argument('--d2', metavar='END DAY', type=int, required=True, help='end day')
  ### parser.add_argument('--pr', metavar='Product Root Dir', type=str, const='/raid15/leipan/products/20220117/', help='product root dir', nargs='?')
  parser.add_argument('--pr', metavar='Product Root Dir', type=str, const='/raid15/leipan/products/dev/', help='product root dir', nargs='?')
  parser.add_argument('--c', metavar='CPU COUNT', type=int, const=36, help='CPU count', nargs='?')
  parser.add_argument('--ar', metavar='AIRS Root Dir', type=str, const='/archive/AIRSOps/airs/gdaac/v5/', help='AIRS root dir', nargs='?')
  parser.add_argument('--mr', metavar='MODIS Root Dir', type=str, const='/peate_archive/NPPOps/aqua_modis/laads/061/', help='MODIS root dir', nargs='?')

  args = parser.parse_args()

  # /archive/AIRSOps/airs/gdaac/v5/2016/01/21/airibrad/AIRS.2016.01.21.111.L1B.AIRS_Rad.v5.0.23.0.G16022093745.hdf
  ### airs_file = 'AIRS.2016.01.21.111.L1B.AIRS_Rad.v5.0.23.0.G16022093745.hdf'
  # /archive/AIRSOps/airs/gdaac/v5/2017/10/21/airibrad/AIRS.2017.10.21.192.L1B.AIRS_Rad.v5.0.23.0.G17295112219.hdf
  airs_file = '/archive/AIRSOps/airs/gdaac/v5/2017/10/21/airibrad/AIRS.2017.10.21.192.L1B.AIRS_Rad.v5.0.23.0.G17295112219.hdf'
  ### airs_file = 'AIRS.2019.09.09.216.L1B.AIRS_Rad.v5.0.23.0.G19253112146.hdf'
  ### airs_file = 'AIRS.2019.09.23.229.L1B.AIRS_Rad.v5.0.23.0.G19267111452.hdf'
  ### airs_file = 'AIRS.2018.09.16.050.L1B.AIRS_Rad.v5.0.23.0.G18259112808.hdf'

  ### MYD03.A2019252.1950.061.2019253151407.hdf'
  ### airs_file = 'AIRS.2019.11.09.050.L1B.AIRS_Rad.v5.0.23.0.G19313102440.hdf'

  modis_dir = args.mr
  output_dir_root = args.pr
  day1 = args.d1

  if args.mr == None:
    args.mr = '/peate_archive/NPPOps/aqua_modis/laads/061/'

  print('airs_file: ', airs_file)
  print('args.mr: ', args.mr)
  print('output_dir_root: ', output_dir_root)
  print('day1: ', day1)

  """
  colocate_one_airs_granual(airs_file, args.mr, output_dir_root)
  sys.exit(0)
  """

  # how many total cores to use for parallel processing
  chunk_size = multiprocessing.cpu_count()
  if chunk_size > args.c:
    chunk_size = args.c

  if args.pr == None:
    args.pr = '/raid15/leipan/products/dev/'
  if args.ar == None:
    args.ar = '/archive/AIRSOps/airs/gdaac/v5/'
  if args.mr == None:
    args.mr = '/peate_archive/NPPOps/aqua_modis/laads/061/'

  print('AIRS root dir: ', args.ar)
  print('MODIS root dir: ', args.mr)
  print('product root dir: ', args.pr)
  print('year: ', args.y)
  print('month: ', args.m)
  print('start day: ', args.d1)
  print('end day: ', args.d2)
  print('CPU count: ', args.c)

  if os.path.exists(args.pr) == False:
    os.makedirs(args.pr)

  month1 = str(args.m).zfill(2)

  PARALLEL = True
  ### PARALLEL = False

  for day in range (args.d1, args.d2+1):
    day1 = str(day).zfill(2)
    print('day1: ', day1)
    print(args.ar+str(args.y)+'/'+month1+'/'+day1+'/'+'airibrad/')

    ### airs_geo_files = sorted(glob.glob(args.ar+str(args.y)+'/'+month1+'/'+day1+'/'+'airibrad/AIRS.*L1B.AIRS*.23.*'+ext1)) # for 2020, 2017
    ### airs_geo_files = sorted(glob.glob(args.ar+str(args.y)+'/'+month1+'/'+day1+'/'+'airibrad/AIRS.*L1B.AIRS*.22.*'+ext1)) # for 2015/01

    airs_geo_files = sorted(glob.glob(args.ar+str(args.y)+'/'+month1+'/'+day1+'/'+'airibrad/AIRS.*L1B.AIRS*.*'+ext1)) # for 2020/08/01

    ### print ('airs_geo_files: ', airs_geo_files)
    print ('len(airs_geo_files): ', len(airs_geo_files))

    ### sys.exit()

    chunks = [airs_geo_files[x:x+chunk_size] for x in range(0, len(airs_geo_files), chunk_size)]
    for airs_files in chunks:
      processes = []
      for airs_file in airs_files:
        if PARALLEL is False:
          ### colocate_one_cris_granual(cris_file, args.vr+str(args.y)+'/', args.pr+str(args.y)+'/'+month1+'/', day1)
          colocate_one_airs_granual(airs_file, args.mr, output_dir_root)
        else:
          ### p1 = Process(target=colocate_one_cris_granual, args=(cris_file, args.vr+str(args.y)+'/', args.pr+str(args.y)+'/'+month1+'/', day1))
          p1 = Process(target=colocate_one_airs_granual, args=(airs_file, args.mr, output_dir_root))
          processes.append(p1)

      if PARALLEL is True:
        for p in processes:
          p.start()

        for p in processes:
          p.join()

  print("done in --- %.2f seconds --- " % (float(time.time() - start_time)))


