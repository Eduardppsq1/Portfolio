terraform {
  backend "s3" {
    bucket       = "terraform-test-edi"
    key          = "test-environment/terraform.tfstate"
    region       = var.AWS_REGION
  }
}

# The bucket has to be created. If it's not, it can be created as below:

#resource "aws_s3_bucket" "terraform-test-edi" {
#  bucket = "terraform-test-edi"
#  versioning {
#    enabled = true
#  }
#  lifecycle {
#    prevent_destroy = false
#  }
#  tags = {
#    Name = "S3 Terraform State for Terraform Project"
#  }
#}
