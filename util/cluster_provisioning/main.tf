provider "aws" {
  shared_credentials_file = var.shared_credentials_file
  region                  = var.region
  profile                 = var.profile
}

module "common" {
  source = "./modules/common"

  hysds_release                         = var.hysds_release
  nisar_pcm_repo                        = var.nisar_pcm_repo
  nisar_pcm_branch                      = var.nisar_pcm_branch
  product_delivery_repo                 = var.product_delivery_repo
  product_delivery_branch               = var.product_delivery_branch
  pcm_commons_repo                      = var.pcm_commons_repo
  pcm_commons_branch                    = var.pcm_commons_branch
  bach_api_repo                         = var.bach_api_repo
  bach_api_branch                       = var.bach_api_branch
  bach_ui_repo                          = var.bach_ui_repo
  bach_ui_branch                        = var.bach_ui_branch
  venue                                 = var.venue
  counter                               = var.counter
  private_key_file                      = var.private_key_file
  git_auth_key                          = var.git_auth_key
  jenkins_api_user                      = var.jenkins_api_user
  keypair_name                          = var.keypair_name
  jenkins_api_key                       = var.jenkins_api_key
  ops_password                          = var.ops_password
  shared_credentials_file               = var.shared_credentials_file
  profile                               = var.profile
  project                               = var.project
  region                                = var.region
  az                                    = var.az
  subnet_id                             = var.subnet_id
  verdi_security_group_id               = var.verdi_security_group_id
  cluster_security_group_id             = var.cluster_security_group_id
  pcm_cluster_role                      = var.pcm_cluster_role
  pcm_verdi_role                        = var.pcm_verdi_role
  mozart                                = var.mozart
  metrics                               = var.metrics
  grq                                   = var.grq
  factotum                              = var.factotum
  ci                                    = var.ci
  common_ci                             = var.common_ci
  autoscale                             = var.autoscale
  lambda_vpc                            = var.lambda_vpc
  lambda_role_arn                       = var.lambda_role_arn
  lambda_job_type                       = var.lambda_job_type
  lambda_job_queue                      = var.lambda_job_queue
  cnm_r_handler_job_type                = var.cnm_r_handler_job_type
  cnm_r_job_queue                       = var.cnm_r_job_queue
  cnm_r_event_trigger                   = var.cnm_r_event_trigger
  cnm_r_allowed_account                 = var.cnm_r_allowed_account
  daac_delivery_proxy                   = var.daac_delivery_proxy
  daac_endpoint_url                     = var.daac_endpoint_url
  asg_use_role                          = var.asg_use_role
  asg_role                              = var.asg_role
  asg_vpc                               = var.asg_vpc
  aws_account_id                        = var.aws_account_id
  lambda_package_release                = var.lambda_package_release
  environment                           = var.environment
  use_artifactory                       = var.use_artifactory
  artifactory_repo                      = var.artifactory_repo
  grq_aws_es                            = var.grq_aws_es
  grq_aws_es_host                       = var.grq_aws_es_host
  grq_aws_es_port                       = var.grq_aws_es_port
  grq_aws_es_host_private_verdi         = var.grq_aws_es_host_private_verdi
  use_grq_aws_es_private_verdi          = var.use_grq_aws_es_private_verdi
  use_daac_cnm                          = var.use_daac_cnm
  pge_snapshots_date                    = var.pge_snapshots_date
  nisar_pge_release                     = var.nisar_pge_release
  crid                                  = var.crid
  cluster_type                          = var.cluster_type
  l0a_timer_trigger_frequency           = var.l0a_timer_trigger_frequency
  rs_fwd_bucket_ingested_expiration     = var.rs_fwd_bucket_ingested_expiration
  dataset_bucket                        = var.dataset_bucket
  code_bucket                           = var.code_bucket
  lts_bucket                            = var.lts_bucket
  triage_bucket                         = var.triage_bucket
  isl_bucket                            = var.isl_bucket
  osl_bucket                            = var.osl_bucket
  use_s3_uri_structure                  = var.use_s3_uri_structure
}

locals {
  lambda_repo = "https://cae-artifactory.jpl.nasa.gov/artifactory/${var.artifactory_repo}/gov/nasa/jpl/nisar/sds/pcm/lambda"
}

resource "null_resource" "mozart" {
  depends_on = [module.common.mozart]

  triggers = {
    private_ip       = module.common.mozart.private_ip
    private_key_file = var.private_key_file
    code_bucket      = module.common.code_bucket
    dataset_bucket   = module.common.dataset_bucket
    triage_bucket    = module.common.triage_bucket
    lts_bucket       = module.common.lts_bucket
  }

  connection {
    type        = "ssh"
    host        = self.triggers.private_ip
    user        = "hysdsops"
    private_key = file(self.triggers.private_key_file)
  }

  provisioner "remote-exec" {
    /*
    inline = [
      "set -ex",
      "source ~/.bash_profile",
      "cd ~/.sds/files",
      "~/mozart/ops/hysds/scripts/ingest_dataset.py AOI_sacramento_valley ~/mozart/etc/datasets.json",
      "echo Your cluster has been provisioned!",
    ]
    */
    inline = ["echo Your cluster has been provisioned!"]
  }
}

