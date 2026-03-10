# Module 07: Composite Agents (Agent-as-Tool)

## Learning Objectives

- Understand the Agent-as-Tool architectural pattern
- Expose a Llama Stack agent as an MCP server
- Build hierarchical agent architectures where agents call other agents

## Prerequisites

- [Module 04: Agents with Tools](../04-agents-with-tools/) completed
- [Module 02: MCP Servers](../02-mcp-servers/) running

## Concepts

The **Agent-as-Tool** pattern wraps an entire agent behind an MCP server. This creates a hierarchical architecture where a parent agent can call child agents as tools, each specialized in a different domain.

## Architecture

```
Parent Agent / LangGraph Client
       |
       | MCP call: customer_agent(prompt)
       v
Customer Agent MCP Server (FastMCP)
       |
       | Llama Stack responses.create()
       v
Llama Stack Agent --> Customer MCP Server --> Customer API
```

## Step-by-Step

### 1. Start the Customer Agent MCP Server

```bash
cd customer-agent
cp ../../.env .env  # copy from repo root
python mcp_server_llama_stack_agent.py
```

### 2. Start the Finance Agent MCP Server

```bash
cd finance-agent
cp ../../.env .env  # copy from repo root
python mcp_server_llama_stack_agent.py
```

### 3. Test with the LangGraph Client

```bash
cd customer-agent
python test_mcp_client_langgraph_1.py
```

## What You Should See

### Customer Agent MCP Server

```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### LangGraph Client Test

```
Connecting to Customer Agent MCP at http://localhost:8001/mcp...
Tools found: ['customer_agent', 'customer_agent_detailed']
Query: Search customer with name Anabela Domingues
Agent response: The customer Anabela Domingues works for Tradição Hipermercados...
```

## Key APIs

```python
# The composite agent uses client.responses.create() for one-shot agent calls
agent_responses = client.responses.create(
    model=INFERENCE_MODEL,
    input=prompt,
    tools=[{"type": "mcp", "server_url": MCP_CUSTOMER_SERVER_URL, "server_label": "customer"}],
)
```

## Key Takeaways

- Agent-as-Tool enables modular, reusable agent architectures
- Each child agent is a specialist with its own tools and instructions
- The parent agent orchestrates across multiple child agents
- `client.responses.create()` provides a simpler one-shot API compared to sessions/turns

## Concepts Applied

- **From Module 02**: MCP server pattern (now wrapping agents, not just APIs)
- **From Module 04**: Tool binding and agent creation
- **New**: `client.responses.create()` for one-shot agent calls, agent-as-tool architecture

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Connection refused" on agent MCP | Ensure both the agent MCP server AND the underlying API MCP server are running |
| Wrong port | Check `CUSTOMER_AGENT_PORT` / `FINANCE_AGENT_PORT` in your `.env` |
| Agent returns empty response | Verify the Llama Stack server and backend APIs are accessible |

## Next Module

Proceed to [08-rag](../08-rag/) to add document retrieval to your agents.
