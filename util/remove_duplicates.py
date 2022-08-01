import os
import shutil

if __name__ == '__main__':

  src_dir = '/raid8/leipan/final_product/20220616/2021/'
  ### src_dir = '/raid8/leipan/final_product/20220616/2021/01/'
  ### src_dir = '/raid15/leipan/products/20220616/'

  info_filename = 'info.txt'
  file1 = open(info_filename, "w")
  file2 = open('duplicates.txt', "w")

  dict1 = {}

  total_nc = 0

  for (dirpath, dirnames, filenames) in os.walk(src_dir):
    """
    print ('------- dirpath: ', dirpath)
    file1.write(f'------- dirpath: {dirpath}\n')
    dirpath_basename = os.path.basename(dirpath)
    """

    for filename in filenames:
      if filename.endswith('.nc'):
        total_nc += 1
        ### print ('------- dirpath: ', dirpath)
        file1.write(f'------- dirpath: {dirpath}\n')
        dirpath_basename = os.path.basename(dirpath)
        upper_dir = dirpath.replace(dirpath_basename, '')
        upper_dir = upper_dir[:-1]
        upper_dir_basename = os.path.basename(upper_dir)
        ### print(f'         {upper_dir_basename}')
        file1.write(f'         {upper_dir_basename}\n')

        if filename in dict1.keys():
          ### dict1[filename].append(upper_dir_basename)
          dict1[filename].append(upper_dir)
          ### print('filename: ', dict1[filename])
        else:
          ### dict1[filename] = [upper_dir_basename]
          dict1[filename] = [upper_dir]

  file1.write(f'\n\n------- total_nc count: {total_nc}\n')

  print('len(dict1): ', len(dict1))

  duplicated_cnt = 0

  # remove the duplicated products
  for key in dict1:
    if len(dict1[key]) > 1:
      duplicated_cnt += 1
      values = ' '.join(str(e) for e in dict1[key])
      ### print('key: {0}, value: {1}'.format(key,  values))
      file2.write('key: {0}, value: {1}\n'.format(key,  values))

      # remove the first subdir altogether
      ### print(f'removing {dict1[key][0]}')
      print(f'shutil.rmtree("{dict1[key][0]}")')
      shutil.rmtree(dict1[key][0])

  # rename subdir names
  for (dirpath, dirnames, filenames) in os.walk(src_dir):
    if 'm06' in dirpath and 'IND_' not in dirpath:
      # rename the subdir to remove the unnecessary string of, e.g., ".L1B.std.v02_05.G.220101024446"
      pp = dirpath.find('.L1B.std')
      dirpath1 = dirpath[:pp]
      ### print(f'renaming {dirpath} to {dirpath1}')
      print(f'os.rename("{dirpath}", "{dirpath1}")')
      os.rename(dirpath, dirpath1)


  file2.close()

  file1.write(f'------- duplicated_cnt: {duplicated_cnt}\n')
  file1.write(f'------- unique count: {len(dict1)}\n')
  file1.close()
