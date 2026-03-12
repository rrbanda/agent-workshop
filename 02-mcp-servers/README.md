# Module 02: MCP Servers

## Learning Objectives

- Understand the Model Context Protocol (MCP)
- Write FastMCP tool wrappers for REST APIs
- Register MCP servers with Llama Stack
- Test MCP tools independently

> **Capstone Preview:** In the capstone, a Mortgage MCP server wraps the Mortgage API using the same FastMCP pattern you learn here -- same `@mcp.tool()` decorators, same `httpx` calls, same structure.

## Prerequisites

- [Module 01: Backend APIs](../01-backend-apis/) running (ports 8081 and 8082)

## Concepts

The **Model Context Protocol (MCP)** provides a standard way to expose tools to LLMs. An MCP server wraps existing APIs as tool functions that an LLM can discover and call. FastMCP is a Python library that makes building MCP servers straightforward.

## NovaCrest MCP Tools

### Customer MCP (port 9001)

| Tool | Wraps | Description |
|------|-------|-------------|
| `search_customers` | `GET /api/customers` | Search by company name, contact name, email, or phone |
| `get_customer` | `GET /api/customers/{id}` | Get a specific customer by ID |

### Finance MCP (port 9002)

| Tool | Wraps | Description |
|------|-------|-------------|
| `fetch_order_history` | `POST /api/finance/orders/history` | Get orders for a customer |
| `fetch_invoice_history` | `POST /api/finance/invoices/history` | Get invoices for a customer |

## Step-by-Step

> **Working directory:** All commands in this module run from `02-mcp-servers/`.
>
> **Services needed:** Customer API (8081), Finance API (8082) from Module 01.

### 1. Start Customer MCP

In a dedicated terminal:

```bash
cd customer-mcp
```

Create a `.env` file with:

```env
CUSTOMER_API_BASE_URL=http://localhost:8081
PORT_FOR_CUSTOMER_MCP=9001
HOST_FOR_CUSTOMER_MCP=0.0.0.0
```

```bash
python customer-api-mcp-server.py
```

### 2. Start Finance MCP

In a new terminal:

```bash
cd finance-mcp
```

Create a `.env` file with:

```env
FINANCE_API_BASE_URL=http://localhost:8082
PORT_FOR_FINANCE_MCP=9002
HOST_FOR_FINANCE_MCP=0.0.0.0
```

```bash
python finance-api-mcp-server.py
```

### 3. Register with Llama Stack

> **Requires:** Llama Stack server running (started in Module 00).

In a new terminal, from the repo root:

```bash
cd examples
python 1_register_customer_mcp.py
python 1_register_finance_mcp.py
```

### 4. Verify Registration

```bash
python 2_list_tools.py
```

## Verification

```bash
# Test Customer MCP directly
curl http://localhost:9001/mcp

# Test Finance MCP directly
curl http://localhost:9002/mcp
```

## Key Takeaways

- MCP servers act as a bridge between LLMs and existing APIs
- The `@mcp.tool()` decorator turns a Python function into an LLM-callable tool
- Tools are registered with Llama Stack via `client.toolgroups.register()`
- MCP uses HTTP transport (streamable HTTP) for communication

## Next Module

Proceed to [03-llama-stack-basics](../03-llama-stack-basics/) to create your first Llama Stack agent.
