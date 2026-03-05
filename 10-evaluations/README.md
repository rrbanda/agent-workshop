# Module 10: Evaluations

## Learning Objectives

- Register evaluation datasets with Llama Stack
- Define scoring functions (rule-based and LLM-as-judge)
- Run benchmark evaluation jobs
- Review and interpret evaluation results

## Prerequisites

- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed

## Scripts

| Script | What It Does |
|--------|--------------|
| `1_list_eval_related_providers.py` | List eval, dataset, and scoring providers |
| `2_register_dataset_basic_subset_of.py` | Register a simple Q&A dataset |
| `2_register_dataset_agent_evals_customer.py` | Register NovaCrest customer eval dataset |
| `3_list_datasets.py` | List all registered datasets |
| `4_list_scoring_functions.py` | List available scoring functions |
| `4_basic_subset_of_scoring_function.py` | Test rule-based scoring directly |
| `5_register_benchmark.py` | Register a benchmark (dataset + scoring) |
| `7_execute_eval.py` | Run an evaluation job |
| `8_review_eval_job.py` | Review eval results |
| `9_llm_as_judge.py` | LLM-as-judge scoring |

## Step-by-Step

### 1. Register a Dataset

```bash
python 2_register_dataset_basic_subset_of.py
```

### 2. Test Scoring Directly

```bash
python 4_basic_subset_of_scoring_function.py
```

### 3. Run a Full Evaluation

```bash
python 5_register_benchmark.py
python 7_execute_eval.py
python 8_review_eval_job.py
```

### 4. LLM-as-Judge

```bash
python 9_llm_as_judge.py
```

## Key Takeaways

- Evals measure agent quality systematically
- `basic::subset_of` is a simple rule-based scorer (expected answer in generated answer)
- LLM-as-judge uses a separate LLM to evaluate response quality
- Benchmarks combine a dataset with scoring functions for repeatable evaluation

## Next Module

Proceed to [11-observability](../11-observability/) for production tracing and feedback.
