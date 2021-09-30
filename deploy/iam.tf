resource "aws_iam_role" "codebuild_executor" {
  name = "C7NPolicyCIRole"

  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": [
          "codebuild.amazonaws.com"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF
}

resource "aws_iam_role_policy_attachment" "codebuild_executor" {
  role       = aws_iam_role.codebuild_executor.name
  policy_arn = var.ci_policy_arn
}

data "aws_iam_policy_document" "codebuild_access" {
  statement {
    effect = "Allow"
    sid    = "LogsAccess"
    actions = [
      "logs:*"
    ]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    sid       = "ECRAccess"
    actions   = ["ecr:*"]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    sid       = "IamAccess"
    actions   = ["iam:PassRole", "sts:AssumeRole"]
    resources = ["*"]
  }

  statement {
    effect = "Allow"
    sid    = "S3Access"
    actions = [
      "s3:*"
    ]
    resources = ["*"]
  }

  statement {
    effect    = "Allow"
    sid       = "secretsmanagerAccess"
    actions   = ["secretsmanager:GetSecretValue"]
    resources = [aws_secretsmanager_secret.github_token.arn]
  }
}

resource "aws_iam_policy" "codebuild_access" {
  name        = "C7NCICodebuildAccess"
  path        = "/"
  description = "Base access for C7N CI"
  policy      = data.aws_iam_policy_document.codebuild_access.json
}

resource "aws_iam_role_policy_attachment" "codebuild_access" {
  role       = aws_iam_role.codebuild_executor.name
  policy_arn = aws_iam_policy.codebuild_access.arn
}
