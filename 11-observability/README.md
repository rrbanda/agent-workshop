# Module 11: Observability with Langfuse

> [!IMPORTANT]
> **This module is standalone and optional.** It uses LangGraph (not Llama Stack) for agent orchestration and requires additional dependencies (`pip install -r backend/requirements.txt`). It is not part of the core workshop path and is not required for the capstone. The observability patterns demonstrated here (tracing, scoring, feedback) apply to any agent framework.

## Learning Objectives

- Integrate Langfuse tracing with agents
- Trace LLM calls, tool invocations, and agent responses
- Run automated evaluations with substring scoring
- Collect and review user feedback

## Prerequisites

- [Module 04: Agents with Tools](../04-agents-with-tools/) completed
- [Module 02: MCP Servers](../02-mcp-servers/) running (ports 9001, 9002)
- Backend APIs running (ports 8081, 8082)
- LangGraph and Langfuse Python packages installed (`pip install -r backend/requirements.txt`)

## Architecture

```text
User --> FastAPI Chatbot --> LangGraph + MCP Tools
              |
              +--> Langfuse (traces, scores, feedback)
```

## Step-by-Step

> [!NOTE]
> **Working directory:** Backend commands run from `11-observability/backend/`. Frontend is at `11-observability/frontend/`.
>
> **Services needed:** Llama Stack, Customer MCP (9001), Finance MCP (9002), Langfuse.

### 1. Set Up Langfuse

You need a running Langfuse instance. The quickest way is Docker:

```bash
# Clone and start Langfuse locally
git clone https://github.com/langfuse/langfuse.git
cd langfuse
docker compose up -d
```

Langfuse will be available at http://localhost:3000. Create an account, then:

1. Go to **Settings > API Keys**
2. Click **Create new API key**
3. Copy the **Secret Key** and **Public Key**

Alternatively, sign up at https://cloud.langfuse.com for a hosted instance.

See [Langfuse self-hosting docs](https://langfuse.com/docs/deployment/self-host) for more options.

### 2. Configure Environment

Set these in your `.env`:

```text
LANGFUSE_SECRET_KEY=sk-lf-...   # from step 1
LANGFUSE_PUBLIC_KEY=pk-lf-...   # from step 1
LANGFUSE_HOST=http://localhost:3000
```

### 3. Run the Chatbot with Tracing

```bash
cd backend
pip install -r requirements.txt
python 6-langgraph-langfuse-fastapi-chatbot.py
```

### 4. Open the Chat UI

From the `11-observability` directory, open `frontend/index.html` in your browser.

### 5. View Traces in Langfuse

Navigate to your Langfuse dashboard to see traces of every request.

## Concepts Applied

- **From Module 04**: Agent tool binding patterns
- **New**: Langfuse `CallbackHandler`, trace viewing, automated evaluation, user feedback

## Troubleshooting

| Problem | Solution |
|---------|----------|
| No traces in Langfuse | Verify `LANGFUSE_SECRET_KEY`, `LANGFUSE_PUBLIC_KEY`, and `LANGFUSE_HOST` are set correctly |
| "Connection refused" on Langfuse | Ensure the Langfuse Docker container is running (`docker compose up -d`) |
| Chat UI can't connect | Check that the FastAPI backend is running and the port matches |
| Import errors | Run `pip install -r requirements.txt` from the `backend/` directory |

## Key Takeaways

- Langfuse provides production-grade observability for LLM applications
- The `CallbackHandler` integrates with LangChain/LangGraph with minimal code
- Automated evaluations help catch regressions before users see them
- User feedback (thumbs up/down) creates a continuous improvement loop

## Next Module

Proceed to [12-low-code](../12-low-code/) for visual agent building with Langflow.
