# Module 11: Observability with Langfuse

## Learning Objectives

- Integrate Langfuse tracing with LangGraph agents
- Trace LLM calls, tool invocations, and agent responses
- Run automated evaluations with substring scoring
- Collect and review user feedback

## Prerequisites

- [Module 06: LangGraph Agents](../06-langgraph-agents/) completed
- Langfuse instance running (local Docker or hosted)

## Architecture

```
User --> FastAPI Chatbot --> LangGraph + MCP Tools
              |
              +--> Langfuse (traces, scores, feedback)
```

## Step-by-Step

### 1. Configure Langfuse

Set these in your `.env`:
```
LANGFUSE_SECRET_KEY=your-secret-key
LANGFUSE_PUBLIC_KEY=your-public-key
LANGFUSE_HOST=http://localhost:3000
```

### 2. Run the Chatbot with Tracing

```bash
cd backend
pip install -r requirements.txt
python 6-langgraph-langfuse-fastapi-chatbot.py
```

### 3. Open the Chat UI

Open `frontend/index.html` in your browser.

### 4. View Traces in Langfuse

Navigate to your Langfuse dashboard to see traces of every request.

## Key Takeaways

- Langfuse provides production-grade observability for LLM applications
- The `CallbackHandler` integrates with LangChain/LangGraph with minimal code
- Automated evaluations help catch regressions before users see them
- User feedback (thumbs up/down) creates a continuous improvement loop

## Next Module

Proceed to [12-low-code](../12-low-code/) for visual agent building with Langflow.
