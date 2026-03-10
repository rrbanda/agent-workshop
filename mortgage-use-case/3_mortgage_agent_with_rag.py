#!/usr/bin/env python3
"""
Step 3: Mortgage agent with MCP tools AND RAG on the lending policy.

This agent combines tool calling with file_search on the mortgage policy
vector store. It can cross-reference NovaCrest's lending policy (what documents
are required, acceptance criteria) with actual application data (what documents
have been submitted).

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
print(f"Mortgage MCP: {MORTGAGE_MCP_SERVER_URL}")
print("=" * 60)

agent = Agent(
    client,
    model=INFERENCE_MODEL,
    instructions=(
        "You are a mortgage underwriting assistant at NovaCrest Financial Services. "
        "You have access to two capabilities:\n"
        "1. MCP tools to look up mortgage applications, documents, conditions, and credit reports\n"
        "2. file_search to look up NovaCrest's mortgage lending policy for document "
        "requirements and acceptance criteria\n\n"
        "When asked about what documents are needed, ALWAYS use file_search to check "
        "the lending policy. When asked about a specific application, use the MCP tools "
        "to get the actual data, then cross-reference with the policy."
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

session_id = agent.create_session(session_name="mortgage-rag")

# Query 1: Policy lookup (RAG)
query1 = "What documents are required for a conventional loan according to NovaCrest policy?"
print(f"Query 1: {query1}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": query1}],
    session_id=session_id,
    stream=True,
)
for log in AgentEventLogger().log(response):
    print(log, end="")

print("\n" + "=" * 60)

# Query 2: Cross-reference policy with application data (RAG + MCP)
query2 = (
    "Application 1 is a conventional loan. Check what documents have been submitted "
    "and compare against the policy requirements. What is still missing or needs attention?"
)
print(f"Query 2: {query2}")
print("-" * 60)

response = agent.create_turn(
    messages=[{"role": "user", "content": query2}],
    session_id=session_id,
    stream=True,
)
for log in AgentEventLogger().log(response):
    print(log, end="")

print()
