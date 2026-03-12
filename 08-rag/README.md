# Module 08: RAG (Retrieval-Augmented Generation)

## Learning Objectives

- Create vector stores with hybrid search (BM25 + semantic)
- Upload and chunk documents for retrieval
- Use the `file_search` tool with Llama Stack agents
- Debug and optimize retrieval quality

## Prerequisites

- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed
- Llama Stack server running with an embedding model available

## Concepts

**RAG** augments LLM responses with relevant information retrieved from a document store. Llama Stack's vector stores support **hybrid search**, combining keyword matching (BM25) with semantic similarity for better retrieval.

## Scripts

| Script | What It Does |
|--------|--------------|
| `0_list_embedding_models.py` | List available embedding models |
| `1_create_vector_store.py` | Create a vector store and ingest HR benefits document |
| `2_list_available_vector_stores.py` | List all vector stores |
| `3_test_rag_hr_benefits.py` | Test RAG with "What do I receive when I retire?" |
| `4_debug_vector_search.py` | Debug retrieval with direct vector search |
| `5_test_gold_watch.py` | Test "When do I get my gold watch?" |
| `6_test_unique_terms.py` | Test with multiple unique-term queries |
| `7_delete_vector_store.py` | Clean up vector stores |
| `8_langgraph_example.py` | LangGraph + RAG integration |

## Step-by-Step

> **Working directory:** All commands in this module run from `08-rag/`.
>
> **Services needed:** Llama Stack server with an embedding model available.

### 1. Create the Vector Store

```bash
python 1_create_vector_store.py
```

This creates a hybrid vector store, uploads the NovaCrest HR benefits document, and chunks it with static chunking (100 tokens, 10 overlap).

### 2. Test RAG Queries

```bash
python 3_test_rag_hr_benefits.py
python 5_test_gold_watch.py
python 6_test_unique_terms.py
```

### 3. Debug Retrieval

```bash
python 4_debug_vector_search.py
```

## What You Should See

### Create Vector Store (script 1)

```
LLAMA_STACK_BASE_URL: http://localhost:8321
EMBEDDING_MODEL: granite-embedding-125m
EMBEDDING_DIMENSION: 768
--------------------------------------------------------------------------------
Initializing Llama Stack client...
Client initialized successfully
Creating vector store...
✓ Vector store created: hr-benefits-hybrid
Loading document from local file...
✓ Loaded 5432 characters from source_docs/NovaCrestHRBenefits_clean.txt
Uploading document to Llama Stack...
✓ File uploaded: file-abc123
Attaching file to vector store...
  Chunking: 100 tokens per chunk, 10 token overlap
✓ File attached to vector store
```

### RAG Query (script 3)

The agent uses `file_search` to retrieve relevant chunks, then answers:

```
Query: What do I receive when I retire?
Agent> Based on the HR Benefits document, when you retire ...
```

(Exact text varies by model.)

### Debug Vector Search (script 4)

```
Search results type: <class 'list'>
Results:
Result 1: Score: 0.87  Content: ...employees with 25+ years of service...
Result 2: Score: 0.72  Content: ...retirement benefits include...
```

## Key Takeaways

- Hybrid search (BM25 + semantic) improves retrieval over either approach alone
- Static chunking with overlap ensures context is preserved across chunk boundaries
- The `file_search` tool integrates seamlessly with Llama Stack agents
- Vector store creation, file upload, and search are all done via the Llama Stack API

## Concepts Applied

- **From Module 03**: `LlamaStackClient` for API access, `Agent` for RAG queries
- **New**: Vector stores, embedding models, hybrid search, `file_search` tool

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "No embedding models found" | Ensure your Llama Stack server has an embedding model registered |
| Empty search results | Check that the vector store was created and documents ingested (run script 2 to verify) |
| "Vector store not found" | Re-run `1_create_vector_store.py` to create it |
| Low retrieval scores | Try different chunking parameters (chunk size, overlap) |

## Next Module

Proceed to [09-safety-shields](../09-safety-shields/) to add content safety to your agents.
