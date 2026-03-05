1. Deploy the NovaCrest microservices and DB
```bash
helm install novacrest-app ./novacrest-app
```
2. Deploy NovaCrest MCP servers to access microservices APIs
```bash
helm install novacrest-mcp ./novacrest-mcp
```
3. Deploy Langgraph agent
```bash
helm install novacrest-agent ./novacrest-agent
```
