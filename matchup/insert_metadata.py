#!/usr/bin/python

import os
import fnmatch

root_dir = './test_output/'
nc_fname = ''
manifest_fname = ''

for root, dir, files in os.walk(root_dir):
  if 'SNDR.SNPP.' in root:
    ### print ('------------- ' + root)
    ### print ("")
    for items in fnmatch.filter(files, '*'):
      if 'manifest.mf' in items:
        manifest_fname = os.path.join(root, items)
        ### print ("... manifest ... " + manifest_fname)

      if '.nc' in items:
        nc_fname = os.path.join(root, items)
        ### print ("... nc ... " + nc_fname)

    """
    for items in fnmatch.filter(dir, '*'):
      if 'SNDR.SNPP.' in items:
        nc_fname = os.path.join(root, items)
        print ("... nc ... " + nc_fname)
    """
    if nc_fname != '' and manifest_fname != '':
      print ("--- got it ---")
      print (manifest_fname)
      print (nc_fname)
      nc_fname = ''
      manifest_fname = ''

      print ("-----------------------------------------")
      print ("")
