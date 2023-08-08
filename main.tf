module "VPC" { #Include VPC module
  source = "./terraform/VPC" #VPC Module PATH

  env = "Pico-dev"
  azs = ["eu-central-1a"]
  public_subnets = ["10.0.64.0/19"]

  public_subnet_tags = {
    "Pico-dev-demo" = "owned"
  }
}