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

## What You Should See

### Register Dataset (script 2)

```
Registered dataset: basic-subset-of-evals
Dataset URI: datasets/basic-subset-of-evals.csv
```

### Scoring Test (script 4)

```
Row 1: expected='Paris' generated='The capital of France is Paris'  -> PASS (1.0)
Row 2: expected='Berlin' generated='The capital is Munich'          -> FAIL (0.0)
```

### Eval Job Review (script 8)

```
Job: eval-job-001  Status: completed
  Rows evaluated: 10
  Average score: 0.80
  Pass: 8 / Fail: 2
```

### LLM-as-Judge (script 9)

```
Judge model: vllm/llama-scout-17b
Query: What is the capital of France?
Generated: Paris is the capital of France.
Judge score: 5/5 - Correct and complete answer.
```

## Key Takeaways

- Evals measure agent quality systematically
- `basic::subset_of` is a simple rule-based scorer (expected answer in generated answer)
- LLM-as-judge uses a separate LLM to evaluate response quality
- Benchmarks combine a dataset with scoring functions for repeatable evaluation

## Concepts Applied

- **From Module 03**: `LlamaStackClient` for API access
- **New**: Datasets, scoring functions, benchmarks, evaluation jobs, LLM-as-judge

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Dataset not found" | Run `2_register_dataset_basic_subset_of.py` first |
| "Benchmark not found" | Run `5_register_benchmark.py` before `7_execute_eval.py` |
| Judge model errors | Verify `JUDGE_MODEL` is available on your Llama Stack server |
| Low eval scores | Check if the candidate model can handle the query complexity |

## Next Module

Proceed to [11-observability](../11-observability/) for production tracing and feedback.
