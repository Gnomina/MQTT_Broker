terraform {
  backend "s3" {
    bucket = "pi-pico-backend" #name of bucket
    key    = "IC2-instance-backend/terraform.tfstate" #path to file
    region = "eu-central-1" #region
  }
}
