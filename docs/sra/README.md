# SRA documentation website

Fork maintenance notes (devarent, 2026-11-22). Original Databricks attribution and
repository licensing remain unchanged. These instructions build locally, not deploy.

## Reproduce the documentation checks

Use Node 22 (the installed Docusaurus 3.10.2 requires Node >=20) and Yarn Classic
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

The Yarn lockfile uses `registry.npmjs.org` rather than `registry.yarnpkg.com`.
The initial host-only fix did not change package versions; the subsequent tested
[dependency refresh](../DOCS-DEPENDENCY-REFRESH.md) does update the dependency graph.
This allows installation where only the npm registry is reachable.
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

The refreshed clean build reports neither the old Browserslist warning nor the
`onBrokenMarkdownLinks` deprecation. All six direct Docusaurus packages are pinned
to 3.10.2; the broken-Markdown-link policy now lives in `markdown.hooks` and remains
`throw`. All direct dependencies use exact stable versions, including explicit React
types; update the lockfile and rerun checks together when changing them.

Installation still reports upstream peer-dependency warnings (react-loadable, acorn,
Algolia/search-insights and the zoom plugin's theme peer). The build passing does not
resolve these warnings or certify browser interactions/security. Major migrations
(Tailwind 4, TypeScript 7, zoom 3, tailwind-merge 3 and Lucide 1) remain separate work.
Do not commit `node_modules`, `.docusaurus`, or `build` outputs.
