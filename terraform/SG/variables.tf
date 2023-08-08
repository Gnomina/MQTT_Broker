
#-------------Security Group Variables-----------------

variable "Name" { #local variable
  default     = "SG"
  type        = string
    description = "Name of the SG"
}

variable "description" { # local variable
  default     = "SG"
  type        = string
    description = "Description of the SG"
}

variable "Tags" { # local variable
  default     = "Tag-SG"
    description = "Tags of the SG"
}

variable "vpc_id" { # local variable
  description = "ID of the VPC from VPC module -> outputs"
}


variable "ingress_ports" { # local variable
  description = "List of ingress ports"
  type        = list(string)
  default     = ["22"]
}