# Modified in the devarent fork, 2026-11-22: document the retained example input name.
variable "prefix" {
  description = "Service account ID passed to the module's sa_name input (legacy example variable name)."
  type        = string
}

variable "project" {
  type    = string
  default = "<my-project-id>"
}

variable "delegate_from" {
  description = "Allow either user:user.name@example.com, group:deployers@example.com or serviceAccount:sa1@project.iam.gserviceaccount.com to impersonate created service account"
  type        = list(string)
}