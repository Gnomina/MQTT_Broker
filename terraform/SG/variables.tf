
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
  type        = map(any)
    description = "Tags of the SG"
}

variable "vpc_id" {
  description = "ID of the VPC from VPC module -> outputs"
}


