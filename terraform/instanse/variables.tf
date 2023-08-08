
#----------------Instance Variables----------------

variable "instance_type"{
  default     = "t2.mikro" # Local variable
    description = "(Free tire eligible t2micro) t2.small instance"
}

variable "key_name"{
  default     = "ubuntu_key" # Local variable
    description = "SSH key for instance"
}

variable "security_group" { # variable from  SG module -> outputs
  description = "local value of the 'security_group_id' variable from the SG module -> outputs"
}

variable "subnet_ids"  { # variable from  VPC module -> outputs
  description = "local value of the 'subnet_id_out' variable from the VPC module -> outputs"
}

variable "Tags" { # local variable
  default     = "Tag-Instance"
    description = "Tags of the Instanse"
}