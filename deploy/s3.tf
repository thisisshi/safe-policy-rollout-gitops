locals {
  bucket_name = var.bucket == "" ? aws_s3_bucket.c7n_ci[0].id : var.bucket
}

resource "aws_s3_bucket" "c7n_ci" {
  count         = var.bucket == "" ? 1 : 0
  bucket_prefix = "c7n-ci"
  acl           = "private"
  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }
}

resource "aws_s3_bucket_object" "parse_output" {
  bucket = local.bucket_name
  key    = "scripts/parse_output.py"
  source = "${path.module}/scripts/parse_output.py"
}

resource "aws_s3_bucket_object" "resolve_base" {
  bucket = local.bucket_name
  key    = "scripts/resolve_base.py"
  source = "${path.module}/scripts/resolve_base.py"
}

resource "aws_s3_bucket_object" "requirements" {
  bucket = local.bucket_name
  key    = "scripts/requirements.txt"
  source = "${path.module}/scripts/requirements.txt"
}

resource "aws_s3_bucket_object" "buildspec" {
  bucket = local.bucket_name
  key    = "buildspec.yaml"
  source = "${path.module}/buildspec.yaml"
}

resource "aws_s3_bucket_object" "accounts_yaml" {
  bucket = local.bucket_name
  key = "accounts.yaml"
  source = var.accounts_yaml
}

output "bucket" {
  value = local.bucket_name
}
