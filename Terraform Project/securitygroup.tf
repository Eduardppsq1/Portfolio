resource "aws_security_group" "europe" {
  name = "Test_SG"
  vpc_id      = aws_vpc.main.id
  
  ingress {
    from_port   = "8089"
    to_port     = "8089"
    protocol    = "tcp"
    cidr_blocks = slice(data.aws_ip_ranges.instances_ec2_europe.cidr_blocks, 0, 50)
  }

  tags = {
    Name          = "Test"
    DataCreare    = data.aws_ip_ranges.instances_ec2_europe.create_date
    SyncToken     = data.aws_ip_ranges.instances_ec2_europe.sync_token
    OptionalTagID = data.aws_ip_ranges.instances_ec2_europe.id
  }

  egress {
    from_port   = "8081"
    protocol    = "tcp"
    to_port     = "8081"
    cidr_blocks = slice(data.aws_ip_ranges.instances_ec2_europe.cidr_blocks, 0, 50)
  }
}
