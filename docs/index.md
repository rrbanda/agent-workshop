---
hide:
  - navigation
  - toc
---

<div class="hero" markdown>

# NovaCrest Agent Workshop

<p class="hero-tagline">
Build production-ready AI agents that run anywhere — using Llama Stack, MCP, and open-source LLMs.
</p>

[Start the Workshop :material-arrow-right:](00-setup/README.md){ .md-button .md-button--primary }
[View on GitHub :fontawesome-brands-github:](https://github.com/rrbanda/agent-workshop){ .md-button }

</div>

---

## What is this workshop?

A progressive, hands-on workshop where you learn each building block of AI agents — tools, RAG, multi-turn conversations, safety, and evaluation — then combine **all of them** into a fully functional **Mortgage Approval Agent** that reasons over real APIs, retrieves lending policy, reviews documents, guards against unsafe inputs, and measures its own accuracy.

Every core module teaches a skill. The capstone uses every one of them.

---

## Why Llama Stack?

> [!NOTE]
> **[Llama Stack](https://github.com/llamastack/llama-stack)** is an open-source, community-driven platform that standardizes the core building blocks for AI agents. Think of it as **Kubernetes for agents** — a run-anywhere contract with a plugin architecture.

**Unified API** — One SDK (`llama-stack-client`) for inference, agents, tools, RAG, safety, and evaluations. No stitching together separate libraries.

**Swap anything** — Change model providers (Ollama, vLLM, AWS Bedrock), vector databases (ChromaDB, Milvus, PGVector), or runtimes — without changing your agent code.

**Open standards** — Built-in support for OpenAI-compatible APIs and the Model Context Protocol (MCP). Existing tools and agents work without rewriting.

**Community-driven** — While initiated by Meta, Llama Stack has moved to a [neutral standalone GitHub organization](https://github.com/llamastack) with contributions from Red Hat, Anthropic, OpenAI, NVIDIA, Groq, AI Alliance, and others.

> [!TIP]
> *"Llama Stack is less about replacing your favorite agent library, and more about creating the open, run-anywhere contract beneath them."* — [Red Hat Engineering Blog](https://www.redhat.com/en/blog/llama-stack-and-case-open-run-anywhere-contract-agents)

---

## What You Will Build

<div class="grid-cards" markdown>

- :material-api:{ .lg } **Backend REST APIs**

    Spring Boot services for customer, finance, and mortgage data with Swagger UI

- :material-tools:{ .lg } **MCP Tool Servers**

    LLM-callable tool layers wrapping REST APIs via Model Context Protocol

- :material-robot:{ .lg } **Single & Multi-Domain Agents**

    Agents that chain tools across multiple data sources autonomously

- :material-chat-processing:{ .lg } **Multi-Turn Conversational Agents**

    Agents that remember context across sequential exchanges

- :material-account-check:{ .lg } **Human-in-the-Loop Agents**

    Interactive agents with human oversight for high-stakes decisions

- :material-file-search:{ .lg } **RAG-Powered Agents**

    Agents that retrieve and reason over documents using vector stores

- :material-shield-check:{ .lg } **Safety-Guarded Agents**

    Content safety shields with Llama Guard for input and output filtering

- :material-chart-box:{ .lg } **Evaluation Pipelines**

    Automated scoring, benchmarks, and LLM-as-judge quality measurement

</div>

Then, in the **capstone**, you apply everything to a real business problem: building a **Mortgage Approval Agent** that automates NovaCrest's conditional approval workflow.

---

## Learning Path

The workshop follows a linear path where every module builds toward the capstone.

### Core Path

| | Module | What You Learn | Duration |
|---|--------|----------------|----------|
| 00 | [Environment Setup](00-setup/README.md) | Install Python, Java, PostgreSQL; configure Llama Stack | 30 min |
| 01 | [Backend APIs](01-backend-apis/README.md) | Build and run NovaCrest Customer and Finance REST APIs | 30 min |
| 02 | [MCP Servers](02-mcp-servers/README.md) | Wrap REST APIs as LLM-callable tools using FastMCP | 20 min |
| 03 | [Llama Stack Basics](03-llama-stack-basics/README.md) | Create your first agent, streaming responses, tool inspection | 20 min |
| 04 | [Agents with MCP Tools](04-agents-with-tools/README.md) | Bind tools to agents, single-domain and multi-domain reasoning | 30 min |
| 05 | [Multi-Turn & HITL](05-multi-turn-and-hitl/README.md) | Conversation memory across turns, human-in-the-loop interaction | 20 min |
| 08 | [RAG](08-rag/README.md) | Vector stores, hybrid search, `file_search` tool | 30 min |
| 09 | [Safety Shields](09-safety-shields/README.md) | Register Llama Guard shields, input/output content safety | 20 min |
| 10 | [Evaluations](10-evaluations/README.md) | Datasets, scoring functions, benchmarks, LLM-as-judge | 30 min |

### Capstone

| Module | What You Build | Duration |
|--------|----------------|----------|
| [Mortgage Approval Agent](mortgage-use-case/README.md) | End-to-end agent combining MCP tools + RAG + multi-turn + HITL + safety shields + evaluation | 90 min |

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

# 4. Verify Llama Stack connectivity
source .env
curl $LLAMA_STACK_BASE_URL/v1/models

# 5. Create databases
createdb novacrest_customer
createdb novacrest_finance
createdb novacrest_mortgage    # for the capstone

# 6. Begin the workshop
# Open 00-setup/README.md and follow the modules in order
```

> [!NOTE]
> **Llama Stack server required.** You need access to a Llama Stack server with an inference model and an embedding model registered. See [00-setup](00-setup/) for details.

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

**Tech stack:** Python 3.12 | Java 21 + Spring Boot | PostgreSQL | Llama Stack | FastMCP

---

## Domain

**NovaCrest** is a fictional financial services company used as the example domain throughout this workshop. It has customers, financial orders/invoices, and a mortgage lending division. All seed data is pre-loaded via SQL scripts when you start the backend APIs.

---

<div class="hero" markdown>

[Start with Module 00: Environment Setup :material-arrow-right:](00-setup/README.md){ .md-button .md-button--primary }

</div>
