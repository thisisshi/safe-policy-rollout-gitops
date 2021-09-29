provider "aws" {
  default_tags {
    tags = var.tags
  }
}

data "aws_region" "current" {}
data "aws_caller_identity" "current" {}
