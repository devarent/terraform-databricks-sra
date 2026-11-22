# Modified in the devarent fork, 2026-11-22: align inputs and outputs with the local module.
module "service_account" {
  source        = "../../modules/service_account/"
  project       = var.project
  sa_name       = var.prefix
  delegate_from = var.delegate_from
}

output "custom_role_url" {
  value = "https://console.cloud.google.com/iam-admin/roles/details/projects%3C${module.service_account.current_project}%3Croles%3C${module.service_account.role_id}"
}

output "service_account" {
  value       = module.service_account.workspace_creator_email
  description = "Add this email as a user in the Databricks account console"
}
