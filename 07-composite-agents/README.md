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

```text
Parent Agent / MCP Client
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

> [!NOTE]
> **Working directory:** Commands run from subdirectories within `07-composite-agents/`.
>
> **Services needed:** Llama Stack, Customer API (8081), Finance API (8082), Customer MCP (9001), Finance MCP (9002).

### 1. Start the Customer Agent MCP Server

In a dedicated terminal:

```bash
cd customer-agent
python mcp_server_llama_stack_agent.py
```

### 2. Start the Finance Agent MCP Server

In a second terminal:

```bash
cd finance-agent
python mcp_server_llama_stack_agent.py
```

### 3. Test the Composite Agents

From the `07-composite-agents/` directory:

```bash
python test_composite_agent.py
```

This script acts as a parent agent, calling the customer and finance agent MCP servers as tools via the Responses API. It runs three tests: customer lookup, order history, and a cross-agent orchestration query.

## What You Should See

### Agent MCP Servers (Steps 1-2)

```text
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

### Test Script (Step 3)

```text
--- Test 1: Customer Agent ---
Query: Find customer with contact email thomashardy@example.com

Thomas Hardy is the contact for Around the Horn (customer ID: AROUT)...

--- Test 2: Finance Agent ---
Query: Get order history for customer AROUT

The order history for customer AROUT includes order #10355...

--- Test 3: Both Agents (Orchestration) ---
Query: Find the customer with email thomashardy@example.com and get their orders

Thomas Hardy works for Around the Horn (AROUT). Their orders include...
```

(Exact text varies by model.)

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
