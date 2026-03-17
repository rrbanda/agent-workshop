"""List all registered MCP toolgroups/servers in Llama Stack."""

from llama_stack_client import Client
from dotenv import load_dotenv
import os
import sys
import logging

load_dotenv()

# Suppress noisy httpx logging
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

BASE_URL = os.getenv("LLAMA_STACK_BASE_URL")
if not BASE_URL:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)

client = Client(
    base_url=BASE_URL,
)


def list_mcp_servers():
    """List all registered MCP servers"""
    print("=" * 50)
    print("Registered Toolgroups")
    print("=" * 50)

    toolgroups = client.toolgroups.list()

    for tg in toolgroups:
        print(f"\nToolgroup ID:  {tg.identifier}")
        print(f"Provider ID:   {tg.provider_id}")
        if hasattr(tg, 'mcp_endpoint') and tg.mcp_endpoint:
            uri = tg.mcp_endpoint.get('uri') if isinstance(tg.mcp_endpoint, dict) else getattr(tg.mcp_endpoint, 'uri', None)
            print(f"MCP Endpoint:  {uri}")
        print("-" * 50)

    print(f"\nTotal toolgroups: {len(toolgroups)}")
    print("=" * 50)
    return toolgroups


if __name__ == "__main__":
    list_mcp_servers()
