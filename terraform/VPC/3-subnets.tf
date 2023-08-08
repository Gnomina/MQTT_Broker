resource "aws_subnet" "public" {
  count = length(var.public_subnets)

  vpc_id = aws_vpc.this.id
  cidr_block = var.public_subnets[count.index]
  availability_zone = var.azs[count.index]
  
  tags = merge(
    { Name = "${var.env}-public-${var.azs[count.index]}" },
    var.public_subnet_tags
  )
}