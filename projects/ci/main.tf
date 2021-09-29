variable "github_token" {
  type = string
}

module "c7n_ci" {
  source = "github.com/thisisshi/terraform-aws-c7n-ci"

  # github token
  github_token   = var.github_token
  # repository url
  repository_url = "https://github.com/thisisshi/safe-policy-rollout-gitops.git"
  # location of buildspec.yaml, defaults to buildspec.yaml
  buildspec      = "buildspec.yaml"
  # branch to compare pr results to
  base_branch    = "main"
  # repo name
  github_repo    = "thisisshi/safe-policy-rollout-gitops"
  # absolute path of the accounts.yaml file you created
  accounts_yaml  = "/Users/sonny/dev/thisisshi/gitops-policy-rollout/accounts.yaml"
  # tags to apply to resource
  tags = {
    Owner = "sonny@stacklet.io"
    Env   = "dev"
  }

}
