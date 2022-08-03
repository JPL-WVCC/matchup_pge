from multiprocessing import Process
import subprocess
import shlex


def download_one_day(year, day):

  work_dir = '/raid15/leipan/VIIRS/'
  cmd = 'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5110/VNP03MOD/{0}/{1}/" --header "Authorization: Bearer bGVpcGFuOmJHVnBjR0Z1UUdwd2JDNXVZWE5oTG1kdmRnPT06MTYzNTQ2NTQ3Nzo5NjA2YTczNjJmNWUyYWExNTIzMDM5OTk5MDYyOTdkNDgzYjMyMTA4" -P .'.format(year, day)
  print('cmd: ', cmd)

  p1 = subprocess.Popen(cmd, shell=True, cwd=work_dir, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = p1.communicate()
  ### print('out: ', out)
  print('err: ', err)
  rc = p1.returncode
  print('return code: ', rc)


if __name__ == "__main__":

  year = 2017

  processes = []
  for day1 in range(273, 306):
    p1 = Process(target=download_one_day, args=(year, day1))
    processes.append(p1)

  for p in processes:
    p.start()

  for p in processes:
    p.join()
