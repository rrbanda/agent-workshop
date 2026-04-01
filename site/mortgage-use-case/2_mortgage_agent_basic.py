#!/usr/bin/env python3
"""
Step 2: Basic mortgage agent with MCP tools only (no RAG).

This agent can query mortgage applications, documents, conditions, and credit
reports through the Mortgage MCP server. It demonstrates tool calling -- the
same pattern from Module 04.

Prerequisites:
    - Llama Stack server running
    - Mortgage API running on port 8083
    - Mortgage MCP server running on port 9003
"""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from mortgage_client_tools import ALL_TOOLS

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL")
if not LLAMA_STACK_BASE_URL:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")

print(f"Model: {INFERENCE_MODEL}")
print("=" * 60)

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at ACME Financial Services. "
        "You can look up mortgage applications, review submitted documents, check "
        "conditions, and retrieve credit reports using the available tools. "
        "Always provide clear, specific information about application status and "
        "outstanding requirements."
    ),
    tools=ALL_TOOLS,
)

session_id = agent.create_session(session_name="mortgage-basic")

query = "What are the outstanding conditions for mortgage application 1?"
print(f"Query: {query}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": query}],
    session_id=session_id,
    stream=True,
)

for log in AgentEventLogger().log(response):
    print(log, end="")

print()
