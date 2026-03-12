# Module 00: Environment Setup

## Learning Objectives

- Install all required tools (Python, Java, Maven, Node.js, PostgreSQL, Docker)
- Configure and start a Llama Stack server
- Verify connectivity to all services

## Prerequisites

None -- this is the starting point.

## Concepts

**[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the building blocks for AI agents. It provides a single unified API for inference, agents, tools, RAG, safety, and evaluations -- instead of stitching together separate libraries, you get one SDK (`llama-stack-client`) that handles the full agent lifecycle. Think of it as the "Kubernetes for agents": a run-anywhere contract with a plugin architecture that lets you swap model providers, vector databases, and runtimes without changing your agent code. In this workshop, Llama Stack is the backbone -- every module from 03 onward uses it.

## Tools Required

| Tool | Version | Purpose | Install |
|------|---------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers | https://python.org |
| uv | Latest | Run Llama Stack server | `curl -LsSf https://astral.sh/uv/install.sh \| sh` |
| Java | 21+ | Backend Spring Boot APIs | https://adoptium.net |
| Maven | 3.8+ | Java build tool | https://maven.apache.org |
| Node.js | 18+ | Chat UI (Module 06) | https://nodejs.org |
| PostgreSQL | 15+ | Database for APIs | https://postgresql.org |
| Docker | Latest | Containerization (Module 13) | https://docker.com |

> **Working directory:** All commands in this module run from the **repo root** (`agent-workshop/`).

> **Multiple terminals:** This workshop requires several services running simultaneously (Llama Stack, backend APIs, MCP servers). Use separate terminal tabs or windows for each long-running process. Keep services running across modules.

## Step-by-Step Setup

### 1. Python Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Llama Stack Server

**Option A: Local with Ollama**

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2:3b
uv run --with llama-stack llama stack run starter
```

**Option B: Remote vLLM endpoint**

Set `LLAMA_STACK_BASE_URL` in your `.env` to point to your vLLM/MaaS endpoint.

### 3. PostgreSQL Databases

```bash
createdb novacrest_customer
createdb novacrest_finance
```

### 4. Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Verification

```bash
# Check Llama Stack (replace with your URL, or source .env first)
source .env
curl $LLAMA_STACK_BASE_URL/v1/models

# Check Python
python --version  # Should be 3.12+

# Check Java
java --version    # Should be 21+
mvn --version     # Should be 3.8+
```

## Key Takeaways

- All workshop modules share the same `.env` configuration
- Llama Stack provides a unified API for inference, agents, tools, RAG, safety, and evals
- The workshop uses NovaCrest (a fictional financial services company) as its example domain

## Next Module

Proceed to [01-backend-apis](../01-backend-apis/) to set up the NovaCrest backend services.
