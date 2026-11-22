<!-- Modified in the devarent fork, 2026-11-22: correct example-root quickstart and safety guidance. -->
# Security Reference Architecture Template

# Introduction:

Databricks has worked with thousands of customers to securly deploy the Databricks platform with appropriate security features to meet their architecture requirements. 

This Security Reference Architecture (SRA) repository implements common security features as a unified terraform templates that are typically deployed by our security conscious customers.

Note that the private service connect blocks were previously developed in this [repository](https://github.com/bhavink/databricks/tree/master/gcpdb4u) and was helpful in putting the PSC-specific modules together.

# Component Breakdown and Description:

In this section, we break down each of the components that we've included and will be created (if not already exists) in this Security Reference Architecture.

In various .tf scripts, we have included direct links to the Databricks Terraform documentation. The [official documentation](https://registry.terraform.io/providers/databricks/databricks/latest/docs) can be found here.

## Core GCP Components:
The following resources are created and must be present before creating the workspace on Databricks:
- **Customer-managed VPC**: Using a [customer-managed VPC](https://docs.gcp.databricks.com/administration-guide/cloud-configurations/gcp/customer-managed-vpc.html) gives you direct control over network configurations, making it easier to meet strict internal security and compliance standards. This approach is required for Private Service Connect and allows you to consolidate multiple workspaces into a single network, which simplifies management and reduces the permissions Databricks needs in your account.

- **Back-end GCP Private Connectivity**: GCP Private Service Connect establishes a private network route between different GCP environments. This template configures the [back-end connection](https://docs.databricks.com/gcp/en/security/network/classic/private-service-connect), using Databricks-specific VPC endpoints to ensure that communication between your classic compute plane and the Databricks control plane does not travel over the public internet. While a [front-end](https://docs.databricks.com/gcp/en/security/network/front-end/front-end-private-connect) option is also available to keep user traffic on the GCP backbone, this particular Terraform template does not include that configuration.

- **Cloud KMS Keys**: GCP Cloud KMS keys are created to support [customer-managed keys](https://docs.databricks.com/gcp/en/security/keys/customer-managed-keys) for encryption for following functionalities:
    - Managed services: Data in the Databricks control plane (notebooks, secrets, and Databricks SQL query data).
    - Workspace storage: The two workspace storage buckets and the GCE Persistent Disk volumes of compute resources.

The following resources are created after the workspace creation:

- **Cloud DNS**: [Private DNS zone](https://docs.databricks.com/gcp/en/security/network/classic/private-service-connect#step-9-configure-dns) are required for backend Private Service Connect (PSC) on GCP to ensure that traffic destined for internal services is resolved to the private IP addresses of the PSC endpoints within the VPC.


# Getting Started

Terraform configuration is under `modules/` and `examples/`. The `gcp/` directory
itself is not a Terraform root: running init/plan there will not deploy an example.

1. Choose an example for your environment:
   - [Existing network / BYO workspace](examples/byo_gcp_workspace_deployment/README.md)
   - [Simple workspace](examples/simple_workspace_deployment/readme.md)
   - [End-to-end provisioning](<examples/end-to-end provisionning/README.md>)
   - [Service account example](examples/service_account/README.md)
2. Read that example's variables, provider constraints and authentication requirements.
   Configure credentials securely; never commit service-account keys, state or real tfvars.
3. Work from the selected example root. For example, from the repository root:

   ```bash
   cp gcp/examples/byo_gcp_workspace_deployment/terraform.tfvars.example \
      gcp/examples/byo_gcp_workspace_deployment/terraform.tfvars
   # Edit the local tfvars before planning; do not use placeholder IDs.
   terraform -chdir=gcp/examples/byo_gcp_workspace_deployment init -backend=false
   terraform -chdir=gcp/examples/byo_gcp_workspace_deployment validate
   ```

   Initialization downloads providers and modules; `validate` is not a deployment.
   For actual planning, configure the intended state backend and authentication first,
   reinitialize as required, then review a plan and its cost/resource changes.
4. Run `apply` only after explicit deployment approval. No plan or apply is performed
   by the offline source checker in this repository.

Some service-account examples generate a key by default. Review that setting and
key/state storage before use; prefer the documented impersonation flow where applicable.
Do not mistake a shell `export` in a Terraform child process for credentials being
set in your current shell.

# Network Diagram


![Network Architecture](images/GCP_PSC.png)
