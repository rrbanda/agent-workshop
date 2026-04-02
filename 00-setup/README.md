# Module 00: Environment Setup

## Learning Objectives

- Install all required tools (Python, Java, Maven, PostgreSQL)
- Connect to a Llama Stack server
- Verify connectivity to all services

## Prerequisites

None -- this is the starting point.

## Concepts

**[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the building blocks for AI agents. It provides a single unified API for inference, agents, tools, RAG, safety, and evaluations -- instead of stitching together separate libraries, you get one SDK (`llama-stack-client`) that handles the full agent lifecycle. Think of it as the "Kubernetes for agents": a run-anywhere contract with a plugin architecture that lets you swap model providers, vector databases, and runtimes without changing your agent code. In this workshop, Llama Stack is the backbone -- every module from 03 onward uses it.

## Tools Required

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers | https://python.org |
| Java | 21+ | Backend Spring Boot APIs | https://adoptium.net |
| Maven | 3.8+ | Java build tool | https://maven.apache.org |
| PostgreSQL | 15+ | Database for APIs | https://postgresql.org |

You also need access to a **Llama Stack server** with at least an inference model and an embedding model registered. The Llama Stack server is pre-deployed on RHOAI (OpenShift AI) with all required models. Set `LLAMA_STACK_BASE_URL` in your `.env` to the server URL provided by your instructor or team.

> [!TIP]
> **For admins deploying a Llama Stack server:** See [llama-stack-config/](./llama-stack-config/) for RHOAI deployment instructions, the server configuration, and an OpenShift CRD template.

> [!NOTE]
> **Working directory:** All commands in this module run from the **repo root** (`agent-workshop/`).

> [!IMPORTANT]
> **Multiple terminals:** This workshop requires several services running simultaneously (backend APIs, MCP servers). Use separate terminal tabs or windows for each long-running process. Keep services running across modules.

## Step-by-Step Setup

### 1. Python Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Environment Variables

```bash
cp .env.example .env
# Edit .env -- set LLAMA_STACK_BASE_URL and verify model names match your server
```

The `.env.example` defaults to `vllm-inference/gpt-oss-120b` for inference and `vllm-embedding/nomic-embed-text-v1-5` for embedding. Update these if your Llama Stack server uses different model identifiers.

### 3. Verify Llama Stack Server

```bash
source .env
curl $LLAMA_STACK_BASE_URL/v1/models
```

You should see at least an inference model (e.g., `vllm-inference/gpt-oss-120b`) and an embedding model (e.g., `vllm-embedding/nomic-embed-text-v1-5`) in the response.

> [!IMPORTANT]
> **MCP connectivity:** The Llama Stack server must be able to reach your MCP servers over the network. If your Llama Stack is remote, MCP servers must also be deployed remotely (or exposed via a public URL). MCP servers running on `localhost` are not reachable from a remote Llama Stack.

### 4. PostgreSQL Databases

Ensure PostgreSQL is running before creating the databases. You can check with `pg_isready`.

```bash
createdb acme_customer
createdb acme_finance
createdb acme_mortgage    # needed for the capstone
```

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
```

### Deep Verification (Optional)

The basic `curl` check confirms the server is reachable. For a thorough check of all capabilities the workshop uses (chat, embedding, vector stores, safety, tool runtime), run:

```bash
python 00-setup/verify_llama_stack.py
```

This tests six capabilities and reports PASS/FAIL for each. All checks should pass before proceeding. Example output:

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

- All workshop modules share the same `.env` configuration
- Llama Stack provides a unified API for inference, agents, tools, RAG, safety, and evals
- The workshop uses ACME (a fictional financial services company) as its example domain

## Next Module

Proceed to [01-backend-apis](../01-backend-apis/) to set up the ACME backend services.
