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

### 5. Remove a failing comment-only workflow from the active directory

After push, GitHub reported `Maintenance checks` successful but also reported failed
runs for `.github/workflows/docs-deploy.yml`, a file containing only comments and no
workflow mapping. The preserved reference now lives at
[.github/workflow-templates/docs-deploy.yml.disabled](../.github/workflow-templates/docs-deploy.yml.disabled).
A regression test checks that every active workflow file has a mapping with triggers
and jobs. GitHub Pages remains disabled; the old template needs review before reuse.

## Verification

```bash
.venv/bin/pip install -r scripts/requirements-code-audit.txt -r scripts/requirements-terraform-checks.txt
PYTHON=.venv/bin/python bash scripts/validate.sh
.venv/bin/python scripts/validate_terraform_sources.py --json
```

Results after implementation:

- **273 / 273 HCL sources parsed; 35 local module calls checked; zero reported issues.**
- **46 offline tests passed**, including 14 new source/workflow regression tests.
- Shell syntax, Python syntax, modified workflow YAML and Git whitespace checks passed.
- Terraform CLI not available: fmt/native validate/test/plan were not run.
- No cloud deployment, dependency upgrades in the application repos, remote fixes to
  other repositories, or GitHub Actions success claims are implied by these local results.

## Remaining work / known limits

- `gcp/modules/service_account` defaults key creation on, and one IAM binding reads
  only `delegate_from[0]` despite an empty-list default. This change documents those
  risks; changing key behavior or IAM resource addressing needs a separate migration
  and native/provider test plan, not a silent bulk edit.
- Docker/Kubernetes runtime tests and full provider/schema validation still require
  suitable environments. The documentation-site build was subsequently verified below.
- The 79-repo source audit and five external patch proposals remain separate from
  these applied changes. No claim is made that all repositories are repaired.

## Subsequent documentation and CI checks — 2026-11-22

The earlier 46-test result above describes the previous increment, not the current
suite. This increment adds documentation build coverage and bounded workflow jobs:

- Node engine minimum aligned to installed Docusaurus (>=20); CI uses Node 22 and
  explicit Yarn 1.22.22. Lockfile registry hosts changed to npm without changing
  dependency versions or integrity hashes. Frozen install with scripts disabled passed.
- Real `yarn typecheck` and `yarn build` passed on Node 22.22.3. Search indexed 21 docs.
- Fixed an incorrect favicon path that the production build did not reject. A new
  asset checker reproduced 23 missing favicon references before the fix, then checked
  23 HTML files / 171 local references with zero errors after rebuilding.
- Docs CI now runs on relevant pushes as well as PRs; it checks types, build and
  generated local assets, uses read-only permissions and a 15-minute timeout, and
  pins its checkout/setup-node actions to verified v6 commit SHAs. No Pages deploy.
- Reusable Terraform jobs now have 30-minute timeouts, explicit noninteractive mode,
  read-only permissions and architecture-separated provider/TFLint caches. Existing
  cloud mock-test filters remain unchanged; no live integration tests enabled.
- Local offline suite now contains **57 tests**. HCL scope remains **273 sources /
  35 local module calls**. Local native Terraform CLI remains unavailable.

The previously pending Azure run completed successfully:
[Azure 45011467437](https://github.com/devarent/terraform-databricks-sra/actions/runs/45011467437).
AWS [45011467337](https://github.com/devarent/terraform-databricks-sra/actions/runs/45011467337)
and AWS Customizations
[45011467379](https://github.com/devarent/terraform-databricks-sra/actions/runs/45011467379)
also succeeded. These runs tested commit `c04c301`, **not this new increment**.
They do not certify GCP, live deployment or the other 79 audited repositories.

Reproduction commands, known nonfatal warnings and checker limitations are in
[the documentation-site README](sra/README.md). At that point dependency upgrades,
Docusaurus type alignment/deprecation migration and browser/runtime validation were
still pending. The subsequent [dependency refresh](DOCS-DEPENDENCY-REFRESH.md)
updates the packages, aligns all six Docusaurus packages, migrates the Markdown hook
and refreshes Browserslist data. Its clean install/typecheck/build passed and the
local suite increased to 59 passing tests. Browser/runtime validation remains pending.
