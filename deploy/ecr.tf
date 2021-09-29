resource "aws_ecr_repository" "policystream" {
  name                 = "policystream"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository" "c7n" {
  name                 = "c7n"
  image_tag_mutability = "MUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }
}

resource "aws_ecr_repository_policy" "codebuild_access_policystream" {
  repository = aws_ecr_repository.policystream.name
  policy     = data.aws_iam_policy_document.codebuild_access_ecr.json
}

resource "aws_ecr_repository_policy" "codebuild_access_c7n" {
  repository = aws_ecr_repository.c7n.name
  policy     = data.aws_iam_policy_document.codebuild_access_ecr.json
}

data "aws_iam_policy_document" "codebuild_access_ecr" {
  statement {
    sid    = "CodeBuildAccessPrincipal"
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["codebuild.amazonaws.com"]
    }
    actions = [
      "ecr:GetDownloadUrlForLayer",
      "ecr:BatchGetImage",
      "ecr:BatchCheckLayerAvailability"
    ]
  }
}
