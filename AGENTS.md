# Repository Guidelines

## Project Structure

This is a progressive workshop organized into numbered modules:

- `00-setup/`: Environment setup guide
  - `llama-stack-config/`: Admin reference -- RHOAI deployment artifacts (ConfigMap, CRD, server config)
  - `verify_llama_stack.py`: Server readiness check (tests all 6 required capabilities)
- `01-backend-apis/`: Spring Boot Customer and Finance APIs (Java 21, Maven, PostgreSQL)
- `02-mcp-servers/`: Python MCP servers wrapping the backend APIs
- `03-llama-stack-basics/`: Llama Stack hello world, tool listing
- `04-agents-with-tools/`: Single and multi-domain agents with MCP tools
- `05-multi-turn-and-hitl/`: Multi-turn conversations, human-in-the-loop
- `08-rag/`: RAG with vector stores and hybrid search
- `09-safety-shields/`: Content safety with safety shields (TrustyAI Guardrails or Llama Guard)
- `10-evaluations/`: Eval pipelines, scoring, LLM-as-judge
- `mortgage-use-case/`: Capstone -- Mortgage Approval Agent

## Build, Test, and Development Commands

### Backend APIs (Module 01)
```bash
cd 01-backend-apis/customer-api && mvn clean package -DskipTests && mvn spring-boot:run
cd 01-backend-apis/finance-api && mvn clean package -DskipTests && mvn spring-boot:run
```

### MCP Servers (Module 02)
```bash
python 02-mcp-servers/customer-mcp/customer-api-mcp-server.py
python 02-mcp-servers/finance-mcp/finance-api-mcp-server.py
```

### Llama Stack Server
The Llama Stack server is pre-deployed on RHOAI. Set `LLAMA_STACK_BASE_URL` in `.env` to the server URL provided by your instructor or from `oc get route llamastack`.

## Coding Style & Naming Conventions

- Java: 4-space indentation, `PascalCase` classes, `camelCase` methods/fields
- Python: 4-space indentation, `snake_case` functions/variables, `PascalCase` classes
- YAML/JSON: 2-space indentation, lowercase keys with hyphens
- Package names: `com.acme.customer`, `com.acme.finance`

## Configuration

- All environment variables documented in `.env.example`
- Key variable groups: Llama Stack connection (`LLAMA_STACK_BASE_URL`, `INFERENCE_MODEL`), backend APIs (`CUSTOMER_API_BASE_URL`, `FINANCE_API_BASE_URL`, `MORTGAGE_API_BASE_URL`), MCP servers (`CUSTOMER_MCP_SERVER_URL`, `FINANCE_MCP_SERVER_URL`, `MORTGAGE_MCP_SERVER_URL`), RAG (`EMBEDDING_MODEL`, `EMBEDDING_DIMENSION`), safety (`SHIELD_PROVIDER`, `SHIELD_ID`), evaluations (`CANDIDATE_MODEL`, `JUDGE_MODEL`)
- Database: `acme_customer` (port 5432), `acme_finance` (port 5432), `acme_mortgage` (port 5432)

## Domain

ACME is a fictional financial services company used as the example domain throughout this workshop.
