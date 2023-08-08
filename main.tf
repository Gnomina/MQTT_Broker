module "VPC" { # Include VPC module
  source = "./terraform/VPC" # VPC Module PATH

  env = "Pico-test" # Enviorement name
  azs = ["eu-central-1a"] # How many zones are needed
  public_subnets = ["10.0.64.0/19"] # How many subnets are needed

  public_subnet_tags = {
    "Pico-dev-demo" = "test"
  }
}

module "SG" { # Include VPC module
  source = "./terraform/SG" # VPC Module PATH
  
  vpc_id = module.VPC.vpc_id_out # Variable from VPC module
  
  Name = "Pico-SG" # Security group name
  ingress_ports = ["22", "80"] # Alloved ports
  
  Tags = {
    Name = "Pico-test_SG" # Security group tags name
  }
}

module "instance" {
  source = "./terraform/instance"

  subnet_id = module.VPS.subnet_id_out
  security_group = module.SG.security_group_id_out
  
  Tags = {
    Name = "Pico-test_Instance" # Security group tags name
  }
  
}
