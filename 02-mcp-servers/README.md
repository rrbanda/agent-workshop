# Module 02: MCP Servers

## Learning Objectives

- Understand the Model Context Protocol (MCP)
- Write FastMCP tool wrappers for REST APIs
- Build and deploy MCP servers on OpenShift
- Register MCP servers with Llama Stack
- Test MCP tools independently

> [!TIP]
> **Capstone Preview:** In the capstone, a Mortgage MCP server wraps the Mortgage API using the same FastMCP pattern you learn here -- same `@mcp.tool()` decorators, same `httpx` calls, same structure.

## Prerequisites

- [Module 01: Backend APIs](../01-backend-apis/) deployed on OpenShift (Customer and Finance APIs running, route URLs set in `.env`)

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
> **Working directory:** All commands in this module run from the **repo root** (`agent-workshop/`).
>
> **Services needed:** Customer API and Finance API deployed on OpenShift (Module 01).

Since Llama Stack runs on RHOAI, MCP servers must also be deployed on OpenShift so Llama Stack can reach them.

### 1. Build Customer MCP

```bash
oc new-build --binary --strategy=docker --name=customer-mcp
oc start-build customer-mcp --from-dir=02-mcp-servers/customer-mcp/ --follow
```

> [!TIP]
> If you see `"customer-mcp" already exists`, skip `oc new-build` and just re-run `oc start-build`.

### 2. Build Finance MCP

```bash
oc new-build --binary --strategy=docker --name=finance-mcp
oc start-build finance-mcp --from-dir=02-mcp-servers/finance-mcp/ --follow
```

> [!TIP]
> If you see `"finance-mcp" already exists`, skip `oc new-build` and just re-run `oc start-build`.

### 3. Deploy to OpenShift

```bash
oc apply -f 02-mcp-servers/openshift/customer-mcp.yaml
oc apply -f 02-mcp-servers/openshift/finance-mcp.yaml
```

### 4. Get the Route URLs

```bash
echo "CUSTOMER_MCP_SERVER_URL=https://$(oc get route mcp-customer-route -o jsonpath='{.spec.host}')/mcp"
echo "FINANCE_MCP_SERVER_URL=https://$(oc get route mcp-finance-route -o jsonpath='{.spec.host}')/mcp"
```

Set these in your `.env` file.

### 5. Verify Pods are Running

```bash
oc get pods -l app=customer-mcp
oc get pods -l app=finance-mcp
```

Both pods should show `1/1 Running`.

### 6. Register with Llama Stack

```bash
python 02-mcp-servers/examples/1_register_customer_mcp.py
python 02-mcp-servers/examples/1_register_finance_mcp.py
```

### 7. Verify Registration

```bash
python 02-mcp-servers/examples/2_list_tools.py
```

You should see `customer_mcp` and `finance_mcp` toolgroups listed with their MCP endpoints.

## Key Takeaways

- MCP servers act as a bridge between LLMs and existing APIs
- The `@mcp.tool()` decorator turns a Python function into an LLM-callable tool
- Tools are registered with Llama Stack via `client.toolgroups.register()`
- MCP uses HTTP transport (streamable HTTP) for communication

## Next Module

Proceed to [03-llama-stack-basics](../03-llama-stack-basics/) to create your first Llama Stack agent.
