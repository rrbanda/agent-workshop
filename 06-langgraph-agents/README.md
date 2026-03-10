# Module 06: LangGraph Agents (Alternative Framework)

## Learning Objectives

- Compare LangGraph with Llama Stack for building agents
- Build a LangGraph StateGraph with MCP tool binding
- Serve an agent as a FastAPI web service
- Run a Node.js chat UI that talks to the agent

## Prerequisites

- [Module 01: Backend APIs](../01-backend-apis/) running (ports 8081 and 8082)
- [Module 02: MCP Servers](../02-mcp-servers/) running (ports 9001 and 9002)
- [Module 05: Multi-Turn and HITL](../05-multi-turn-and-hitl/) completed (for context)

## Concepts

**LangGraph** is LangChain's framework for building stateful agent workflows as directed graphs. While Llama Stack uses an `Agent` class with sessions and turns, LangGraph uses `StateGraph` with nodes, edges, and state reducers.

## Architecture

```
Chat UI (Node.js) --> FastAPI Backend --> LangGraph StateGraph --> MCP Tools
                                              |
                                         ChatOpenAI (Llama Stack)
```

## Exploration Scripts

Before running the FastAPI backend, you can explore LangGraph concepts with these progressive scripts in the module root:

| Script | What It Does |
|--------|--------------|
| `5_langgraph_client_customer.py` | Single-domain LangGraph agent (customer MCP only) |
| `5_langgraph_client_finance.py` | Single-domain LangGraph agent (finance MCP only) |
| `6_langgraph_client_list_orders_for_franwilson.py` | Multi-domain agent: email to orders |
| `6_langgraph_client_list_orders_for_thomashardy.py` | Multi-domain agent: email to orders |
| `7_langgraph_client_list_orders_any_customer.py` | Tool listing utility (Llama Stack client) |
| `8_langgraph_client_list_invoices_any_customer.py` | Tool listing utility (Llama Stack client) |

## Step-by-Step

### 1. Start the FastAPI Backend

```bash
cd langgraph-fastapi
pip install -r requirements.txt
python 9_langgraph_fastapi.py
```

The API runs at http://localhost:8000. Swagger docs at http://localhost:8000/docs.

### 2. Start the Chat UI

```bash
cd chat-ui
npm install
npm start
```

Open http://localhost:3001 in your browser.

### 3. Test the API

```bash
curl "http://localhost:8000/question?q=Who%20is%20Thomas%20Hardy"
curl "http://localhost:8000/find_orders?email=thomashardy@example.com"
curl "http://localhost:8000/find_invoices?email=thomashardy@example.com"
```

## What You Should See

### FastAPI Backend

```
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

### curl Test

```bash
$ curl "http://localhost:8000/question?q=Who%20is%20Thomas%20Hardy"
{"answer":"Thomas Hardy is a customer at Around the Horn. His email is thomashardy@example.com."}
```

### Chat UI

Open http://localhost:3001 and type a question. The agent responds in real-time with tool call results.

## Key Differences: Llama Stack vs LangGraph

| Aspect | Llama Stack | LangGraph |
|--------|-------------|-----------|
| Agent model | `Agent` class with sessions/turns | `StateGraph` with nodes/edges |
| Tool binding | `tools=[{"type":"mcp",...}]` | `llm.bind(tools=[{"type":"mcp",...}])` |
| State management | Server-side sessions | In-graph state reducers |
| Streaming | `AgentEventLogger` | Graph event streaming |

## Key Takeaways

- LangGraph and Llama Stack can both use MCP tools for the same backend
- LangGraph is more explicit about the agent's decision flow (graph structure)
- Llama Stack's Agent API is more declarative and handles routing internally
- Both frameworks can be served behind FastAPI for production use

## Next Module

Proceed to [07-composite-agents](../07-composite-agents/) for agent-as-tool patterns.
