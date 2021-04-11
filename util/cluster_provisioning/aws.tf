provider "aws" {
  shared_credentials_file = var.shared_credentials_file
  region                  = var.region
  profile              = var.profile
}

resource "null_resource" "initialize" {
  provisioner "local-exec" {
    command = "touch pcm_cluster_ip_address.txt"
  }
}

resource "random_id" "counter" { 
  byte_length = 2
}

locals {
  counter = var.counter != "" ? var.counter : random_id.counter.hex
  dataset_bucket = "${var.project}-${var.environment}-lts-fwd-${var.venue}"
  code_bucket = "${var.project}-${var.environment}-cc-fwd-${var.venue}"
}

######################
# mozart
######################

resource "aws_instance" "mozart" {
  ### depends_on            = ["aws_instance.metrics", "aws_instance.ci"]
  depends_on            = [aws_instance.metrics]
  ami                    = var.mozart["ami"]
  instance_type          = var.mozart["instance_type"]
  key_name               = var.key_name
  availability_zone      = var.az
  iam_instance_profile = var.pcm_cluster_role["name"]
  tags                   = {
                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.mozart["name"]}"
                           }
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids_mozart


  ebs_block_device {
    device_name = var.mozart["data_dev"]
    volume_size = var.mozart["data_dev_size"]
    volume_type = "gp2"
    delete_on_termination = true
  }
  ebs_block_device {
    device_name = var.mozart["data2_dev"]
    volume_size = var.mozart["data2_dev_size"]
    volume_type = "gp2"
    delete_on_termination = true
  }

  connection {
    ### host = self.private_ip
    host     = aws_instance.mozart.private_ip
    type     = "ssh"
    user     = "hysdsops"
    private_key = file(var.private_key_file)
  }

  provisioner "local-exec" {
    command = "echo aws_instance.mozart.public_ip = ${aws_instance.mozart.public_ip} >> pcm_cluster_ip_address.txt"
  }
  
  provisioner "file" {
    source      = var.private_key_file
    destination = ".ssh/${basename(var.private_key_file)}"
  }

  provisioner "remote-exec" {
    inline = [
      "set -ex",
      "chmod 400 ~/.ssh/${basename(var.private_key_file)}",
      "mkdir ~/.sds",
      "echo TYPE: hysds > ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo MOZART_PVT_IP: ${aws_instance.mozart.private_ip} >> ~/.sds/config",
      "echo MOZART_PUB_IP: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_FQDN: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo MOZART_RABBIT_PVT_IP: ${aws_instance.mozart.private_ip} >> ~/.sds/config",
      "echo MOZART_RABBIT_PUB_IP: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_RABBIT_FQDN: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_RABBIT_USER: guest >> ~/.sds/config",
      "echo MOZART_RABBIT_PASSWORD: guest >> ~/.sds/config",

      "echo >> ~/.sds/config",
      "echo MOZART_REDIS_PVT_IP: ${aws_instance.mozart.private_ip} >> ~/.sds/config",
      "echo MOZART_REDIS_PUB_IP: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_REDIS_FQDN: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_REDIS_PASSWORD: >> ~/.sds/config",
      "echo >> ~/.sds/config",
     
      "echo MOZART_ES_PVT_IP: ${aws_instance.mozart.private_ip} >> ~/.sds/config",
      "echo MOZART_ES_PUB_IP: ${aws_instance.mozart.public_ip} >> ~/.sds/config",
      "echo MOZART_ES_FQDN: ${aws_instance.mozart.public_ip} >> ~/.sds/config",

      "echo OPS_USER: ops >> ~/.sds/config",
      "echo OPS_HOME: $$HOME >> ~/.sds/config",
      "echo OPS_PASSWORD_HASH: $(echo -n ${var.ops_password} | sha224sum |awk '{ print $1}') >> ~/.sds/config",
      "echo LDAP_GROUPS: wvcc-pcm-dev >> ~/.sds/config",
      "echo KEY_FILENAME: $$HOME/.ssh/${basename(var.private_key_file)} >> ~/.sds/config",
      "echo JENKINS_USER: jenkins >> ~/.sds/config",
      "echo JENKINS_DIR: /var/lib/jenkins >> ~/.sds/config",

      "echo >> ~/.sds/config",
      "echo METRICS_PVT_IP: ${aws_instance.metrics.private_ip} >> ~/.sds/config",
      "echo METRICS_PUB_IP: ${aws_instance.metrics.public_ip} >> ~/.sds/config",
      "echo METRICS_FQDN: ${aws_instance.metrics.public_ip} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo METRICS_REDIS_PVT_IP: ${aws_instance.metrics.private_ip} >> ~/.sds/config",
      "echo METRICS_REDIS_PUB_IP: ${aws_instance.metrics.public_ip} >> ~/.sds/config",
      "echo METRICS_REDIS_FQDN: ${aws_instance.metrics.public_ip} >> ~/.sds/config",
      "echo METRICS_REDIS_PASSWORD: >> ~/.sds/config",
      "echo >> ~/.sds/config",

      "echo METRICS_ES_PVT_IP: ${aws_instance.metrics.private_ip} >> ~/.sds/config",
      "echo METRICS_ES_PUB_IP: ${aws_instance.metrics.public_ip} >> ~/.sds/config",
      "echo METRICS_ES_FQDN: ${aws_instance.metrics.public_ip} >> ~/.sds/config",

      "echo >> ~/.sds/config",
      "echo GRQ_PVT_IP: ${aws_instance.grq.private_ip} >> ~/.sds/config",
      "echo GRQ_PUB_IP: ${aws_instance.grq.public_ip} >> ~/.sds/config",
      "echo GRQ_FQDN: ${aws_instance.grq.public_ip} >> ~/.sds/config",
      "echo GRQ_PORT: 8878 >> ~/.sds/config",

      "echo >> ~/.sds/config",
      "echo GRQ_ES_PVT_IP: ${aws_instance.grq.private_ip} >> ~/.sds/config",
      "echo GRQ_ES_PUB_IP: ${aws_instance.grq.public_ip} >> ~/.sds/config",
      "echo GRQ_ES_FQDN: ${aws_instance.grq.public_ip} >> ~/.sds/config",

      "echo >> ~/.sds/config",
      "echo FACTOTUM_PVT_IP: ${aws_instance.factotum.private_ip} >> ~/.sds/config",
      "echo FACTOTUM_PUB_IP: ${aws_instance.factotum.public_ip} >> ~/.sds/config",
      "echo FACTOTUM_FQDN: ${aws_instance.factotum.public_ip} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      ### "echo CI_PVT_IP: ${aws_instance.ci.private_ip} >> ~/.sds/config",
      "echo CI_PVT_IP: ${var.common_ci["private_ip"]} >> ~/.sds/config",
      ### "echo CI_PUB_IP: ${aws_instance.ci.public_ip} >> ~/.sds/config",
      "echo CI_PUB_IP: 100.67.45.139 >> ~/.sds/config",
      ### "echo CI_FQDN: ${aws_instance.ci.public_ip} >> ~/.sds/config",
      "echo CI_FQDN: 100.67.45.139 >> ~/.sds/config",
      "echo JENKINS_API_USER: ${var.jenkins_api_user != "" ? var.jenkins_api_user : var.venue} >> ~/.sds/config",
      "echo JENKINS_API_KEY: ${var.jenkins_api_key} >> ~/.sds/config",

      "echo >> ~/.sds/config",
      ### "echo VERDI_PVT_IP: ${aws_instance.ci.private_ip} >> ~/.sds/config",
      "echo VERDI_PVT_IP: 100.67.45.139 >> ~/.sds/config",
      ### "echo VERDI_PUB_IP: ${aws_instance.ci.public_ip} >> ~/.sds/config",
      "echo VERDI_PUB_IP: 100.67.45.139 >> ~/.sds/config",
      ### "echo VERDI_FQDN: ${aws_instance.ci.public_ip} >> ~/.sds/config",
      "echo VERDI_FQDN: 100.67.45.139 >> ~/.sds/config",
      "echo OTHER_VERDI_HOSTS: >> ~/.sds/config",
      "echo '  - VERDI_PVT_IP:' >> ~/.sds/config",
      "echo '    VERDI_PUB_IP:' >> ~/.sds/config",
      "echo '    VERDI_FQDN:' >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo DAV_SERVER: None >> ~/.sds/config",
      "echo DAV_USER: None >> ~/.sds/config",
      "echo DAV_PASSWORD: None >> ~/.sds/config",
      
      "echo >> ~/.sds/config",
      "echo DATASET_AWS_REGION: us-west-2 >> ~/.sds/config",
      "echo DATASET_AWS_ACCESS_KEY: >> ~/.sds/config",
      "echo DATASET_AWS_SECRET_KEY: >> ~/.sds/config",
      "echo DATASET_S3_ENDPOINT: s3-us-west-2.amazonaws.com >> ~/.sds/config",
      "echo DATASET_S3_WEBSITE_ENDPOINT: s3-website-us-west-2.amazonaws.com >> ~/.sds/config",
      "echo DATASET_BUCKET: ${local.dataset_bucket} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo AWS_REGION: us-west-2 >> ~/.sds/config",
      "echo AWS_ACCESS_KEY: >> ~/.sds/config",
      "echo AWS_SECRET_KEY: >> ~/.sds/config",
      "echo S3_ENDPOINT: s3-us-west-2.amazonaws.com >> ~/.sds/config",
      "echo CODE_BUCKET: ${local.code_bucket} >> ~/.sds/config",
      "echo VERDI_PRIMER_IMAGE: https://s3.console.aws.amazon.com/s3/object/${local.code_bucket}/hysds-verdi-latest.tar.gz >> ~/.sds/config",
      "echo VERDI_TAG: latest >> ~/.sds/config",
      "echo VERDI_UID: 1002 >> ~/.sds/config",
      "echo VERDI_GID: 1002 >> ~/.sds/config",
      "echo QUEUES: ${var.project}-job_worker-small ${var.project}-job_worker-large >> ~/.sds/config",
      "echo INSTANCE_TYPES: c3.xlarge c3.xlarge >> ~/.sds/config",
      "echo INSTANCE_BIDS: 0.21 0.21 >> ~/.sds/config",
      "echo VENUE: ${var.project}-${var.venue}-${local.counter} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo ASG: >> ~/.sds/config",
      "echo '  AMI: ${var.asg_ami}' >> ~/.sds/config",
      "echo '  KEYPAIR: ${var.asg_keypair}' >> ~/.sds/config",
      "echo '  USE_ROLE: ${var.asg_use_role}' >> ~/.sds/config",
      "echo '  ROLE: ${var.asg_role}' >> ~/.sds/config",
      "echo '  SECURITY_GROUPS:' >> ~/.sds/config",
      "echo '    - ${var.asg_secgroup1}' >> ~/.sds/config",
      "echo '    - ${var.asg_secgroup2}' >> ~/.sds/config",
      "echo '  VPC: ${var.asg_vpc}' >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo STAGING_AREA: >> ~/.sds/config",
      "echo '  LAMBDA_SECURITY_GROUPS:' >> ~/.sds/config",
      "echo '    - ${var.lambda_secgroup}' >> ~/.sds/config",
      "echo '  LAMBDA_VPC: ${var.lambda_vpc}' >> ~/.sds/config",
      "echo '  LAMBDA_ROLE: \"${var.lambda_role_arn}\"' >> ~/.sds/config",
      "echo '  JOB_TYPE: ${var.lambda_job_type}' >> ~/.sds/config",
      "echo '  JOB_RELEASE: ${var.wvcc_pcm_branch}' >> ~/.sds/config",
      "echo '  JOB_QUEUE: ${var.lambda_job_queue}' >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo GIT_OAUTH_TOKEN: ${var.git_auth_key} >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo PROVES_URL: https://prov-es.jpl.nasa.gov/beta >> ~/.sds/config",
      "echo PROVES_IMPORT_URL: https://prov-es.jpl.nasa.gov/beta/api/v0.1/prov_es/import/json >> ~/.sds/config",
      "echo DATASETS_CFG: $${HOME}/verdi/etc/datasets.json >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo SYSTEM_JOBS_QUEUE: system-jobs-queue >> ~/.sds/config",
      "echo >> ~/.sds/config",
      "echo MOZART_ES_CLUSTER: resource_cluster >> ~/.sds/config",
      "echo METRICS_ES_CLUSTER: metrics_cluster >> ~/.sds/config",
      "echo DATASET_QUERY_INDEX: grq >> ~/.sds/config",
      "echo USER_RULES_DATASET_INDEX: user_rules >> ~/.sds/config",
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "set -ex",
      "mv ~/.sds ~/.sds.bak",
      "rm -rf ~/mozart",
      "if [ \"${var.hysds_release}\" = \"develop\" ]; then",
      "  git clone --single-branch -b ${var.hysds_release} https://${var.git_auth_key}@github.jpl.nasa.gov/IEMS-SDS/pcm-releaser.git",
      "  cd pcm-releaser",
      "  export release=${var.hysds_release}",
      "  export conda_dir=$HOME/conda",
      "  ./build_conda.sh $conda_dir $release",
      "  cd ..",
      "  rm -rf pcm-releaser",
      "  scp -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysds-conda_env-${var.hysds_release}.tar.gz hysdsops@${aws_instance.metrics.private_ip}:hysds-conda_env-${var.hysds_release}.tar.gz",
      "  ssh -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysdsops@${aws_instance.metrics.private_ip} 'mkdir -p ~/conda; tar xvfz hysds-conda_env-${var.hysds_release}.tar.gz -C conda; export PATH=$HOME/conda/bin:$PATH; conda-unpack; rm -rf hysds-conda_env-${var.hysds_release}.tar.gz'",
      "  scp -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysds-conda_env-${var.hysds_release}.tar.gz hysdsops@${aws_instance.grq.private_ip}:hysds-conda_env-${var.hysds_release}.tar.gz",
      "  ssh -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysdsops@${aws_instance.grq.private_ip} 'mkdir -p ~/conda; tar xvfz hysds-conda_env-${var.hysds_release}.tar.gz -C conda; export PATH=$HOME/conda/bin:$PATH; conda-unpack; rm -rf hysds-conda_env-${var.hysds_release}.tar.gz'",
      "  scp -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysds-conda_env-${var.hysds_release}.tar.gz hysdsops@${aws_instance.factotum.private_ip}:hysds-conda_env-${var.hysds_release}.tar.gz",
      "  ssh -o StrictHostKeyChecking=no -q -i ~/.ssh/${basename(var.private_key_file)} hysdsops@${aws_instance.factotum.private_ip} 'mkdir -p ~/conda; tar xvfz hysds-conda_env-${var.hysds_release}.tar.gz -C conda; export PATH=$HOME/conda/bin:$PATH; conda-unpack; rm -rf hysds-conda_env-${var.hysds_release}.tar.gz'",
      "  git clone https://github.com/hysds/hysds-framework",
      "  cd hysds-framework",
      "  git fetch",
      "  git fetch --tags",
      "  git checkout ${var.hysds_release}",
      "  ./install.sh mozart -d",
      "  rm -rf ~/mozart/pkgs/hysds-verdi-latest.tar.gz",
      "else",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/iems/sds/pcm/${var.hysds_release}/hysds-conda_env-${var.hysds_release}.tar.gz\"",
      "  mkdir -p ~/conda",
      "  tar xvfz hysds-conda_env-${var.hysds_release}.tar.gz -C conda",
      "  export PATH=$HOME/conda/bin:$PATH",
      "  conda-unpack",
      "  rm -rf hysds-conda_env-${var.hysds_release}.tar.gz",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/iems/sds/pcm/${var.hysds_release}/hysds-mozart_venv-${var.hysds_release}.tar.gz\"",
      "  tar xvfz hysds-mozart_venv-${var.hysds_release}.tar.gz",
      "  rm -rf hysds-mozart_venv-${var.hysds_release}.tar.gz",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/iems/sds/pcm/${var.hysds_release}/hysds-verdi_venv-${var.hysds_release}.tar.gz\"",
      "  tar xvfz hysds-verdi_venv-${var.hysds_release}.tar.gz",
      "  rm -rf hysds-verdi_venv-${var.hysds_release}.tar.gz",
      "fi",
      "cd ~/mozart/ops",
      "if [ \"${var.use_artifactory}\" = true ]; then",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/nisar-pcm-${var.nisar_pcm_branch}.tar.gz\"",
      "  tar xvfz nisar-pcm-${var.nisar_pcm_branch}.tar.gz",
      "  ln -s /export/home/hysdsops/mozart/ops/nisar-pcm-${var.nisar_pcm_branch} /export/home/hysdsops/mozart/ops/nisar-pcm",
      "  rm -rf nisar-pcm-${var.nisar_pcm_branch}.tar.gz ",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/CNM_product_delivery-${var.product_delivery_branch}.tar.gz\"",
      "  tar xvfz CNM_product_delivery-${var.product_delivery_branch}.tar.gz",
      "  ln -s /export/home/hysdsops/mozart/ops/CNM_product_delivery-${var.product_delivery_branch} /export/home/hysdsops/mozart/ops/CNM_product_delivery",
      "  rm -rf CNM_product_delivery-${var.product_delivery_branch}.tar.gz",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/pcm_commons-${var.pcm_commons_branch}.tar.gz\"",
      "  tar xvfz pcm_commons-${var.pcm_commons_branch}.tar.gz",
      "  ln -s /export/home/hysdsops/mozart/ops/pcm_commons-${var.pcm_commons_branch} /export/home/hysdsops/mozart/ops/pcm_commons",
      "  rm -rf pcm_commons-${var.pcm_commons_branch}.tar.gz",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/bach-api-${var.bach_api_branch}.tar.gz\"",
      "  tar xvfz bach-api-${var.bach_api_branch}.tar.gz",
      "  ln -s /export/home/hysdsops/mozart/ops/bach-api-${var.bach_api_branch} /export/home/hysdsops/mozart/ops/bach-api",
      "  rm -rf bach-api-${var.bach_api_branch}.tar.gz ",
      "  curl -O \"https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/bach-ui-${var.bach_ui_branch}.tar.gz\"",
      "  tar xvfz bach-ui-${var.bach_ui_branch}.tar.gz",
      "  ln -s /export/home/hysdsops/mozart/ops/bach-ui-${var.bach_ui_branch} /export/home/hysdsops/mozart/ops/bach_ui",
      "  rm -rf bach-ui-${var.bach_ui_branch}.tar.gz ",
      "else",
      "  git clone --single-branch -b ${var.nisar_pcm_branch} https://${var.git_auth_key}@${var.nisar_pcm_repo}",
      "  git clone --single-branch -b ${var.product_delivery_branch} https://${var.git_auth_key}@${var.product_delivery_repo}",
      "  git clone --single-branch -b ${var.pcm_commons_branch} https://${var.git_auth_key}@${var.pcm_commons_repo}",
      "  git clone --single-branch -b ${var.bach_api_branch} https://${var.git_auth_key}@${var.bach_api_repo}",
      "  git clone --single-branch -b ${var.bach_ui_branch} https://${var.git_auth_key}@${var.bach_ui_repo} bach_ui",
      "fi",
      "export PATH=~/conda/bin:$PATH",
      "cp -rp nisar-pcm/conf/sds ~/.sds",
      "cp ~/.sds.bak/config ~/.sds",
      "cd bach_ui",
      "~/conda/bin/npm install --silent",
      "sh create_config_simlink.sh",
      "~/conda/bin/npm run build --silent",
      "cd ../",
      "if [ \"${var.grq_aws_es}\" = true ]; then",
      "  cp -f ~/.sds/files/supervisord.conf.grq.aws_es ~/.sds/files/supervisord.conf.grq",
      "fi",
      "if [ \"${var.factotum["instance_type"]}\" = \"c5.xlarge\" ]; then",
      "  cp -f ~/.sds/files/supervisord.conf.factotum.small_instance ~/.sds/files/supervisord.conf.factotum",
      "fi"
    ]

  }

}

output "mozart_pvt_ip" {
  value = aws_instance.mozart.private_ip
}

output "mozart_pub_ip" {
  value = aws_instance.mozart.public_ip
}


######################
# metrics
######################

resource "aws_instance" "metrics" {
  ami                    = var.metrics["ami"]
  instance_type          = var.metrics["instance_type"]
  key_name               = var.key_name
  availability_zone      = var.az
  iam_instance_profile   = var.pcm_cluster_role["name"]
  tags                   = {
                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.metrics["name"]}"
                           }
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids_metrics

  ebs_block_device {
    device_name = var.metrics["data_dev"]
    volume_size = var.metrics["data_dev_size"]
    volume_type = "gp2"
    delete_on_termination = true
  }

  connection {
    host = self.private_ip
    type     = "ssh"
    user     = "hysdsops"
    private_key = file(var.private_key_file)
  }

  provisioner "local-exec" {
    command = "echo aws_instance.metrics.public_ip = ${aws_instance.metrics.private_ip} >> pcm_cluster_ip_address.txt"
  }

}

output "metrics_pvt_ip" {
  value = aws_instance.metrics.private_ip
}

output "metrics_pub_ip" {
  value = aws_instance.metrics.public_ip
}



######################
# grq
######################

resource "aws_instance" "grq" {
  ami                    = var.grq["ami"]
  instance_type          = var.grq["instance_type"]
  key_name               = var.key_name
  availability_zone      = var.az
  iam_instance_profile   = var.pcm_cluster_role["name"]
  tags                   = {
                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.grq["name"]}"
                           }
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids_grq
  ebs_block_device {
    device_name = var.grq["data_dev"]
    volume_size = var.grq["data_dev_size"]
    volume_type = "gp2"
    delete_on_termination = true
  }

  connection {
    host = self.private_ip
    type     = "ssh"
    user     = "hysdsops"
    private_key = file(var.private_key_file)
  }

 
  provisioner "local-exec" {
    command = "echo aws_instance.grq.public_ip = ${aws_instance.grq.private_ip} >> pcm_cluster_ip_address.txt"
  }


  provisioner "remote-exec" {
    inline = [
      /*
      "sudo mkfs.xfs ${var.grq["data_dev"]}",
      "sudo bash -c \"echo ${lookup(var.grq, "data_dev_mount", var.grq["data_dev"])} ${var.grq["data"]} auto defaults,nofail,comment=terraform 0 2 >> /etc/fstab\"",
      "sudo mkdir -p ${var.grq["data"]}",
      "sudo mount ${var.grq["data"]}",
      "sudo chown -R ops:ops ${var.grq["data"]}",
      "sudo systemctl stop elasticsearch",
      "sudo systemctl stop redis",
      "sudo mkdir -p ${var.grq["data"]}/var/lib",
      "sudo mv /var/lib/redis ${var.grq["data"]}/var/lib/",
      "sudo ln -sf ${var.grq["data"]}/var/lib/redis /var/lib/redis",
      "sudo systemctl start redis",
      "(sudo mv /var/lib/elasticsearch ${var.grq["data"]}/var/lib/ && sudo ln -sf ${var.grq["data"]}/var/lib/elasticsearch /var/lib/elasticsearch && sudo systemctl start elasticsearch) &"
     */
    ]
  }
}

output "grq_pvt_ip" {
  value = aws_instance.grq.private_ip
}

output "grq_pub_ip" {
  value = aws_instance.grq.public_ip
}


######################
# factotum
######################

resource "aws_instance" "factotum" {
  ami                    = var.factotum["ami"]
  instance_type          = var.factotum["instance_type"]
  key_name               = var.key_name
  availability_zone      = var.az
  iam_instance_profile   = var.pcm_cluster_role["name"]
  tags                   = {
                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.factotum["name"]}"
                           }
  subnet_id              = var.subnet_id
  vpc_security_group_ids = var.vpc_security_group_ids_factotum

  #ebs_block_device {
  #  device_name = var.factotum["docker_storage_dev"]
  #  volume_size = var.factotum["docker_storage_dev_size"]
  #  volume_type = "gp2"
  #  delete_on_termination = true
  #}
  ebs_block_device {
    device_name = var.factotum["data_dev"]
    volume_size = var.factotum["data_dev_size"]
    volume_type = "gp2"
    delete_on_termination = true
  }

  connection {
    host = self.private_ip
    type     = "ssh"
    user     = "hysdsops"
    private_key = file(var.private_key_file)
  }

  provisioner "local-exec" {
    command = "echo aws_instance.factotum.private_ip = ${aws_instance.factotum.private_ip} >> pcm_cluster_ip_address.txt"
  }

  provisioner "remote-exec" {
    inline = [
      "cd /tmp",
      "git clone https://github.com/pymonger/docker-ephemeral-lvm.git",
      "cd docker-ephemeral-lvm/docker-ephemeral-lvm.d"
      /*
      "sudo bash docker-ephemeral-lvm.sh.no_encrypt_data",
      "sudo systemctl stop redis",
      "sudo mkdir -p ${var.factotum["data"]}/var/lib",
      "sudo mv /var/lib/redis ${var.factotum["data"]}/var/lib/",
      "sudo ln -sf ${var.factotum["data"]}/var/lib/redis /var/lib/redis",
      "sudo systemctl start redis",
      "sudo bash -c \"echo ${lookup(var.factotum, "data_dev_mount", var.factotum["data_dev"])} ${var.factotum["data"]} auto defaults,nofail,comment=terraform 0 2 >> /etc/fstab\""
     */
    ]
  }
}

output "factotum_pvt_ip" {
  value = aws_instance.factotum.private_ip
}

output "factotum_pub_ip" {
  value = aws_instance.factotum.public_ip
}

######################
# ci
######################

/* comment out cause the ci instance is already up and running
#resource "aws_instance" "ci" {
#  ami                    = "${var.ci["ami"]}"
#  instance_type          = "${var.ci["instance_type"]}"
#  key_name               = "${var.key_name}"
#  availability_zone      = "${var.az}"
#  tags                   = {
#                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.ci["name"]}"
#                           }
#  subnet_id              = "${var.subnet_id}"
#  vpc_security_group_ids = "${var.vpc_security_group_ids_ci}"
#  iam_instance_profile = "${var.pcm_cluster_role["name"]}"
#  ebs_block_device {
#    device_name = "${var.ci["docker_storage_dev"]}"
#    volume_size = "${var.ci["docker_storage_dev_size"]}"
#    volume_type = "gp2"
#    delete_on_termination = true
#  }
#  ebs_block_device {
#    device_name = "${var.ci["data_dev"]}"
#    volume_size = "${var.ci["data_dev_size"]}"
#    volume_type = "gp2"
#    delete_on_termination = true
#  }
#
#  connection {
#    type     = "ssh"
#    user     = "ops"
#    private_key = "${file(var.private_key_file)}"
#  }
#
#  provisioner "local-exec" {
#    ### command = "echo aws_instance.ci.private_ip = ${aws_instance.ci.private_ip} >> pcm_cluster_ip_address.txt"
#    command = "echo aws_instance.ci.private_ip = 100.67.45.139 >> pcm_cluster_ip_address.txt"
#  }
#
#  provisioner "remote-exec" {
#    inline = [
#      "cd /tmp",
#      "git clone https://github.com/pymonger/docker-ephemeral-lvm.git",
#      "cd docker-ephemeral-lvm/docker-ephemeral-lvm.d"
#    ]
#  }
#}
#*/

output "ci_pvt_ip" {
  ### value = "${aws_instance.ci.private_ip}"
  value = "100.67.45.139"
}

output "ci_pub_ip" {
  ### value = "${aws_instance.ci.public_ip}"
  value = "100.67.45.139"
}

/*

######################
# autoscale
######################

resource "aws_instance" "autoscale" {
  ami                    = "${var.autoscale["ami"]}"
  instance_type          = "${var.autoscale["instance_type"]}"
  key_name               = "${var.key_name}"
  availability_zone      = "${var.az}"
  tags                   = {
                             Name = "${var.project}-${var.venue}-${local.counter}-pcm-${var.autoscale["name"]}"
                           }
  subnet_id              = "${var.subnet_id}"
  vpc_security_group_ids = "${var.vpc_security_group_ids}"
  ebs_block_device {
    device_name = "${var.autoscale["docker_storage_dev"]}"
    volume_size = "${var.autoscale["docker_storage_dev_size"]}"
    volume_type = "gp2"
    delete_on_termination = true
  }
  ebs_block_device {
    device_name = "${var.autoscale["data_dev"]}"
    volume_size = "${var.autoscale["data_dev_size"]}"
    volume_type = "gp2"
    delete_on_termination = true
  }

  connection {
    type     = "ssh"
    user     = "ops"
    private_key = "${file(var.private_key_file)}"
  }

  provisioner "local-exec" {
    command = "echo ${aws_instance.autoscale.private_ip} > autoscale_ip_address.txt"
  }

  provisioner "remote-exec" {
    inline = [
      "cd /tmp",
      "git clone https://github.com/pymonger/docker-ephemeral-lvm.git",
      "cd docker-ephemeral-lvm/docker-ephemeral-lvm.d"
      
      #"sudo bash docker-ephemeral-lvm.sh.no_encrypt_data",
      #"sudo bash -c \"echo ${lookup(var.autoscale, "data_dev_mount", var.autoscale["data_dev"])} ${var.autoscale["data"]} auto defaults,nofail,comment=terraform 0 2 >> /etc/fstab\""
       
    ]
  }
}

output "autoscale_pvt_ip" {
  value = "${aws_instance.autoscale.private_ip}"
}

output "autoscale_pub_ip" {
  value = "${aws_instance.autoscale.public_ip}"
}

*/
