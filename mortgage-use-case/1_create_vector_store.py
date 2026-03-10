#!/usr/bin/env python3
"""
Step 1: Create a vector store from the NovaCrest Mortgage Lending Policy document.

This script ingests the mortgage policy into a Llama Stack vector store with
hybrid search (BM25 keyword + semantic) so the mortgage agent can look up
document requirements, acceptance criteria, and underwriting rules.

Prerequisites:
    - Llama Stack server running
    - .env configured with LLAMA_STACK_BASE_URL, EMBEDDING_MODEL, EMBEDDING_DIMENSION
"""

import os
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL", "http://localhost:8321")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "granite-embedding-125m")
EMBEDDING_DIMENSION = int(os.getenv("EMBEDDING_DIMENSION", "768"))

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

print(f"Llama Stack URL: {LLAMA_STACK_BASE_URL}")
print(f"Embedding model: {EMBEDDING_MODEL}")
print(f"Embedding dimension: {EMBEDDING_DIMENSION}")
print("-" * 60)

# Create the vector store with hybrid search
print("Creating vector store 'mortgage-lending-policy'...")
vector_store = client.vector_stores.create(
    name="mortgage-lending-policy",
    embedding_model=EMBEDDING_MODEL,
    embedding_dimension=EMBEDDING_DIMENSION,
    config={
        "type": "on_demand",
        "search_mode": "hybrid",
        "bm25_weight": 0.5,
        "semantic_weight": 0.5,
    },
)
print(f"Vector store created: {vector_store.id}")

# Upload the mortgage policy document
policy_path = os.path.join(os.path.dirname(__file__), "source_docs", "MortgageLendingPolicy.txt")
print(f"Uploading policy document: {policy_path}")

with open(policy_path, "r") as f:
    content = f.read()
    print(f"Document size: {len(content)} characters")

file = client.files.create(
    purpose="file-search",
    file_path=policy_path,
)
print(f"File uploaded: {file.id}")

# Attach file to vector store with chunking
print("Ingesting document into vector store (chunking + embedding)...")
client.vector_stores.files.create(
    vector_store_id=vector_store.id,
    file_id=file.id,
    chunking_strategy={
        "type": "static",
        "static": {
            "max_chunk_size_tokens": 100,
            "chunk_overlap_tokens": 10,
        },
    },
)

print("-" * 60)
print("Vector store ready!")
print(f"  Store ID: {vector_store.id}")
print(f"  Name: mortgage-lending-policy")
print(f"  Search mode: hybrid (BM25 + semantic)")
print()
print("You can now use this vector store with the mortgage agent scripts.")
