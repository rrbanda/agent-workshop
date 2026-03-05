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
| `1_multi_turn_agent.py` | Two scripted turns showing context carryover |
| `2_hitl_agent.py` | Interactive loop where you chat with the agent |

## Step-by-Step

### 1. Multi-Turn Conversation

```bash
python 1_multi_turn_agent.py
```

- **Turn 1**: "Who does Thomas Hardy work for?" -- agent searches customers
- **Turn 2**: "What are their orders?" -- agent uses context from Turn 1 to look up orders

### 2. Human-in-the-Loop

```bash
python 2_hitl_agent.py
```

Type questions interactively. The agent remembers the full conversation. Type `exit` to quit.

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

## Next Module

Choose your path:
- [06-langgraph-agents](../06-langgraph-agents/) -- Try the same patterns with LangGraph
- [07-composite-agents](../07-composite-agents/) -- Build agent-as-tool architectures
