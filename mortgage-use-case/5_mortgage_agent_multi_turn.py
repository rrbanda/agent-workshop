#!/usr/bin/env python3
"""
Step 5: Multi-turn mortgage agent session.

Demonstrates conversation memory across multiple turns -- the agent remembers
context from earlier turns to resolve references like "that application" or
"remaining conditions." Same pattern as Module 05.

Turn 1: Check the outstanding conditions for application 1
Turn 2: What documents have been submitted for that same application?
Turn 3: A borrower uploaded a new bank statement -- does it meet the 60-day rule?
Turn 4: Notify the borrower about remaining missing documents

Prerequisites:
    - Run 1_create_vector_store.py first
    - Llama Stack server, Mortgage API, and Mortgage MCP all running
"""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent

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
        "You are a mortgage underwriting assistant at NovaCrest Financial Services. "
        "You manage the conditional approval process -- reviewing applications, "
        "checking documents against policy, and communicating with borrowers. "
        "Use the available tools to access application data and take actions."
    ),
    tools=ALL_TOOLS,
)

session_id = agent.create_session(session_name="multi-turn-mortgage")


def print_response(response):
    """Extract and print text from the agent response."""
    for output in response.output:
        if hasattr(output, 'content'):
            for content in output.content:
                if hasattr(content, 'text'):
                    print(content.text)


turns = [
    (
        "What are the outstanding conditions for mortgage application 1?"
    ),
    (
        "What documents have been submitted for that same application?"
    ),
    (
        "The borrower just uploaded a new bank statement dated February 2026. "
        "Does this meet the 60-day requirement? "
        "If so, what should we do about the bank statement condition?"
    ),
    (
        "Send a notification to the borrower (customer AROUT) listing the "
        "remaining missing documents they still need to provide."
    ),
]

for i, turn in enumerate(turns, 1):
    print(f"[Turn {i}] User: {turn}")
    print("-" * 60)

    response = agent.create_turn(
        messages=[{"role": "user", "content": turn}],
        session_id=session_id,
        stream=False,
    )
    print_response(response)

    print("\n" + "=" * 60)
