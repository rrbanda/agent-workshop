# Module 13: Production Deployment

## Learning Objectives

- Containerize all workshop components with Docker
- Deploy the full stack with Helm charts on OpenShift/Kubernetes
- Configure Llama Stack server on Kubernetes
- Understand service wiring via Kubernetes DNS

## Prerequisites

- All previous modules completed
- Access to an OpenShift/Kubernetes cluster
- Helm 3 installed

## Helm Charts

| Chart | Components |
|-------|-----------|
| `novacrest-app` | Customer API + Finance API + PostgreSQL instances |
| `novacrest-mcp` | Customer MCP + Finance MCP servers |
| `novacrest-agent` | LangGraph FastAPI backend + Chat UI |

## Step-by-Step

### 1. Deploy Backend + Databases

```bash
helm install novacrest-app ./helm/novacrest-app
```

### 2. Deploy MCP Servers

```bash
helm install novacrest-mcp ./helm/novacrest-mcp
```

### 3. Deploy Agent + UI

```bash
helm install novacrest-agent ./helm/novacrest-agent
```

## Service Wiring

```
PostgreSQL (postgres-cust:5432)
       |
Customer API (novacrest-customer-service:8081)
       |
Customer MCP (mcp-customer-service:9001)  <-->  LangGraph FastAPI (langgraph-fastapi:8000)
                                                        |
Llama Stack (llamastack-distribution-vllm-service:8321)
                                                        |
Finance MCP (mcp-finance-service:9002)  <-->  LangGraph FastAPI
       |
Finance API (novacrest-finance-service:8082)
       |
PostgreSQL (postgres-fin:5432)

Chat UI (simple-agent-chat-ui:3000) --> langgraph-fastapi:8000
```

## Dockerfiles

Pre-built Dockerfiles are in `dockerfiles/`:

| File | Component |
|------|-----------|
| `Dockerfile.customer-api` | NovaCrest Customer API |
| `Dockerfile.finance-api` | NovaCrest Finance API |
| `Dockerfile.customer-mcp` | Customer MCP Server |
| `Dockerfile.finance-mcp` | Finance MCP Server |
| `Dockerfile.langgraph-fastapi` | LangGraph FastAPI Agent |
| `Dockerfile.chat-ui` | Chat UI |

## Key Takeaways

- Helm charts wire all services together via Kubernetes internal DNS
- Each layer (APIs, MCP, agents) deploys independently
- Llama Stack runs as a Kubernetes service with ConfigMap-based configuration
- The same MCP tools work in both local development and Kubernetes deployment
