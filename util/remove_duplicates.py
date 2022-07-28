import os

if __name__ == '__main__':

  src_dir = '/raid8/leipan/final_product/20220616/2021/'
  ### src_dir = '/raid15/leipan/products/20220616/'

  info_filename = 'info.txt'
  file1 = open(info_filename, "w")
  file2 = open('duplicates.txt', "w")

  dict1 = {}

  for (dirpath, dirnames, filenames) in os.walk(src_dir):
    """
    print ('------- dirpath: ', dirpath)
    file1.write(f'------- dirpath: {dirpath}\n')
    dirpath_basename = os.path.basename(dirpath)
    """

    for filename in filenames:
      if filename.endswith('.nc'):
        print ('------- dirpath: ', dirpath)
        file1.write(f'------- dirpath: {dirpath}\n')
        dirpath_basename = os.path.basename(dirpath)
        upper_dir = dirpath.replace(dirpath_basename, '')
        upper_dir = upper_dir[:-1]
        upper_dir_basename = os.path.basename(upper_dir)
        print(f'         {upper_dir_basename}')
        file1.write(f'         {upper_dir_basename}\n')

        if filename in dict1.keys():
          dict1[filename].append(upper_dir_basename)
          print('filename: ', dict1[filename])
        else:
          dict1[filename] = [upper_dir_basename]

  file1.close()

  print('len(dict1): ', len(dict1))

  for key in dict1:
    if len(dict1[key]) > 1:
      values = ' '.join(str(e) for e in dict1[key])
      print('key: {0}, value: {1}'.format(key,  values))
      file2.write('key: {0}, value: {1}\n'.format(key,  values))

  file2.close()
