# SRA documentation website

Fork maintenance notes (devarent, 2026-11-22). Original Databricks attribution and
repository licensing remain unchanged. These instructions build locally, not deploy.

## Reproduce the documentation checks

Use Node 22 (the installed Docusaurus 3.9.2 requires Node >=20) and Yarn Classic
1.22.22. From the repository root:

```bash
npm install --global yarn@1.22.22 --ignore-scripts --registry=https://registry.npmjs.org
cd docs/sra
yarn install --frozen-lockfile --ignore-scripts --non-interactive --registry https://registry.npmjs.org
yarn typecheck
yarn build
cd ../..
python3 scripts/check_docs_assets.py
```

The asset checker uses Python >=3.10. Run it from the repository root, or pass an
explicit `--build-dir`. It requires an existing build and rejects missing local
script, image, stylesheet, favicon and selected preload assets. It does not fetch
external URLs, inspect CSS URLs/srcset, or replace browser testing. Docusaurus also
checks links and anchors during the build.

The Yarn lockfile's download host was changed from `registry.yarnpkg.com` to
`registry.npmjs.org`; locked versions, integrity hashes and dependency graphs were
not upgraded. This allows installation where only the npm registry is reachable.
Dependency lifecycle scripts are intentionally disabled, as verified for this build.
The `packageManager` field documents the pinned Yarn version; CI installs it explicitly.

CI runs typecheck, build and local-asset validation on relevant pushes and pull
requests, with read-only repository permissions and a 15-minute job limit. The
workflow's historical filename `docs-test-deploy.yml` is retained, but it **does not
deploy**. GitHub Pages remains disabled. Site URL/organization metadata still refer
to the upstream Databricks site; decide the hosting target before enabling deployment.

## Verified results and remaining warnings

Local Node 22.22.3 / Yarn 1.22.22: frozen installation, typecheck and production build
passed; search indexed 21 documents. The generated 23 HTML files contain 171 checked
local asset references with zero errors after the favicon fix.

Installation still reports peer-dependency warnings. Build reports outdated
Browserslist data and a deprecated `onBrokenMarkdownLinks` option. The locked root
`@docusaurus/types` is 3.8.1 while core is 3.9.2; coordinated dependency/type updates
and config migration are deferred rather than silently updating this graph. These
warnings do not mean a security audit or dependency compatibility review has passed.
Do not commit `node_modules`, `.docusaurus`, or `build` outputs.
