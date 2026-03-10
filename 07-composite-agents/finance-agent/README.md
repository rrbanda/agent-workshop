# Finance Agent MCP Server

An MCP server that wraps a Llama Stack finance agent, exposing it as MCP tools via HTTP transport using FastMCP.

## Architecture

```
MCP Client (LangGraph)
       |
       | finance_agent(prompt) / finance_agent_detailed(prompt)
       v
FastMCP Server (HTTP transport)
       |
       | client.responses.create()
       v
Llama Stack Agent --> Finance MCP Server --> Finance API
```

## Files

- **mcp_server_llama_stack_agent.py** -- MCP server exposing the finance agent as tools
- **test_mcp_client_langgraph_1.py** -- LangGraph client that uses the agent-as-tool
- **requirements.txt** -- Python dependencies

## Available Tools

### `finance_agent(prompt)`

Execute the finance agent with a natural language prompt. Returns the agent's text response.

### `finance_agent_detailed(prompt)`

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
   - Finance API (port 8082)
   - Finance MCP server (port 9002)

## Usage

### Start the MCP Server

```bash
python mcp_server_llama_stack_agent.py
```

The server runs on the port defined by `FINANCE_AGENT_PORT` in `.env` (default: 8002).

### Test with the LangGraph Client

```bash
python test_mcp_client_langgraph_1.py
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LLAMA_STACK_BASE_URL` | Llama Stack server URL | `http://localhost:8321` |
| `INFERENCE_MODEL` | LLM model identifier | -- |
| `MCP_FINANCE_SERVER_URL` | Finance MCP endpoint | `http://localhost:9002/mcp` |
| `FINANCE_AGENT_PORT` | Port for this agent server | `8002` |
