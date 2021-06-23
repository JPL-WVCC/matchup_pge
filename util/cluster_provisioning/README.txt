
. artifactory release versions
  https://cae-artifactory.jpl.nasa.gov/artifactory/general-develop/gov/nasa/jpl/iems/sds/pcm/


. terraform commands (outdated)

  terraform validate --var hysds_release=develop --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1 --var git_auth_key=b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee --var jenkins_api_key=11114e63d8baded1bded892c01f8b91781 --var cluster_security_group_id=sg-029b5af59364a4b3c --var verdi_security_group_id=sg-0b4e1f7038191c5e1 --var asg_vpc=vpc-0db7a713a6785cd0f

  terraform apply --var hysds_release=develop --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1 --var git_auth_key=b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee --var jenkins_api_key=11114e63d8baded1bded892c01f8b91781 --var cluster_security_group_id=sg-029b5af59364a4b3c --var verdi_security_group_id=sg-0b4e1f7038191c5e1 --var asg_vpc=vpc-0db7a713a6785cd0f

  terraform destroy --var hysds_release=develop --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1 --var git_auth_key=b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee --var jenkins_api_key=11114e63d8baded1bded892c01f8b91781 --var cluster_security_group_id=sg-029b5af59364a4b3c --var verdi_security_group_id=sg-0b4e1f7038191c5e1 --var asg_vpc=vpc-0db7a713a6785cd0f


. terraform commands for run under ci:/export/home/hysdsops/github/matchup_pge/util/cluster_provisioning

  terraform validate
  terraform apply
  terraform destroy

. note: the ami definations are in 
  modules/common/variables.tf
  but not in
  wvcc_variables.tf

. npm installation (outdated)

  npm install sass-loader sass webpack --save-dev


. after terraform apply run (outdated)
  source env.sh
 
  sds -d update grq -f -c
  sds -d update mozart -f -c
  sds -d update metrics -f -c
  sds -d update factotum -f -c
 
  if ${use_artifactory} = "True"; then
    fab -f ~/.sds/cluster.py -R mozart,grq,factotum update_wvcc_packages
  else
    fab -f ~/.sds/cluster.py -R mozart,grq,factotum,verdi update_wvcc_packages
  fi
 
  sds -d ship
  cd ~/mozart/pkgs
  sds -d pkg import container-hysds_lightweight-jobs-*.sdspkg.tar
  aws s3 cp hysds-verdi-${hysds_release}.tar.gz s3://${code_bucket}/
  aws s3 cp docker-registry-2.tar.gz s3://${code_bucket}/
  aws s3 cp logstash-7.1.1.tar.gz s3://${code_bucket}/
  sds -d reset all -f
  cd ~/mozart/ops/pcm_commons
  pip install -e .
 
  sds -d kibana import -f
  sds -d cloud storage ship_style --bucket ${dataset_bucket}
  sds -d cloud storage ship_style --bucket ${osl_bucket}
  sds -d cloud storage ship_style --bucket ${triage_bucket}
  sds -d cloud storage ship_style --bucket ${lts_bucket}

. keys
  var.git_auth_key
  Enter a value: b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee

  var.jenkins_api_key
  Enter a value: 11114e63d8baded1bded892c01f8b91781


. how to ssh to the PCM servers
  ssh -i ~/.ssh/wvcc-pcm-dev.pem hysdsops@<ip>


. if c3.xlarge is used for factotum, ssh to factotum would fail to connect, 
  which is why switching to r4.xlarge (which is used for all other PCM servers)

  Previous Generation Instance Details
  Instance Type Processor Arch vCPU	Memory (GiB)	Instance Storage (GB)   EBS-optimized Available  Network Performance
  c3.xlarge     64-bit         4        7.5             2 x 40                  Yes                      Moderate

  r4.xlarge     64-bit         4        30.5                                                             Up to 10 Gigabit

. supervisorctl status all

. the shared CI web frontend:
  https://wvcc-pcm-ci.jpl.nasa.gov/
  (use JPL credentials to log in)

. add jobs from mozart
  sds ci add_job -b master -k https://github.com/leipan/matchup_pge.git s3
  sds ci add_job -b singularity_dev -k https://github.com/aria-jpl/topsApp_pge.git s3

. install singularity on ci
# remove old version of singularity
$ sudo rm -rf \
    /usr/local/libexec/singularity \
    /usr/local/var/singularity \
    /usr/local/etc/singularity \
    /usr/local/bin/singularity \
    /usr/local/bin/run-singularity \
    /usr/local/etc/bash_completion.d/singularity

# when normal installation does not work, one can copy these files from an existing installation
  cd /usr/local/libexec/
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/libexec/singularity .
  cd /usr/local/var/
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/var/singularity .
  cd /usr/local/etc/
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/etc/singularity .
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/etc/bash_completion.d/singularity .
  cd /usr/local/bin/
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/bin/singularity .
  scp -r -i "~/.ssh/msas.pem" ops@54.167.55.23:/usr/local/bin/run-singularity .


# SDSC instructions
Step 1: run the script below to remove your existing Singularity:

#!/bin/bash
#
# A cleanup script to remove Singularity

sudo rm -rf /usr/local/libexec/singularity
sudo rm -rf /usr/local/etc/singularity
sudo rm -rf /usr/local/include/singularity  <--
sudo rm -rf /usr/local/lib/singularity  <--
sudo rm -rf /usr/local/var/lib/singularity/ <--
sudo rm /usr/local/bin/singularity
sudo rm /usr/local/bin/run-singularity
sudo rm /usr/local/etc/bash_completion.d/singularity
sudo rm /usr/local/man/man1/singularity.1 <--


. outputs (outdated)
---- ran on Sun, 4/18/21 ----
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

ssh -i ~/.ssh/wvcc-pcm-dev.pem hysdsops@<ip>

Outputs:

ci_pub_ip = 100.67.45.139
ci_pvt_ip = 100.67.45.139
ssh hysdsops@wvcc-pcm-ci.jpl.nasa.gov
(This is where terraform scripts are, and where the singularity sandbox build scripts is)

(as of 6/22/21)
export MOZART_IP=100.67.41.42
export FACTOTUM_IP=100.67.40.120
export GRQ_IP=100.67.43.241
export METRICS_IP=100.67.41.48


