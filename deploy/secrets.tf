resource "aws_secretsmanager_secret" "github_token" {
  name = "C7NGithubToken"
}

resource "aws_secretsmanager_secret_version" "github_token" {
  secret_id     = aws_secretsmanager_secret.github_token.id
  secret_string = var.github_token
}
