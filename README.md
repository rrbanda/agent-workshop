# NovaCrest Agent Workshop

A progressive, hands-on workshop for building AI agents using **Llama Stack** and **LangGraph**. You'll learn to create agents that interact with real backend APIs through the Model Context Protocol (MCP), implement RAG, safety shields, evaluations, observability, and production deployment.

## Architecture

```
User / Chat UI
       |
  LangGraph / Llama Stack Agents (Python)
       |
  MCP Servers (FastMCP, Python)
       |
  Spring Boot REST APIs (Java 21)
       |
  PostgreSQL Databases
```

## Workshop Modules

| Module | Topic | What You Learn |
|--------|-------|----------------|
| [00-setup](00-setup/) | Environment Setup | Install prerequisites, configure Llama Stack |
| [01-backend-apis](01-backend-apis/) | Backend APIs | NovaCrest Customer and Finance REST APIs |
| [02-mcp-servers](02-mcp-servers/) | MCP Tool Layer | Wrap APIs as LLM-callable tools with FastMCP |
| [03-llama-stack-basics](03-llama-stack-basics/) | Llama Stack Fundamentals | Create agents, streaming, tool inspection |
| [04-agents-with-tools](04-agents-with-tools/) | Agents with MCP Tools | Single-domain and multi-domain agents |
| [05-multi-turn-and-hitl](05-multi-turn-and-hitl/) | Multi-Turn and HITL | Conversation memory, human-in-the-loop |
| [06-langgraph-agents](06-langgraph-agents/) | LangGraph (Alt Framework) | StateGraph, FastAPI backend, Chat UI |
| [07-composite-agents](07-composite-agents/) | Composite Agents | Agent-as-Tool pattern |
| [08-rag](08-rag/) | RAG | Vector stores, hybrid search, file_search |
| [09-safety-shields](09-safety-shields/) | Safety Shields | Llama Guard, content safety |
| [10-evaluations](10-evaluations/) | Evaluations | Scoring, benchmarks, LLM-as-judge |
| [11-observability](11-observability/) | Observability | Langfuse tracing, feedback |
| [12-low-code](12-low-code/) | Low-Code | Langflow visual agent builder |
| [13-deployment](13-deployment/) | Deployment | Helm, Docker, OpenShift |

## Prerequisites

- Python 3.12+
- Java 21+ and Maven 3.8+
- Node.js 18+ (for Chat UI)
- PostgreSQL 15+
- Docker (for containerization)
- Access to a Llama Stack server (local via Ollama or remote via vLLM)

## Quick Start

1. Clone this repo and set up your environment:
   ```bash
   git clone https://github.com/rrbanda/agent-workshop.git
   cd agent-workshop
   cp .env.example .env
   # Edit .env with your Llama Stack URL and model
   ```

2. Start with [00-setup](00-setup/) and follow the modules in order.

## Environment Variables

See [.env.example](.env.example) for all configurable variables. Key ones:

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_STACK_BASE_URL` | Llama Stack server URL | `http://localhost:8321` |
| `INFERENCE_MODEL` | LLM model identifier | `ollama/llama3.2:3b` |
| `CUSTOMER_MCP_SERVER_URL` | Customer MCP endpoint | `http://localhost:9001/mcp` |
| `FINANCE_MCP_SERVER_URL` | Finance MCP endpoint | `http://localhost:9002/mcp` |
| `CUSTOMER_API_BASE_URL` | Customer REST API | `http://localhost:8081` |
| `FINANCE_API_BASE_URL` | Finance REST API | `http://localhost:8082` |

## License

Apache-2.0
