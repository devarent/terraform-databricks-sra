# Disabled workflow references

`docs-deploy.yml.disabled` preserves the original commented-out Pages deployment
example. It was moved here in the devarent fork on 2026-11-22 because a comment-only
`.yml` under `.github/workflows` is not a valid runnable workflow and generated failed
workflow runs on pushes.

**Do not rename/copy it into `.github/workflows` unchanged.** The old example also
needs review of `needs`, artifact paths, fork-specific Docusaurus configuration,
permissions and Pages settings before use. Deployment has not been enabled.

Active workflow files must parse to a mapping containing `on` and `jobs`. The offline
workflow regression tests check this baseline structure; they are not a complete
GitHub Actions schema validator.
