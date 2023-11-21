data "aws_ip_ranges" "instances_ec2_europe" {
  regions  = ["eu-west-1", "eu-central-1"]
  services = ["ec2"]
}