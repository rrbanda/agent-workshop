# Capstone: Mortgage Approval Agent

Build an AI agent that manages the **conditional approval loop** in a mortgage application process. The agent uses MCP tools to access application data, RAG to look up lending policy, and multi-turn conversations to guide the underwriting workflow.

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

## Architecture

```
                    Llama Stack (:8321)
                         |
                    Mortgage Agent
                    /           \
               RAG               MCP Tools
    (Lending Policy)        (mortgage-mcp :9003)
                                    |
                             Mortgage API (:8083)
                                    |
                              PostgreSQL
                          (novacrest_mortgage)
```

## Prerequisites

Before starting this capstone, you should have completed:

- **Module 00** -- Environment setup (Python 3.12, Java 21, PostgreSQL)
- **Module 01** -- Understand Spring Boot API patterns
- **Module 02** -- Understand MCP server patterns
- **Module 03** -- Llama Stack basics (agent creation, sessions)
- **Module 04** -- Agents with MCP tools (tool binding, tool calling)
- **Module 05** -- Multi-turn conversations and human-in-the-loop
- **Module 08** -- RAG (vector stores, file_search, hybrid search)

And have running:

- Llama Stack server
- PostgreSQL

## Setup

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

### 3. Start the Mortgage MCP Server

```bash
cd mortgage-mcp
pip install -r requirements.txt
python mortgage-api-mcp-server.py
```

The MCP server starts on port 9003 with 8 tools.

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

### Step 3: Agent with RAG + Tools

```bash
python 3_mortgage_agent_with_rag.py
```

Adds RAG (`file_search`) alongside MCP tools. The agent can now:
- Look up policy requirements: "What documents are needed for a conventional loan?"
- Cross-reference actual data with policy: "Does application 1 have all required documents?"

**Concepts applied:** RAG with file_search, combining tools with file_search (from Module 08)

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

### Step 5: Multi-Turn Conversation

```bash
python 5_mortgage_agent_multi_turn.py
```

Three-turn conversation showing session memory:

- **Turn 1:** "Review the conditional approval for application 1" -- agent lists all conditions and documents
- **Turn 2:** "The borrower uploaded a new bank statement dated February 2026" -- agent checks policy, determines it meets the 60-day requirement
- **Turn 3:** "Notify the borrower about remaining documents" -- agent remembers the application context and sends a targeted notification

**Concepts applied:** Multi-turn sessions, conversation memory (from Module 05)

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

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Mortgage API errors | Verify PostgreSQL database `novacrest_mortgage` exists and API is running on port 8083 |
| MCP tools not found | Check `MORTGAGE_MCP_SERVER_URL` in `.env` and that the MCP server is running on port 9003 |
| Vector store creation fails | Ensure your Llama Stack server has an embedding model registered |
| RAG returns no results | Verify `MortgageLendingPolicy.txt` was ingested (re-run `1_create_vector_store.py`) |
| Agent doesn't chain tools | Try a more capable model (e.g., `qwen3:14b`) -- small models may struggle with complex tool chains |
