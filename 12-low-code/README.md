# Module 12: Low-Code Agent Building with Langflow

## Learning Objectives

- Build agents visually using Langflow's drag-and-drop interface
- Create custom LLM components for vLLM/MaaS endpoints
- Connect MCP tools to agents through the Langflow UI
- Deploy Langflow on OpenShift

## Prerequisites

- [Module 02: MCP Servers](../02-mcp-servers/) running
- Langflow installed (`pip install langflow==1.7.1`)

## Step-by-Step

### 1. Start Langflow

```bash
langflow run --port 7860
```

### 2. Import the NovaCrest Agent Flow

Import `flows/novacrest-agent-flow.json` through the Langflow UI.

### 3. Configure MCP Tool URLs

Update the MCP Tools components in the flow to point to your MCP server URLs:

- **Customer MCP**: `http://localhost:9001/mcp` (or `CUSTOMER_MCP_SERVER_URL` from your `.env`)
- **Finance MCP**: `http://localhost:9002/mcp` (or `FINANCE_MCP_SERVER_URL` from your `.env`)

For LLM configuration, set the vLLM/Llama Stack endpoint:
- **API Base URL**: `http://localhost:8321/v1` (or `LLAMA_STACK_BASE_URL` from your `.env` + `/v1`)
- **Model Name**: Same as your `INFERENCE_MODEL` value
- **API Key**: Same as your `API_KEY` value (default: `fake`)

### 4. Test the Flow

Use the built-in chat to ask questions about NovaCrest customers and orders.

## Key Takeaways

- Langflow enables non-developers to build agent workflows visually
- Custom components extend Langflow with new LLM providers (vLLM, MaaS)
- MCP tools work seamlessly in visual flows just like they do in code
- Langflow can be deployed on OpenShift for team collaboration

## Next Module

Proceed to [13-deployment](../13-deployment/) for production deployment.
