# Module 00: Environment Setup

## Learning Objectives

- Install all required tools (Python, Java, Maven, Node.js, PostgreSQL, Docker)
- Configure and start a Llama Stack server
- Verify connectivity to all services

## Prerequisites

None -- this is the starting point.

## Tools Required

| Tool | Version | Purpose |
|------|---------|---------|
| Python | 3.12+ | Agent scripts, MCP servers |
| Java | 21+ | Backend Spring Boot APIs |
| Maven | 3.8+ | Java build tool |
| Node.js | 18+ | Chat UI (Module 06) |
| PostgreSQL | 15+ | Database for APIs |
| Docker | Latest | Containerization (Module 13) |

## Step-by-Step Setup

### 1. Python Environment

```bash
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 2. Llama Stack Server

**Option A: Local with Ollama**

```bash
# Install Ollama from https://ollama.com
ollama pull llama3.2:3b
uv run --with llama-stack llama stack run starter
```

**Option B: Remote vLLM endpoint**

Set `LLAMA_STACK_BASE_URL` in your `.env` to point to your vLLM/MaaS endpoint.

### 3. PostgreSQL Databases

```bash
createdb novacrest_customer
createdb novacrest_finance
```

### 4. Environment Variables

```bash
cp .env.example .env
# Edit .env with your configuration
```

## Verification

```bash
# Check Llama Stack
curl $LLAMA_STACK_BASE_URL/v1/models

# Check Python
python --version  # Should be 3.12+

# Check Java
java --version    # Should be 21+
mvn --version     # Should be 3.8+
```

## Key Takeaways

- All workshop modules share the same `.env` configuration
- Llama Stack provides a unified API for inference, agents, tools, RAG, safety, and evals
- The workshop uses NovaCrest (a fictional financial services company) as its example domain

## Next Module

Proceed to [01-backend-apis](../01-backend-apis/) to set up the NovaCrest backend services.
