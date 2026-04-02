# Llama Stack Server Setup (Admin Reference)

The Llama Stack server is **pre-deployed on RHOAI** (OpenShift AI) with all required models and capabilities. Workshop participants do not need to deploy or configure Llama Stack -- they only need the server URL.

## Get the Server URL

```bash
LLAMA_STACK_BASE_URL=https://$(oc get route llamastack -o jsonpath='{.spec.host}')
echo $LLAMA_STACK_BASE_URL
```

Set this URL in your `.env` file. Your instructor will provide this if you are in an instructor-led workshop.

## Verify All Capabilities

From the repo root, run the readiness check:

```bash
python 00-setup/verify_llama_stack.py
```

All 6 checks should pass before starting the workshop.

## What's In This Directory

These files are the RHOAI deployment artifacts used to set up the Llama Stack server. They are kept here for reference -- the server is already deployed and running.

| File | Description |
|---|---|
| `llamastack-configmap.yaml` | ConfigMap containing the server configuration |
| `llamastack-distribution.yaml` | RHOAI CRD that creates the Llama Stack pod |
| `run.yaml` | Server configuration (embedded in the ConfigMap) |

## What the Server Provides

| Capability | Provider | Workshop Modules |
|---|---|---|
| LLM Inference | `remote::vllm` (via MaaS) | All modules |
| Embedding | `inline::sentence-transformers` (or `remote::vllm` for vLLM-hosted embedding) | 08-rag, Mortgage |
| Vector Store | `inline::milvus` (workshop scripts use `provider_id: "faiss"` -- ensure your server has a matching provider) | 08-rag, Mortgage |
| Agents | `inline::meta-reference` | 03-10, Mortgage |
| Safety | `inline::llama-guard` or `trustyai_fms` (see Module 09) | 09-safety-shields |
| Eval / Scoring | `inline::meta-reference`, `inline::llm-as-judge` | 10-evaluations |
| Tool Runtime | `inline::rag-runtime`, `remote::model-context-protocol` | 04, 08, Mortgage |
| Files / Datasets | `inline::localfs` | 08-rag, 10-evaluations |

## Deploy Backend Services (Instructor-Led Workshop)

For an instructor-led workshop, you also need to deploy the ACME backend APIs, PostgreSQL databases, and MCP servers so that participants have pre-deployed services available.

### Automated Deploy Script

A single script builds all container images using OpenShift Binary Builds (no external registry needed) and deploys everything:

```bash
cd agent-workshop
bash 00-setup/admin/deploy.sh acme-workshop
```

This will:

1. Build 6 container images via `oc new-build --binary`:
   - 3 Java Spring Boot APIs (Customer, Finance, Mortgage)
   - 3 Python MCP servers (Customer, Finance, Mortgage)
2. Deploy 3 PostgreSQL instances
3. Deploy all 6 services with OpenShift Routes
4. Print the `.env` block with all URLs ready for participants

The full process takes approximately 15-20 minutes (Java builds take 2-4 minutes each).

To tear down all resources later:

```bash
bash 00-setup/admin/teardown.sh acme-workshop
```

> [!TIP]
> Helm charts are also available in `site/13-deployment/helm/` (Customer and Finance only). Images must be built first via `oc new-build`. For the full workshop including the Mortgage capstone, use the deploy script above.

### Building Images Manually

If you need to build images individually (for example, to update a single service):

```bash
# MCP server example (Python)
oc new-build --binary --strategy=docker --name=customer-mcp -n acme-workshop
oc start-build customer-mcp --from-dir=02-mcp-servers/customer-mcp/ --follow -n acme-workshop

# API example (Java -- uses multi-stage Dockerfile under deployment/)
oc new-build --binary --strategy=docker --name=customer-api -n acme-workshop
oc start-build customer-api --from-dir=01-backend-apis/customer-api/ --follow -n acme-workshop
```

Each service has a `Dockerfile` in its directory:

- APIs: `01-backend-apis/<name>/deployment/Dockerfile` and `mortgage-use-case/mortgage-api/deployment/Dockerfile`
- MCP servers: `02-mcp-servers/<name>/Dockerfile` and `mortgage-use-case/mortgage-mcp/Dockerfile`

### Collect URLs for Participants

After all services are deployed, gather the route URLs:

```bash
echo "LLAMA_STACK_BASE_URL=https://$(oc get route llamastack -n llamastack -o jsonpath='{.spec.host}')"
echo "CUSTOMER_API_BASE_URL=https://$(oc get route acme-customer-service -o jsonpath='{.spec.host}')"
echo "FINANCE_API_BASE_URL=https://$(oc get route acme-finance-service -o jsonpath='{.spec.host}')"
echo "MORTGAGE_API_BASE_URL=https://$(oc get route mortgage-api-route -o jsonpath='{.spec.host}')"
echo "CUSTOMER_MCP_SERVER_URL=https://$(oc get route mcp-customer-route -o jsonpath='{.spec.host}')/mcp"
echo "FINANCE_MCP_SERVER_URL=https://$(oc get route mcp-finance-route -o jsonpath='{.spec.host}')/mcp"
echo "MORTGAGE_MCP_SERVER_URL=https://$(oc get route mcp-mortgage-route -o jsonpath='{.spec.host}')/mcp"
```

Participants paste these values into their `.env` file.

## Troubleshooting

| Problem | Solution |
|---|---|
| `curl` returns connection error | Verify the route exists: `oc get route llamastack`. If the server was recently restarted, wait for `1/1 Running` in `oc get pods`. |
| Models list empty | Check the Llama Stack pod logs: `oc logs -l llamastack.io/distribution=llamastack-acme-workshop`. The vLLM provider auto-discovers models from the MaaS endpoint. |
| `verify_llama_stack.py` fails on embedding | Verify the embedding model is registered: `curl $LLAMA_STACK_BASE_URL/v1/models`. If using vLLM-hosted embedding, ensure the endpoint supports the `dimensions` parameter. |
