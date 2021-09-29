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

variable "c7n_image_tag" {
  type        = string
  description = "C7N Image Tag"
  default     = "latest"
}

variable tags {
  type = map(string)
  description  = "Tags"
  default = {}
}

variable policy_dir {
  type = string
  description = "Policies Directory (relative path from repo root)"
  default = "policies"
}
