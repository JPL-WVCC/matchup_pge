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
def create_dataset(dirpath, files, ingest_dir_root, script_file):

  ### print ('files: ', files)

  for f1 in files:
    ### print ('f1: ', f1)
    basename1 = f1[:-3]
    ### basename1 = os.path.splitext(os.path.basename(f1))[0]
    dir1 = os.path.join(ingest_dir_root, basename1)
    print ('dir1: ', dir1)

    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.mkdir(dir1)
    ### print ('copy %s to %s' % (os.path.join(dirpath, f1), os.path.join(dir1, basename1+ext)))

    shutil.copyfile(os.path.join(dirpath, f1), os.path.join(dir1, basename1+ext))

    f = nc4.Dataset(os.path.join(dirpath, f1), 'r')
    ### print (f.time_coverage_start)
    ### print (f.time_coverage_end)
    ### print (f.geospatial_bounds)

    # create minimal dataset JSON file
    dataset_json_file = os.path.join(dir1, basename1+'.dataset.json')

    now = datetime.now()
    datetime1 = now.strftime("%Y-%m-%dT%H:%M:%SZ")

    dataset_dict = {"version": "v1.0",
                    "label": basename1,
                    "starttime": f.time_coverage_start,
                    "endtime": f.time_coverage_end,
                    "creation_timestamp": datetime1
                   }

    json_object = json.dumps(dataset_dict, indent = 4) 

    with open(dataset_json_file, "w") as outfile: 
      outfile.write(json_object)

    # create minimal metadata file
    metadata_json_file=os.path.join(dir1, basename1+'.met.json')
    m_file = open(metadata_json_file, 'w')
    m_file.write('{}')
    m_file.write('\n')
    m_file.close()

    script_file.write('~/mozart/ops/hysds/scripts/ingest_dataset.py %s ~/mozart/etc/datasets.json\n' % dir1)

    ### sys.exit()




if __name__ == '__main__':

  ### src_dir = '/raid15/leipan/VIIRS/VNP03MOD/2015/'
  src_dir = '/raid15/leipan/VIIRS/VNP03MOD/2017/'
  ingest_dir_root = '/raid15/leipan/ingest/VIIRS/2017/'

  script_filename = "ingest_script_viirs.sh"
  scriptfile1 = open(script_filename, "w")
  scriptfile1.write('#!/usr/bin/env bash\n')

  for (dirpath, dirnames, filenames) in os.walk(src_dir):
    ### print ('dirpath: ', dirpath)
    dirpath_basename = os.path.basename(dirpath)
    if dirpath_basename != '':
      dirpath_basename_num = int(dirpath_basename)
      ### print ('dirpath_basename_num: ', dirpath_basename_num)
      # in 2015, DOY 149 is 5/29 and DOY 184 is 7/3
      ### if dirpath_basename_num > 149 and dirpath_basename_num < 184:
      if dirpath_basename_num == 10: # to ingest 2017/10
        ### print ('--------------')
        ### print ('dirpath: ', dirpath)
        ### print ('dirnames: ', dirnames)
        ### print ('filenames: ', filenames)
        create_dataset(dirpath, filenames, ingest_dir_root, scriptfile1)

  scriptfile1.close()



