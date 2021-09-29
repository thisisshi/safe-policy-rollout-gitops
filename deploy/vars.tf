variable "repository_url" {
  type        = string
  description = "Policy Repository URL"
}

variable "ci_policy_arn" {
  type        = string
  description = "CI Role Policy ARN, defaults to ReadOnlyAccess"
  default     = "arn:aws:iam::aws:policy/ReadOnlyAccess"
}

variable "base_branch" {
  type        = string
  description = "Base Branch"
}

variable "c7n_version" {
  type        = string
  description = "C7N Version"
  default     = "0.9.13"
}

variable "tags" {
  type        = map(string)
  description = "Tags"
  default     = {}
}

variable "policy_dir" {
  type        = string
  description = "Policies Directory (relative path from repo root)"
  default     = "policies"
}

variable "config" {
  type = map(string)
  description = "Config for policies"
  default = {}
}

variable "output_dir" {
  type = string
  description = "Cloud Custodian Output directory"
  default = "output"
}

variable github_api_url {
  type = string
  description = "Github API Url"
  default = "https://github.com/api/v3"
}

variable github_token {
  type = string
  sensitive = true
  description = "Github Token to Create Status Checks"
}

variable github_repo {
  type = string
  description = "Github Repo Name"
}
