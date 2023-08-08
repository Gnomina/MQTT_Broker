
#---------------VPC outputs-----------------

output "vpc_id_out" { # Local output variable
  value = aws_vpc.this.id
  description = "vps_id"
}

output "subnet_id_out" { # Local output variable
  value = aws_subnet.public[*].id
  description = "subnet_id"
}