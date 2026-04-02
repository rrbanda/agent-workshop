## Deployment

In this workshop, the Finance MCP server is built and deployed to OpenShift. See [Module 02 README](../README.md) for the full build-deploy workflow.

## Configuration

The server uses these environment variables (set via OpenShift deployment manifests or `.env`):

```env
FINANCE_API_BASE_URL=https://<finance-api-openshift-route>
PORT_FOR_FINANCE_MCP=9002
HOST_FOR_FINANCE_MCP=0.0.0.0
```

## Local Development (optional)

For local development and testing of the MCP server code itself:

```bash
pip install -r requirements.txt
python finance-api-mcp-server.py
```

## Testing with MCP Inspector

```bash
brew install mcp-inspector
mcp-inspector
```
