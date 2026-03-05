# Repository Guidelines

## Project Structure

This is a progressive workshop organized into numbered modules:

- `00-setup/`: Environment setup guide
- `01-backend-apis/`: Spring Boot Customer and Finance APIs (Java 21, Maven, PostgreSQL)
- `02-mcp-servers/`: Python MCP servers wrapping the backend APIs
- `03-llama-stack-basics/`: Llama Stack hello world, tool listing
- `04-agents-with-tools/`: Single and multi-domain agents with MCP tools
- `05-multi-turn-and-hitl/`: Multi-turn conversations, human-in-the-loop
- `06-langgraph-agents/`: LangGraph alternative framework, FastAPI backend, Chat UI
- `07-composite-agents/`: Agent-as-Tool pattern (agents calling agents)
- `08-rag/`: RAG with vector stores and hybrid search
- `09-safety-shields/`: Content safety with Llama Guard
- `10-evaluations/`: Eval pipelines, scoring, LLM-as-judge
- `11-observability/`: Langfuse tracing, feedback, automated evaluation
- `12-low-code/`: Langflow visual agent builder
- `13-deployment/`: Helm charts, Dockerfiles, OpenShift deployment
- `helpers/`: Llama Stack server scripts, web search demos

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
```bash
python3.12 -m venv .venv && source .venv/bin/activate
uv run --with llama-stack llama stack run starter
```

### LangGraph Agent (Module 06)
```bash
cd 06-langgraph-agents/langgraph-fastapi && python 9_langgraph_fastapi.py
cd 06-langgraph-agents/chat-ui && npm install && npm start
```

## Coding Style & Naming Conventions

- Java: 4-space indentation, `PascalCase` classes, `camelCase` methods/fields
- Python: 4-space indentation, `snake_case` functions/variables, `PascalCase` classes
- YAML/JSON: 2-space indentation, lowercase keys with hyphens
- Package names: `com.novacrest.customer`, `com.novacrest.finance`

## Configuration

- All environment variables documented in `.env.example`
- Common vars: `LLAMA_STACK_BASE_URL`, `INFERENCE_MODEL`, `CUSTOMER_MCP_SERVER_URL`, `FINANCE_MCP_SERVER_URL`
- Database: `novacrest_customer` (port 5432), `novacrest_finance` (port 5432)

## Domain

NovaCrest is a fictional financial services company used as the example domain throughout this workshop.
