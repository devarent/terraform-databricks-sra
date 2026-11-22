<!-- Modified in the devarent fork, 2026-11-22: contribution and verification guidance. -->
# Contributing

This repository is a fork of [Databricks SRA](https://github.com/databricks/terraform-databricks-sra).
Keep upstream attribution and the [LICENSE](LICENSE) and [NOTICE](NOTICE) intact.
Upstream welcomes contributions and accepts PRs pursuant to a CLA; check upstream's
current contribution requirements when submitting fixes there.

## Before a pull request

1. Describe the problem, affected cloud/modules, and intended behavior.
2. Keep infrastructure changes separate from portfolio/documentation maintenance.
3. Run `bash scripts/validate.sh` (Python 3 required). It reports skipped tools explicitly.
4. For Terraform changes, use a version accepted by the affected `versions.tf`, run
   formatting, initialize the module without a backend where appropriate, then validate
   and run the applicable mock tests described in [.github/workflows/README.md](.github/workflows/README.md).
   Mock tests still need provider downloads. Do not run live tests without authorization.
5. For documentation-site changes, run `yarn install --frozen-lockfile` and `yarn build`
   from `docs/sra` with Node 20+ and Yarn Classic.
6. Include actual test results and any skips in your PR; do not label unrun tests as passing.

## Portfolio inventory

Run `bash scripts/audit-repos.sh --write` with authenticated GitHub CLI access to refresh
`docs/REPO-ATLAS.json` and `docs/REPO-ATLAS.md` together. All public repository pages are
included. The tool only reads GitHub; the narrative audit is maintained manually.
Tests use mocks and the saved snapshot, so CI needs no account-wide GitHub credentials.

## Safety and style

- Use `terraform fmt` for HCL; preserve provider constraints unless a tested change requires otherwise.
- Never commit tokens, service-account keys, Terraform state/plans or real `.tfvars`.
- An absent workflow, a different branch name or a custom license is not automatically a defect.
- Choose license changes and repository archival only after owner review; preserve upstream rights.
- Report vulnerabilities according to [SECURITY.md](SECURITY.md), not a public issue containing secrets.
