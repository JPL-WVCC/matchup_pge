variable "artifactory_repo" {
  default = "general-develop"
}

variable "hysds_release" {
}

variable "nisar_pcm_repo" {
}

variable "nisar_pcm_branch" {
}

variable "pcm_commons_repo" {
}

variable "pcm_commons_branch" {
}

variable "product_delivery_repo" {
}

variable "product_delivery_branch" {
}

variable "bach_api_repo" {
}

variable "bach_api_branch" {
}

variable "bach_ui_repo" {
}

variable "bach_ui_branch" {
}

variable "venue" {
}

variable "counter" {
}

variable "private_key_file" {
}

variable "git_auth_key" {
}

variable "jenkins_api_user" {
}

variable "keypair_name" {
}

variable "jenkins_api_key" {
}

variable "jenkins_host" {
  default = "https://nisar-pcm-ci.jpl.nasa.gov"
}

variable "jenkins_enabled" {
  default = true
}

variable "ops_password" {
}

variable "shared_credentials_file" {
}

variable "profile" {
}

variable "project" {
}

variable "region" {
}

variable "az" {
}

variable "subnet_id" {
}

variable "verdi_security_group_id" {
}

variable "cluster_security_group_id" {
}

variable "pcm_cluster_role" {
}

variable "pcm_verdi_role" {
}

variable "grq_aws_es" {
  //  boolean
}

variable "grq_aws_es_host" {
}

variable "grq_aws_es_port" {
}

variable "grq_aws_es_host_private_verdi" {
}

variable "use_grq_aws_es_private_verdi" {
}

# ami vars
variable "amis" {
  type = map(string)
  default = {
    mozart    = "ami-034cac101413163d1"
    metrics   = "ami-02b96854c127138c8"
    grq       = "ami-024ab0dc53721534a"
    factotum  = "ami-04a53e3809bc4a9a5"
    ci        = ""
    autoscale = "ami-07db5946dc5d4d6fa"
  }
}

variable "mozart" {
}

variable "metrics" {
}

variable "grq" {
}

variable "factotum" {
}

variable "ci" {
}

variable "common_ci" {
}

variable "autoscale" {
}

variable "lambda_vpc" {
}

variable "lambda_role_arn" {
}

variable "lambda_job_type" {
}

variable "lambda_job_queue" {
}

variable "cnm_r_handler_job_type" {
}

variable "cnm_r_job_queue" {
}

variable "cnm_r_event_trigger" {
}

variable "cnm_r_event_trigger_values_list" {
  description = "acceptable values for setting cnm_r_event_trigger"
  type        = list(string)
  default     = ["sns", "kinesis", "sqs"]
}

variable "cnm_r_allowed_account" {
}

variable "daac_delivery_proxy" {
}

variable "daac_endpoint_url" {
}

variable "asg_use_role" {
}

variable "asg_role" {
}

variable "asg_vpc" {
}

variable "aws_account_id" {
}

variable "lambda_cnm_r_handler_package_name" {
  default = "lambda-cnm-r-handler"
}

variable "lambda_harikiri_handler_package_name" {
  default = "lambda-harikiri-handler"
}

variable "lambda_isl_handler_package_name" {
  default = "lambda-isl-handler"
}

variable "lambda_timer_handler_package_name" {
  default = "lambda-timer-handler"
}

variable "lambda_e-misfire_handler_package_name" {
  default = "lambda-event-misfire-handler"
}

variable "lambda_package_release" {
}

variable "queues" {
  default = {
    "nisar-job_worker-gpu" = {
      "instance_type" = ["p2.xlarge", "p3.2xlarge"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-small" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-large" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-rrst-acct" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-l0a" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-time_extractor" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-datatake-acct" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-track-frame-acct" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-l0b" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-rslc" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-gslc" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-gcov" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-sciflo-insar" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-send_cnm_notify" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-job_worker-rcv_cnm_notify" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
     "nisar-job_worker-net" = {
      "instance_type" = ["c5.4xlarge"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
    "nisar-workflow_profiler" = {
      "instance_type" = ["p2.xlarge", "p3.2xlarge", "r5.2xlarge", "r5.4xlarge", "r5.8xlarge", "r5.12xlarge", "r5.16xlarge", "r5.24xlarge", "r5.metal"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    },
    "nisar-job_worker-timer" = {
      "instance_type" = ["t2.medium", "t3a.medium", "t3.medium"]
      "root_dev_size" = 50
      "data_dev_size" = 100
      "max_size" = 10
    }
    "nisar-job_worker-pta" = {
      "instance_type" = ["c5.4xlarge"]
      "root_dev_size" = 50
      "data_dev_size" = 25
      "max_size"      = 10
    }
  }
}

variable "environment" {
}

variable "use_artifactory" {
}

variable "event_misfire_trigger_frequency" {
  default = "rate(5 minutes)"
}

variable "event_misfire_delay_threshold_seconds" {
  type    = number
  default = 60
}

variable "use_daac_cnm" {
}

variable "daac_cnm_sqs_arn" {
  type = map(string)
  default = {
    dev  = "arn:aws:sqs:us-west-2:271039147104:nisar-dev-daac-cnm-response"
    test = "arn:aws:sqs:us-west-2:399787141461:nisar-test-daac-cnm-response"
    int  = "arn:aws:sqs:us-west-2:271039147104:nisar-int-daac-cnm-response"
  }
}

variable "lambda_log_retention_in_days" {
  type    = number
  default = 30
}

variable "pge_names" {
  default = "nisar_pge-l0a,nisar_pge-lsar_time_extractor,nisar_pge-l0b,nisar_pge-l1_l2"
}

variable "docker_registry_bucket" {
  default = "nisar-pcm-registry-bucket"
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

variable "l0a_timer_trigger_frequency" {
}

variable "cluster_type" {}

variable "valid_cluster_type_values" {
  type = list(string)
  default = ["forward", "reprocessing"]
}

variable "rs_fwd_bucket_ingested_expiration" {
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
