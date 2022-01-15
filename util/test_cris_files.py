import numpy as np
import glob
import time
import pdb
import os
import pickle
import netCDF4 as nc4

start_time = time.time()
"""
dataDir1='/peate_archive/.data5/Ops/npp/noaa/op/2012/05/15/scris/'
dataDir2='/peate_archive/.data5/Ops/npp/noaa/op/2012/05/15/gcrso/'
dataDir3='/peate_archive/.data5/Ops/npp/noaa/op/2012/05/15/svm15/'
dataDir4='/peate_archive/.data5/Ops/npp/noaa/op/2012/05/15/gmodo/'
"""
#for iday in range(15,23,1):
for iday in range (1,3,1):
    ### dataDir2='/peate_archive/.data1/Ops/snpp/gdisc/2/2016/01/'+str(iday).zfill(2)+'/crisl1b/'
    ### dataDir2='/peate_archive/.data1/Ops/snpp/gdisc/2/2015/07/'+str(iday).zfill(2)+'/crisl1b/'
    dataDir2='/peate_archive/NPPOps/snpp/gdisc/2/2015/11/'+str(iday).zfill(2)+'/crisl1b/'
    print(iday)
    for iloop in range(0,240,1):
        print(iloop)
# get CrIS files 
#cris_sdr_files = sorted(glob.glob(dataDir1+'SCRIS*d2012*'))[21:40]
        cris_geo_files = sorted(glob.glob(dataDir2+'SNDR.SNPP.CRIS*L1B.std*'))[iloop:iloop+1]#+10]
        print('cris_geo_files: ', cris_geo_files)
