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
def create_dataset(files, ingest_dir_root, script_file):

  for f1 in files:
    ### print ('f1: ', f1)
    basename1 = os.path.splitext(os.path.basename(f1))[0]
    dir1 = os.path.join(ingest_dir_root, basename1)
    print ('dir1: ', dir1)

    if os.path.exists(dir1):
      shutil.rmtree(dir1)
    os.mkdir(dir1)
    shutil.copyfile(f1, os.path.join(dir1, basename1+ext))

    f = nc4.Dataset(f1, 'r')
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




if __name__ == '__main__':

  ingest_dir_root = '/raid15/leipan/ingest'
  if os.path.exists(ingest_dir_root) == False:
    os.mkdir(ingest_dir_root)

  ### dataDir2='/peate_archive/.data6/Ops/snpp/gdisc/2/2015/06/01/crisl1b/'
  dataDir2='/peate_archive/.data6/Ops/snpp/gdisc/2/2015/06/'
  ### dataDir4='/raid15/qyue/VIIRS/VIIRS/20150601/'
  dataDir4='/raid15/leipan/VIIRS/VNP03MOD/2015/'
 
  script_filename = "ingest_script.sh"
  scriptfile1 = open(script_filename, "w")
  scriptfile1.write('#!/usr/bin/env bash\n')

  # get CrIS files
  ### cris_geo_files = sorted(glob.glob(dataDir2+'SNDR*1809042004*'))
  cris_geo_files = sorted(glob.glob(dataDir2+'**/**/SNDR.SNPP.CRIS*L1B_NSR*'+ext))
  ### print ('cris_geo_files: ', cris_geo_files)
  create_dataset(cris_geo_files, ingest_dir_root, scriptfile1)

  # get VIIRS files
  ### viirs_geo_files = sorted(glob.glob(dataDir4+'VNP03MOD*201726106455*'))
  viirs_geo_files = sorted(glob.glob(dataDir4+'**/VNP03MOD*'+ext))
  ### print ('viirs_geo_files: ', viirs_geo_files)
  create_dataset(viirs_geo_files, ingest_dir_root, scriptfile1)

  scriptfile1.close()

  st = os.stat(script_filename)
  os.chmod(script_filename, st.st_mode | stat.S_IEXEC)

