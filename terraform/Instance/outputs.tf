
#--------------Instance Outputs-----------------

output "instance_public_ip" { # Local output variable
  value = aws_instance.this.public_ip # Public IP that the instance receives from AWS. output variable.
 }

 output "instance_id" { # Local output variable
  value = aws_instance.this.id # Instance ID that the instance receives from AWS. output variable.}
}