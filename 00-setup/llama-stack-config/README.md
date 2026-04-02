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

## Troubleshooting

| Problem | Solution |
|---|---|
| `curl` returns connection error | Verify the route exists: `oc get route llamastack`. If the server was recently restarted, wait for `1/1 Running` in `oc get pods`. |
| Models list empty | Check the Llama Stack pod logs: `oc logs -l llamastack.io/distribution=llamastack-acme-workshop`. The vLLM provider auto-discovers models from the MaaS endpoint. |
| `verify_llama_stack.py` fails on embedding | Verify the embedding model is registered: `curl $LLAMA_STACK_BASE_URL/v1/models`. If using vLLM-hosted embedding, ensure the endpoint supports the `dimensions` parameter. |
