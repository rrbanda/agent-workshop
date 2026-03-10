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

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage document review agent at NovaCrest Financial Services. "
        "Your job is to review documents submitted by borrowers and determine if they "
        "meet NovaCrest's acceptance criteria.\n\n"
        "When reviewing a document:\n"
        "1. Use file_search to look up the acceptance criteria for that document type "
        "in the NovaCrest lending policy\n"
        "2. Use get_application_documents to see the document's metadata (dates, type, description)\n"
        "3. Compare the document against the policy criteria\n"
        "4. Call review_document to ACCEPT or REJECT with a clear reason\n"
        "5. If accepted and it satisfies a condition, call update_condition_status to mark it SATISFIED\n"
        "6. Call send_notification to inform the borrower of the outcome\n\n"
        "Be specific in rejection reasons so the borrower knows exactly what to fix."
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

session_id = agent.create_session(session_name="doc-review")

# Scenario: Review the uploaded bank statement (DOC-002) for application 1.
# This document is dated August 2025 — the policy requires statements within 60 days.
query = (
    "Review document 2 (DOC-002) for mortgage application 1. "
    "It is a bank statement uploaded on February 18, 2026. "
    "The statement is dated August 2025. "
    "Check the lending policy for bank statement acceptance criteria, "
    "then accept or reject the document accordingly. "
    "If you reject it, notify the borrower (customer AROUT) with the reason."
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
