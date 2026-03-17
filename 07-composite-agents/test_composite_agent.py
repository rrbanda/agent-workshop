"""Test the composite agent MCP servers by calling them via the Responses API."""

import os
import sys
import logging
from dotenv import load_dotenv, find_dotenv
from llama_stack_client import LlamaStackClient

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv(find_dotenv(usecwd=True))

base_url = os.getenv("LLAMA_STACK_BASE_URL")
if not base_url:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)

INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "vllm-inference/gpt-oss-120b")
CUSTOMER_AGENT_URL = os.getenv("CUSTOMER_AGENT_URL", "http://localhost:8001/mcp")
FINANCE_AGENT_URL = os.getenv("FINANCE_AGENT_URL", "http://localhost:8002/mcp")

print(f"Base URL:       {base_url}")
print(f"Model:          {INFERENCE_MODEL}")
print(f"Customer Agent: {CUSTOMER_AGENT_URL}")
print(f"Finance Agent:  {FINANCE_AGENT_URL}")
print("=" * 60)

client = LlamaStackClient(base_url=base_url)

print("\n--- Test 1: Customer Agent ---")
print("Query: Find customer with contact email thomashardy@example.com\n")

response = client.responses.create(
    model=INFERENCE_MODEL,
    input="Find customer with contact email thomashardy@example.com",
    tools=[
        {
            "type": "mcp",
            "server_url": CUSTOMER_AGENT_URL,
            "server_label": "customer_agent",
        }
    ],
)
print(response.output_text)

print("\n--- Test 2: Finance Agent ---")
print("Query: Get order history for customer AROUT\n")

response = client.responses.create(
    model=INFERENCE_MODEL,
    input="Get order history for customer AROUT",
    tools=[
        {
            "type": "mcp",
            "server_url": FINANCE_AGENT_URL,
            "server_label": "finance_agent",
        }
    ],
)
print(response.output_text)

print("\n--- Test 3: Both Agents (Orchestration) ---")
print("Query: Find the customer with email thomashardy@example.com and get their orders\n")

response = client.responses.create(
    model=INFERENCE_MODEL,
    input="Find the customer with email thomashardy@example.com and get their orders",
    tools=[
        {
            "type": "mcp",
            "server_url": CUSTOMER_AGENT_URL,
            "server_label": "customer_agent",
        },
        {
            "type": "mcp",
            "server_url": FINANCE_AGENT_URL,
            "server_label": "finance_agent",
        },
    ],
)
print(response.output_text)
