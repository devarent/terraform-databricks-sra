# GCP service-account example

This example calls `../../modules/service_account`. It is a deployable example,
not an offline test fixture. Read the [GCP guide](../../README.md) first.

## Inputs and output

- `project`: your GCP project ID; replace the placeholder default.
- `prefix`: retained legacy input name, now passed to the module's `sa_name`.
  Supply a valid GCP service-account ID (6–30 lowercase letters/digits/hyphens,
  beginning with a letter and ending with a letter or digit), not an arbitrary label.
- `delegate_from`: supply the IAM principal intended for the module's impersonation
  binding. The module currently reads element zero, so the list must not be empty;
  additional entries are not all granted permissions by that resource.
- Output `service_account`: email from the module's `workspace_creator_email` output.
  It is an email string, not a private key or a resource object.

## Validate before deploying

From the repository root, after reviewing provider requirements:

```bash
terraform -chdir=gcp/examples/service_account init -backend=false
terraform -chdir=gcp/examples/service_account validate
```

Supply real input values only in an ignored local tfvars file or a secure variable
source. Initialize the correct state backend before planning a real deployment.
Review IAM permissions, names, cost and the plan before any `apply`.

**Credential warning:** the called module currently defaults
`create_service_account_key` to `true`. This example does not override that default.
Review its generated key, helper scripts and sensitive state handling before use;
do not commit generated files. Prefer an approved impersonation-based configuration
when persistent keys are not necessary.

## Maintenance correction (devarent fork, 2026-11-22)

The example previously passed an unsupported module argument named `prefix` and
referenced an absent output named `service_account`. The example's public variable
and output names are retained, but they now map to the actual module contract.
No IAM resources or resource addresses in the shared module were changed. This
static correction has not been validated by a live cloud deployment.
