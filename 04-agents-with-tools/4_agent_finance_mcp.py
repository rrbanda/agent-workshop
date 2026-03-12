"""Agent with finance MCP tools that retrieves orders and financial data for customers."""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent

# Suppress httpx and llama_stack_client INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

# Load environment variables
load_dotenv()

# Get configuration from environment
base_url = os.getenv("LLAMA_STACK_BASE_URL")
if not base_url:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)
LLAMA_STACK_BASE_URL = base_url
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "vllm/qwen3-14b")
FINANCE_MCP_SERVER_URL = os.getenv("FINANCE_MCP_SERVER_URL")
if not FINANCE_MCP_SERVER_URL:
    print("Error: FINANCE_MCP_SERVER_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)

print(f"Base URL:    {LLAMA_STACK_BASE_URL}")
print(f"Model:       {INFERENCE_MODEL}")
print(f"Finance MCP: {FINANCE_MCP_SERVER_URL}")

# Initialize client
client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

# Configure MCP tools
mcp_tools = [
    {
        "type": "mcp",
        "server_url": FINANCE_MCP_SERVER_URL,
        "server_label": "finance",
    }
]

# Create an agent with MCP tools
agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions="You are a helpful assistant that can retrieve order and financial information using the available tools.",
    tools=mcp_tools,
)

# Create a session
session_id = agent.create_session(session_name="finance_search_session")

# Create a turn to get orders for customer AROUT
response = agent.create_turn(
    session_id=session_id,
    messages=[{"role": "user", "content": "get me the orders for AROUT"}],
    stream=False,
)

# Print the response - extract text from the final message
for output in response.output:
    if hasattr(output, 'content'):
        for content in output.content:
            if hasattr(content, 'text'):
                print(content.text)
