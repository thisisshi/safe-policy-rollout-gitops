output "c7n_image_url" {
  value = aws_ecr_repository.c7n.repository_url
}

output "policystream_image_url" {
  value = aws_ecr_repository.policystream.repository_url
}

output "c7n_image_tag" {
  value = var.c7n_image_tag
}
