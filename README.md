<!-- Modified in the devarent fork, 2026-11-22: navigation, fork context and portfolio audit. -->
# Databricks Security Reference Architectures — Terraform

> Fork of [databricks/terraform-databricks-sra](https://github.com/databricks/terraform-databricks-sra).
> Upstream authors retain their attribution. This fork adds a public-repository inventory,
> read-only audit tooling, documentation improvements and targeted CI hardening.
> No Terraform deployment logic is changed by this maintenance update.

## Navigation

- [Overview and support](#project-overview)
- [Getting started](#getting-started)
- [Repository layout](#repository-layout)
- [Validation](#validation)
- [All repositories](#all-repositories)
- [Contributing](CONTRIBUTING.md) · [Security](SECURITY.md) · [License](LICENSE) · [Notice](NOTICE)

## Project Overview

The [Security Reference Architecture (SRA)](https://databricks.github.io/terraform-databricks-sra/) with Terraform enables deployment of Databricks workspaces and cloud infrastructure configured with security best practices. Using the official Databricks Terraform provider, environments are programmatically set up with hardened configurations modeled after our most security-conscious customers. The included templates are built on [Databricks Security Best Practices](https://www.databricks.com/trust/security-features#best-practices), providing a strong, prescriptive foundation for secure deployments.



- [AWS and AWS GovCloud](https://databricks.github.io/terraform-databricks-sra/docs/usage/AWS/)
- [Azure](https://databricks.github.io/terraform-databricks-sra/docs/usage/Azure/)
- [GCP](https://databricks.github.io/terraform-databricks-sra/docs/usage/GCP/)

## Project Support

The code in this project is provided **for exploration purposes only** and is **not formally supported** by Databricks under any Service Level Agreements (SLAs). It is provided **AS-IS**, without any warranties or guarantees.  

Please **do not submit support tickets** to Databricks for issues related to the use of this project.  

The source code provided is subject to the Databricks [LICENSE](https://github.com/databricks/terraform-databricks-sra/blob/main/LICENSE) . All third-party libraries included or referenced are subject to their respective licenses set forth in the project license.

Any issues or bugs found should be submitted as [GitHub Issues](https://github.com/databricks/terraform-databricks-sra/issues) on the project repository. While these will be reviewed as time permits, there are **no formal SLAs** for support.

## Point-in-Time Solution

The **Security Reference Architecture (SRA)** - Terraform Templates is designed as a point-in-time solution that captures security best practices at the time of each release. 

This project **does not** guarantee backward compatibility between versions; new releases are not drop-in replacements for existing codebases.

## Getting started

1. Choose the upstream deployment guide for [AWS/GovCloud](https://databricks.github.io/terraform-databricks-sra/docs/usage/AWS/),
   [Azure](https://databricks.github.io/terraform-databricks-sra/docs/usage/Azure/), or
   [GCP](https://databricks.github.io/terraform-databricks-sra/docs/usage/GCP/).
2. Read the selected module's `versions.tf` and variable definitions. Install a compatible
   Terraform version and configure cloud/Databricks credentials through the documented method.
3. Prepare local variables; never commit credentials, state or plans. Review a plan and its
   costs before any deployment. This maintenance work does not run `terraform apply`.

GCP in this checkout contains a [guide](gcp/README.md), not a `gcp/tf` module.
Do not assume every cloud has an identical layout or validation coverage.

## Repository layout

| Path | Purpose |
|---|---|
| [aws/tf](aws/tf/) | AWS and GovCloud Terraform modules and tests |
| [aws/customizations](aws/customizations/) | Optional integrations and customizations |
| [azure/tf](azure/tf/) | Azure Terraform modules and tests |
| [gcp](gcp/) | GCP guide and architecture image |
| [common/tests](common/tests/) | Shared test fixtures |
| [.workflow-mock](.workflow-mock/) | Reusable-workflow fixture |
| [.github/workflows](.github/workflows/) | Existing Terraform and documentation CI |
| [docs/sra](docs/sra/) | Docusaurus documentation site |
| [scripts](scripts/) | Read-only portfolio audit and local checks |

## Validation

```bash
# Offline audit-tool tests, atlas consistency, local documentation links and diff checks
bash scripts/validate.sh

# Read-only inventory of every public repo (requires authenticated gh + Python 3)
bash scripts/audit-repos.sh --write
```

The validation script runs `terraform fmt -check -recursive` if Terraform is installed;
otherwise it explicitly reports a skip. It does not run cloud deployment tests or certify
infrastructure security. For module validation and mock tests, see
[the existing workflow guide](.github/workflows/README.md).

Documentation build (use Node 20+ and Yarn Classic, as in the existing docs CI):

```bash
cd docs/sra
yarn install --frozen-lockfile
yarn build
```

## All repositories

The [Repository Atlas](docs/REPO-ATLAS.md) lists all **79 public repositories** observed
on 2026-11-22, with links, descriptions, languages, branches, licenses and file-presence
checks. [Raw JSON evidence](docs/REPO-ATLAS.json) and the
[audit / prioritized follow-ups](docs/AUDIT-2026-11-22.md) are included.

The follow-up [source-code audit](docs/CODE-AUDIT-2026-11-22.md) records bounded static
checks across all 79 repos, reviewed defects, local reproductions and coverage limits.
[Five proposed patches](docs/audit-patches/README.md) passed local applicability checks;
they have **not** been applied to the remote repositories. A selected demo's SQLite tests
were run; full builds, integration tests and cloud deployments across the portfolio were not.

This is an index, not a clone or submodule collection. Changes in this branch affect only
`terraform-databricks-sra`; findings and patch proposals for other repos are not remote repairs.
`NOASSERTION` is GitHub's license classification, not permission to relicense this code:
the Databricks [LICENSE](LICENSE) and [NOTICE](NOTICE) remain authoritative.

### Databricks ecosystem and web integration plan

The separate [Databricks × devarent portfolio package](docs/portfolio/README.md) adds:

- [253 upstream repositories](docs/portfolio/DATABRICKS-CATALOG.md), with license, archive status, category and integration priority.
- A [fork dry-run](docs/portfolio/FORK-DRY-RUN.md) that identifies existing forks and review gates; **no remote changes**.
- [332 metadata entries](docs/portfolio/WEB-CATALOG.json) keeping upstream and owned repositories distinct by `owner/name`.
- A [Next.js / React / Tailwind / Radix integration plan](docs/portfolio/WEB-INTEGRATION-PLAN.md) for `repo-atlas-next`, with optional separate Laravel/API services.

These are snapshot counts, not installed dependencies. Regenerate the local catalogues with
`python3 scripts/plan_databricks_portfolio.py` (offline), or add `--refresh` to read current
public GitHub metadata. The planner has no execute/fork/deploy mode.
