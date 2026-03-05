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

## Key Takeaways

- Hybrid search (BM25 + semantic) improves retrieval over either approach alone
- Static chunking with overlap ensures context is preserved across chunk boundaries
- The `file_search` tool integrates seamlessly with Llama Stack agents
- Vector store creation, file upload, and search are all done via the Llama Stack API

## Next Module

Proceed to [09-safety-shields](../09-safety-shields/) to add content safety to your agents.
