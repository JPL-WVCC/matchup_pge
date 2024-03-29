# globals
#
# venue : leipan 
# counter : 1-n
# private_key_file : the equivalent to .ssh/id_rsa or .pem file
#
variable "wvcc_pcm_repo" {
  default = "github.jpl.nasa.gov/msas-hysds/wvcc-pcm.git"
}
variable "wvcc_pcm_branch" {
  default = "develop"
}
variable "venue" {default = "leipan"}
variable "environment" {default = "dev"}
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
variable "jenkins_api_key" {
  default = "11114e63d8baded1bded892c01f8b91781"
}

/*
variable "ops_password" {
  default = "ops"
}
*/

variable "shared_credentials_file" {
  default = "~/.aws/credentials"
}
#
# "default" links to [default] profile in "shared_credentials_file" above
#
/*
variable "profile" {
  default = "saml-pub"
}
*/
# __key_name__ is the aws Key pair name
variable "key_name" {
  default = "wvcc-pcm-dev"
}

variable "project" {
  default = "wvcc"
}

/*
variable "region" {
  default = "us-west-2"
}

variable "az" {
  default = "us-west-2a"
}
*/

variable "subnet_id" {
  default = "subnet-058bb180c744135dc"
}

variable "cluster_security_group_id" {
  default = "sg-029b5af59364a4b3c"
}

variable "vpc_security_group_ids" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "vpc_security_group_ids_mozart" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "vpc_security_group_ids_metrics" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "vpc_security_group_ids_grq" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "vpc_security_group_ids_factotum" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "vpc_security_group_ids_ci" {
  type = list
  default = [
    "sg-0ada8792640d0c6c2"
  ]
}

variable "pcm_cluster_role" {
  default = {
      name = "am-pcm-dev-cluster-role"
      path = "/"
  }
}

variable "pcm_verdi_role" {
  default = {
      name = "am-pcm-dev-verdi-role"
      path = "/"
  }
}
# mozart vars
variable "mozart" {
  type = map
  default = {
    name = "mozart"
    ami = "ami-06e70d2b695da7784"
    instance_type = "r4.xlarge"
    data = "/data"
    data_dev = "/dev/xvdb"
    data_dev_size = 50
    data2 = "/data2"
    data2_dev = "/dev/xvdc"
    data2_dev_size = 50
  }
}

# metrics vars
variable "metrics" {
  type = map
  default = {
    name = "metrics"
    ami = "ami-036dbc4e5e449dc4a"
    instance_type = "r4.xlarge"
    data = "/data"
    data_dev = "/dev/xvdb"
    data_dev_size = 100
  }
}

# grq vars
variable "grq" {
  type = map
  default = {
    name = "grq"
    ami = "ami-04d8c34c8245995be"
    instance_type = "r4.xlarge"
    data = "/data"
    data_dev = "/dev/xvdb"
    data_dev_size = 100
  }
}

# factotum vars
variable "factotum" {
  type = map
  default = {
    name = "factotum"
    ami = "ami-02cf4271eaab67085"
    instance_type = "r4.xlarge"
  ###  instance_type = "c3.xlarge"
  #  docker_storage_dev = "/dev/xvdb"
  #  docker_storage_dev_size = 50
    data = "/data"
    data_dev = "/dev/xvdf"
    data_dev_size = 150
  }
}

# ci vars
variable "ci" {
  type = map
  default = {
    name = "ci"
    ami = "ami-020e21e5712afefc4"
    instance_type = "c3.xlarge"
    docker_storage_dev = "/dev/xvdb"
    docker_storage_dev_size = 50
    data = "/data"
    data_dev = "/dev/xvdc"
    data_dev_size = 100
  }
}

variable "common_ci" {
  type = map(string)
  default = {
    name       = "ci"
    private_ip = "100.67.45.139"
    public_ip  = "100.67.45.139"
  }
}
# autoscale vars
variable "autoscale" {
  type = map
  default = {
    name = "autoscale"
    ami = "ami-0601c031b967d1e15"
    instance_type = "c3.large"
    docker_storage_dev = "/dev/xvdb"
    docker_storage_dev_size = 50
    data = "/data"
    data_dev = "/dev/xvdc"
    data_dev_size = 100
  }
}

# staging area vars
variable "lambda_secgroup" {
  default = "sg-0ada8792640d0c6c2"
}

variable "lambda_vpc" {
  default = "vpc-0ed9261aea0ac2286"
}

variable "lambda_role_arn" {
  default = "arn:aws:iam::293861788641:role/am-pcm-dev-lambda-role"
}

variable "lambda_job_type" {
  default = "INGEST_STAGED"
}

variable "lambda_job_queue" {
  default = "factotum-job_worker-small"
}

# asg vars
variable "asg_ami" {
  default = "ami-07db5946dc5d4d6fa"
}

variable "asg_keypair" {
  default = "wvcc-pcm-dev"
}

variable "asg_use_role" {
  default = "true"
}

variable "asg_role" {
  default = "am-pcm-dev-verdi-role"
}

variable "asg_secgroup1" {
  default = "sg-0cf54bed963ec6435"
}

variable "asg_secgroup2" {
 default = ""
}

variable "asg_secgroup3" {
 default = ""
}

variable "asg_vpc" {
  default = "vpc-0db7a713a6785cd0f"
}
