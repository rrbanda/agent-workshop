#!/usr/bin/env python3
"""
Run an eval job on a benchmark and display the results.
"""

import logging
import os
import sys
import time

from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient

logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    force=True
)
logger = logging.getLogger(__name__)

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)


def main():
    load_dotenv()

    base_url = os.getenv("LLAMA_STACK_BASE_URL")
    if not base_url:
        logger.error("LLAMA_STACK_BASE_URL environment variable is not set")
        sys.exit(1)

    model_id = os.getenv("CANDIDATE_MODEL")
    if not model_id:
        logger.error("CANDIDATE_MODEL environment variable is not set")
        sys.exit(1)

    benchmark_id = os.getenv("LLAMA_STACK_BENCHMARK_ID", "my-basic-quality-benchmark")

    logger.info(f"Connecting to Llama Stack server at: {base_url}")
    logger.info(f"Running eval for benchmark: {benchmark_id}")
    logger.info(f"Using candidate model: {model_id}")

    client = LlamaStackClient(base_url=base_url)

    benchmark_config = {
        "eval_candidate": {
            "type": "model",
            "model": model_id,
            "sampling_params": {
                "strategy": {"type": "greedy"},
                "max_tokens": 1024,
            },
        },
        "scoring_params": {},
    }

    try:
        job = client.alpha.eval.run_eval(
            benchmark_id,
            benchmark_config=benchmark_config,
        )
    except Exception as exc:
        logger.error(f"Failed to run eval: {exc}")
        sys.exit(1)

    job_id = getattr(job, "job_id", None)
    status = getattr(job, "status", "unknown")
    logger.info(f"Eval job created: job_id={job_id}  status={status}")

    if status != "completed":
        logger.info("Waiting for job to complete...")
        for _ in range(30):
            time.sleep(2)
            job = client.alpha.eval.jobs.status(job_id, benchmark_id=benchmark_id)
            status = getattr(job, "status", "unknown")
            if status in ("completed", "failed"):
                break
        logger.info(f"Job status: {status}")

    if status == "failed":
        logger.error("Eval job failed")
        sys.exit(1)

    try:
        result = client.alpha.eval.jobs.retrieve(job_id, benchmark_id=benchmark_id)
    except Exception as exc:
        logger.error(f"Failed to retrieve eval results: {exc}")
        sys.exit(1)

    if not result or not result.scores:
        logger.warning("No scores returned")
        return

    logger.info("\n===== Evaluation Results =====\n")
    for scoring_fn_id, scoring_result in result.scores.items():
        logger.info(f"Scoring Function: {scoring_fn_id}")

        if scoring_result.aggregated_results:
            logger.info(f"  Aggregated: {scoring_result.aggregated_results}")

        if scoring_result.score_rows:
            logger.info(f"  Rows scored: {len(scoring_result.score_rows)}")
            for i, row in enumerate(scoring_result.score_rows):
                gen = ""
                if result.generations and i < len(result.generations):
                    answer = result.generations[i].get("generated_answer", "")
                    gen = f"  | Answer: {answer[:120]}"
                logger.info(f"    Row {i+1}: score={row.get('score', 'N/A')}{gen}")
        logger.info("")


if __name__ == "__main__":
    main()
