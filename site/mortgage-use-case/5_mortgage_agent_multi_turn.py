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
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from mortgage_client_tools import ALL_TOOLS

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL", "http://localhost:8321")
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

print(f"Model: {INFERENCE_MODEL}")
print("=" * 60)

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at ACME Financial Services. "
        "You manage the conditional approval process -- reviewing applications, "
        "checking documents against policy, and communicating with borrowers.\n\n"
        "Use file_search to look up lending policy requirements. "
        "Use function tools to access application data and take actions."
    ),
    tools=ALL_TOOLS,
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
