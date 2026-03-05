# Module 06: LangGraph Agents (Alternative Framework)

## Learning Objectives

- Compare LangGraph with Llama Stack for building agents
- Build a LangGraph StateGraph with MCP tool binding
- Serve an agent as a FastAPI web service
- Run a Node.js chat UI that talks to the agent

## Prerequisites

- [Module 02: MCP Servers](../02-mcp-servers/) running
- [Module 05: Multi-Turn and HITL](../05-multi-turn-and-hitl/) completed (for context)

## Concepts

**LangGraph** is LangChain's framework for building stateful agent workflows as directed graphs. While Llama Stack uses an `Agent` class with sessions and turns, LangGraph uses `StateGraph` with nodes, edges, and state reducers.

## Architecture

```
Chat UI (Node.js) --> FastAPI Backend --> LangGraph StateGraph --> MCP Tools
                                              |
                                         ChatOpenAI (Llama Stack)
```

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
