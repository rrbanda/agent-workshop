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
Creating vector store 'novacrest_hr_benefits'...
Vector store created: vs_abc123
Uploading document: source_docs/NovaCrest_HR_Benefits.txt
Document uploaded and chunked into 12 chunks
```

### RAG Query (script 3)

```
Query: What do I receive when I retire?
inference> Based on the HR Benefits document, when you retire you receive:
  - A gold watch after 25 years of service
  - Full pension benefits
  ...
```

### Debug Vector Search (script 4)

```
Query: "gold watch"
Result 1 (score: 0.87): "...employees with 25+ years receive a gold watch..."
Result 2 (score: 0.72): "...retirement benefits include..."
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
