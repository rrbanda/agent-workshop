#!/usr/bin/env python3
"""
Step 4b: Mortgage agent that performs a credit-based underwriting review.

The agent retrieves an application's details and credit reports, looks up
the policy requirements for that loan type (min credit score, max DTI,
down payment), and makes a preliminary approval or denial recommendation
with reasoning.

This demonstrates the "analyzes assets, makes a decision" workflow
from the mortgage approval flow diagram.

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

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL")
if not LLAMA_STACK_BASE_URL:
    print("Error: LLAMA_STACK_BASE_URL not set. Copy .env.example to .env and configure it.")
    sys.exit(1)
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
        "You are a mortgage underwriting analyst at NovaCrest Financial Services. "
        "Your job is to perform credit-based underwriting reviews.\n\n"
        "When reviewing an application:\n"
        "1. Use get_mortgage_application to retrieve the application details "
        "(loan type, loan amount, credit score, annual income, DTI ratio)\n"
        "2. Use get_credit_report to pull credit reports from all bureaus\n"
        "3. Use file_search to look up the NovaCrest lending policy requirements "
        "for that specific loan type (minimum credit score, maximum DTI, "
        "down payment requirements, any special conditions)\n"
        "4. Compare the applicant's financials against each policy requirement\n"
        "5. Provide a structured recommendation: APPROVE, CONDITIONAL APPROVE, "
        "or DENY with detailed reasoning for each criterion\n\n"
        "Always cite specific numbers from both the application and the policy. "
        "Flag any borderline cases where the applicant is close to a threshold."
    ),
    tools=ALL_TOOLS + [
        {
            "type": "file_search",
            "vector_store_ids": [vector_store.id],
        },
    ],
)

session_id = agent.create_session(session_name="credit-review")

# Review application 1 (AROUT -- Conventional, credit 715, DTI 38.5%)
query1 = (
    "Perform a credit-based underwriting review for mortgage application 1. "
    "Retrieve the application details and credit reports, look up the policy "
    "requirements for that loan type, and provide your recommendation."
)

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

# Review application 4 (FRANR -- Jumbo, credit 580, DTI 52%, DENIED)
query2 = (
    "Now review mortgage application 4. Same process: retrieve the details "
    "and credit reports, check the policy, and explain why this application "
    "should be approved or denied."
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
