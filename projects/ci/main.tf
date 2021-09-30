variable "github_token" {
  type = string
}

provider "aws" {}

module "c7n_ci" {
  source = "github.com/thisisshi/terraform-aws-c7n-ci"

  github_token   = var.github_token
  repository_url = "https://github.com/thisisshi/safe-policy-rollout-gitops.git"
  base_branch    = "main"
  github_repo    = "thisisshi/safe-policy-rollout-gitops"
  accounts_yaml  = "/Users/sonny/dev/thisisshi/gitops-policy-rollout/accounts.yaml"
  tags = {
    Owner = "sonny@stacklet.io"
    Env   = "dev"
  }

}
