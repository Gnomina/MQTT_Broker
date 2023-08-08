provider "aws" { # provider
  region = "eu-central-1" 
}

terraform{ #terraform version setting and backend
  required_version = ">=1.0"

  backend "s3" {
    bucket = "pi-pico-backend" #name of bucket
    key    = "IC2-instance-backend/terraform.tfstate" #path to file
    region = "eu-central-1" #region
  }

  required_providers {
    aws = {
      source = "hashicorp/aws"
      version = "~>4.62"
    }
  }
}