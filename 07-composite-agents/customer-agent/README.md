# Customer Agent MCP Server

An MCP server that wraps a Llama Stack customer agent, exposing it as MCP tools via HTTP transport using FastMCP.

## Architecture

```
MCP Client (LangGraph)
       |
       | customer_agent(prompt) / customer_agent_detailed(prompt)
       v
FastMCP Server (HTTP transport)
       |
       | client.responses.create()
       v
Llama Stack Agent --> Customer MCP Server --> Customer API
```

## Files

- **mcp_server_llama_stack_agent.py** -- MCP server exposing the customer agent as tools
- **test_mcp_client_langgraph_1.py** -- LangGraph client that uses the agent-as-tool
- **requirements.txt** -- Python dependencies

## Available Tools

### `customer_agent(prompt)`

Execute the customer agent with a natural language prompt. Returns the agent's text response.

### `customer_agent_detailed(prompt)`

Same as above but returns a JSON execution trace showing `mcp_list_tools`, `mcp_call`, and `message` steps.

## Setup

1. Copy environment from repo root:

```bash
cp ../../.env .env
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Ensure these services are running:
   - Llama Stack server
   - Customer API (port 8081)
   - Customer MCP server (port 9001)

## Usage

### Start the MCP Server

```bash
python mcp_server_llama_stack_agent.py
```

The server runs on the port defined by `CUSTOMER_AGENT_PORT` in `.env` (default: 8001).

### Test with the LangGraph Client

```bash
python test_mcp_client_langgraph_1.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_STACK_BASE_URL` | Llama Stack server URL | `http://localhost:8321` |
| `INFERENCE_MODEL` | LLM model identifier | -- |
| `MCP_CUSTOMER_SERVER_URL` | Customer MCP endpoint | `http://localhost:9001/mcp` |
| `CUSTOMER_AGENT_PORT` | Port for this agent server | `8001` |
