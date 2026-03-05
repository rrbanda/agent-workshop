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
| `1_agent_customer_mcp.py` | Agent with customer tools only |
| `2_agent_finance_mcp.py` | Agent with finance tools only |
| `3_agent_customer_and_finance.py` | Agent with both tool sets |

## Step-by-Step

### 1. Single-Domain: Customer Agent

```bash
python 1_agent_customer_mcp.py
```

The agent searches for a customer by email using the `search_customers` tool.

### 2. Single-Domain: Finance Agent

```bash
python 2_agent_finance_mcp.py
```

The agent retrieves orders for a customer ID using `fetch_order_history`.

### 3. Multi-Domain: Customer + Finance

```bash
python 3_agent_customer_and_finance.py
```

The agent chains tools: email -> `search_customers` -> customer ID -> `fetch_order_history`.

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

## Next Module

Proceed to [05-multi-turn-and-hitl](../05-multi-turn-and-hitl/) for conversation memory and human oversight.
