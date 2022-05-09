#!/usr/bin/python

import os,sys
import fnmatch
import netCDF4 as nc4
import datetime
import shlex, subprocess
import numpy as np

### root_dir = './test_output/'
### root_dir = '/raid15/leipan/products/20220504/'
### root_dir = '/raid15/leipan/products/20220117/'
root_dir = 'tmp/'
### year1 = '2015'
### month1 = '11'
year1 = '2020'
month1 = '08'
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

      print ("-----------------------------------------")
      print ("")
