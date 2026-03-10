#!/usr/bin/env python3
"""
Step 6: Interactive human-in-the-loop mortgage agent.

You act as the underwriter, guiding the agent through the conditional approval
process. The agent has access to all mortgage tools and the lending policy --
you drive the conversation.

Try these interactions:
  - "Show me the conditions for application 1"
  - "What does our policy say about bank statement requirements?"
  - "Review document 2 and tell me if it should be accepted"
  - "Reject that document and notify the borrower"
  - "Pull the credit report for customer AROUT"
  - "What's the DTI limit for a conventional loan?"

Type 'quit' or 'exit' to end the session.

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

print("=" * 60)
print("NovaCrest Mortgage Underwriting Agent (HITL)")
print(f"Model: {INFERENCE_MODEL}")
print(f"Policy vector store: {vector_store.id}")
print("=" * 60)
print()
print("You are the underwriter. Guide the agent through the")
print("conditional approval process for mortgage applications.")
print("Type 'quit' or 'exit' to end.")
print()

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at NovaCrest Financial Services. "
        "You help underwriters manage the conditional approval process.\n\n"
        "Capabilities:\n"
        "- Look up mortgage applications, documents, and conditions via MCP tools\n"
        "- Look up lending policy requirements via file_search\n"
        "- Review documents (accept/reject) and update condition statuses\n"
        "- Send notifications to borrowers\n"
        "- Pull credit reports\n\n"
        "Always be precise and reference specific document numbers, condition numbers, "
        "and policy sections when applicable."
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

session_id = agent.create_session(session_name="hitl-mortgage")

while True:
    try:
        user_input = input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break

    if not user_input:
        continue

    if user_input.lower() in ("quit", "exit", "q"):
        print("Goodbye!")
        break

    print("-" * 60)
    response = agent.create_turn(
        messages=[{"role": "user", "content": user_input}],
        session_id=session_id,
        stream=True,
    )
    for log in AgentEventLogger().log(response):
        print(log, end="")
    print()
