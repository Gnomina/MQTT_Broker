

output "instance_public_ip" {
  value = module.instance.instance_public_ip #This variable locate in Instance module -> outputs 
  description = "public ip of instance from Instance module (outputs_source = ./terraform/instanse)"
}

output "instance_id" { # Local output variable
  value = module.instance.instance_id # Instance ID that the instance receives from AWS. output variable.}
}
