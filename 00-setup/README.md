# Module 00: Environment Setup

## Learning Objectives

- Install all required tools (Python, Java, Maven)
- Log in to your OpenShift cluster
- Connect to the pre-deployed Llama Stack server
- Verify connectivity to all services

## Prerequisites

None -- this is the starting point.

You will be provided with:

- An **OpenShift cluster** with Llama Stack pre-deployed on RHOAI (OpenShift AI)
- A **cluster URL** and **login credentials** (or token) for `oc` CLI access
- The **Llama Stack server URL** (`LLAMA_STACK_BASE_URL`)

## Concepts

**[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the building blocks for AI agents. It provides a single unified API for inference, agents, tools, RAG, safety, and evaluations -- instead of stitching together separate libraries, you get one SDK (`llama-stack-client`) that handles the full agent lifecycle. Think of it as the "Kubernetes for agents": a run-anywhere contract with a plugin architecture that lets you swap model providers, vector databases, and runtimes without changing your agent code. In this workshop, Llama Stack is the backbone -- every module from 03 onward uses it.

## Tools Required

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers | https://python.org |
| Java | 21+ | Backend Spring Boot APIs | https://adoptium.net |
| Maven | 3.8+ | Java build tool | https://maven.apache.org |
| `oc` CLI | 4.x | OpenShift command-line tool | https://mirror.openshift.com/pub/openshift-v4/clients/ocp/stable/ |

> [!NOTE]
> **No local PostgreSQL needed.** The backend APIs run on OpenShift with their own PostgreSQL instances. You do not need to install or configure PostgreSQL locally.

> [!TIP]
> **Admin reference:** The RHOAI deployment artifacts (ConfigMap, CRD, server config) are in [llama-stack-config/](./llama-stack-config/) for reference. The Llama Stack server is already deployed and running.

> [!NOTE]
> **Working directory:** All commands in this module run from the **repo root** (`agent-workshop/`).

## Step-by-Step Setup

### 1. Python Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Log In to OpenShift

Use the cluster URL and credentials you were provided:

```bash
oc login <cluster-api-url> --username=<your-username> --password=<your-password>
```

Or, if you were given a token (from the OpenShift web console under your username > "Copy login command"):

```bash
oc login --token=<your-token> --server=<cluster-api-url>
```

Verify you are logged in:

```bash
oc whoami
oc project
```

### 3. Environment Variables

```bash
cp .env.example .env
```

Edit `.env` and set `LLAMA_STACK_BASE_URL` to the Llama Stack server URL you were provided. You can also get it from your cluster:

```bash
oc get route llamastack -o jsonpath='https://{.spec.host}'
```

> [!NOTE]
> **What to set now vs later:** At this point, you only need to set `LLAMA_STACK_BASE_URL`. The API and MCP server URLs (`CUSTOMER_API_BASE_URL`, `FINANCE_MCP_SERVER_URL`, etc.) will be filled in as you deploy those services in Modules 01 and 02. The remaining variables (RAG, safety, evals) use sensible defaults from `.env.example`.

The `.env.example` defaults to `vllm-inference/gpt-oss-120b` for inference and `vllm-embedding/nomic-embed-text-v1-5` for embedding. Update these if your Llama Stack server uses different model identifiers.

### 4. Verify Llama Stack Server

```bash
source .env
curl $LLAMA_STACK_BASE_URL/v1/models
```

You should see at least an inference model (e.g., `vllm-inference/gpt-oss-120b`) and an embedding model (e.g., `vllm-embedding/nomic-embed-text-v1-5`) in the response.

## Verification

```bash
source .env

# Check Llama Stack
curl $LLAMA_STACK_BASE_URL/v1/models

# Check Python
python --version  # Should be 3.12+

# Check Java
java --version    # Should be 21+
mvn --version     # Should be 3.8+

# Check OpenShift
oc whoami         # Should print your username
```

### Deep Verification (Optional)

The basic `curl` check confirms the server is reachable. For a thorough check of all capabilities the workshop uses (chat, embedding, vector stores, safety, tool runtime), run:

```bash
python 00-setup/verify_llama_stack.py
```

This tests six capabilities and reports PASS/FAIL for each. All six checks should pass. Example output:

```
Llama Stack Workshop Readiness Check
Server: https://llamastack.apps.example.com
========================================================
[1/6] Models ............. PASS (inference: vllm-inference/gpt-oss-120b; embedding: ...)
[2/6] Chat ............... PASS (response received, ~5 words)
[3/6] Embedding .......... PASS (dimension: 768)
[4/6] Vector Store ....... PASS (create/insert/search/delete)
[5/6] Safety ............. PASS (trustyai_fms provider available)
[6/6] Tool Runtime ....... PASS (rag-runtime + model-context-protocol)
========================================================
Result: 6/6 checks passed -- server is ready for the workshop
```

## Key Takeaways

- All workshop modules share the same `.env` configuration at the repo root
- Llama Stack provides a unified API for inference, agents, tools, RAG, safety, and evals
- The workshop uses ACME (a fictional financial services company) as its example domain
- Backend APIs and MCP servers run on OpenShift -- you do not need a local database

## Next Module

Proceed to [01-backend-apis](../01-backend-apis/) to build and deploy the ACME backend services.
