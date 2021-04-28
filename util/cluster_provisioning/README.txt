
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


. outputs (outdated)
---- ran on Sun, 4/18/21 ----
Apply complete! Resources: 6 added, 0 changed, 0 destroyed.

Outputs:

ci_pub_ip = 100.67.45.139
ci_pvt_ip = 100.67.45.139
factotum_pub_ip =
factotum_pvt_ip = 100.67.40.8
grq_pub_ip =
grq_pvt_ip = 100.67.43.56
metrics_pub_ip =
metrics_pvt_ip = 100.67.40.34
mozart_pub_ip =
mozart_pvt_ip = 100.67.42.96

