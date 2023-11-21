resource "aws_instance" "test_node" {
  ami           = var.AMIS[var.AWS_REGION]
  instance_type = "t2.micro"

  # VPC subnet
  subnet_id = aws_subnet.subnet-public-1.id

  # Atasam Firewall-ul la nivel de instanta SG-ul
  vpc_security_group_ids = [aws_security_group.europe.id]

  # cheia publica SSH
  key_name = aws_key_pair.mykeypair.key_name

  # user data
  user_data = data.template_cloudinit_config.cloudinit-example.rendered

  tags = {
    Name = "Testing"
  }
}

resource "aws_ebs_volume" "ebs-volum" {
  availability_zone = "eu-west-1a"
  size              = 20
  type              = "gp2"
  tags = {
    Name = "Atasam un volum extra"
  }
}

resource "aws_volume_attachment" "ebs-volum-attachment" {
  device_name  = var.FORMAT_DISC
  volume_id    = aws_ebs_volume.ebs-volum.id
  instance_id  = aws_instance.test_node.id
  skip_destroy = true
}

