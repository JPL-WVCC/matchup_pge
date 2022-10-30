import netCDF4 as nc4
import shutil
import os
import glob
from datetime import datetime, timedelta
import logging
from airs_modis_parallel_run_matchup import colocate_one_airs_granual

module_logger = logging.getLogger("process_invalid_coordinates")

def process(output_nc_file):

    f = nc4.Dataset(output_nc_file, 'r', format='NETCDF4') #'w' stands for write

    module_logger.info('SOUTHBOUNDINGCOORDINATE: '+str(f.SOUTHBOUNDINGCOORDINATE))
    ### print('SOUTHBOUNDINGCOORDINATE: ', str(f.SOUTHBOUNDINGCOORDINATE))

    ### f.WESTBOUNDINGCOORDINATE
    ### f.NORTHBOUNDINGCOORDINATE
    ### f.EASTBOUNDINGCOORDINATE

    if f.SOUTHBOUNDINGCOORDINATE == -9999.0:
      print('SOUTHBOUNDINGCOORDINATE: ', str(f.SOUTHBOUNDINGCOORDINATE))
      reset_coords(output_nc_file)


def reset_coords(output_nc_file):

    dir_path = os.path.dirname(output_nc_file)
    print('dir_path: ', dir_path)

    manifest1 = os.path.join(dir_path, 'manifest.mf')
    print('manifest1: ', manifest1)


if __name__ == '__main__':

    ext1 = '.hdf'
    ar = '/archive/AIRSOps/airs/gdaac/v5/'
    mr = '/peate_archive/NPPOps/aqua_modis/laads/061/'

    # airs_geo_files = sorted(glob.glob(args.ar+str(args.y)+'/'+month1+'/'+day1+'/'+'airibrad/AIRS.*L1B.AIRS*.*'+ext1))
    # '/archive/AIRSOps/airs/gdaac/v5/2004/10/13/airibrad/AIRS.2004.10.13.226.L1B.AIRS_Rad.v5.0.0.0.G07103093218.hdf'

    ### dir1 = '/raid15/leipan/test/2002/09/06/AIRS.2002.09.06.160/IND_AIRS_MODIS1km.2002.09.06.160.nc'

    dst_dir = '/raid15/leipan/products/20221029/'
    print('dst_dir: ', dst_dir)
    src_dir = '/raid15/leipan/products/20220923/'
    input_file = 'Aqua_AIRS_MODIS1km_IND.1.failed.txt'

    if not os.path.exists(dst_dir):
      os.makedirs(dst_dir)

    with open(input_file) as f:
      lines = f.readlines()

      # IND_AIRS_MODIS1km.2022.03.21.128.nc
      # /raid15/leipan/products/20220923/2022/03/21/AIRS.2022.03.21.128

      for line in lines:
        line = line.replace('\n', '')
        print('line: ', line)
        split1 = line.split('_')
        str1 = split1[2]
        ### print('str1: ', str1)
        str2 = str1.split('.')
        yy = str2[1]
        mm = str2[2]
        dd = str2[3]
        num = str2[4]

        subdir_name = 'AIRS.'+yy+'.'+mm+'.'+dd+'.'+num
        dir1 = src_dir+yy+'/'+mm+'/'+dd+'/'+subdir_name+'/'
        ### print('dir1: ', dir1)

        # copy to dst_dir
        ### shutil.copytree(dir1, dst_dir+subdir_name)

        airs_geo_file = glob.glob(ar+str(yy)+'/'+mm+'/'+dd+'/'+'airibrad/AIRS.'+yy+'.'+mm+'.'+dd+'.'+num+'.L1B.AIRS*.*'+ext1)
        print('airs_geo_file: ', airs_geo_file)
        print('')

        colocate_one_airs_granual(airs_geo_file[0], mr, dst_dir)


