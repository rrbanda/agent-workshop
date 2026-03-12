# Module 10: Evaluations

## Learning Objectives

- Register evaluation datasets with Llama Stack
- Define scoring functions (rule-based and LLM-as-judge)
- Run benchmark evaluation jobs
- Review and interpret evaluation results

> **Capstone Preview:** In the capstone, you will build a mortgage-specific eval dataset and benchmark to measure your agent's accuracy against the lending policy.

## Prerequisites

- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed

## Concepts

**Evaluations (evals)** measure an agent's quality systematically rather than relying on manual spot-checks. A **dataset** contains question-answer pairs that define what "correct" looks like. A **scoring function** compares the model's generated answer against the expected answer -- rule-based scorers like `basic::subset_of` check for exact containment, while **LLM-as-judge** uses a separate LLM to assess quality on a scale. A **benchmark** combines a dataset with scoring functions into a repeatable test suite you can run against different models or configurations.

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

> **Working directory:** All commands in this module run from `10-evaluations/`.
>
> **Services needed:** Llama Stack server.

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
```

Script 7 will print a job ID when it completes. Copy it and set it before running script 8:

```bash
export LLAMA_STACK_JOB_ID=<job-id-from-script-7-output>
python 8_review_eval_job.py
```

### 4. LLM-as-Judge

```bash
python 9_llm_as_judge.py
```

## What You Should See

### Register Dataset (script 2)

```
Connecting to Llama Stack server at: http://localhost:8321
Registering dataset: basic-subset-of-evals
Using dataset provider: localfs
Registered dataset: basic-subset-of-evals
```

### Scoring Test (script 4)

```
=== basic::subset_of ===
Accuracy: 100.0%
Correct: 1 / 1

Row scores:
  Row 1: ✓ (score: 1.0)
```

The script scores `"What is 2 + 2?"` with expected answer `"4"` against generated answer `"4"`.

### Execute Eval (script 7)

```
Running eval for benchmark: my-basic-quality-benchmark
Using candidate model: vllm/qwen3-14b
Eval job started: eval-job-abc123
```

Copy the job ID from this output for the next step.

### LLM-as-Judge (script 9)

```
================================================================================
EVALUATION RESULTS
================================================================================

--- Evaluation 1 ---
Generated Answer: 4
Score: 1.0
Judge Feedback:
The answer is correct and complete...

================================================================================
Total evaluations: 1
================================================================================
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
