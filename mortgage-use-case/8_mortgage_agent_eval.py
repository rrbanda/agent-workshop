#!/usr/bin/env python3
"""
Step 8: Evaluate the mortgage agent's knowledge with an eval pipeline.

Registers a mortgage-specific eval dataset (Q&A pairs from the lending policy),
runs a benchmark evaluation against the model, and displays the results.

This evaluates the base model WITHOUT RAG. Comparing these results with the
RAG-powered agent's answers (Steps 3-6) demonstrates why retrieval augmentation
is essential for domain-specific accuracy.

Prerequisites:
    - Llama Stack server running
    - Module 10 completed (understand eval concepts)
"""

import os
import sys
import logging
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, BadRequestError

logging.basicConfig(level=logging.INFO, format="%(message)s", force=True)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv()

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL", "http://localhost:8321")
CANDIDATE_MODEL = os.getenv("CANDIDATE_MODEL") or os.getenv("INFERENCE_MODEL")

DATASET_ID = "mortgage-policy-evals"
BENCHMARK_ID = "mortgage-quality-benchmark"
SCORING_FN = "basic::subset_of"

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATASET_URI = os.path.join(_SCRIPT_DIR, "datasets", "mortgage-evals.csv")

if not CANDIDATE_MODEL:
    logger.error("CANDIDATE_MODEL (or INFERENCE_MODEL) environment variable is not set")
    sys.exit(1)

client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)

print(f"Model: {CANDIDATE_MODEL}")
print(f"Dataset: {DATASET_URI}")
print(f"Scoring: {SCORING_FN}")
print("=" * 60)

# --- 1. Register the mortgage eval dataset ---
print("\n1. Registering eval dataset...")
try:
    client.datasets.register(
        purpose="eval/question-answer",
        source={"type": "uri", "uri": DATASET_URI},
        dataset_id=DATASET_ID,
        extra_body={"provider_id": "localfs"},
    )
    print(f"   Dataset '{DATASET_ID}' registered")
except BadRequestError as e:
    if "already exists" in str(e):
        print(f"   Dataset '{DATASET_ID}' already registered, continuing")
    else:
        raise

# --- 2. Register the benchmark ---
print("\n2. Registering benchmark...")
try:
    client.benchmarks.register(
        benchmark_id=BENCHMARK_ID,
        dataset_id=DATASET_ID,
        scoring_functions=[SCORING_FN],
    )
    print(f"   Benchmark '{BENCHMARK_ID}' registered")
except BadRequestError as e:
    if "already exists" in str(e):
        print(f"   Benchmark '{BENCHMARK_ID}' already registered, continuing")
    else:
        raise

# --- 3. Run the evaluation ---
print("\n3. Running evaluation...")
print(f"   Candidate model: {CANDIDATE_MODEL}")

job = client.alpha.eval.run_eval(
    benchmark_id=BENCHMARK_ID,
    benchmark_config={
        "eval_candidate": {
            "type": "model",
            "model": CANDIDATE_MODEL,
            "sampling_params": {
                "strategy": {"type": "greedy"},
                "max_tokens": 128,
            },
        },
        "scoring_params": {
            SCORING_FN: {
                "type": "basic",
                "aggregation_functions": ["accuracy"],
            },
        },
    },
)

job_id = getattr(job, "job_id", None)
print(f"   Job started: {job_id}")

# --- 4. Retrieve and display results ---
print("\n4. Retrieving results...")
result = client.alpha.eval.jobs.retrieve(job_id=job_id, benchmark_id=BENCHMARK_ID)

if not result or not result.scores:
    print("   No scores returned. The eval may still be processing.")
    sys.exit(0)

print("\n" + "=" * 60)
print("MORTGAGE EVAL RESULTS")
print("=" * 60)

scoring_result = result.scores.get(SCORING_FN)
generations = result.generations or []

correct = 0
total = len(generations)

for i, gen in enumerate(generations):
    query = gen.get("input_query", "N/A")
    expected = gen.get("expected_answer", "N/A")
    generated = gen.get("generated_answer", "N/A")

    if isinstance(generated, str) and len(generated) > 120:
        display_answer = generated[:120] + "..."
    else:
        display_answer = generated

    score = None
    if scoring_result and scoring_result.score_rows and i < len(scoring_result.score_rows):
        score = scoring_result.score_rows[i].get("score")

    status = "PASS" if score and str(score).lower() in ("true", "1", "1.0") else "FAIL"
    if status == "PASS":
        correct += 1

    print(f"\n  Q: {query}")
    print(f"  Expected: {expected}")
    print(f"  Got:      {display_answer}")
    print(f"  Result:   {status}")

print(f"\n{'='*60}")
accuracy = (correct / total * 100) if total > 0 else 0
print(f"Accuracy: {correct}/{total} ({accuracy:.0f}%)")

if scoring_result and scoring_result.aggregated_results:
    print(f"Aggregated: {scoring_result.aggregated_results}")

print("=" * 60)

if accuracy < 100:
    print(
        "\nNote: The model was evaluated WITHOUT RAG. With the lending policy\n"
        "document available via file_search (Steps 3-6), the agent can\n"
        "answer these questions accurately. This demonstrates why RAG\n"
        "is essential for domain-specific knowledge."
    )
