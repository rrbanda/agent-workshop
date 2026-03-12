# NovaCrest Agent Workshop

> **Build production-ready AI agents that run anywhere -- using Llama Stack, MCP, and open-source LLMs.**

A progressive, hands-on workshop where you learn each building block of AI agents -- tools, RAG, multi-turn conversations, safety, and evaluation -- then combine **all of them** into a fully functional **Mortgage Approval Agent** that reasons over real APIs, retrieves lending policy, reviews documents, guards against unsafe inputs, and measures its own accuracy.

Every core module teaches a skill. The capstone uses every one of them.

---

## Why Llama Stack?

**[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the core building blocks for AI agents. It provides a **unified API** for inference, agents, tools, RAG, safety, and evaluations -- so you don't stitch together separate libraries for each capability.

Think of it as **Kubernetes for agents**: a run-anywhere contract with a plugin architecture. You can swap model providers (Ollama, vLLM, AWS Bedrock), vector databases (ChromaDB, Milvus, PGVector), or runtimes -- without changing your agent code. Built-in support for **OpenAI-compatible APIs** and the **Model Context Protocol (MCP)** means existing tools and agents work without rewriting.

While initiated by Meta, Llama Stack has moved to a [neutral standalone GitHub organization](https://github.com/llamastack) with contributions from Red Hat, Anthropic, OpenAI, NVIDIA, Groq, AI Alliance, and others.

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
- **Safety-guarded agents** -- agents with Llama Guard content safety shields
- **Evaluation pipelines** -- automated scoring, benchmarks, and LLM-as-judge

Then, in the **capstone**, you apply everything to a real business problem: building a **Mortgage Approval Agent** that automates NovaCrest's conditional approval workflow -- the most delay-prone step in mortgage processing.

---

## Architecture

```
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

**Tech stack:** Python 3.12 | Java 21 + Spring Boot | PostgreSQL | Llama Stack | FastMCP | Ollama or vLLM

---

## Learning Path

The workshop follows a linear core path where every module builds toward the capstone. Complete the core path first, then explore optional modules based on your interests.

```
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
                              ┌─────────────────┐  ┌──────▼──────┐  ┌─────────────────┐
                              │    (optional)    │  │ 08          │  │    (optional)    │
                              │  06 LangGraph   │  │ RAG         │  │  07 Composite    │
                              │  11 Observ.     │  ├─────────────┤  │  12 Low-Code     │
                              │  13 Deployment  │  │ 09 Safety   │  │                  │
                              │                 │  ├─────────────┤  │                  │
                              │                 │  │ 10 Evals    │  │                  │
                              └─────────────────┘  └──────┬──────┘  └─────────────────┘
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
# Edit .env with your Llama Stack URL and model

# 4. Start Llama Stack (local with Ollama)
ollama pull llama3.2:3b
uv run --with llama-stack llama stack run starter

# 5. Create databases
createdb novacrest_customer
createdb novacrest_finance
createdb novacrest_mortgage    # for the capstone

# 6. Begin the workshop
# Open 00-setup/README.md and follow the modules in order
```

> **No GPU required for local development.** Ollama can run quantized models (e.g., `llama3.2:3b`) on CPU. For larger models, use a remote vLLM endpoint.

---

## Workshop Modules

### Core Path

| # | Module | What You Learn | Duration |
|---|--------|----------------|----------|
| 00 | [Environment Setup](00-setup/) | Install Python, Java, PostgreSQL; configure Llama Stack | 30 min |
| 01 | [Backend APIs](01-backend-apis/) | Build and run NovaCrest Customer and Finance REST APIs | 30 min |
| 02 | [MCP Servers](02-mcp-servers/) | Wrap REST APIs as LLM-callable tools using FastMCP | 20 min |
| 03 | [Llama Stack Basics](03-llama-stack-basics/) | Create your first agent, streaming responses, tool inspection | 20 min |
| 04 | [Agents with MCP Tools](04-agents-with-tools/) | Bind tools to agents, single-domain and multi-domain reasoning | 30 min |
| 05 | [Multi-Turn & HITL](05-multi-turn-and-hitl/) | Conversation memory across turns, human-in-the-loop interaction | 20 min |
| 08 | [RAG](08-rag/) | Vector stores, hybrid search (BM25 + semantic), `file_search` tool | 30 min |
| 09 | [Safety Shields](09-safety-shields/) | Register Llama Guard shields, input/output content safety | 20 min |
| 10 | [Evaluations](10-evaluations/) | Datasets, scoring functions, benchmarks, LLM-as-judge | 30 min |

### Capstone

| Module | What You Build | Duration |
|--------|----------------|----------|
| [Mortgage Approval Agent](mortgage-use-case/) | End-to-end agent combining MCP tools + RAG + multi-turn + HITL + safety shields + evaluation for mortgage conditional approval workflow | 90 min |

### Optional Modules

| # | Module | What You Learn |
|---|--------|----------------|
| 06 | [LangGraph Agents](06-langgraph-agents/) | Alternative framework: StateGraph, FastAPI backend, Chat UI |
| 07 | [Composite Agents](07-composite-agents/) | Agent-as-Tool pattern -- agents calling other agents |
| 11 | [Observability](11-observability/) | Langfuse tracing, automated evaluation, user feedback |
| 12 | [Low-Code](12-low-code/) | Langflow visual agent builder with custom components |
| 13 | [Deployment](13-deployment/) | Helm charts, Dockerfiles, OpenShift deployment |

---

## Prerequisites

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers |
| uv | Latest | Run Llama Stack server (`curl -LsSf https://astral.sh/uv/install.sh \| sh`) |
| Java | 21+ | Backend Spring Boot APIs |
| Maven | 3.8+ | Java build tool |
| PostgreSQL | 15+ | Database for Customer, Finance, Mortgage APIs |
| Docker | Latest | Containerization (optional modules) |
| Ollama **or** vLLM | Latest | LLM inference backend for Llama Stack |

---

## Domain

**NovaCrest** is a fictional financial services company used as the example domain throughout this workshop. It has customers, financial orders/invoices, and a mortgage lending division. All seed data is pre-loaded via SQL scripts when you start the backend APIs.

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
| **Llama Guard** | Safety classifier that detects harmful content in inputs and outputs | Module 09 |
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
| `INFERENCE_MODEL` | LLM model identifier | `ollama/llama3.2:3b` |
| `CUSTOMER_MCP_SERVER_URL` | Customer MCP endpoint | `http://localhost:9001/mcp` |
| `FINANCE_MCP_SERVER_URL` | Finance MCP endpoint | `http://localhost:9002/mcp` |
| `MORTGAGE_MCP_SERVER_URL` | Mortgage MCP endpoint | `http://localhost:9003/mcp` |

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
| FastAPI (LangGraph) | 8000 | 06 |
| Chat UI | 3001 | 06 |
| Langfuse | 3000 | 11 |

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Connection refused` on Llama Stack | Verify the server is running: `curl http://localhost:8321/v1/models` |
| Empty tool lists | Ensure MCP servers are running on their expected ports |
| `LLAMA_STACK_BASE_URL not set` | Copy `.env.example` to `.env` and configure your values |
| Model not found | Check `INFERENCE_MODEL` matches a model available on your server (`ollama list`) |
| Database errors | Verify PostgreSQL is running and databases exist (`createdb novacrest_customer`) |
| Import errors | Activate your venv and run `pip install -r requirements.txt` |

---

## License

Apache-2.0
