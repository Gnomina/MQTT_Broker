resource "aws_internet_gateway" "igw"{
  vps_id = aws_vpc.main.id

  tags = {
    Name = "pico-dev-igv"
  }
}