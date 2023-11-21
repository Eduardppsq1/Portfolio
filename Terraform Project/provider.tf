provider "aws" {
  shared_credentials_files = var.AWS_PATH_TO_CREDENTIALS
  profile                  = var.AWS_USER
  region                   = var.AWS_REGION
}

