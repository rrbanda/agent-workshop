# Llama Stack Server Setup

Deploy a Llama Stack server with all capabilities the ACME Agent Workshop requires.

## Prerequisites

- OpenShift cluster with **RHOAI operator** installed (includes the Llama Stack K8s operator)
- A **MaaS / vLLM inference endpoint** accessible from the cluster (provides models like `gpt-oss-120b`)

## Deploy on OpenShift (2 commands)

1. Edit `llamastack-distribution.yaml` -- set your MaaS endpoint:

   ```yaml
   - name: VLLM_API_URL
     value: "https://your-maas-endpoint/v1"   # <-- your MaaS URL
   - name: VLLM_API_TOKEN
     value: "your-api-token"                   # <-- your MaaS token
   ```

2. Apply both files:

   ```bash
   oc apply -f llamastack-configmap.yaml
   oc apply -f llamastack-distribution.yaml
   ```

3. Wait for the pod:

   ```bash
   oc get pods -w -l llamastack.io/distribution=llamastack-acme-workshop
   ```

4. Create a route and get the URL:

   ```bash
   oc create route edge llamastack --service=llamastack-acme-workshop-service --port=8321
   LLAMA_STACK_URL=https://$(oc get route llamastack -o jsonpath='{.spec.host}')
   echo $LLAMA_STACK_URL
   ```

5. Verify:

   ```bash
   curl -s "$LLAMA_STACK_URL/v1/models" | python3 -m json.tool
   ```

6. Set `LLAMA_STACK_BASE_URL` in your `.env`:

   ```
   LLAMA_STACK_BASE_URL=https://llamastack-....apps.your-cluster.com
   ```

That's it. The Llama Stack pod connects to your MaaS endpoint for LLM inference and runs vector store, agents, eval, and tool runtime inline. Embedding runs either inline (sentence-transformers) or via a remote vLLM embedding endpoint, depending on your configuration.

## Verify All Capabilities

From the repo root, run the readiness check:

```bash
python 00-setup/verify_llama_stack.py
```

All 6 checks should pass before starting the workshop.

## What's In This Directory

| File | Description |
|---|---|
| `llamastack-configmap.yaml` | ConfigMap containing the full `run.yaml` (apply this first) |
| `llamastack-distribution.yaml` | RHOAI CRD that creates the Llama Stack pod (apply this second) |
| `run.yaml` | Server configuration (embedded in ConfigMap for RHOAI deployment) |

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
| Pod in CrashLoopBackOff | Check logs: `oc logs -l llamastack.io/distribution=llamastack-acme-workshop`. Usually a bad `VLLM_API_URL` or token. |
| Models list empty | The vLLM provider auto-discovers models. Verify your MaaS has models: `curl -H "Authorization: Bearer $TOKEN" $VLLM_API_URL/models` |
| Embedding model missing | If using `sentence-transformers`: pod needs internet access, downloads on first use (~1-2 min). If using `vllm-embedding`: verify the vLLM embedding endpoint is accessible and supports the `dimensions` parameter (may need `--hf-overrides` for matryoshka models). |
| Route returns 503 | Pod still starting. Wait for `1/1 Running` in `oc get pods`. |
