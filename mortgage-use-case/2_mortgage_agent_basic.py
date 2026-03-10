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
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL", "http://localhost:8321")
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")
MORTGAGE_MCP_SERVER_URL = os.getenv("MORTGAGE_MCP_SERVER_URL", "http://localhost:9003/mcp")

print(f"Model: {INFERENCE_MODEL}")
print(f"Mortgage MCP: {MORTGAGE_MCP_SERVER_URL}")
print("=" * 60)

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at NovaCrest Financial Services. "
        "You can look up mortgage applications, review submitted documents, check "
        "conditions, and retrieve credit reports using the available tools. "
        "Always provide clear, specific information about application status and "
        "outstanding requirements."
    ),
    tools=[
        {
            "type": "mcp",
            "server_url": MORTGAGE_MCP_SERVER_URL,
            "server_label": "mortgage",
        },
    ],
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
