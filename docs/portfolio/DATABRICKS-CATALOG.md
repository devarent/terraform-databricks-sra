# Databricks — 253 public repositories

Snapshot UTC: 2026-11-22T09:59:44.979134+00:00. Source: `GET /orgs/databricks/repos?type=public&per_page=100` with pagination.

This catalogue is **separate from devarent ownership**. It does not copy code or certify code quality/security.
See [integration plan](WEB-INTEGRATION-PLAN.md), [fork dry-run](FORK-DRY-RUN.md), [manifest](DATABRICKS-MANIFEST.json) and [web import data](WEB-CATALOG.json).

- Public destinations observed: **79** (listed separately in the JSON manifest; original [devarent atlas](../REPO-ATLAS.md) retained).
- Archived: **73**. Forks of other repositories: **94**.
- License classification: Apache-2.0: 114; BSD-2-Clause: 4; BSD-3-Clause: 5; GPL-3.0: 1; ISC: 2; MIT: 40; MIT-0: 1; MPL-2.0: 2; NOASSERTION: 45; not detected: 39.
- P1: review first for SRA/web integration; P2: optional use-case integrations; P3: reference/review only. These are recommendations, not installations.
- Category is a name-based navigation heuristic; language is GitHub primary language, not all languages present.
- `NOASSERTION` / missing SPDX require reading actual terms; a known SPDX is not a full licensing approval.

| Repository | Description | Language | SPDX | Archived | Fork | Category | Priority | GitHub KB |
|---|---|---|---|---|---|---|---|---|
| [alertmanager](https://github.com/databricks/alertmanager) | Prometheus Alertmanager | Go | Apache-2.0 | False | True | Other / manual classification | P3-review | 40284 |
| [api-linter](https://github.com/databricks/api-linter) | A linter for APIs defined in protocol buffers. | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 2507 |
| [app-templates](https://github.com/databricks/app-templates) | — | TypeScript | NOASSERTION | False | False | Web / developer experience | P1 | 5588 |
| [appkit](https://github.com/databricks/appkit) | Build Databricks Apps faster with our brand-new Node.js + React SDK. Built for humans and AI. | TypeScript | Apache-2.0 | False | False | Web / developer experience | P1 | 27190 |
| [appkit-registry](https://github.com/databricks/appkit-registry) | — | TypeScript | Apache-2.0 | False | False | Web / developer experience | P3-review | 118 |
| [arcion-docs](https://github.com/databricks/arcion-docs) | — | SCSS | NOASSERTION | False | False | Other / manual classification | P3-review | 7529 |
| [arcion-loadgen](https://github.com/databricks/arcion-loadgen) | — | Shell | MIT | False | False | Other / manual classification | P3-review | 85384 |
| [async-file-io](https://github.com/databricks/async-file-io) | — | Java | Apache-2.0 | False | False | Other / manual classification | P3-review | 73 |
| [automl](https://github.com/databricks/automl) | — | Python | Apache-2.0 | False | False | AI / ML | P3-review | 445 |
| [azure-databricks-demos](https://github.com/databricks/azure-databricks-demos) | — | — | — | False | False | Data / analytics | P3-review | 199 |
| [azure-relay-node](https://github.com/databricks/azure-relay-node) | ☁️Node.js library for Azure Relay Hybrid Connections | JavaScript | MIT | False | True | Other / manual classification | P3-review | 216 |
| [bazel](https://github.com/databricks/bazel) | Correct, reproducible, and fast builds for everyone. | Java | Apache-2.0 | False | True | Tooling / build | P3-review | 1003391 |
| [bazel-remote](https://github.com/databricks/bazel-remote) | A remote cache for Bazel | — | Apache-2.0 | False | True | Tooling / build | P3-review | 3747 |
| [bazel-toolchain](https://github.com/databricks/bazel-toolchain) | LLVM toolchain for bazel | Starlark | Apache-2.0 | False | True | Tooling / build | P3-review | 141 |
| [benchbase](https://github.com/databricks/benchbase) | Multi-DBMS SQL Benchmarking Framework via JDBC | Java | NOASSERTION | False | True | Other / manual classification | P3-review | 109689 |
| [bitdotio-csharp-example](https://github.com/databricks/bitdotio-csharp-example) | An example of using C# with bit.io | C# | MIT | True | False | Other / manual classification | P3-reference | 8 |
| [bitdotio-golang-example](https://github.com/databricks/bitdotio-golang-example) | Example of using golang with bit.io | Go | — | True | False | Other / manual classification | P3-reference | 11 |
| [bitdotio-java-example](https://github.com/databricks/bitdotio-java-example) | An example of using Java & JDBC with bit.io | Java | MIT | True | False | Other / manual classification | P3-reference | 6 |
| [blobfuse-fork-public](https://github.com/databricks/blobfuse-fork-public) | A virtual file system adapter for Azure Blob storage | C++ | MIT | False | True | Other / manual classification | P3-review | 1299 |
| [bootstrap](https://github.com/databricks/bootstrap) | The most popular HTML, CSS, and JavaScript framework for developing responsive, mobile first projects on the web. | — | MIT | True | True | Other / manual classification | P3-reference | 185154 |
| [brew](https://github.com/databricks/brew) | 🍺 The missing package manager for macOS (or Linux) | Ruby | BSD-2-Clause | True | True | Tooling / build | P3-reference | 51129 |
| [brew-install](https://github.com/databricks/brew-install) | 📥 Homebrew (un)installer | Shell | BSD-2-Clause | True | True | Tooling / build | P3-reference | 583 |
| [btrace](https://github.com/databricks/btrace) | BTrace - a safe, dynamic tracing tool for the Java platform | Java | — | False | True | Other / manual classification | P3-review | 16865 |
| [buildtools](https://github.com/databricks/buildtools) | A bazel BUILD file formatter and editor | Go | Apache-2.0 | True | True | Tooling / build | P3-reference | 2523 |
| [bundle-examples](https://github.com/databricks/bundle-examples) | Examples of Databricks Asset Bundles | Python | NOASSERTION | False | False | Other / manual classification | P2 | 4393 |
| [clean-room-orchestration](https://github.com/databricks/clean-room-orchestration) | — | Python | NOASSERTION | False | False | Other / manual classification | P3-review | 35 |
| [CleverCSV](https://github.com/databricks/CleverCSV) | CleverCSV is a Python package for handling messy CSV files. It provides a drop-in replacement for the builtin CSV module with improved dialect detection, and comes with a handy command line application for working with CSV files. | — | MIT | True | True | Other / manual classification | P3-reference | 2298 |
| [cli](https://github.com/databricks/cli) | Databricks CLI | Go | NOASSERTION | False | False | Tooling / build | P1 | 353225 |
| [click](https://github.com/databricks/click) | The "Command Line Interactive Controller for Kubernetes" | Rust | Apache-2.0 | False | False | Tooling / build | P3-review | 1292 |
| [cloud-latency-map](https://github.com/databricks/cloud-latency-map) | — | Python | MIT | False | False | Other / manual classification | P3-review | 615 |
| [cloudflare-b2-proxy](https://github.com/databricks/cloudflare-b2-proxy) | Proxy Backblaze S3 compatible API requests, optionally sending notifications to a webhook | — | Apache-2.0 | True | True | Other / manual classification | P3-reference | 48 |
| [cluster-api-1](https://github.com/databricks/cluster-api-1) | Home for Cluster API, a subproject of sig-cluster-lifecycle | — | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 174958 |
| [cluster-api-provider-aws-1](https://github.com/databricks/cluster-api-provider-aws-1) | Kubernetes Cluster API Provider AWS provides consistent deployment and day 2 operations of "self-managed" and EKS Kubernetes clusters on AWS. | Go | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 74108 |
| [cluster-api-provider-azure-1](https://github.com/databricks/cluster-api-provider-azure-1) | Cluster API implementation for Microsoft Azure | Go | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 84372 |
| [cluster-api-provider-gcp-1](https://github.com/databricks/cluster-api-provider-gcp-1) | The GCP provider implementation for Cluster API | Go | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 54523 |
| [code-scanning-javascript-demo](https://github.com/databricks/code-scanning-javascript-demo) | GitHub Code Scanning Javascript Tutorial | JavaScript | MIT | True | True | Other / manual classification | P3-reference | 83 |
| [compose-rl](https://github.com/databricks/compose-rl) | — | Python | Apache-2.0 | True | False | Other / manual classification | P3-reference | 1732 |
| [congruity](https://github.com/databricks/congruity) | The goal of this library is to provide a compatibility layer that makes it easier to adopt Spark Connect. The library is designed to be simply imported in your application and will then monkey-patch the existing API to provide the legacy functionality. | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 111 |
| [consent-manager-bitio](https://github.com/databricks/consent-manager-bitio) | — | TypeScript | MIT | True | False | Other / manual classification | P3-reference | 5600 |
| [containerregistry](https://github.com/databricks/containerregistry) | A set of Python libraries and tools for interacting with a Docker Registry. | Python | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 432 |
| [containers](https://github.com/databricks/containers) | Sample base images for Databricks Container Services | Jupyter Notebook | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 42428 |
| [covid](https://github.com/databricks/covid) | Documentation on bit.io's Covid Explorer | — | — | True | False | Other / manual classification | P3-reference | 79 |
| [dagster](https://github.com/databricks/dagster) | A data orchestrator for machine learning, analytics, and ETL. | Python | Apache-2.0 | True | True | Other / manual classification | P3-reference | 265224 |
| [dais-cow-bff](https://github.com/databricks/dais-cow-bff) | Code for the "Path to Production" DAIS 2024 and 2023 talks | Jupyter Notebook | — | False | False | Other / manual classification | P3-review | 531 |
| [data](https://github.com/databricks/data) | A repository to stuff data and loader scripts for Tabular demos | — | Apache-2.0 | False | False | Data / analytics | P3-review | 7 |
| [data-classification-review-app](https://github.com/databricks/data-classification-review-app) | — | Python | — | False | False | Data / analytics | P3-review | 61 |
| [datableio-datable.io](https://github.com/databricks/datableio-datable.io) | — | HTML | — | True | False | Data / analytics | P3-reference | 8 |
| [databricks-accelerators](https://github.com/databricks/databricks-accelerators) | Accelerate the use of Databricks for customers [public repo] | Python | — | False | False | Data / analytics | P3-review | 2143 |
| [databricks-agent-skills](https://github.com/databricks/databricks-agent-skills) | Databricks AI Tools: skills and plugins for building on Databricks with Claude Code, Cursor, Codex, GitHub Copilot, and other AI coding agents. | Python | NOASSERTION | False | False | AI / ML | P1 | 4244 |
| [databricks-ai-bridge](https://github.com/databricks/databricks-ai-bridge) | — | Python | NOASSERTION | False | False | Data / analytics | P2 | 44457 |
| [databricks-asset-bundles-dais2023](https://github.com/databricks/databricks-asset-bundles-dais2023) | — | Python | NOASSERTION | False | False | Data / analytics | P3-review | 1040 |
| [databricks-cli](https://github.com/databricks/databricks-cli) | (Legacy) Command Line Interface for Databricks | Python | NOASSERTION | True | False | Data / analytics | P3-reference | 895 |
| [databricks-dbutils-scala](https://github.com/databricks/databricks-dbutils-scala) | The Scala SDK for Databricks. | Scala | NOASSERTION | False | False | Data / analytics | P3-review | 146 |
| [databricks-empty-ide-project](https://github.com/databricks/databricks-empty-ide-project) | Empty IDE project used by the VSCode extension for Databricks | — | — | False | False | Data / analytics | P3-review | 4 |
| [databricks-grafana-datasource](https://github.com/databricks/databricks-grafana-datasource) | Community Grafana datasource for Databricks - visualize costs, jobs and SDP pipelines in your dashboards. | TypeScript | NOASSERTION | False | False | Data / analytics | P3-review | 584 |
| [databricks-jdbc](https://github.com/databricks/databricks-jdbc) | JDBC for Databricks SQL | Java | Apache-2.0 | False | False | SDK / data connector | P2 | 156867 |
| [databricks-ml-examples](https://github.com/databricks/databricks-ml-examples) | — | Python | Apache-2.0 | False | False | AI / ML | P3-review | 2298 |
| [databricks-repos-debug](https://github.com/databricks/databricks-repos-debug) | — | Jupyter Notebook | NOASSERTION | False | False | Data / analytics | P3-review | 16 |
| [databricks-repos-proxy](https://github.com/databricks/databricks-repos-proxy) | — | Jupyter Notebook | — | False | False | Data / analytics | P3-review | 2228 |
| [databricks-sdk-go](https://github.com/databricks/databricks-sdk-go) | Databricks SDK for Go | Go | Apache-2.0 | False | False | SDK / data connector | P2 | 44812 |
| [databricks-sdk-java](https://github.com/databricks/databricks-sdk-java) | Databricks SDK for Java | Java | Apache-2.0 | False | False | SDK / data connector | P2 | 17047 |
| [databricks-sdk-py](https://github.com/databricks/databricks-sdk-py) | Databricks SDK for Python (Beta) | Python | Apache-2.0 | False | False | SDK / data connector | P1 | 29511 |
| [databricks-sql-cli](https://github.com/databricks/databricks-sql-cli) | CLI for querying Databricks SQL | Python | NOASSERTION | False | False | SDK / data connector | P3-review | 4046 |
| [databricks-sql-go](https://github.com/databricks/databricks-sql-go) | Golang database/sql driver for Databricks SQL. | Go | Apache-2.0 | False | False | SDK / data connector | P3-review | 5259 |
| [databricks-sql-kernel-bindings](https://github.com/databricks/databricks-sql-kernel-bindings) | — | Go | Apache-2.0 | False | False | SDK / data connector | P3-review | 616476 |
| [databricks-sql-nodejs](https://github.com/databricks/databricks-sql-nodejs) | Databricks SQL Connector for Node.js | TypeScript | Apache-2.0 | False | False | SDK / data connector | P1 | 16570 |
| [databricks-sql-python](https://github.com/databricks/databricks-sql-python) | Databricks SQL Connector for Python | Python | Apache-2.0 | False | False | SDK / data connector | P1 | 6940 |
| [databricks-sqlalchemy](https://github.com/databricks/databricks-sqlalchemy) | See PECO-1396 for more details about this repository. | Python | Apache-2.0 | False | False | SDK / data connector | P3-review | 441 |
| [databricks-ttyd](https://github.com/databricks/databricks-ttyd) | — | C | MIT | False | False | Data / analytics | P3-review | 11509 |
| [databricks-vscode](https://github.com/databricks/databricks-vscode) | VS Code extension for Databricks | TypeScript | NOASSERTION | False | False | Web / developer experience | P3-review | 46416 |
| [dbt-databricks](https://github.com/databricks/dbt-databricks) | A dbt adapter for Databricks. | Python | Apache-2.0 | False | False | SDK / data connector | P2 | 7612 |
| [dbt-tabular](https://github.com/databricks/dbt-tabular) | Repository for the dbt ❤️ Tabular blogpost | — | Apache-2.0 | False | False | SDK / data connector | P3-review | 11 |
| [delta-live-tables-notebooks](https://github.com/databricks/delta-live-tables-notebooks) | — | Python | — | False | False | Data / analytics | P3-review | 70331 |
| [demokit.gtihub.io](https://github.com/databricks/demokit.gtihub.io) | Arcion Demo Kit docs | Ruby | — | False | False | Other / manual classification | P3-review | 79639 |
| [devhub](https://github.com/databricks/devhub) | DevHub (developers.databricks.com) is the developer site for building on Databricks. | TypeScript | NOASSERTION | False | False | Web / developer experience | P1 | 41368 |
| [devrel](https://github.com/databricks/devrel) | This repository contains the notebooks and presentations we use for our Databricks Tech Talks  | HTML | — | False | False | Other / manual classification | P3-review | 136171 |
| [dicer](https://github.com/databricks/dicer) | Dicer auto-sharder: Infrastructure for building sharded services | Scala | Apache-2.0 | False | False | Other / manual classification | P3-review | 6765 |
| [diviner](https://github.com/databricks/diviner) | Grouped time series forecasting engine | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 2083 |
| [django-allauth](https://github.com/databricks/django-allauth) | Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication. | — | MIT | True | True | Other / manual classification | P3-reference | 6659 |
| [django-rest-framework](https://github.com/databricks/django-rest-framework) | Web APIs for Django. 🎸 | Python | NOASSERTION | True | True | Other / manual classification | P3-reference | 48405 |
| [docker-dev](https://github.com/databricks/docker-dev) | Arcion Demo Kit for testing database to database replication | Shell | GPL-3.0 | False | False | Infrastructure / deployment | P3-review | 6047 |
| [docker-spark-iceberg](https://github.com/databricks/docker-spark-iceberg) | — | Jupyter Notebook | Apache-2.0 | True | False | Infrastructure / deployment | P3-reference | 18658 |
| [dockerize](https://github.com/databricks/dockerize) | Utility to simplify running applications in docker containers | — | MIT | False | True | Infrastructure / deployment | P3-review | 123 |
| [drunken-data-quality-1](https://github.com/databricks/drunken-data-quality-1) | Spark package for checking data quality | Scala | Apache-2.0 | False | True | Data / analytics | P3-review | 445 |
| [ec2-plugin](https://github.com/databricks/ec2-plugin) | Jenkins ec2 plugin | Java | MIT | False | True | Other / manual classification | P3-review | 1088 |
| [environments](https://github.com/databricks/environments) | Per-compute dependency constraint artifacts (pyproject.toml / constraints.txt) for Databricks runtimes | — | NOASSERTION | False | False | Other / manual classification | P3-review | 474 |
| [examples](https://github.com/databricks/examples) | Examples of using bit.io with various programming languages | TypeScript | MIT | True | False | Other / manual classification | P3-reference | 23 |
| [expectations](https://github.com/databricks/expectations) | — | Python | — | False | False | Other / manual classification | P3-review | 57 |
| [fastar](https://github.com/databricks/fastar) | — | Go | Apache-2.0 | False | False | Other / manual classification | P3-review | 4500 |
| [flashoptim](https://github.com/databricks/flashoptim) | — | Python | Apache-2.0 | False | False | AI / ML | P3-review | 384 |
| [flink-connector-elasticsearch](https://github.com/databricks/flink-connector-elasticsearch) | Apache Flink connector for ElasticSearch | Java | Apache-2.0 | False | True | SDK / data connector | P3-review | 1088 |
| [genai-cookbook](https://github.com/databricks/genai-cookbook) | — | Python | NOASSERTION | False | False | AI / ML | P3-review | 101242 |
| [genie-code-cli](https://github.com/databricks/genie-code-cli) | Genie command-line coding agent | — | NOASSERTION | False | False | AI / ML | P3-review | 246 |
| [genomics-pipelines](https://github.com/databricks/genomics-pipelines) | secondary analysis pipelines parallelized with apache spark | Scala | Apache-2.0 | False | False | Other / manual classification | P3-review | 14658 |
| [glibc_version_header](https://github.com/databricks/glibc_version_header) | Build portable Linux binaries without using an ancient distro | — | MIT | True | True | Other / manual classification | P3-reference | 224 |
| [govmm-1](https://github.com/databricks/govmm-1) | Virtual Machine Manager for Go (govmm) is a suite of packages that provide Go APIs for creating and managing virtual machines. | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 608 |
| [graphframes.github.io](https://github.com/databricks/graphframes.github.io) | The documentation website for graphframes | HTML | — | True | True | Other / manual classification | P3-reference | 9931 |
| [hadoop-thirdparty](https://github.com/databricks/hadoop-thirdparty) | Apache Hadoop Thirdparty | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 94 |
| [hive-metastore](https://github.com/databricks/hive-metastore) | Apache Hive Metastore as a Standalone server in Docker | Shell | Apache-2.0 | False | True | Other / manual classification | P3-review | 24 |
| [homebrew-core](https://github.com/databricks/homebrew-core) | 🍻 Default formulae for the missing package manager for macOS | Ruby | BSD-2-Clause | True | True | Tooling / build | P3-reference | 383139 |
| [homebrew-tap](https://github.com/databricks/homebrew-tap) | Homebrew Tap for the Databricks CLI | Ruby | NOASSERTION | False | False | Tooling / build | P3-review | 255 |
| [iceberg-aws-ext](https://github.com/databricks/iceberg-aws-ext) | — | Java | — | False | False | Data / analytics | P3-review | 74 |
| [iceberg-kafka-connect](https://github.com/databricks/iceberg-kafka-connect) | — | Java | Apache-2.0 | False | False | Data / analytics | P3-review | 1039 |
| [iceberg-rest-image](https://github.com/databricks/iceberg-rest-image) | Simple project to expose a catalog over REST using a Java catalog backend | Java | Apache-2.0 | False | False | Data / analytics | P3-review | 207 |
| [iceberg-tutorials](https://github.com/databricks/iceberg-tutorials) | — | — | Apache-2.0 | False | False | Data / analytics | P3-review | 4 |
| [ide-best-practices](https://github.com/databricks/ide-best-practices) | Best practices for working with Databricks from an IDE | Python | Apache-2.0 | False | False | Tooling / build | P3-review | 26 |
| [incubator-airflow](https://github.com/databricks/incubator-airflow) | Apache Airflow (Incubating) | Python | Apache-2.0 | False | True | Other / manual classification | P3-review | 12903 |
| [intellij-jsonnet](https://github.com/databricks/intellij-jsonnet) | Intellij Jsonnet Plugin | Java | Apache-2.0 | False | False | Other / manual classification | P3-review | 210 |
| [jackson-module-scala](https://github.com/databricks/jackson-module-scala) | Add-on module for Jackson (https://github.com/FasterXML/jackson) to support Scala-specific datatypes | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 2183 |
| [jarjar](https://github.com/databricks/jarjar) | Jar Jar Links is a utility that makes it easy to repackage Java libraries and embed them into your own distribution. | — | Apache-2.0 | True | True | Other / manual classification | P3-reference | 1936 |
| [jarjar-abrams](https://github.com/databricks/jarjar-abrams) | an experimental Scala extension of Jar Jar Links  | Java | — | True | True | Other / manual classification | P3-reference | 4477 |
| [jenkins-job-builder](https://github.com/databricks/jenkins-job-builder) | Fork of https://docs.openstack.org/infra/jenkins-job-builder/ to include unmerged patches | Python | Apache-2.0 | False | False | Tooling / build | P3-review | 2786 |
| [jenkins-job-builder-addons](https://github.com/databricks/jenkins-job-builder-addons) | Addons for jenkins job builder | Python | Apache-2.0 | False | True | Tooling / build | P3-review | 43 |
| [jetty.project](https://github.com/databricks/jetty.project) | Eclipse Jetty® - Web Container & Clients - supports HTTP/2, HTTP/1.1, HTTP/1.0, websocket, servlets, and more | Java | NOASSERTION | False | True | Other / manual classification | P3-review | 226168 |
| [json-bigint](https://github.com/databricks/json-bigint) | JSON.parse/stringify with bigints support | JavaScript | MIT | False | True | Other / manual classification | P3-review | 2202 |
| [jsonnet-style-guide](https://github.com/databricks/jsonnet-style-guide) | Databricks Jsonnet Coding Style Guide | — | — | False | False | Tooling / build | P3-review | 22 |
| [jsonschema](https://github.com/databricks/jsonschema) | An implementation of the JSON Schema specification for Python | — | MIT | False | True | Other / manual classification | P3-review | 3017 |
| [jsqsh](https://github.com/databricks/jsqsh) | Console based database query tool, featuring command line editing, piping of output to other programs, and much much more | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 12563 |
| [judges](https://github.com/databricks/judges) | A small library of LLM judges | Python | Apache-2.0 | True | False | Other / manual classification | P3-reference | 751 |
| [k8s-wait-for](https://github.com/databricks/k8s-wait-for) | A simple script that allows to wait for a k8s service, job or pods to enter a desired state | Shell | MIT | True | True | Infrastructure / deployment | P3-reference | 60 |
| [kata-containers-1](https://github.com/databricks/kata-containers-1) | Kata Containers version 2.x repository. Kata Containers is an open source project and community working to build a standard implementation of lightweight Virtual Machines (VMs) that feel and perform like containers, but provide the workload isolation and security advantages of VMs. https://katacontainers.io/ | Go | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 40277 |
| [kdd24-forecasting-anomaly-detection](https://github.com/databricks/kdd24-forecasting-anomaly-detection) | — | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 3598 |
| [knowledge-repo](https://github.com/databricks/knowledge-repo) | A next-generation curated knowledge sharing platform for data scientists and other technical professions. | Python | Apache-2.0 | True | True | Other / manual classification | P3-reference | 1221 |
| [koalas](https://github.com/databricks/koalas) | Koalas: pandas API on Apache Spark | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 12259 |
| [latency-metrics](https://github.com/databricks/latency-metrics) | fly.io app that reports inter-region latency to prometheus and http clients | Go | — | False | False | Other / manual classification | P3-review | 38 |
| [learning-spark](https://github.com/databricks/learning-spark) | Example code from Learning Spark book | Java | MIT | False | False | Data / analytics | P3-review | 372 |
| [LearningSparkV2](https://github.com/databricks/LearningSparkV2) | This is the github repo for Learning Spark: Lightning-Fast Data Analytics [2nd Edition] | Scala | Apache-2.0 | False | False | Data / analytics | P3-review | 78816 |
| [Lenses](https://github.com/databricks/Lenses) | Tiny lenses library with focus on ease of use. | — | — | False | True | Other / manual classification | P3-review | 66 |
| [libpg_query_old](https://github.com/databricks/libpg_query_old) | C library for accessing the PostgreSQL parser outside of the server environment | C | BSD-3-Clause | True | True | Other / manual classification | P3-reference | 4533 |
| [lilac](https://github.com/databricks/lilac) | Curate better data for LLMs | Python | Apache-2.0 | True | False | Other / manual classification | P3-reference | 38834 |
| [linuxbrew-core](https://github.com/databricks/linuxbrew-core) | 🍻🐧 Core formulae for the Homebrew package manager on Linux | — | BSD-2-Clause | True | True | Tooling / build | P3-reference | 435232 |
| [llama-hub-llilac](https://github.com/databricks/llama-hub-llilac) | A library of data loaders for LLMs made by the community -- to be used with GPT Index and/or LangChain | Jupyter Notebook | MIT | False | True | Other / manual classification | P3-review | 4309 |
| [lumin](https://github.com/databricks/lumin) | Repository for code related to Lumin migration | Java | — | False | False | Other / manual classification | P3-review | 144 |
| [m3](https://github.com/databricks/m3) | M3 monorepo - Distributed TSDB, Aggregator and Query Engine, Prometheus Sidecar, Graphite Compatible, Metrics Platform | Go | Apache-2.0 | False | True | Other / manual classification | P3-review | 103292 |
| [m3db-operator](https://github.com/databricks/m3db-operator) | Kubernetes operator for M3DB  | — | Apache-2.0 | True | True | Infrastructure / deployment | P3-reference | 3002 |
| [megablocks](https://github.com/databricks/megablocks) | — | Python | Apache-2.0 | True | False | Other / manual classification | P3-reference | 4104 |
| [mfg_dlt_workshop](https://github.com/databricks/mfg_dlt_workshop) | DLT Manufacturing Workshop | Python | — | False | False | Other / manual classification | P3-review | 8 |
| [mlflow](https://github.com/databricks/mlflow) | Open source platform for the machine learning lifecycle | Python | Apache-2.0 | True | True | AI / ML | P3-reference | 8291 |
| [mlflow-example-sklearn-elasticnet-wine](https://github.com/databricks/mlflow-example-sklearn-elasticnet-wine) | — | Jupyter Notebook | — | False | False | AI / ML | P3-review | 72 |
| [mlops-stacks](https://github.com/databricks/mlops-stacks) | This repo provides a customizable stack for starting new ML projects on Databricks that follow production best-practices out of the box. | Go Template | Apache-2.0 | False | False | AI / ML | P2 | 40401 |
| [mssql-docker](https://github.com/databricks/mssql-docker) | Official Microsoft repository for SQL Server in Docker resources | Dockerfile | MIT | False | True | Infrastructure / deployment | P3-review | 340 |
| [nailgun](https://github.com/databricks/nailgun) | Nailgun is a client, protocol, and server for running Java programs from the command line without incurring the JVM startup overhead. | Java | NOASSERTION | False | True | Other / manual classification | P3-review | 5370 |
| [node-bitdotio](https://github.com/databricks/node-bitdotio) | Node SDK for bit.io | TypeScript | MIT | True | False | Other / manual classification | P3-reference | 429 |
| [node-pg-types](https://github.com/databricks/node-pg-types) | Type parsing for node-postgres | JavaScript | — | True | True | Data / analytics | P3-reference | 194 |
| [node-postgres](https://github.com/databricks/node-postgres) | PostgreSQL client for node.js. | JavaScript | MIT | True | True | Data / analytics | P3-reference | 5031 |
| [notebook-best-practices](https://github.com/databricks/notebook-best-practices) | An example showing how to apply software engineering best practices to Databricks notebooks. | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 755 |
| [notebook_gallery](https://github.com/databricks/notebook_gallery) | — | Jupyter Notebook | Apache-2.0 | False | False | Other / manual classification | P3-review | 106325 |
| [officeqa](https://github.com/databricks/officeqa) | Repository for getting started with the OfficeQA Benchmark. | Jupyter Notebook | Apache-2.0 | False | False | Other / manual classification | P3-review | 3728 |
| [offset-buffer](https://github.com/databricks/offset-buffer) | — | JavaScript | MIT | True | True | Other / manual classification | P3-reference | 16 |
| [pg-int8](https://github.com/databricks/pg-int8) | 64-bit big-endian signed integer-to-string conversion | JavaScript | ISC | True | True | Data / analytics | P3-reference | 15 |
| [pg-numeric](https://github.com/databricks/pg-numeric) | reads PostgreSQL binary format for numeric values into a string | JavaScript | ISC | True | True | Data / analytics | P3-reference | 25 |
| [pg-text-query](https://github.com/databricks/pg-text-query) | Helpers for generating Postgres queries from text. | Python | MIT | False | False | Data / analytics | P3-review | 910 |
| [pg_query_go](https://github.com/databricks/pg_query_go) | Go library to parse and normalize SQL queries using the PostgreSQL query parser | — | BSD-3-Clause | True | True | Other / manual classification | P3-reference | 7437 |
| [pglast](https://github.com/databricks/pglast) | PostgreSQL Languages AST and statements prettifier: master branch covers PG10, v2 branch covers PG12 | Python | — | True | True | Other / manual classification | P3-reference | 4141 |
| [pgpool2](https://github.com/databricks/pgpool2) | This is the official mirror of git://git.postgresql.org/git/pgpool2.git. Note that this is just a *mirror* - we don't work with issues/pull requests on github. Please visit our web site to file bug reports or submit patches.  | C | NOASSERTION | True | True | Other / manual classification | P3-reference | 33022 |
| [pgproto3](https://github.com/databricks/pgproto3) | — | Go | MIT | True | True | Other / manual classification | P3-reference | 162 |
| [pgsqlite](https://github.com/databricks/pgsqlite) | Load sqlite databases into Postgres databases | Python | MIT | False | False | Other / manual classification | P3-review | 98087 |
| [pig-on-spark](https://github.com/databricks/pig-on-spark) | proof-of-concept implementation of Pig-on-Spark integrated at the logical node level | Scala | Apache-2.0 | True | False | Data / analytics | P3-reference | 70095 |
| [pileup.js](https://github.com/databricks/pileup.js) | Interactive in-browser track viewer | JavaScript | Apache-2.0 | False | True | Other / manual classification | P3-review | 10250 |
| [pilot-commit](https://github.com/databricks/pilot-commit) | Pilot-Commit: Rollout allocation for efficient group-based RL post-training | Python | Apache-2.0 | False | False | Other / manual classification | P3-review | 1420 |
| [postgres-array](https://github.com/databricks/postgres-array) | Parse postgres array columns | JavaScript | MIT | True | True | Data / analytics | P3-reference | 27 |
| [postgres-bytea](https://github.com/databricks/postgres-bytea) | Postgres bytea parser | JavaScript | MIT | True | True | Data / analytics | P3-reference | 26 |
| [postgres-date](https://github.com/databricks/postgres-date) | Postgres date column parser | JavaScript | MIT | True | True | Data / analytics | P3-reference | 44 |
| [postgres-interval](https://github.com/databricks/postgres-interval) | Parse Postgres interval columns | JavaScript | MIT | True | True | Data / analytics | P3-reference | 53 |
| [postgres-range](https://github.com/databricks/postgres-range) | Range data type parser and serializer for PostgreSQL | JavaScript | MIT | True | True | Data / analytics | P3-reference | 258 |
| [protoc-gen-jsonschema](https://github.com/databricks/protoc-gen-jsonschema) | Protobuf to JSON-Schema compiler | Go | Apache-2.0 | False | True | Other / manual classification | P3-review | 228 |
| [public-data](https://github.com/databricks/public-data) | A directory of Public Data Sources on bit.io | — | MIT | True | False | Data / analytics | P3-reference | 59 |
| [pyodbc](https://github.com/databricks/pyodbc) | Python ODBC bridge | Python | MIT-0 | False | True | Other / manual classification | P3-review | 1499 |
| [python-apt-mirror-updater](https://github.com/databricks/python-apt-mirror-updater) | Automated, robust apt-get mirror selection for Debian and Ubuntu | Python | MIT | True | True | Other / manual classification | P3-reference | 218 |
| [python-bitdotio](https://github.com/databricks/python-bitdotio) | Python SDK for bit.io | Python | MIT | True | False | Other / manual classification | P3-reference | 252 |
| [python-interview](https://github.com/databricks/python-interview) | Databricks Python interview setup instructions | — | — | False | False | Other / manual classification | P3-review | 11 |
| [quantile](https://github.com/databricks/quantile) | an aggregation function for PostgreSQL | — | NOASSERTION | True | True | Other / manual classification | P3-reference | 73 |
| [reference-apps](https://github.com/databricks/reference-apps) | Spark reference applications | Scala | NOASSERTION | False | False | Other / manual classification | P3-review | 6097 |
| [responsive-docs](https://github.com/databricks/responsive-docs) | — | TypeScript | — | False | False | Web / developer experience | P3-review | 11645 |
| [responsive-pub](https://github.com/databricks/responsive-pub) | A highly available and infinitely scalable, drop-in replacement for Kafka Streams | Java | NOASSERTION | False | False | Other / manual classification | P3-review | 3409 |
| [rollout-operator](https://github.com/databricks/rollout-operator) | Kubernetes Rollout Operator | Go | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 18019 |
| [rules_docker](https://github.com/databricks/rules_docker) | Rules for building and handling Docker images with Bazel | Python | Apache-2.0 | False | True | Infrastructure / deployment | P3-review | 1005 |
| [rules_proto](https://github.com/databricks/rules_proto) | Modern bazel build rules for protobuf / gRPC | Python | NOASSERTION | False | True | Tooling / build | P3-review | 1890 |
| [rules_proto_grpc](https://github.com/databricks/rules_proto_grpc) | Bazel rules for building Protobuf and gRPC code and libraries from proto_library targets | — | Apache-2.0 | False | True | Tooling / build | P3-review | 3945 |
| [run-notebook](https://github.com/databricks/run-notebook) | — | TypeScript | Apache-2.0 | False | False | Other / manual classification | P3-review | 96 |
| [sbt-databricks](https://github.com/databricks/sbt-databricks) | An sbt plugin for deploying code to Databricks Cloud | Scala | NOASSERTION | True | False | Data / analytics | P3-reference | 135 |
| [sbt-spark-package](https://github.com/databricks/sbt-spark-package) | Sbt plugin for Spark packages | Scala | Apache-2.0 | True | False | Data / analytics | P3-reference | 74 |
| [scala](https://github.com/databricks/scala) | Scala 2 compiler and standard library. For bugs, see scala/bug | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 159412 |
| [scala-style-guide](https://github.com/databricks/scala-style-guide) | Databricks Scala Coding Style Guide | — | — | False | False | Tooling / build | P3-review | 355 |
| [sdk-go](https://github.com/databricks/sdk-go) | — | Go | Apache-2.0 | False | False | SDK / data connector | P3-review | 6760 |
| [sdk-js](https://github.com/databricks/sdk-js) | Databricks Modular SDKs for JavaScript | TypeScript | Apache-2.0 | False | False | SDK / data connector | P2 | 14537 |
| [security-bucket-brigade](https://github.com/databricks/security-bucket-brigade) | — | JavaScript | MIT | False | False | Other / manual classification | P3-review | 4014 |
| [setup-cli](https://github.com/databricks/setup-cli) | Sets up the Databricks CLI in your GitHub Actions workflow. | Shell | NOASSERTION | False | False | Tooling / build | P1 | 321 |
| [simple-pipeline](https://github.com/databricks/simple-pipeline) | Example pipeline for bit.io | Python | MIT | True | False | Other / manual classification | P3-reference | 2300 |
| [simr](https://github.com/databricks/simr) | Spark In MapReduce (SIMR) - launching Spark applications on existing Hadoop MapReduce infrastructure | Java | — | False | False | Other / manual classification | P3-review | 6669 |
| [sjsonet-old](https://github.com/databricks/sjsonet-old) | — | — | — | False | False | Other / manual classification | P3-review | 0 |
| [sjsonnet](https://github.com/databricks/sjsonnet) | A Scala implementation of the Jsonnet configuration language, running on JVM, GraalVM, Scala Native and JavaScript. | Scala | Apache-2.0 | False | False | Other / manual classification | P3-review | 6256 |
| [SnpEff](https://github.com/databricks/SnpEff) | Databricks snpeff fork | Java | — | False | False | Other / manual classification | P3-review | 251683 |
| [social-app-django](https://github.com/databricks/social-app-django) | Python Social Auth - Application - Django | Python | BSD-3-Clause | True | True | Other / manual classification | P3-reference | 2423 |
| [spark-avro](https://github.com/databricks/spark-avro) | Avro Data Source for Apache Spark | Scala | Apache-2.0 | True | False | Data / analytics | P3-reference | 405 |
| [spark-csv](https://github.com/databricks/spark-csv) | CSV Data Source for Apache Spark 1.x | Scala | Apache-2.0 | True | False | Data / analytics | P3-reference | 438 |
| [spark-deep-learning](https://github.com/databricks/spark-deep-learning) | Deep Learning Pipelines for Apache Spark | Python | Apache-2.0 | False | False | Data / analytics | P3-review | 8678 |
| [spark-integration-tests](https://github.com/databricks/spark-integration-tests) | Integration tests for Spark | Scala | Apache-2.0 | False | False | Data / analytics | P3-review | 379 |
| [spark-knowledgebase](https://github.com/databricks/spark-knowledgebase) | Spark Knowledge Base | — | NOASSERTION | False | False | Data / analytics | P3-review | 765 |
| [spark-package-cmd-tool](https://github.com/databricks/spark-package-cmd-tool) | A command line tool for Spark packages | Python | Apache-2.0 | False | False | Data / analytics | P3-review | 104 |
| [spark-pr-dashboard](https://github.com/databricks/spark-pr-dashboard) | Dashboard to aid in Spark pull request reviews | JavaScript | Apache-2.0 | False | False | Data / analytics | P3-review | 272 |
| [spark-redshift](https://github.com/databricks/spark-redshift) | Redshift data source for Apache Spark | Scala | Apache-2.0 | False | False | Data / analytics | P3-review | 796 |
| [spark-sklearn](https://github.com/databricks/spark-sklearn) | (Deprecated) Scikit-learn integration package for Apache Spark | Python | Apache-2.0 | True | False | Data / analytics | P3-reference | 801 |
| [spark-sklearn-docs](https://github.com/databricks/spark-sklearn-docs) | — | HTML | — | True | False | Data / analytics | P3-reference | 268 |
| [spark-tfocs](https://github.com/databricks/spark-tfocs) | A Spark port of TFOCS: Templates for First-Order Conic Solvers (cvxr.com/tfocs) | Scala | Apache-2.0 | False | False | Data / analytics | P3-review | 194 |
| [Spark-The-Definitive-Guide](https://github.com/databricks/Spark-The-Definitive-Guide) | Spark: The Definitive Guide's Code Repository | Scala | NOASSERTION | False | False | Data / analytics | P3-review | 536465 |
| [spark-training](https://github.com/databricks/spark-training) | Apache Spark training material | Scala | — | True | False | Data / analytics | P3-reference | 682214 |
| [spark-xml](https://github.com/databricks/spark-xml) | XML data source for Spark SQL and DataFrames | Scala | Apache-2.0 | True | False | AI / ML | P3-reference | 912 |
| [sqltools-databricks-driver](https://github.com/databricks/sqltools-databricks-driver) | SQLTools driver for Databricks SQL | TypeScript | NOASSERTION | False | False | Data / analytics | P3-review | 14470 |
| [style-guide](https://github.com/databricks/style-guide) | A Vale-compatible implementation of the Microsoft Writing Style Guide extended to Tabular.  | — | MIT | False | True | Tooling / build | P3-review | 243 |
| [subpar](https://github.com/databricks/subpar) | Subpar is a utility for creating self-contained python executables. It is designed to work well with Bazel. | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 174 |
| [superset](https://github.com/databricks/superset) | Apache Superset is a Data Visualization and Data Exploration Platform | TypeScript | Apache-2.0 | False | True | Other / manual classification | P3-review | 504785 |
| [tableau-connector](https://github.com/databricks/tableau-connector) | — | JavaScript | Apache-2.0 | False | False | SDK / data connector | P3-review | 1094 |
| [tabular-cdc-bootstrapper](https://github.com/databricks/tabular-cdc-bootstrapper) | This repository is intended to bootstrap a fileloader to CDC processing pipeline for new s3 data detected within a given bucket and prefix. It's like magic 🌙✨ | Python | — | False | False | Other / manual classification | P3-review | 114 |
| [tabular-sdk-go](https://github.com/databricks/tabular-sdk-go) | Golang SDK for interacting with the Tabular API  | Shell | — | False | False | SDK / data connector | P3-review | 187 |
| [tailscale](https://github.com/databricks/tailscale) | The easiest, most secure way to use WireGuard and 2FA. | — | BSD-3-Clause | True | True | Other / manual classification | P3-reference | 12000 |
| [tensorframes](https://github.com/databricks/tensorframes) | [DEPRECATED] Tensorflow wrapper for DataFrames on Apache Spark | Scala | Apache-2.0 | False | False | Other / manual classification | P3-review | 1836 |
| [terraform-aws-tabular-storage-profile](https://github.com/databricks/terraform-aws-tabular-storage-profile) | — | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 14 |
| [terraform-databricks-examples](https://github.com/databricks/terraform-databricks-examples) | Examples of using Terraform to deploy Databricks resources  | HCL | NOASSERTION | False | False | Infrastructure / deployment | P1 | 19028 |
| [terraform-databricks-lakehouse-blueprints](https://github.com/databricks/terraform-databricks-lakehouse-blueprints) | Set of Terraform automation templates and quickstart demos to jumpstart the design of a Lakehouse on Databricks. This project has incorporated best practices across the industries we work with to deliver composable modules to build a workspace to comply with the highest platform security and governance standards.  | Python | NOASSERTION | False | False | Infrastructure / deployment | P3-review | 2535 |
| [terraform-databricks-mlops-aws-infrastructure](https://github.com/databricks/terraform-databricks-mlops-aws-infrastructure) | This module sets up multi-workspace model registry between a Databricks AWS development (dev) workspace, staging workspace, and production (prod) workspace, allowing READ access from dev/staging workspaces to staging & prod model registries. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 13 |
| [terraform-databricks-mlops-aws-project](https://github.com/databricks/terraform-databricks-mlops-aws-project) | This module creates and configures service principals with appropriate permissions and entitlements to run CI/CD for a project, and creates a workspace directory as a container for project-specific resources for the Databricks AWS staging and prod workspaces. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 17 |
| [terraform-databricks-mlops-azure-infrastructure-with-sp-creation](https://github.com/databricks/terraform-databricks-mlops-azure-infrastructure-with-sp-creation) | This module sets up multi-workspace model registry between an Azure Databricks development (dev) workspace, staging workspace, and production (prod) workspace, allowing READ access from dev/staging workspaces to staging & prod model registries. It also creates the relevant Azure Active Directory (AAD) applications for the service principals. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 22 |
| [terraform-databricks-mlops-azure-infrastructure-with-sp-linking](https://github.com/databricks/terraform-databricks-mlops-azure-infrastructure-with-sp-linking) | This module sets up multi-workspace model registry between an Azure Databricks development (dev) workspace, staging workspace, and production (prod) workspace, allowing READ access from dev/staging workspaces to staging & prod model registries. It also links pre-existing Azure Active Directory (AAD) applications to the service principals. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 20 |
| [terraform-databricks-mlops-azure-project-with-sp-creation](https://github.com/databricks/terraform-databricks-mlops-azure-project-with-sp-creation) | This module creates and configures service principals with appropriate permissions and entitlements to run CI/CD for a project, and creates a workspace directory as a container for project-specific resources for the Azure Databricks staging and prod workspaces. It also creates the relevant Azure Active Directory (AAD) applications for the service principals. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 20 |
| [terraform-databricks-mlops-azure-project-with-sp-linking](https://github.com/databricks/terraform-databricks-mlops-azure-project-with-sp-linking) | This module creates and configures service principals with appropriate permissions and entitlements to run CI/CD for a project, and creates a workspace directory as a container for project-specific resources for the Azure Databricks staging and prod workspaces.  It also links pre-existing Azure Active Directory (AAD) applications to the service principals. | HCL | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 20 |
| [terraform-databricks-sra](https://github.com/databricks/terraform-databricks-sra) | The Security Reference Architecture (SRA) with Terraform enables deployment of Databricks workspaces and cloud infrastructure configured with security best practices. | HCL | NOASSERTION | False | False | Infrastructure / deployment | P1 | 6554 |
| [terraform-provider-databricks](https://github.com/databricks/terraform-provider-databricks) | Databricks Terraform Provider | Go | NOASSERTION | False | False | Infrastructure / deployment | P1 | 152139 |
| [terraform-provider-tabular](https://github.com/databricks/terraform-provider-tabular) | — | Go | MPL-2.0 | False | False | Infrastructure / deployment | P3-review | 149 |
| [test-infra](https://github.com/databricks/test-infra) | Test infrastructure for the Kubernetes project. | — | Apache-2.0 | True | True | Other / manual classification | P3-reference | 119206 |
| [tests-1](https://github.com/databricks/tests-1) | Kata Containers tests, CI, and metrics | — | Apache-2.0 | False | True | Other / manual classification | P3-review | 10282 |
| [thanos](https://github.com/databricks/thanos) | Highly available Prometheus setup with long term storage capabilities. A CNCF Incubating project. | Go | Apache-2.0 | True | True | Other / manual classification | P3-reference | 196723 |
| [thanos-receive-controller](https://github.com/databricks/thanos-receive-controller) | Kubernetes controller to automatically configure Thanos receive hashrings | Go | Apache-2.0 | True | True | Other / manual classification | P3-reference | 842 |
| [tmm](https://github.com/databricks/tmm) | — | Python | NOASSERTION | False | False | Other / manual classification | P3-review | 155375 |
| [tpcds-kit](https://github.com/databricks/tpcds-kit) | TPC-DS benchmark kit with some modifications/fixes | C | — | False | True | Other / manual classification | P3-review | 12547 |
| [tpch-dbgen](https://github.com/databricks/tpch-dbgen) | Patched version of dbgen | C | — | False | False | Other / manual classification | P3-review | 384 |
| [trino-container](https://github.com/databricks/trino-container) | A repository to build images of building upcoming Trino features | — | Apache-2.0 | False | False | Infrastructure / deployment | P3-review | 5 |
| [unity-catalog-setup](https://github.com/databricks/unity-catalog-setup) | Notebooks, terraform, tools to enable setting up Unity Catalog | — | NOASSERTION | False | False | Other / manual classification | P3-review | 1490 |
| [unity-gateway](https://github.com/databricks/unity-gateway) | — | Python | NOASSERTION | False | False | Other / manual classification | P3-review | 38391 |
| [upickle](https://github.com/databricks/upickle) | uPickle: a simple, fast, dependency-free JSON & Binary (MessagePack) serialization library for Scala | — | MIT | False | True | Other / manual classification | P3-review | 4910 |
| [upload-dbfs-temp](https://github.com/databricks/upload-dbfs-temp) | — | TypeScript | Apache-2.0 | False | False | Other / manual classification | P3-review | 220 |
| [vagrant](https://github.com/databricks/vagrant) | Vagrant Builds | — | — | False | True | Other / manual classification | P3-review | 1008 |
| [vector](https://github.com/databricks/vector) | A high-performance observability data pipeline. | Rust | MPL-2.0 | True | True | Other / manual classification | P3-reference | 98186 |
| [weld](https://github.com/databricks/weld) | High-performance runtime for data analytics applications | Rust | BSD-3-Clause | False | True | Other / manual classification | P3-review | 2266 |
| [workflows-examples](https://github.com/databricks/workflows-examples) | — | — | Apache-2.0 | False | False | Other / manual classification | P3-review | 24 |
| [xgb-regressor](https://github.com/databricks/xgb-regressor) | MLflow XGBoost Regressor | Python | — | False | False | Other / manual classification | P3-review | 9 |
| [xgboost-linux64](https://github.com/databricks/xgboost-linux64) | Databricks Private xgboost Linux64 fork | C++ | NOASSERTION | False | False | Other / manual classification | P3-review | 8514 |
| [YCSB](https://github.com/databricks/YCSB) | Yahoo! Cloud Serving Benchmark | Java | Apache-2.0 | False | True | Other / manual classification | P3-review | 32563 |
| [zerobus-sdk](https://github.com/databricks/zerobus-sdk) | Databricks's Zerobus Ingest SDKs | Rust | Apache-2.0 | False | False | SDK / data connector | P2 | 488646 |
| [zerobus-sdk-go](https://github.com/databricks/zerobus-sdk-go) | Zerobus SDK for Go | Go | NOASSERTION | True | False | SDK / data connector | P3-reference | 184575 |
| [zerobus-sdk-java](https://github.com/databricks/zerobus-sdk-java) | Zerobus SDK for Java | Java | NOASSERTION | True | False | SDK / data connector | P3-reference | 16669 |
| [zerobus-sdk-py](https://github.com/databricks/zerobus-sdk-py) | Zerobus SDK for Python | Python | NOASSERTION | True | False | SDK / data connector | P3-reference | 194 |
| [zerobus-sdk-ts](https://github.com/databricks/zerobus-sdk-ts) | Zerobus SDK for TypeScript | Rust | NOASSERTION | True | False | SDK / data connector | P3-reference | 97 |
