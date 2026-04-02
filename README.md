# ACME Agent Workshop

> **Build production-ready AI agents that run anywhere -- using Llama Stack, MCP, and open-source LLMs.**

A progressive, hands-on workshop where you learn each building block of AI agents -- tools, RAG, multi-turn conversations, safety, and evaluation -- then combine **all of them** into a fully functional **Mortgage Approval Agent** that reasons over real APIs, retrieves lending policy, reviews documents, guards against unsafe inputs, and measures its own accuracy.

Every core module teaches a skill. The capstone uses every one of them.

---

## Why Llama Stack?

**[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the core building blocks for AI agents. It provides a **unified API** for inference, agents, tools, RAG, safety, and evaluations -- so you don't stitch together separate libraries for each capability.

Think of it as **Kubernetes for agents**: a run-anywhere contract with a plugin architecture. You can swap model providers (Ollama, vLLM, AWS Bedrock), vector databases (ChromaDB, Milvus, PGVector), or runtimes -- without changing your agent code. Built-in support for **OpenAI-compatible APIs** and the **Model Context Protocol (MCP)** means existing tools and agents work without rewriting.

While initiated by Meta, Llama Stack has moved to a [neutral standalone GitHub organization](https://github.com/llamastack) with contributions from Red Hat, Anthropic, OpenAI, NVIDIA, Groq, AI Alliance, and others.

> [!NOTE]
> *"Llama Stack is less about replacing your favorite agent library, and more about creating the open, run-anywhere contract beneath them."* -- [Red Hat Engineering Blog](https://www.redhat.com/en/blog/llama-stack-and-case-open-run-anywhere-contract-agents)

---

## What You Will Build

By the end of this workshop, you will have built:

- **Backend REST APIs** -- Spring Boot services for customer, finance, and mortgage data
- **MCP Tool Servers** -- LLM-callable tool layers wrapping those APIs via Model Context Protocol
- **Single and multi-domain agents** -- agents that chain tools across multiple data sources
- **Multi-turn conversational agents** -- agents that remember context across turns
- **Human-in-the-loop agents** -- interactive agents with human oversight
- **RAG-powered agents** -- agents that retrieve and reason over documents
- **Safety-guarded agents** -- agents with content safety shields
- **Evaluation pipelines** -- automated scoring, benchmarks, and LLM-as-judge

Then, in the **capstone**, you apply everything to a real business problem: building a **Mortgage Approval Agent** that automates ACME's conditional approval workflow -- the most delay-prone step in mortgage processing.

---

## Architecture

```text
                          ┌──────────────────┐
                          │   User / Chat UI │
                          └────────┬─────────┘
                                   │
                          ┌────────▼─────────┐
                          │   Llama Stack    │
                          │   Agents (Python) │
                          └────────┬─────────┘
                                   │
                    ┌──────────────┼──────────────┐
                    │              │              │
             ┌──────▼──────┐ ┌────▼────┐ ┌───────▼───────┐
             │  Customer   │ │ Finance │ │   Mortgage    │
             │  MCP Server │ │   MCP   │ │     MCP       │
             └──────┬──────┘ └────┬────┘ └───────┬───────┘
                    │              │              │
             ┌──────▼──────┐ ┌────▼────┐ ┌───────▼───────┐
             │  Customer   │ │ Finance │ │   Mortgage    │
             │  REST API   │ │REST API │ │   REST API    │
             │  (8081)     │ │ (8082)  │ │    (8083)     │
             └──────┬──────┘ └────┬────┘ └───────┬───────┘
                    │              │              │
                    └──────────────┼──────────────┘
                                   │
                          ┌────────▼─────────┐
                          │    PostgreSQL     │
                          └──────────────────┘
```

> [!NOTE]
> **Capstone architecture note:** The capstone mortgage agent uses **client-side tools** (`@client_tool`) that call the Mortgage API directly from your machine, bypassing the MCP server. The Customer and Finance agents in Modules 03-05 use MCP tools via Llama Stack. See `mortgage_client_tools.py` for the client-tool implementation.

**Tech stack:** Python 3.12 | Java 21 + Spring Boot | PostgreSQL | Llama Stack | FastMCP

---

## Learning Path

The workshop follows a linear path where every module builds toward the capstone.

```text
┌─────────┐   ┌───────────────┐   ┌──────────────┐   ┌────────────────────┐
│ 00      │──▶│ 01            │──▶│ 02           │──▶│ 03                 │
│ Setup   │   │ Backend APIs  │   │ MCP Servers  │   │ Llama Stack Basics │
└─────────┘   └───────────────┘   └──────────────┘   └─────────┬──────────┘
                                                                │
                                                    ┌───────────▼───────────┐
                                                    │ 04                    │
                                                    │ Agents with MCP Tools │
                                                    └───────────┬───────────┘
                                                                │
                                                    ┌───────────▼───────────┐
                                                    │ 05                    │
                                                    │ Multi-Turn & HITL     │
                                                    └──────┬────────────────┘
                                                           │
                                                    ┌──────▼──────┐
                                                    │ 08          │
                                                    │ RAG         │
                                                    ├─────────────┤
                                                    │ 09 Safety   │
                                                    ├─────────────┤
                                                    │ 10 Evals    │
                                                    └──────┬──────┘
                                                           │
                                                 ┌─────────▼──────────┐
                                                 │ CAPSTONE           │
                                                 │ Mortgage Approval  │
                                                 │ Agent              │
                                                 └────────────────────┘
```

---

## Quick Start

```bash
# 1. Clone the repo
git clone https://github.com/rrbanda/agent-workshop.git
cd agent-workshop

# 2. Set up Python environment
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env -- set LLAMA_STACK_BASE_URL to your Llama Stack server
# Instructor-led workshop? Uncomment the "Remote" lines and use URLs from your instructor
# Self-paced / local? Use the localhost defaults, or: uv run --with llama-stack llama stack run starter

# 4. Verify Llama Stack connectivity
source .env
curl $LLAMA_STACK_BASE_URL/v1/models

# 5. Create databases
createdb acme_customer
createdb acme_finance
createdb acme_mortgage    # for the capstone

# 6. Begin the workshop
# Continue with Module 01 (01-backend-apis/README.md)
```

> [!NOTE]
> **Llama Stack server required.** You need access to a Llama Stack server with an inference model and an embedding model registered. For detailed setup instructions (tool versions, verification), see [00-setup](00-setup/).

---

## Workshop Modules

### Core Path

| # | Module | What You Learn | Duration |
|---|--------|----------------|----------|
| 00 | [Environment Setup](00-setup/) | Install Python, Java, PostgreSQL; configure Llama Stack | 30 min |
| 01 | [Backend APIs](01-backend-apis/) | Build and run ACME Customer and Finance REST APIs | 30 min |
| 02 | [MCP Servers](02-mcp-servers/) | Wrap REST APIs as LLM-callable tools using FastMCP | 20 min |
| 03 | [Llama Stack Basics](03-llama-stack-basics/) | Create your first agent, streaming responses, tool inspection | 20 min |
| 04 | [Agents with MCP Tools](04-agents-with-tools/) | Bind tools to agents, single-domain and multi-domain reasoning | 30 min |
| 05 | [Multi-Turn & HITL](05-multi-turn-and-hitl/) | Conversation memory across turns, human-in-the-loop interaction | 20 min |
| 08 | [RAG](08-rag/) | Vector stores, hybrid search (BM25 + semantic), `file_search` tool | 30 min |
| 09 | [Safety Shields](09-safety-shields/) | Register safety shields, input/output content safety | 20 min |
| 10 | [Evaluations](10-evaluations/) | Datasets, scoring functions, benchmarks, LLM-as-judge | 30 min |

### Capstone

| Module | What You Build | Duration |
|--------|----------------|----------|
| [Mortgage Approval Agent](mortgage-use-case/) | End-to-end agent combining MCP tools + RAG + multi-turn + HITL + safety shields + evaluation for mortgage conditional approval workflow | 90 min |

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers |
| Java | 21+ | Backend Spring Boot APIs |
| Maven | 3.8+ | Java build tool |
| PostgreSQL | 15+ | Database for Customer, Finance, Mortgage APIs |
| Llama Stack server | Any | Provides inference, embedding, and safety models (local or remote) |

---

## Domain

**ACME** is a fictional financial services company used as the example domain throughout this workshop. It has customers, financial orders/invoices, and a mortgage lending division. All seed data is pre-loaded via SQL scripts when you start the backend APIs.

---

## Reference

### Key Concepts

| Concept | What It Is | Where You Learn It |
|---------|------------|-------------------|
| **Llama Stack** | Open-source, community-driven platform providing a unified API for inference, agents, tools, RAG, safety, and evals -- a run-anywhere contract for AI agents | Module 03 |
| **MCP** (Model Context Protocol) | Open protocol for exposing backend APIs as tools that LLMs can call autonomously | Module 02 |
| **FastMCP** | Python library for building MCP servers with minimal boilerplate | Module 02 |
| **Agent** | An LLM with tools, instructions, and session management that can reason and act | Modules 03-05 |
| **RAG** | Retrieval-Augmented Generation -- augmenting LLM responses with relevant documents | Module 08 |
| **Safety Shields** | Content classifiers (TrustyAI Guardrails for PII detection, or Llama Guard for broader classification) that check inputs and outputs | Module 09 |
| **LLM-as-Judge** | Using a separate LLM to evaluate response quality | Module 10 |

### Script Numbering

Scripts in the core learning path (Modules 03-05) use a **global numbering scheme** that runs continuously across modules:

| Scripts | Module | Topic |
|---------|--------|-------|
| `1_*` | 03-llama-stack-basics | Hello world, streaming, tool listing |
| `4_*` - `5_*` | 04-agents-with-tools | Single and multi-domain agents |
| `6_*` - `7_*` | 05-multi-turn-and-hitl | Multi-turn conversations, HITL |

Other modules (08, 09, 10, mortgage-use-case) use **module-local numbering** starting at `0_` or `1_`.

### Environment Variables

All modules share a single `.env` file at the repo root. See [.env.example](.env.example) for the full list.

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_STACK_BASE_URL` | Llama Stack server URL | `http://localhost:8321` |
| `LLAMA_STACK_API_KEY` | API key for Llama Stack (use `fake` if none required) | `fake` |
| `INFERENCE_MODEL` | LLM model identifier | `vllm-inference/gpt-oss-120b` |
| `CUSTOMER_API_BASE_URL` | Customer REST API | `http://localhost:8081` |
| `FINANCE_API_BASE_URL` | Finance REST API | `http://localhost:8082` |
| `MORTGAGE_API_BASE_URL` | Mortgage REST API (capstone) | `http://localhost:8083` |
| `CUSTOMER_MCP_SERVER_URL` | Customer MCP endpoint | `http://localhost:9001/mcp` |
| `FINANCE_MCP_SERVER_URL` | Finance MCP endpoint | `http://localhost:9002/mcp` |
| `MORTGAGE_MCP_SERVER_URL` | Mortgage MCP endpoint (capstone) | `http://localhost:9003/mcp` |
| `EMBEDDING_MODEL` | Embedding model for RAG | `vllm-embedding/nomic-embed-text-v1-5` |
| `EMBEDDING_DIMENSION` | Embedding vector dimension | `768` |
| `SHIELD_PROVIDER` | Safety shield provider | `trustyai_fms` |
| `SHIELD_ID` | Registered shield identifier | `pii_detector` |
| `CANDIDATE_MODEL` | Model to evaluate in evals | `vllm-inference/gpt-oss-120b` |
| `JUDGE_MODEL` | LLM-as-judge model for evals | `vllm-inference/gpt-oss-120b` |

### Port Reference

| Service | Port | Module |
|---------|------|--------|
| Llama Stack | 8321 | All |
| Customer API | 8081 | 01 |
| Finance API | 8082 | 01 |
| Mortgage API | 8083 | Capstone |
| Customer MCP | 9001 | 02 |
| Finance MCP | 9002 | 02 |
| Mortgage MCP | 9003 | Capstone |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `RuntimeError: No response available` | Your Llama Stack is remote but MCP servers are on `localhost`. Remote Llama Stack cannot reach your local machine. Deploy MCP servers on OpenShift (`oc apply -f 02-mcp-servers/openshift/`) or run Llama Stack locally. See [Deployment Scenarios](documentation/modules/ROOT/pages/00-setup.adoc). |
| `Connection refused` on Llama Stack | Verify the server is running: `source .env && curl $LLAMA_STACK_BASE_URL/v1/models` |
| Empty tool lists | Ensure MCP servers are running on their expected ports. If Llama Stack is remote, MCP servers must also be deployed remotely -- `localhost` MCP URLs are not reachable from a remote server. |
| MCP tools fail with remote Llama Stack | MCP server URLs must be reachable *from the Llama Stack server*, not just from your laptop. Deploy MCP servers on the same cluster or expose them via public routes. |
| `LLAMA_STACK_BASE_URL not set` | Copy `.env.example` to `.env` and set `LLAMA_STACK_BASE_URL` to your server URL (local or remote) |
| Model not found | Check `INFERENCE_MODEL` matches a model on your Llama Stack server (`curl $LLAMA_STACK_BASE_URL/v1/models`) |
| `429 Too Many Requests` / rate limiting | MaaS backend has rate limits. Wait 30-60 seconds and retry. Eval scripts include built-in retry logic. |
| Database errors (Linux) | Set postgres password: `sudo -u postgres psql -c "ALTER USER postgres PASSWORD 'postgres';"` and check `pg_hba.conf` |
| Import errors | Activate your venv and run `pip install -r requirements.txt` |

---

## License

Apache-2.0
