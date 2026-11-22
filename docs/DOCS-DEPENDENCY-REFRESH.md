# Documentation dependency refresh — 2026-11-22

## Scope and policy

Applied only to `docs/sra` in `devarent/terraform-databricks-sra`, on the existing
working branch. This is not a repair or push of all repositories in the account,
a cloud deployment, or a Terraform provider upgrade. Original attribution and
licenses remain unchanged.

Versions were checked against the npm registry during this change. Prefer stable
updates within the existing major release line, pin direct dependencies exactly,
and preserve the frozen lockfile installation in CI. Version numbers alone do not
prove compatibility, security or runtime correctness.

## Applied versions

| Package / family | Previous manifest declaration | New exact version |
| --- | --- | --- |
| Docusaurus core, preset-classic, theme-mermaid | ^3.9.2 | 3.10.2 |
| Docusaurus module-type-aliases, tsconfig, types | ^3.8.1 | 3.10.2 |
| React / React DOM | ^19.0.0 | 19.3.1 |
| React / React DOM types | Not directly declared | 19.3.0 |
| TypeScript | ~5.6.2 | 5.9.3 |
| Tailwind CSS | ^3.4.17 | 3.4.19 |
| Tailwind typography | ^0.5.16 | 0.5.20 |
| tailwind-merge | ^2.6.0 | 2.6.2 |
| MDX React | ^3.0.0 | 3.1.1 |
| Radix React Slot | ^1.1.1 | 1.5.0 |
| Lucide React | ^0.471.1 | 0.577.0 |
| Prism React Renderer | ^2.3.0 | 2.4.1 |
| Autoprefixer | ^10.4.20 | 10.7.0 |
| PostCSS | ^8.5.1 | 8.5.33 |

`class-variance-authority`, `clsx`, `tailwindcss-animate`, the image zoom plugin
and Lunr search retain their existing version line. All 25 direct packages now use
exact stable versions. The lockfile was regenerated through Yarn, not hand-edited to
pretend old integrity hashes match new packages. Download URLs remain on npm.

The Docusaurus Markdown link policy moved from the deprecated top-level option to
`markdown.hooks.onBrokenMarkdownLinks`. Its value remains `throw`; broken-link and
anchor checks have not been weakened. The official `update-browserslist-db` command
refreshed the stale `caniuse-lite` entries to 1.0.30001826. The final clean build no
longer emitted either the Browserslist age warning or the Markdown deprecation.

## Why not force the largest version everywhere?

Registry candidates observed but **not adopted** in this increment:

- Tailwind 4.3.5: requires a separate CSS/PostCSS/configuration migration; current
  styling uses Tailwind 3 and tailwind-merge 2.
- TypeScript 7.0.2: major compiler migration; latest stable 5.x was selected instead.
- Image zoom 3.0.1, tailwind-merge 3.7.1 and Lucide 1.77.0: major migrations deferred
  pending focused API/browser checks. Lucide's 0.x update still needs browser review.
- Lunr search: npm's `latest` tag returned 3.6.0, lower than installed 3.6.1. The
  existing 3.6.1 was confirmed available and was not silently downgraded.

## Verification performed

On Node 22.22.3 and Yarn 1.22.22:

1. Removed the generated `node_modules` directory and installed anew with
   `--frozen-lockfile --ignore-scripts --non-interactive` against the npm registry.
2. Read the 25 installed direct package manifests and confirmed exact equality with
   the declared versions.
3. Ran `yarn clear`, `yarn typecheck` and `yarn build`: all passed. Search indexed
   21 documents. Final build stderr was empty.
4. Ran `python3 scripts/check_docs_assets.py`: 23 HTML files, 171 local references,
   zero missing assets.
5. Ran `PYTHON=.venv/bin/python bash scripts/validate.sh`: **59 tests passed**;
   **273 HCL files / 35 local module calls**, zero checker findings. Two new regression
   tests enforce direct dependency alignment/pinning and the strict Markdown hook.

Build commands are in [the site README](sra/README.md). The generic maintenance
script does not build docs; documentation checks above were executed separately.

## CI evidence and limits

At the start of this increment, all returned runs for previous commit `753d342`
were successful: maintenance (45012569822), docs (45012569781), AWS (45012569794),
Azure (45012569766), AWS Customizations (45012569913), and Workflow Mock Tests
(45012569907). These are **previous-commit results**, not proof of CI on this update.

Installation still emits upstream peer-dependency warnings for react-loadable,
acorn, Algolia/search-insights and the image zoom plugin's theme peer. No claim of
zero vulnerabilities is made; a security audit was not performed in this increment.
Browser interactions (search, zoom, mobile styling), Pages deployment, Docker/K8s,
live cloud deployment and other repositories are outside the tests above. Native
Terraform is still unavailable locally; HCL parsing does not replace provider/schema
validation. Further work must preserve these distinctions.
