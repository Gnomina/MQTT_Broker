

output "instance_public_ip" {
  value = module.instanse.instance_public_ip #This variable locate in Instance module -> outputs 
  description = "public ip of instance from Instance module (outputs_source = ./terraform/instanse)"
}
