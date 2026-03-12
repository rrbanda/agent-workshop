# Module 05: Multi-Turn Conversations and Human-in-the-Loop

## Learning Objectives

- Build agents that maintain context across multiple conversation turns
- Implement an interactive human-in-the-loop (HITL) agent
- Understand session persistence in Llama Stack

> **Capstone Preview:** In the capstone, multi-turn sessions let the mortgage agent track an application across multiple interactions, and HITL lets you act as the underwriter.

## Prerequisites

- [Module 04: Agents with Tools](../04-agents-with-tools/) completed

## Concepts

In a **multi-turn conversation**, the agent maintains context across sequential exchanges within a session. Each call to `create_turn` adds to the session's message history, so the agent can resolve references like "their orders" or "that application" from previous turns. **Human-in-the-loop (HITL)** adds a human operator to the agent loop -- the operator can steer the agent, override decisions, or ask follow-up questions in real time, which is critical for high-stakes workflows like financial approvals.

## Scripts

| Script | What It Does |
|--------|--------------|
| `6_multi_turn_agent.py` | Two scripted turns showing context carryover |
| `7_hitl_agent.py` | Interactive loop where you chat with the agent |

## Step-by-Step

> **Working directory:** All commands in this module run from `05-multi-turn-and-hitl/`.
>
> **Services needed:** Llama Stack, Customer API (8081), Finance API (8082), Customer MCP (9001), Finance MCP (9002).

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

### Multi-Turn (script 6)

```
============================================================
Turn 1: who does Thomas Hardy work for?
============================================================
Thomas Hardy works for Around the Horn (customer ID: AROUT)...

============================================================
Turn 2: what are their orders?
============================================================
Around the Horn has the following orders: order #10355...
```

The agent uses context from Turn 1 (customer ID AROUT) to look up orders in Turn 2. Only the final text is printed.

### Human-in-the-Loop (script 7)

```
============================================================
Human-in-the-Loop Agent
Type 'exit' or 'quit' to end the conversation
============================================================

You: Who is the contact for LONEP?
[Turn 1]
Agent: The contact for Lonesome Pine Restaurant is Fran Wilson...

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
