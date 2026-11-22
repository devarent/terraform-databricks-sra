# Terraform and CI follow-up — 22 November 2026

## Changes implemented in this repository

### 1. Correct the GCP service-account example

`gcp/examples/service_account/main.tf` had two local-module contract mismatches:

- The caller supplied `prefix`, but `gcp/modules/service_account/variables.tf`
  declares `sa_name`, not `prefix`. The retained example variable `prefix` now feeds
  the supported `sa_name` argument.
- The caller accessed `module.service_account.service_account`, but the module
  exports `workspace_creator_email`. The retained example output `service_account`
  now returns that email.

The offline checker reproduced both errors before the fix and no longer reports
them afterward. Regression fixtures preserve the original mismatches. No shared IAM
resource definitions/addresses were modified. Native provider validation and live
cloud deployment remain unrun; review a plan before applying to an existing environment.

### 2. Make shared changes trigger cloud CI

AWS, Azure and AWS-customization caller workflows now watch changes to
`.github/workflows/terraform-ruw.yml` and `common/tests/**`, in addition to their own
cloud paths. They previously missed those changes. They now explicitly request
`contents: read` and cancel superseded runs with workflow-specific concurrency groups.

Azure enables the reusable workflow's `terraform_validate_enabled` input, as AWS
already did. AWS/Azure mock test filters are retained; **live integration tests are
not enabled by this change**. Tests enforce that the filter arguments stay mock-only.
Triggering CI on a shared fixture change does not mean live fixtures get executed.

### 3. Add offline HCL and module-contract validation

New tool: [validate_terraform_sources.py](../scripts/validate_terraform_sources.py).

- Enumerates Git-tracked and non-ignored untracked `.tf`/`.hcl` files, not downloaded
  caches, virtual environments or generated dependencies.
- Parses HCL and reports errors without echoing potentially sensitive source literals.
- Checks relative local module targets, supported/required input names and simple
  local-module output references, plus duplicate variable/output/module names.
- Rejects source paths escaping the checkout; explicitly counts remote/dynamic modules
  as skipped rather than pretending to validate them.
- Uses `python-hcl2==8.2.0`. Version 7.3.1 rejected the valid multiline conditional in
  `gcp/modules/workspace_deployment/vpc.tf`; upgrading the parser resolved that false
  positive. The Terraform expression itself was left unchanged.

This tool does **not** evaluate HCL expressions or inspect provider resource schemas,
remote modules, `.tf.json`, arbitrary dynamic output references, runtime permissions,
state, secrets history, version compatibility or cloud behavior. Syntax success is not
`terraform validate` success. Tests with no optional parser installed are explicitly
skipped; the CLI itself exits nonzero when its required parser is unavailable.

The maintenance workflow installs the parser, checks HCL contracts and runs regression
tests for Terraform/configuration/workflow changes. `scripts/validate.sh` also invokes
the checker if installed and reports a skip otherwise.

### 4. Correct the GCP documentation

Earlier audit prose and README navigation understated the GCP layout. **GCP has actual
Terraform modules in `gcp/modules` and example roots in `gcp/examples`.** It does not
have a `gcp/tf` root. The earlier “guide/image only” description was inaccurate.

The root README and GCP quickstart now point to real example directories instead of
instructing users to initialize an empty `gcp/` root. A new service-account example
README documents the retained input/output names and credential-generation risk.

## Verification

```bash
.venv/bin/pip install -r scripts/requirements-code-audit.txt -r scripts/requirements-terraform-checks.txt
PYTHON=.venv/bin/python bash scripts/validate.sh
.venv/bin/python scripts/validate_terraform_sources.py --json
```

Results after implementation:

- **273 / 273 HCL sources parsed; 35 local module calls checked; zero reported issues.**
- **45 offline tests passed**, including 13 new source/workflow regression tests.
- Shell syntax, Python syntax, modified workflow YAML and Git whitespace checks passed.
- Terraform CLI not available: fmt/native validate/test/plan were not run.
- No cloud deployment, dependency upgrades in the application repos, remote fixes to
  other repositories, or GitHub Actions success claims are implied by these local results.

## Remaining work / known limits

- `gcp/modules/service_account` defaults key creation on, and one IAM binding reads
  only `delegate_from[0]` despite an empty-list default. This change documents those
  risks; changing key behavior or IAM resource addressing needs a separate migration
  and native/provider test plan, not a silent bulk edit.
- Documentation-site build, Docker/Kubernetes runtime tests and full provider/schema
  validation still require their toolchains and suitable environments.
- The 79-repo source audit and five external patch proposals remain separate from
  these applied changes. No claim is made that all repositories are repaired.
