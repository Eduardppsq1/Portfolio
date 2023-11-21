variable "AWS_REGION" {
  default = "eu-west-1"
}

variable "AWS_PATH_TO_CREDENTIALS" {
  default = ["~/.aws/credentials"]
}

variable "AWS_USER" {
  default = "default"
}

variable "CHEIE_PRIVATA" {
  default = "mykey"
}

variable "CHEIE_PUBLICA" {
  default = "mykey.pub"
}

variable "AMIS" {
  type = map(string)
  default = {
    us-east-1 = "ami-13be557e"
    us-west-2 = "ami-06b94666"
    eu-west-1 = "ami-0694d931cee176e7d"
  }
}

variable "FORMAT_DISC" {
  default = "/dev/xvdh"
}

