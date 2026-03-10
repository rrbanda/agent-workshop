# Module 05: Multi-Turn Conversations and Human-in-the-Loop

## Learning Objectives

- Build agents that maintain context across multiple conversation turns
- Implement an interactive human-in-the-loop (HITL) agent
- Understand session persistence in Llama Stack

## Prerequisites

- [Module 04: Agents with Tools](../04-agents-with-tools/) completed

## Scripts

| Script | What It Does |
|--------|--------------|
| `6_multi_turn_agent.py` | Two scripted turns showing context carryover |
| `7_hitl_agent.py` | Interactive loop where you chat with the agent |

## Step-by-Step

### 1. Multi-Turn Conversation

```bash
python 6_multi_turn_agent.py
```

- **Turn 1**: "Who does Thomas Hardy work for?" -- agent searches customers
- **Turn 2**: "What are their orders?" -- agent uses context from Turn 1 to look up orders

### 2. Human-in-the-Loop

```bash
python 7_hitl_agent.py
```

Type questions interactively. The agent remembers the full conversation. Type `exit` to quit.

## What You Should See

### Multi-Turn

```
--- Turn 1 ---
User: Who does Thomas Hardy work for?
inference> [tool_call] search_customers(...)
inference> Thomas Hardy works for Around the Horn.

--- Turn 2 ---
User: What are their orders?
inference> [tool_call] fetch_order_history({"customer_id": "AROUT"})
inference> Around the Horn has the following orders: ...
```

### Human-in-the-Loop

```
You: Who is the contact for LONEP?
Agent> [tool_call] search_customers(...)
Agent> The contact for Lonesome Pine Restaurant is Fran Wilson.
You: exit
Goodbye!
```

## How It Works

Both turns use the same `session_id`, which preserves conversation history:

```python
session_id = agent.create_session(session_name="multi_turn_session")

# Turn 1
agent.create_turn(session_id=session_id, messages=[{"role": "user", "content": "..."}])

# Turn 2 -- agent remembers Turn 1
agent.create_turn(session_id=session_id, messages=[{"role": "user", "content": "..."}])
```

## Key Takeaways

- Session IDs enable multi-turn conversations with persistent context
- The agent resolves pronouns ("their orders") using conversation history
- HITL agents allow real-time human oversight and guidance
- Each `create_turn` call adds to the session's message history

## Concepts Applied

- **From Module 04**: Tool binding with MCP servers
- **From Module 03**: `create_session` for session persistence, `AgentEventLogger` for streaming

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Agent loses context between turns | Verify you're reusing the same `session_id` |
| HITL agent exits immediately | Make sure you type a question, not just press Enter |
| "No tools found" | Ensure MCP servers are running (ports 9001, 9002) |

## Next Module

Choose your path:
- [06-langgraph-agents](../06-langgraph-agents/) -- Try the same patterns with LangGraph
- [07-composite-agents](../07-composite-agents/) -- Build agent-as-tool architectures
