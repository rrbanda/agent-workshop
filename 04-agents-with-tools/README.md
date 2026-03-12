# Module 04: Agents with MCP Tools

## Learning Objectives

- Bind MCP tools to a Llama Stack agent
- Build single-domain agents (customer-only or finance-only)
- Build a multi-domain agent that reasons across customer and finance data
- Understand cross-domain reasoning (email -> customer ID -> orders)

## Prerequisites

- [Module 02: MCP Servers](../02-mcp-servers/) running (ports 9001 and 9002)
- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed

## Scripts

| Script | What It Does |
|--------|--------------|
| `4_agent_customer_mcp.py` | Agent with customer tools only |
| `4_agent_finance_mcp.py` | Agent with finance tools only |
| `5_agent_customer_and_finance.py` | Agent with both tool sets |

## Step-by-Step

> **Working directory:** All commands in this module run from `04-agents-with-tools/`.
>
> **Services needed:** Llama Stack, Customer API (8081), Finance API (8082), Customer MCP (9001), Finance MCP (9002).

### 1. Single-Domain: Customer Agent

```bash
python 4_agent_customer_mcp.py
```

The agent searches for a customer by email using the `search_customers` tool.

### 2. Single-Domain: Finance Agent

```bash
python 4_agent_finance_mcp.py
```

The agent retrieves orders for a customer ID using `fetch_order_history`.

### 3. Multi-Domain: Customer + Finance

```bash
python 5_agent_customer_and_finance.py
```

The agent chains tools: email -> `search_customers` -> customer ID -> `fetch_order_history`.

## What You Should See

### Customer Agent (script 4)

```
Base URL: http://localhost:8321
Model: ollama/llama3.2:3b
Customer MCP: http://localhost:9001/mcp
The customer with email thomashardy@example.com is Thomas Hardy,
contact for Around the Horn (customer ID: AROUT)...
```

The agent calls `search_customers` behind the scenes. Only the final text response is printed. (Exact wording varies by model.)

### Multi-Domain Agent (script 5)

```
Base URL: http://localhost:8321
Model: ollama/llama3.2:3b
Customer MCP: http://localhost:9001/mcp
Finance MCP: http://localhost:9002/mcp
The customer with email thomashardy@example.com is Thomas Hardy from
Around the Horn (AROUT). Their orders include order #10355...
```

The agent chains `search_customers` then `fetch_order_history` autonomously. Only the final text is printed.

## How Tool Binding Works

```python
mcp_tools = [
    {
        "type": "mcp",
        "server_url": os.getenv("CUSTOMER_MCP_SERVER_URL"),
        "server_label": "customer",
    },
    {
        "type": "mcp",
        "server_url": os.getenv("FINANCE_MCP_SERVER_URL"),
        "server_label": "finance",
    }
]

agent = Agent(client, model=MODEL, instructions="...", tools=mcp_tools)
```

## Key Takeaways

- MCP tools are bound to agents via `tools=[{"type": "mcp", "server_url": ..., "server_label": ...}]`
- The LLM autonomously decides which tools to call based on the user's question
- Multi-domain agents can chain tool calls across different MCP servers
- The `instructions` parameter acts as the system prompt guiding agent behavior

## Concepts Applied

- **From Module 02**: MCP server URLs and tool exposure
- **From Module 03**: `Agent` class, `create_session`, `create_turn`, `AgentEventLogger`

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Empty tool list | Verify MCP servers are running on ports 9001/9002 |
| Connection refused | Check `LLAMA_STACK_BASE_URL` and that the Llama Stack server is running |
| Agent doesn't call tools | Ensure `INFERENCE_MODEL` supports tool calling (e.g., `llama3.2:3b`) |

## Next Module

Proceed to [05-multi-turn-and-hitl](../05-multi-turn-and-hitl/) for conversation memory and human oversight.
