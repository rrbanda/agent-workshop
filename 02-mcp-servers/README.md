# Module 02: MCP Servers

## Learning Objectives

- Understand the Model Context Protocol (MCP)
- Write FastMCP tool wrappers for REST APIs
- Register MCP servers with Llama Stack
- Test MCP tools independently

> [!TIP]
> **Capstone Preview:** In the capstone, a Mortgage MCP server wraps the Mortgage API using the same FastMCP pattern you learn here -- same `@mcp.tool()` decorators, same `httpx` calls, same structure.

## Prerequisites

- [Module 01: Backend APIs](../01-backend-apis/) running (ports 8081 and 8082)

## Concepts

The **Model Context Protocol (MCP)** provides a standard way to expose tools to LLMs. An MCP server wraps existing APIs as tool functions that an LLM can discover and call. FastMCP is a Python library that makes building MCP servers straightforward.

## ACME MCP Tools

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

> [!NOTE]
> **Working directory:** All commands in this module run from `02-mcp-servers/`.
>
> **Services needed:** Customer API (8081), Finance API (8082) from Module 01.

### 1. Start Customer MCP

In a dedicated terminal:

```bash
cd customer-mcp
python customer-api-mcp-server.py
```

> [!NOTE]
> The MCP server uses `load_dotenv()` which loads `.env` from the current working directory. Since you run these from `02-mcp-servers/customer-mcp/`, make sure your root `.env` is also accessible. The simplest approach: run from the repo root instead (e.g., `python 02-mcp-servers/customer-mcp/customer-api-mcp-server.py`), or set the env vars `CUSTOMER_API_BASE_URL`, `PORT_FOR_CUSTOMER_MCP`, and `HOST_FOR_CUSTOMER_MCP` in your shell before starting.

### 2. Start Finance MCP

In a new terminal:

```bash
cd finance-mcp
python finance-api-mcp-server.py
```

### 3. Register with Llama Stack

> [!IMPORTANT]
> **Requires:** Llama Stack server running (started in Module 00).

In a new terminal, from the repo root:

```bash
cd 02-mcp-servers/examples
python 1_register_customer_mcp.py
python 1_register_finance_mcp.py
```

### 4. Verify Registration

```bash
python 2_list_tools.py
```

## Verification

The best way to verify MCP registration is `python 2_list_tools.py` (Step 4 above). You can also check that the MCP servers themselves are responding:

```bash
# Should return a JSON response (MCP protocol handshake)
curl -s http://localhost:9001/mcp | head -c 200
curl -s http://localhost:9002/mcp | head -c 200
```

## Key Takeaways

- MCP servers act as a bridge between LLMs and existing APIs
- The `@mcp.tool()` decorator turns a Python function into an LLM-callable tool
- Tools are registered with Llama Stack via `client.toolgroups.register()`
- MCP uses HTTP transport (streamable HTTP) for communication

## Next Module

Proceed to [03-llama-stack-basics](../03-llama-stack-basics/) to create your first Llama Stack agent.
