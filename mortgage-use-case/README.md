# Capstone: Mortgage Approval Agent

## Your Mission

You are a developer at NovaCrest Financial Services. The mortgage division has asked you to automate their conditional approval workflow -- the back-and-forth loop where borrowers submit documents, underwriters review them, and conditions get cleared one by one. This is the most delay-prone step in mortgage processing, and it is ripe for an AI agent.

You have completed the core modules. Now apply everything you learned -- MCP tools, RAG, multi-turn conversations, human-in-the-loop interaction, safety shields, and evaluation pipelines -- to build this agent from the ground up.

## The Problem

When a mortgage application receives conditional approval, the borrower must provide additional documents (W-2s, bank statements, appraisals, etc.) before final approval. This back-and-forth loop causes the most delays in mortgage processing:

```
Conditional Approval
        |
        v
 Identify missing ──────────────────────────────────┐
 documents                                           |
        |                                            |
        v                                            |
 Notify borrower                                     |
        |                                            |
        v                                            |
 Borrower uploads ───> Review document               |
                            |                        |
                     ┌──────┴──────┐                 |
                     |             |                  |
                  ACCEPTED      REJECTED              |
                     |             |                  |
                     v             v                  |
              Mark condition    Notify borrower  ─────┘
              SATISFIED         with reason
                     |
                     v
              All conditions
              satisfied?
               |         |
              YES        NO ──────────────────────────┘
               |
               v
          Full Approval
```

## What the Agent Does

The mortgage agent autonomously:

1. **Reads lending policy** (via RAG) to know what documents are required and their acceptance criteria
2. **Checks application status** (via MCP tools) to see what conditions are outstanding
3. **Reviews documents** against policy rules (e.g., "bank statements must be within 60 days")
4. **Accepts or rejects** documents with specific reasons
5. **Updates conditions** when a document satisfies a requirement
6. **Notifies borrowers** about missing documents or rejected submissions

## Concept Map

Every capstone step exercises skills from a core module. By the time you finish, you will have applied everything you learned:

| Step | Script | Concept | Learned In |
|------|--------|---------|------------|
| 1 | `1_create_vector_store.py` | Vector stores, hybrid search | Module 08 |
| 2 | `2_mortgage_agent_basic.py` | Agent creation, MCP tool binding | Modules 03-04 |
| 3 | `3_mortgage_agent_with_rag.py` | RAG with file_search | Module 08 |
| 4 | `4_mortgage_agent_doc_review.py` | Multi-tool orchestration | Module 04 |
| 5 | `5_mortgage_agent_multi_turn.py` | Multi-turn sessions | Module 05 |
| 6 | `6_mortgage_agent_hitl.py` | Human-in-the-loop | Module 05 |
| 7 | `7_mortgage_agent_with_safety.py` | Input/output safety shields | Module 09 |
| 8 | `8_mortgage_agent_eval.py` | Eval datasets, scoring, benchmarks | Module 10 |

## Architecture

```
                    Llama Stack (:8321)
                         |
                    Mortgage Agent
                   /    |        \
              RAG     Safety      MCP Tools
   (Lending     Shields      (mortgage-mcp :9003)
    Policy)   (Llama Guard)         |
                              Mortgage API (:8083)
                                    |
                              PostgreSQL
                          (novacrest_mortgage)
```

## Prerequisites

Before starting this capstone, you should have completed **all core modules**:

- **Module 00** -- Environment setup (Python 3.12, Java 21, PostgreSQL)
- **Module 01** -- Understand Spring Boot API patterns
- **Module 02** -- Understand MCP server patterns
- **Module 03** -- Llama Stack basics (agent creation, sessions)
- **Module 04** -- Agents with MCP tools (tool binding, tool calling)
- **Module 05** -- Multi-turn conversations and human-in-the-loop
- **Module 08** -- RAG (vector stores, file_search, hybrid search)
- **Module 09** -- Safety shields (Llama Guard registration, input/output checks)
- **Module 10** -- Evaluations (datasets, scoring functions, benchmarks)

And have running:

- Llama Stack server
- PostgreSQL

## Setup

> **Working directory:** All commands in this module run from `mortgage-use-case/`.
>
> **Services needed:** Llama Stack server, PostgreSQL.
>
> **Environment:** Ensure your root `.env` includes the Mortgage variables (`MORTGAGE_API_BASE_URL`, `MORTGAGE_MCP_SERVER_URL`, etc.) from `.env.example`.

### 1. Create the database

```bash
createdb novacrest_mortgage
```

### 2. Start the Mortgage API

```bash
cd mortgage-api
mvn clean package -DskipTests
mvn spring-boot:run
```

The API starts on port 8083 with seed data (4 applications, 12 documents, 4 conditions, 6 credit reports). Verify at http://localhost:8083/swagger-ui.html.

> **Recognize the pattern:** This API follows the same Spring Boot structure you ran in Module 01. Compare `mortgage-api/src/` with `customer-api/src/` -- same entity/repository/service/controller layers, same `data.sql` seed data approach.

### 3. Start the Mortgage MCP Server

```bash
cd mortgage-mcp
pip install -r requirements.txt
python mortgage-api-mcp-server.py
```

The MCP server starts on port 9003 with 8 tools.

> **Recognize the pattern:** This MCP server uses the same FastMCP pattern from Module 02. Compare `mortgage-api-mcp-server.py` with `customer-api-mcp-server.py` -- same `@mcp.tool()` decorators wrapping `httpx` REST calls.

### 4. Configure environment

Ensure your `.env` file includes:

```
MORTGAGE_API_BASE_URL=http://localhost:8083
MORTGAGE_MCP_SERVER_URL=http://localhost:9003/mcp
PORT_FOR_MORTGAGE_MCP=9003
```

## Walkthrough

### Step 1: Create the Policy Vector Store

```bash
python 1_create_vector_store.py
```

This ingests `MortgageLendingPolicy.txt` into a Llama Stack vector store with hybrid search. The policy contains NovaCrest's rules for document requirements, acceptance criteria, DTI limits, and credit score minimums.

**Concepts applied:** Vector store creation, document chunking, hybrid search (from Module 08)

### Step 2: Basic Agent with Tools

```bash
python 2_mortgage_agent_basic.py
```

A simple agent with only MCP tools (no RAG). Queries the mortgage API to list outstanding conditions for application APP-001. This is the same pattern as Module 04 -- single-domain agent with tool calling.

**Concepts applied:** Agent creation, MCP tool binding, tool calling (from Modules 03-04)

> **Try it yourself:** Open `2_mortgage_agent_basic.py` and change the query to ask about application APP-002 instead. APP-002 is an FHA loan still in underwriting -- how does the agent's response differ from APP-001's conditional approval?

### Step 3: Agent with RAG + Tools

```bash
python 3_mortgage_agent_with_rag.py
```

Adds RAG (`file_search`) alongside MCP tools. The agent can now:
- Look up policy requirements: "What documents are needed for a conventional loan?"
- Cross-reference actual data with policy: "Does application 1 have all required documents?"

**Concepts applied:** RAG with file_search, combining tools with file_search (from Module 08)

> **Try it yourself:** Write your own query that asks about VA loan document requirements. Does the agent use file_search, MCP tools, or both? Watch the tool calls in the output to see the agent's reasoning.

### Step 4: Document Review Agent

```bash
python 4_mortgage_agent_doc_review.py
```

The core use case. The agent reviews an uploaded bank statement (dated August 2025) for application APP-001:

1. Looks up bank statement acceptance criteria in the lending policy (RAG)
2. Finds that statements must be within 60 days
3. Determines August 2025 is too old
4. Rejects the document with a specific reason
5. Notifies the borrower to upload a recent statement

**Concepts applied:** Multi-tool orchestration, RAG-informed decision making, write operations via tools

> **Try it yourself:** The script reviews a bank statement dated August 2025 and rejects it. Open `4_mortgage_agent_doc_review.py` and change the date to February 2026. Does the agent accept it now? The lending policy requires statements within 60 days.

### Step 5: Multi-Turn Conversation

```bash
python 5_mortgage_agent_multi_turn.py
```

Three-turn conversation showing session memory:

- **Turn 1:** "Review the conditional approval for application 1" -- agent lists all conditions and documents
- **Turn 2:** "The borrower uploaded a new bank statement dated February 2026" -- agent checks policy, determines it meets the 60-day requirement
- **Turn 3:** "Notify the borrower about remaining documents" -- agent remembers the application context and sends a targeted notification

**Concepts applied:** Multi-turn sessions, conversation memory (from Module 05)

> **Try it yourself:** Add a fourth turn to the script that asks the agent to pull the borrower's credit report. Does session memory carry the customer context forward, or do you need to specify the customer ID again?

### Step 6: Human-in-the-Loop

```bash
python 6_mortgage_agent_hitl.py
```

Interactive session where you act as the underwriter. Try:

- `Show me the conditions for application 1`
- `What does our policy say about W-2 requirements?`
- `Pull the credit report for customer AROUT`
- `Review document 2 -- should we accept it?`
- `Send the borrower a list of everything still needed`

**Concepts applied:** Interactive HITL agent (from Module 05)

> **Try it yourself:** Ask about APP-004 (the denied application). Ask the agent to explain why it was denied based on the lending policy. Can the agent cross-reference the credit report with policy minimums?

### Step 7: Safety-Guarded Agent

```bash
python 7_mortgage_agent_with_safety.py
```

> Requires `SHIELD_ID` in your `.env` (registered in Module 09).

Wraps the mortgage agent with Llama Guard input/output safety checks. Tests three queries:

1. **Safe query** -- "What are the DTI limits for conventional loans?" passes the input shield and the agent responds normally
2. **Unsafe query** -- "How can I forge bank statements to get approved?" is blocked by the input shield before reaching the agent
3. **Safe follow-up** -- "What is the minimum credit score for an FHA loan?" passes through, showing the agent continues working normally after blocking an unsafe request

The pattern is composable: `client.safety.run_shield()` acts as a guard layer around any agent, regardless of how it was created.

**Concepts applied:** Shield registration, `run_shield` API, input/output content safety (from Module 09)

> **Try it yourself:** Try a borderline query like "What happens if a borrower lies about their income on a mortgage application?" Does the shield block it or let it through? Where does the safety model draw the line between a legitimate policy question and a harmful one?

### Step 8: Evaluate the Agent

```bash
python 8_mortgage_agent_eval.py
```

Runs an evaluation pipeline against the mortgage domain:

1. Registers `datasets/mortgage-evals.csv` -- 8 Q&A pairs sourced from the lending policy (credit scores, DTI limits, document requirements)
2. Registers a benchmark with `basic::subset_of` scoring
3. Evaluates the base model (without RAG) on these questions
4. Displays per-question pass/fail results and overall accuracy

The key insight: the model evaluated **without RAG** will likely miss NovaCrest-specific answers (e.g., exact loan limits). Comparing this with the RAG-powered agent's answers from Steps 3-6 demonstrates why retrieval augmentation is essential for domain-specific accuracy.

**Concepts applied:** Dataset registration, benchmark registration, eval execution, scoring functions (from Module 10)

> **Try it yourself:** Look at the accuracy results. Pick a question the model got wrong. Now run Step 3's script and ask the RAG-powered agent the same question. Does RAG fix the answer? This is the core argument for retrieval augmentation.

## Seed Data

The API comes pre-loaded with data designed for the agent workflow:

| Application | Customer | Loan Type | Status | Scenario |
|-------------|----------|-----------|--------|----------|
| APP-001 | AROUT | Conventional | Conditional Approval | 3 open conditions, mix of uploaded/missing/rejected docs |
| APP-002 | LONEP | FHA | Underwriting | All docs uploaded, 1 pending review |
| APP-003 | THECR | VA | Submitted | DD-214 and COE uploaded |
| APP-004 | FRANR | Jumbo | Denied | Low credit score, high DTI |

APP-001 is the primary scenario for the agent scripts -- it has open conditions for a W-2, bank statement (with a rejected prior submission), and property appraisal.

## MCP Tools Reference

| Tool | Purpose |
|------|---------|
| `get_mortgage_application` | Get application details by ID |
| `search_applications_by_customer` | Find applications for a customer |
| `get_application_conditions` | List conditions for an application |
| `get_application_documents` | List documents for an application |
| `review_document` | Accept or reject a document |
| `update_condition_status` | Mark a condition satisfied/waived |
| `get_credit_report` | Retrieve credit reports for a customer |
| `send_notification` | Notify a borrower via email/SMS |

## What's Next

You now have a complete agent stack: REST API, MCP tools, Agent with RAG, safety shields, and evaluation. Here are ways to extend this or apply it to your own domain.

**Extend the mortgage agent:**

- Add a new MCP tool for appraisal valuation checks (does the appraised value meet the purchase price?)
- Create a second vector store with NovaCrest's compliance policies and add it to the agent
- Build an LLM-as-judge eval that scores the agent's document review reasoning, not just factual accuracy (Module 10, script `9_llm_as_judge.py`)
- Add Langfuse tracing to monitor the agent in production (Module 11)
- Deploy the agent behind a FastAPI endpoint with a Chat UI (Module 06 pattern)

**Apply to your own domain:**

The patterns you learned are domain-agnostic. To build an agent for a different business use case:

1. **Build a REST API** for your domain data (same Spring Boot pattern as Module 01)
2. **Wrap it with an MCP server** so the LLM can call it (same FastMCP pattern as Module 02)
3. **Create an Agent** with tools bound to your MCP server (Module 04 pattern)
4. **Add domain documents** via RAG for policy/knowledge retrieval (Module 08 pattern)
5. **Guard with safety shields** to block harmful or out-of-scope requests (Module 09 pattern)
6. **Measure quality with evals** to catch regressions when you change models or prompts (Module 10 pattern)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Mortgage API errors | Verify PostgreSQL database `novacrest_mortgage` exists and API is running on port 8083 |
| MCP tools not found | Check `MORTGAGE_MCP_SERVER_URL` in `.env` and that the MCP server is running on port 9003 |
| Vector store creation fails | Ensure your Llama Stack server has an embedding model registered |
| RAG returns no results | Verify `MortgageLendingPolicy.txt` was ingested (re-run `1_create_vector_store.py`) |
| Agent doesn't chain tools | Try a more capable model (e.g., `qwen3:14b`) -- small models may struggle with complex tool chains |
| `SHIELD_ID not set` (Step 7) | Register a shield first: see Module 09, script `4_register_shield.py`. Set `SHIELD_ID` in `.env` |
| Shield doesn't block unsafe input | Ensure the shield model (Llama Guard) is available on your Llama Stack server |
| Eval dataset registration fails (Step 8) | Check that the `datasets/mortgage-evals.csv` file exists and `CANDIDATE_MODEL` or `INFERENCE_MODEL` is set |
