resource "aws_subnet" "public_eu_central_1a" {
  vpc_id = aws_vpc.main.id
  cidr_block = "10.0.64.0/19"
  availability_zone = "eu-central-1a"
  
  tags = {
    Name = "pico-dev-PUB-subnet"
  }
}