# Helpers

Utility scripts for working with the Llama Stack server and testing features outside the main workshop modules.

## llama-stack-scripts/

Shell scripts and Python tests for directly interacting with the Llama Stack server:

| Script | Purpose |
|--------|---------|
| `1_setenv.sh` / `1_setenv_k8s.sh` | Set environment variables (local / Kubernetes) |
| `2_echoenv.sh` | Print current env var values |
| `3_available_models.sh` | List available models on the server |
| `4_available_apis.sh` | List available APIs |
| `5_chat_completions.sh` | Test chat completions endpoint |
| `6_responses_api.sh` | Test the responses API |
| `7_tool_groups.sh` / `7_tool_providers.sh` | List registered tool groups and providers |
| `8_list_mcp_tools.sh` | List MCP tools registered with Llama Stack |
| `9_customer_mcp_tools.sh` / `9_finance_mcp_tools.sh` | Test customer/finance MCP tools |
| `9_rag_tool.sh` | Test RAG toolgroup |
| `start_debug.sh` / `start_debug_detailed.sh` | Start Llama Stack with debug logging |
| `clean_slate.sh` | Reset Llama Stack state |
| `update-llamastack-langfuse.sh` | Update Langfuse integration config |
| `test_customer_mcp_direct.py` / `test_finance_mcp_direct.py` | Python scripts to test MCP servers directly |

## web-search/

Progressive examples demonstrating web search tool integration with Llama Stack:

| Script | Purpose |
|--------|---------|
| `1_list_tools.py` | List available tool groups (builtin web search) |
| `2_no_web_search*.py` | Ask questions without web search (shows knowledge cutoff) |
| `3_web_search*.py` | Same questions with web search enabled |
| `4_what_is_my_knowledge_cutoff.py` | Ask the model about its own knowledge cutoff |
| `5_web_search_*_today.py` | Real-time queries using web search |

> **Prerequisite:** Set `TAVILY_SEARCH_API_KEY` in your `.env` for web search scripts.
