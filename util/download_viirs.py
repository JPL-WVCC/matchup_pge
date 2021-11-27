import subprocess
import shlex

work_dir = '/raid15/leipan/VIIRS/'

for day1 in range(276, 306):
  cmd = 'wget -e robots=off -m -np -R .html,.tmp -nH --cut-dirs=3 "https://ladsweb.modaps.eosdis.nasa.gov/archive/allData/5110/VNP03MOD/2017/{0}/" --header "Authorization: Bearer bGVpcGFuOmJHVnBjR0Z1UUdwd2JDNXVZWE5oTG1kdmRnPT06MTYzNTQ2NTQ3Nzo5NjA2YTczNjJmNWUyYWExNTIzMDM5OTk5MDYyOTdkNDgzYjMyMTA4" -P .'.format(day1)
  print('cmd: ', cmd)
  args = shlex.split(cmd)
  proc = subprocess.Popen(cmd, shell=True, cwd=work_dir, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
  out, err = proc.communicate()
  print('out: ', out)
  print('err: ', err)
  

