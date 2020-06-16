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





if __name__ == '__main__':

  ingest_dir_root = '/raid15/leipan/ingest'
  if os.path.exists(ingest_dir_root) == False:
    os.mkdir(ingest_dir_root)

  script_filename = "ingest_script.sh"
  scriptfile1 = open(script_filename, "w")
  scriptfile1.write('#!/usr/bin/env bash\n')

  dataDir1 = '/raid15/leipan/ingest/CrIS/1/'
  list1 = sorted([os.path.join(dataDir1, name) for name in os.listdir(dataDir1) if os.path.isdir(os.path.join(dataDir1, name))])
  print ('list1: ', list1)

  for dir1 in list1:
    script_file.write('~/mozart/ops/hysds/scripts/ingest_dataset.py %s ~/mozart/etc/datasets.json\n' % dir1)

  scriptfile1.close()

  st = os.stat(script_filename)
  os.chmod(script_filename, st.st_mode | stat.S_IEXEC)

