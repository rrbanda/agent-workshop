#!/usr/bin/env python3
"""
Step 4c: End-to-end conditional approval workflow.

Demonstrates the full conditional approval loop from the mortgage process
flow diagram in a single multi-turn session:

Turn 1: Review conditions, documents, and credit -- full status check
Turn 2: Review unreviewed documents against policy, accept/reject
Turn 3: Final assessment and borrower notification

This script ties together tools, RAG, and multi-turn reasoning into
the complete "Conditional Loop" workflow that the diagram identifies
as the key area for AI agent automation.

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
        "You are a senior mortgage underwriting agent at NovaCrest Financial Services. "
        "You manage the full conditional approval workflow: reviewing conditions, "
        "validating documents against policy, assessing credit, and deciding next steps.\n\n"
        "When processing an application through the conditional approval loop:\n"
        "1. Check all conditions and their statuses\n"
        "2. For each condition, check if a matching document has been uploaded\n"
        "3. For uploaded documents, look up the policy acceptance criteria using file_search "
        "and validate the document against those criteria\n"
        "4. Accept or reject documents using review_document, with clear reasons\n"
        "5. Update satisfied conditions using update_condition_status\n"
        "6. After reviewing everything, assess whether the application can move to "
        "'clear to close' or what remains outstanding\n"
        "7. Notify the borrower of the outcome and any remaining action items\n\n"
        "Be thorough but concise. Use short bullet points, not large tables. "
        "Cite specific policy rules when making decisions."
    ),
    tools=ALL_TOOLS + [
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id],
        },
    ],
)

session_id = agent.create_session(session_name="e2e-workflow")


def print_response(response):
    """Extract and print text and tool calls from the agent response."""
    has_text = False
    for output in response.output:
        if hasattr(output, "content"):
            for content in output.content:
                if hasattr(content, "text"):
                    print(content.text)
                    has_text = True
        if hasattr(output, "tool_name"):
            print(f"  [Tool: {output.tool_name}]")
    if not has_text:
        print("  [Agent completed with tool calls but no text summary]")


turns = [
    (
        "Review mortgage application 1. List all conditions, their statuses, "
        "and whether a matching document has been uploaded. Also pull the "
        "credit reports and check if the applicant meets the policy's credit "
        "score and DTI requirements for this loan type. Keep it brief."
    ),
    (
        "Review each uploaded-but-unreviewed document against the lending "
        "policy. Accept or reject each one and update satisfied conditions."
    ),
    (
        "Send a notification to borrower AROUT listing the remaining missing "
        "documents. Then give your final assessment: can this application "
        "move to clear-to-close, or what must happen first?"
    ),
]

for i, turn in enumerate(turns, 1):
    print(f"\n[Turn {i}] User: {turn}")
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
