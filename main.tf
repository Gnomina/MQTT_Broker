module "VPC" { #Include VPC module
  source = "./terraform/VPC" #VPC Module PATH

  env = "Pico-test"
  azs = ["eu-central-1a", "eu-central-1b"]
  public_subnets = ["10.0.64.0/19", "10.0.94.0/19"]

  public_subnet_tags = {
    "Pico-dev-demo" = "test"
  }
}