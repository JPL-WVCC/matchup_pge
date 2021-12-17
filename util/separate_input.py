#!/usr/bin/env python
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
def move_input_granules(src_input_dir_root, input_dir_root):

  print('in func, input_dir_root: ', input_dir_root)

  subdirs = sorted(glob.glob(src_input_dir_root+'/**'))
  ### print('subdirs: ', subdirs)

  mv_cnt = 0
  rm_cnt = 0

  cnt1 = 0
  for d1 in subdirs:  # '/raid15/leipan/pair/201710/'
    """
    cnt1 += 1
    if cnt1 > 3:
      break
    """
    day1 = d1.split('/')[-1]  # '01'
    print ('day1: ', day1)
    cris_name_subdirs = sorted(glob.glob(d1+'/**'))
    ### print ('cris_name_subdirs: ', cris_name_subdirs)
    cnt2 = 0
    for c_subdir in cris_name_subdirs:  # '/raid15/leipan/pair/201710/02/SNDR.SNPP.CRIS.20171002T0006.m06.g002.L1B_NSR.std.v02_05.G.180623060846'
      """
      cnt2 += 1
      if cnt2 > 3:
        break
      """
      print ('c_subdir: ', c_subdir)
      prod_dir_name = c_subdir.split('/')[-1]
      print ('prod_dir_name: ', prod_dir_name)
      input_files = sorted(glob.glob(c_subdir+'/*.nc'))
      for src_file_name in input_files:  # '/raid15/leipan/pair/201710/01/SNDR.SNPP.CRIS.20171001T2354.m06.g240.L1B_NSR.std.v02_05.G.180623065059/VNP03MOD.A2017274.2348.001.2018002163618.nc'
        ### print('src_file_name: ', src_file_name)
        ### print ('prod_dir_name: ', prod_dir_name)
        dst_file_dir = os.path.join(input_dir_root, day1, prod_dir_name) +'/' # '/raid8/leipan/pair/input/201710/01/SNDR.SNPP.CRIS.20171001T0012.m06.g003.L1B_NSR.std.v02_05.G.180623020533/'
        dst_file = os.path.basename(src_file_name)  # 'VNP03MOD.A2017274.0006.001.2018002163701.nc'
        print('dst_file_dir: ', dst_file_dir)
        if os.path.exists(dst_file_dir) == False:
          os.makedirs(dst_file_dir)

        if os.path.exists(os.path.join(dst_file_dir, dst_file)):
          os.remove(src_file_name)  # if dest file already exists, remove src
          rm_cnt += 1
        else:
          # if dest file does not exist, move src to dest
          shutil.move(src_file_name, dst_file_dir, copy_function = shutil.copy2)
          mv_cnt += 1

  print('num files moved: ', mv_cnt)
  print('num files removed: ', rm_cnt)



if __name__ == '__main__':

  dir_root = '/raid8/leipan/pair/'
  yearmon = '201710'
  product_dir_root = os.path.join(dir_root, 'product', yearmon)
  input_dir_root = os.path.join(dir_root, 'input', yearmon)
  if os.path.exists(product_dir_root) == False:
    os.makedirs(product_dir_root)
  if os.path.exists(input_dir_root) == False:
    os.makedirs(input_dir_root)

  src_dir_root = '/raid15/leipan/pair/'
  src_input_dir_root = os.path.join(src_dir_root, yearmon)

  print('src_input_dir_root: ', src_input_dir_root)
  print('input_dir_root: ', input_dir_root)

  move_input_granules(src_input_dir_root, input_dir_root)

