resource "aws_codebuild_project" "policy_ci" {
  name          = "c7n-policy-ci"
  description   = "Cloud Custodian poilcy testing"
  build_timeout = "480"
  service_role  = aws_iam_role.codebuild_executor.arn

  artifacts {
    type = "NO_ARTIFACTS"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:5.0"
    type                        = "LINUX_CONTAINER"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = true

    environment_variable {
      name  = "SCRIPT_BUCKET"
      value = local.bucket_name
    }

    environment_variable {
      name  = "POLICYSTREAM_BASE"
      value = var.base_branch
    }

    environment_variable {
      name  = "POLICYSTREAM_VERSION"
      value = var.policystream_version
    }

    environment_variable {
      name  = "C7N_ORG_VERSION"
      value = var.c7n_org_version
    }

    environment_variable {
      name  = "C7N_VERSION"
      value = var.c7n_version
    }

    environment_variable {
      name  = "POLICY_DIR"
      value = var.policy_dir
    }

    environment_variable {
      name  = "OUTPUT_DIR"
      value = var.output_dir
    }

    environment_variable {
      name  = "GITHUB_API_URL"
      value = var.github_api_url
    }

    environment_variable {
      name  = "GITHUB_REPO"
      value = var.github_repo
    }

    environment_variable {
      name  = "RESOURCE_THRESHOLD"
      value = var.resource_threshold
    }

    environment_variable {
      name  = "RESOURCE_THRESHOLD_PERCENT"
      value = var.resource_threshold_percent
    }

  }

  logs_config {
    cloudwatch_logs {
      status = "ENABLED"
    }
  }

  source {
    type            = "GITHUB"
    location        = var.repository_url
    git_clone_depth = 0
    buildspec       = "deploy/buildspec.yaml"
  }
}

resource "aws_codebuild_webhook" "policy_ci" {
  project_name = aws_codebuild_project.policy_ci.name
  build_type   = "BUILD"
  filter_group {
    filter {
      type    = "EVENT"
      pattern = "PULL_REQUEST_CREATED, PULL_REQUEST_UPDATED, PULL_REQUEST_REOPENED"
    }
    filter {
      type    = "BASE_REF"
      pattern = "^refs/heads/${var.base_branch}$"
    }
  }
}
