# Module 03: Llama Stack Basics

## Learning Objectives

- Create a basic Llama Stack agent (hello world)
- Understand streaming vs non-streaming responses
- Inspect registered toolgroups and tools
- Learn the key Llama Stack SDK classes: `LlamaStackClient`, `Agent`, `Client`

## Prerequisites

- [Module 00: Environment Setup](../00-setup/) completed
- Llama Stack server running

## Concepts

**Llama Stack** is Meta's open-source platform for building AI applications. The `Agent` class provides a high-level API for creating agents with tools, while `Client` provides low-level access to individual Llama Stack APIs (models, tools, safety, etc.).

## Scripts

| Script | What It Does |
|--------|--------------|
| `1_hello_world_agent_no_stream.py` | Create an agent and get a single response |
| `1_hello_world_agent_streaming.py` | Same agent with streaming response events |
| `2_list_tools.py` | List all registered toolgroups |
| `3_list_customer_tools.py` | Inspect customer MCP tools in detail |
| `3_list_finance_tools.py` | Inspect finance MCP tools in detail |

## Step-by-Step

### 1. Run Hello World (Non-Streaming)

```bash
python 1_hello_world_agent_no_stream.py
```

This creates an agent, opens a session, and sends a single message.

### 2. Run Hello World (Streaming)

```bash
python 1_hello_world_agent_streaming.py
```

Observe the difference: events stream in real-time via `AgentEventLogger`.

### 3. List Registered Tools

```bash
python 2_list_tools.py
python 3_list_customer_tools.py
python 3_list_finance_tools.py
```

## Verification

All scripts should run without errors and produce meaningful output.

## Key Takeaways

- `LlamaStackClient` is the low-level client; `Agent` is the high-level agent wrapper
- Agents use sessions (`create_session`) and turns (`create_turn`) to manage conversations
- Streaming responses provide real-time feedback via event logging
- Tools must be registered with Llama Stack before agents can use them

## Next Module

Proceed to [04-agents-with-tools](../04-agents-with-tools/) to give your agents real tools to call.
