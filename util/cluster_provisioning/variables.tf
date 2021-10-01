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
  default = "develop"
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

/*
variable "venue" {
  default = "leipan"
}

variable "counter" {
  default = "1"
}

variable "private_key_file" {
  default = "/export/home/hysdsops/.ssh/wvcc-pcm-dev.pem"
}

variable "git_auth_key" {
  default = "b2cb57ce8b3daa3f5c72a34a99d2cf1434b6c3ee"
}

variable "jenkins_api_user" {
  default = ""
}
*/

variable "keypair_name" {
  default = ""
}

/*
variable "jenkins_api_key" {
  default = "11114e63d8baded1bded892c01f8b91781"
}
*/

variable "ops_password" {
  default = "hysdsops"
}

/*
variable "shared_credentials_file" {
  default = "~/.aws/credentials"
}
*/

#
# "default" links to [default] profile in "shared_credentials_file" above
#
variable "profile" {
  default = "saml-pub"
}

/*
variable "project" {
  default = "wvcc"
}
*/

variable "region" {
  default = "us-west-2"
}

variable "az" {
  default = "us-west-2a"
}

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
  ### default = "sg-029b5af59364a4b3c"
  default = "sg-0b4e1f7038191c5e1"
}

/*
variable "cluster_security_group_id" {
}
*/



# mozart vars
/*
variable "mozart" {
  type = map(string)
  default = {
    name          = "mozart"
    instance_type = "r5.xlarge"
    root_dev_size = 100
    private_ip    = ""
    public_ip     = ""
  }
}
*/



# metrics vars
/*
variable "metrics" {
  type = map(string)
  default = {
    name          = "metrics"
    instance_type = "r5.xlarge"
    private_ip    = ""
    public_ip     = ""
  }
}
*/

# grq vars
/*
variable "grq" {
  type = map(string)
  default = {
    name          = "grq"
    instance_type = "r5.xlarge"
    private_ip    = ""
    public_ip     = ""
  }
}
*/



# factotum vars
/*
variable "factotum" {
  type = map(string)
  default = {
    name          = "factotum"
    instance_type = "c5.xlarge"
    root_dev_size = 50
    data          = "/data"
    data_dev      = "/dev/xvdb"
    data_dev_size = 300
    private_ip    = ""
    public_ip     = ""
  }
}
*/


# ci vars
/*
variable "ci" {
  type = map(string)
  default = {
    name          = "ci"
    instance_type = "c5.xlarge"
    data          = "/data"
    data_dev      = "/dev/xvdb"
    data_dev_size = 100
    private_ip    = ""
    public_ip     = ""
  }
}
*/



/*
variable "common_ci" {
  type = map(string)
  default = {
    name       = "ci"
    private_ip = "100.64.122.201"
    public_ip  = "100.64.122.201"
  }
}
*/

# autoscale vars
/*
variable "autoscale" {
  type = map(string)
  default = {
    name          = "autoscale"
    instance_type = "t2.micro"
    data          = "/data"
    data_dev      = "/dev/xvdb"
    data_dev_size = 300
    private_ip    = ""
    public_ip     = ""
  }
}
*/



# staging area vars
/*
variable "lambda_secgroup" {
  default = "sg-0ada8792640d0c6c2"
}

variable "lambda_vpc" {
  ### default = "vpc-b42510d0"
  default = "vpc-0ed9261aea0ac2286"
}

variable "lambda_role_arn" {
  ### default = "arn:aws:iam::271039147104:role/am-pcm-lambda-role"
  default = "arn:aws:iam::293861788641:role/am-pcm-dev-lambda-role"
}

variable "lambda_job_type" {
  default = "INGEST_STAGED"
}

variable "lambda_job_queue" {
  ### default = "nisar-job_worker-small"
  default = "factotum-job_worker-small"
}
*/

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
#  arn:aws:sqs:us-west-2:871271927522:asf-w2-cumulus-dev-nisar-workflow-queue
variable "daac_delivery_proxy" {
  default = "arn:aws:sqs:us-west-2:782376038308:daac-proxy-for-nisar"
}

variable "use_daac_cnm" {
  default = false

}

variable "daac_endpoint_url" {
  default = ""
}

# asg vars
/*
variable "asg_use_role" {
  default = "true"
}

variable "asg_role" {
  ### default = "am-pcm-verdi-role"
  default = "am-pcm-dev-verdi-role"
}
*/

/*
variable "asg_vpc" {
  ### default = "vpc-b42510d0"
  default = "vpc-0db7a713a6785cd0f"
}
*/

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

/*
variable "environment" {
  default = "dev"
}
*/

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
  ### default = true
  default = false
}
