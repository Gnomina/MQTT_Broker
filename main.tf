module "VPC" { #Include VPC module
  source = "./terraform/VPC" #VPC Module PATH

  env = "Pico-test" #enviorement name
  azs = ["eu-central-1a"] # how many zones are needed
  public_subnets = ["10.0.64.0/19"] # how many subnets are needed

  public_subnet_tags = {
    "Pico-dev-demo" = "test"
  }
}

module "SG" {
  source = "./terraform/SG"
  
  vpc_id = module.VPC.vpc_id_out

  Name = "Pico-SG"
  Tags = {
    Name = "Pico-test_SG"
  }
}
