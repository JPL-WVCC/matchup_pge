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

split_into = 3 # num of loads the ingest process will be split into

# list1 is the list of dirs that needs to be split
# dataDir1 is their root dir
def move_to_split(list1, dataDir1):

  total_num = len(list1)
  batch_cnt = total_num/split_into + 1 # count of each batch

  subdir_cnt = 0
  tot_cnt = 1
  subdir1 = ''
  for path1 in list1:
    ### print ('path1: ', path1)
    d1 = tot_cnt/batch_cnt + 1
    if d1 != subdir_cnt: # new batch?
      subdir_cnt = d1
      subdir1 = os.path.join(dataDir1, str(subdir_cnt)) # new subdir for new batch
      if not os.path.exists(subdir1):
        os.mkdir(subdir1)
        print ('made dir %s' % subdir1)

    if False:
      shutil.move(path1, subdir1)
    print ('mv %s to %s' %(path1, subdir1))

    tot_cnt += 1


if __name__ == '__main__':

  ingest_dir_root = '/raid15/leipan/ingest'

  """
  dataDir1=os.path.join(ingest_dir_root, 'VIIRS')
  ### print ('dataDir1: ', dataDir1)

  list1 = sorted([os.path.join(dataDir1, name) for name in os.listdir(dataDir1) if os.path.isdir(os.path.join(dataDir1, name))])
  move_to_split(list1, dataDir1)

  """

  dataDir2=os.path.join(ingest_dir_root, 'CrIS')
  list2 = sorted([os.path.join(dataDir2, name) for name in os.listdir(dataDir2) if os.path.isdir(os.path.join(dataDir2, name))])
  move_to_split(list2, dataDir2)
 
