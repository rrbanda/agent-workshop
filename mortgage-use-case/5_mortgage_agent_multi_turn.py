#!/usr/bin/env python3
"""
Step 5: Multi-turn mortgage agent session.

Demonstrates conversation memory across multiple turns -- the agent remembers
context from earlier turns to resolve references like "that application" or
"remaining conditions." Same pattern as Module 05, now with RAG so the agent
looks up policy rules (like the 60-day bank statement requirement) from the
lending policy document.

Turn 1: Check the outstanding conditions for application 1
Turn 2: What documents have been submitted for that same application?
Turn 3: A borrower uploaded a new bank statement -- check the policy and advise
Turn 4: Notify the borrower about remaining missing documents

Prerequisites:
    - Run 1_create_vector_store.py first
    - Llama Stack server, Mortgage API, and Mortgage MCP all running
"""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

sys.path.insert(0, os.path.dirname(__file__))
from mortgage_client_tools import ALL_TOOLS, ChatCompletionAgent

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL")
if not LLAMA_STACK_BASE_URL:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL")

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

# Find the mortgage policy vector store for RAG
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

agent = ChatCompletionAgent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at ACME Financial Services. "
        "You manage the conditional approval process -- reviewing applications, "
        "checking documents against policy, and communicating with borrowers. "
        "Use the function tools to access application data and take actions. "
        "Use file_search to look up ACME's lending policy for document "
        "requirements, acceptance criteria, and underwriting rules. "
        "Keep responses concise -- use short bullet points, not large tables."
    ),
    tools=ALL_TOOLS + [
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id],
        },
    ],
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
        "Check the lending policy for bank statement recency requirements. "
        "Does this new statement meet the policy criteria? "
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

    try:
        response = agent.create_turn(
            messages=[{"role": "user", "content": turn}],
            session_id=session_id,
            stream=False,
        )
        print_response(response)
    except Exception as e:
        print(f"[Turn {i} error: {e} -- continuing to next turn]")

    print("\n" + "=" * 60)
