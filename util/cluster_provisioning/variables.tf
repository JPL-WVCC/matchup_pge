# globals
#
# venue : userId 
# counter : 1-n
# private_key_file : the equivalent to .ssh/id_rsa or .pem file
#
variable "artifactory_repo" {
  default = "general-develop"
}

variable "hysds_release" {
}

variable "nisar_pcm_repo" {
  default = "github.jpl.nasa.gov/IEMS-SDS/nisar-pcm.git"
}

variable "nisar_pcm_branch" {
  default = "develop"
}

variable "pcm_commons_repo" {
  default = "github.jpl.nasa.gov/IEMS-SDS/pcm_commons.git"
}

variable "pcm_commons_branch" {
  default = "develop"
}

variable "product_delivery_repo" {
  default = "github.jpl.nasa.gov/IEMS-SDS/CNM_product_delivery.git"
}

variable "product_delivery_branch" {
  default = "develop"
}

variable "bach_api_repo" {
  default = "github.jpl.nasa.gov/IEMS-SDS/bach-api.git"
}

variable "bach_api_branch" {
  default = "nisar"
}

variable "bach_ui_repo" {
  default = "github.jpl.nasa.gov/IEMS-SDS/bach-ui.git"
}

variable "bach_ui_branch" {
  default = "nisar"
}

variable "keypair_name" {
  default = ""
}

#
# "default" links to [default] profile in "shared_credentials_file" above
#
variable grq_aws_es {
  default = false
}

variable grq_aws_es_host {
  default = "vpce-0d33a52fc8fed6e40-ndiwktos.vpce-svc-09fc53c04147498c5.us-west-2.vpce.amazonaws.com"
}

variable "grq_aws_es_host_private_verdi" {
  default = "vpce-07498e8171c201602-l2wfjtow.vpce-svc-09fc53c04147498c5.us-west-2.vpce.amazonaws.com"
}

variable grq_aws_es_port {
  default = 443
}

variable "use_grq_aws_es_private_verdi" {
  default = true
}

variable "verdi_security_group_id" {
}

variable "cluster_security_group_id" {
}

# CNM Response job vars

variable "cnm_r_handler_job_type" {
  default = "process_cnm_response"
}

variable "cnm_r_job_queue" {
  default = "nisar-job_worker-rcv_cnm_notify"
}

variable "cnm_r_event_trigger" {
  default = "sqs"
}

variable "cnm_r_allowed_account" {
  default = "*"
}

#The value of daac_delivery_proxy can be
#  arn:aws:sqs:us-west-2:782376038308:daac-proxy-for-nisar
#  arn:aws:sqs:us-west-2:871271927522:sds-n-cumulus-dev-nisar-workflow-queue
variable "daac_delivery_proxy" {
  default = "arn:aws:sqs:us-west-2:782376038308:daac-proxy-for-nisar"
}

variable "use_daac_cnm" {
  default = false

}

variable "daac_endpoint_url" {
  default = ""
}

variable "aws_account_id" {
  ### default = "271039147104"
  default = "293861788641"
}

variable "lambda_package_release" {
  default = "develop"
}

variable "cop_catalog_url" {
  default = ""
}

variable "delete_old_cop_catalog" {
  default = false
}

variable "rost_catalog_url" {
  default = ""
}

variable "delete_old_rost_catalog" {
  default = false
}

variable "pass_catalog_url" {
  default = ""
}

variable "delete_old_pass_catalog" {
  default = false
}

variable "delete_old_observation_catalog" {
  default = false
}

variable "delete_old_radar_mode_catalog" {
  default = false
}

variable "use_artifactory" {
  default = false
}

variable "event_misfire_trigger_frequency" {
  default = "rate(5 minutes)"
}

variable "event_misfire_delay_threshold_seconds" {
  type    = number
  default = 60
}

variable "lambda_log_retention_in_days" {
  type    = number
  default = 30
}

variable "pge_snapshots_date" {
  default = "20210325-R1.1.1"
}

variable "nisar_pge_release" {
  default = "R1.1.1"
}

variable "crid" {
  default = "D00001"
}

variable "cluster_type" {
  default = "reprocessing"
}

variable "l0a_timer_trigger_frequency" {
  default = "rate(60 minutes)"
}

variable "rs_fwd_bucket_ingested_expiration" {
  default = 14
}

variable "dataset_bucket" {
  default = ""
}

variable "code_bucket" {
  default = ""
}

variable "lts_bucket" {
  default = ""
}

variable "triage_bucket" {
  default = ""
}

variable "isl_bucket" {
  default = ""
}

variable "osl_bucket" {
  default = ""
}

variable "use_s3_uri_structure" {
  default = false
}
