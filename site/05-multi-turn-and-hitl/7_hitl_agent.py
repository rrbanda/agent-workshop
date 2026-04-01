"""Human-in-the-loop agent with interactive CLI for conversational queries."""

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
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "vllm-inference/gpt-oss-120b")
CUSTOMER_MCP_SERVER_URL = os.getenv("CUSTOMER_MCP_SERVER_URL")
FINANCE_MCP_SERVER_URL = os.getenv("FINANCE_MCP_SERVER_URL")

print(f"Base URL:     {LLAMA_STACK_BASE_URL}")
print(f"Model:        {INFERENCE_MODEL}")
print(f"Customer MCP: {CUSTOMER_MCP_SERVER_URL}")
print(f"Finance MCP:  {FINANCE_MCP_SERVER_URL}")
print()

from urllib.parse import urlparse
_ls = urlparse(LLAMA_STACK_BASE_URL)
for _label, _url in [("CUSTOMER_MCP_SERVER_URL", CUSTOMER_MCP_SERVER_URL), ("FINANCE_MCP_SERVER_URL", FINANCE_MCP_SERVER_URL)]:
    if _url:
        _mcp = urlparse(_url)
        if _ls.hostname not in ("localhost", "127.0.0.1") and _mcp.hostname in ("localhost", "127.0.0.1"):
            print(f"ERROR: Llama Stack is remote but {_label} is on localhost.")
            print("The remote Llama Stack server cannot reach localhost on your machine.")
            print(f"Fix: set {_label} to a remote URL that Llama Stack can reach,")
            print("     or run Llama Stack locally. See Module 00 'Deployment Scenarios'.")
            sys.exit(1)

# Initialize client
client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

# Configure MCP tools - both customer and finance servers
mcp_tools = [
    {
        "type": "mcp",
        "server_url": CUSTOMER_MCP_SERVER_URL,
        "server_label": "customer",
    },
    {
        "type": "mcp",
        "server_url": FINANCE_MCP_SERVER_URL,
        "server_label": "finance",
    }
]

# Create an agent with both MCP tools
agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions="You are a helpful assistant that can search for customer information and retrieve order/financial data using the available tools.",
    tools=mcp_tools,
)

# Create a session
session_id = agent.create_session(session_name="hitl_session")


def print_response(response):
    """Extract and print text from the response"""
    for output in response.output:
        if hasattr(output, 'content'):
            for content in output.content:
                if hasattr(content, 'text'):
                    print(content.text)


print("=" * 60)
print("Human-in-the-Loop Agent")
print("Type 'exit' or 'quit' to end the conversation")
print("=" * 60)
print()

# Interactive loop
turn_count = 0
while True:
    try:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ['exit', 'quit', 'q']:
            print("\nGoodbye!")
            break

        turn_count += 1
        print(f"\n[Turn {turn_count}]")

        response = agent.create_turn(
            session_id=session_id,
            messages=[{"role": "user", "content": user_input}],
            stream=False,
        )

        print("Agent: ", end="")
        print_response(response)
        print()

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        break
    except EOFError:
        print("\n\nGoodbye!")
        break
