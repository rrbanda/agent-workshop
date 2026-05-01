#!/usr/bin/env python3
"""
Step 4: Mortgage agent that reviews a document upload.

This script demonstrates the core conditional approval loop from the workshop:
1. Agent checks the policy for document acceptance criteria (RAG)
2. Agent reviews a specific uploaded document against those criteria (MCP tools)
3. Agent accepts or rejects the document (MCP tool: review_document)
4. If accepted, agent marks the condition as satisfied (MCP tool: update_condition_status)
5. Agent notifies the borrower of the outcome (MCP tool: send_notification)

Prerequisites:
    - Run 1_create_vector_store.py first
    - Llama Stack server, Mortgage API, and Mortgage MCP all running
"""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, AgentEventLogger

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

# Find the mortgage policy vector store
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
        "You are a mortgage document review agent at ACME Financial Services. "
        "Your job is to review documents submitted by borrowers and determine if they "
        "meet ACME's acceptance criteria.\n\n"
        "When reviewing a document:\n"
        "1. Use file_search to look up the acceptance criteria for that document type "
        "in the ACME lending policy\n"
        "2. Use get_application_documents to see the document's metadata (dates, type, description)\n"
        "3. Compare the document against the policy criteria\n"
        "4. Call review_document to ACCEPT or REJECT with a clear reason\n"
        "5. If accepted and it satisfies a condition, call update_condition_status to mark it SATISFIED\n"
        "6. Call send_notification to inform the borrower of the outcome\n\n"
        "Be specific in rejection reasons so the borrower knows exactly what to fix."
    ),
    tools=ALL_TOOLS + [
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id],
        },
    ],
)

session_id = agent.create_session(session_name="doc-review")

# Scenario: Review the uploaded bank statement (DOC-002) for application 1.
# The agent should discover the document type, dates, and status from the API,
# then look up the lending policy for acceptance criteria, and reason autonomously.
query = (
    "Review document 2 for mortgage application 1. "
    "First, retrieve the document details and the application info. "
    "Then check the lending policy for the acceptance criteria for that document type. "
    "Based on the policy rules and the document's dates, accept or reject it. "
    "If you reject it, notify the borrower with the specific reason."
)

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
