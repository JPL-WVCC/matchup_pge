terraform validate --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1

terraform validate --var hysds_release=v4.0.0 --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1 --var git_auth_key=b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee --var jenkins_api_key=11114e63d8baded1bded892c01f8b91781 --var cluster_security_group_id=sg-029b5af59364a4b3c --var verdi_security_group_id=sg-0b4e1f7038191c5e1 --var asg_vpc=vpc-0db7a713a6785cd0f --var bach_api_branch=nisar

terraform apply --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1

terraform apply --var hysds_release=v4.0.0 --var private_key_file=/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem --var project=wvcc --var venue=leipan --var counter=1 --var git_auth_key=b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee --var jenkins_api_key=11114e63d8baded1bded892c01f8b91781 --var cluster_security_group_id=sg-029b5af59364a4b3c --var verdi_security_group_id=sg-0b4e1f7038191c5e1 --var asg_vpc=vpc-0db7a713a6785cd0f --var bach_api_branch=nisar

var.git_auth_key
  Enter a value: b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee

var.jenkins_api_key
  Enter a value: 11114e63d8baded1bded892c01f8b91781


---- ran on Sunday, 4/11/21 ----
Outputs:

ci_pub_ip = 100.67.45.139
ci_pvt_ip = 100.67.45.139
factotum_pub_ip = 
factotum_pvt_ip = 100.67.42.114
grq_pub_ip = 
grq_pvt_ip = 100.67.42.164
metrics_pub_ip = 
metrics_pvt_ip = 100.67.41.84
mozart_pub_ip = 
mozart_pvt_ip = 100.67.43.230
