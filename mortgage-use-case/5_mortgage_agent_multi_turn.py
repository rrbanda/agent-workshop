#!/usr/bin/env python3
"""
Step 5: Multi-turn mortgage agent session.

Demonstrates conversation memory across multiple turns -- the agent remembers
context from earlier turns to resolve references like "that application" or
"remaining conditions." Same pattern as Module 05.

Turn 1: Review the conditional approval status for application 1
Turn 2: A borrower uploaded a new bank statement -- review it
Turn 3: Notify the borrower about remaining missing documents

Prerequisites:
    - Run 1_create_vector_store.py first
    - Llama Stack server, Mortgage API, and Mortgage MCP all running
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

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

# Find vector store
vector_stores = list(client.vector_stores.list())
matching = [vs for vs in vector_stores if vs.name == "mortgage-lending-policy"]
if not matching:
    print("ERROR: Vector store 'mortgage-lending-policy' not found.")
    print("Please run 1_create_vector_store.py first.")
    exit(1)

vector_store = max(matching, key=lambda vs: vs.created_at)
print(f"Model: {INFERENCE_MODEL}")
print(f"Vector store: {vector_store.id}")
print("=" * 60)

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at NovaCrest Financial Services. "
        "You manage the conditional approval process -- reviewing applications, "
        "checking documents against policy, and communicating with borrowers.\n\n"
        "Use file_search to look up lending policy requirements. "
        "Use MCP tools to access application data and take actions."
    ),
    tools=[
        {
            "type": "mcp",
            "server_url": MORTGAGE_MCP_SERVER_URL,
            "server_label": "mortgage",
        },
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id],
        },
    ],
)

session_id = agent.create_session(session_name="multi-turn-mortgage")

# --- Turn 1 ---
turn1 = (
    "Review the conditional approval status for mortgage application 1. "
    "List all outstanding conditions and what documents have been submitted so far."
)
print(f"[Turn 1] User: {turn1}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": turn1}],
    session_id=session_id,
    stream=True,
)
for log in AgentEventLogger().log(response):
    print(log, end="")

print("\n" + "=" * 60)

# --- Turn 2 ---
turn2 = (
    "The borrower just uploaded a new bank statement dated February 2026. "
    "According to our lending policy, does this meet the 60-day requirement? "
    "If so, what should we do about the bank statement condition?"
)
print(f"[Turn 2] User: {turn2}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": turn2}],
    session_id=session_id,
    stream=True,
)
for log in AgentEventLogger().log(response):
    print(log, end="")

print("\n" + "=" * 60)

# --- Turn 3 ---
turn3 = (
    "Now send a notification to the borrower listing the remaining missing "
    "documents they still need to provide to complete their application."
)
print(f"[Turn 3] User: {turn3}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": turn3}],
    session_id=session_id,
    stream=True,
)
for log in AgentEventLogger().log(response):
    print(log, end="")

print()
