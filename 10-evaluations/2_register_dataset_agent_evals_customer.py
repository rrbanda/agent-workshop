#!/usr/bin/env python3
"""
Register datasets/agent-evals-customer.csv with a Llama Stack server.
"""

import csv
import logging
import os
import sys

from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    force=True
)
logger = logging.getLogger(__name__)

# Suppress httpx INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

DATASET_ID = "agent-evals-customer"
_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_DATASET_URI = os.path.join(_SCRIPT_DIR, "datasets", "agent-evals-customer.csv")


def main():
    # Load environment variables from .env file
    load_dotenv()

    base_url = os.getenv("LLAMA_STACK_BASE_URL")
    if not base_url:
        logger.error("LLAMA_STACK_BASE_URL environment variable is not set")
        sys.exit(1)

    dataset_path = os.getenv("AGENT_EVALS_CUSTOMER_DATASET_URI", DEFAULT_DATASET_URI)

    logger.info(f"Connecting to Llama Stack server at: {base_url}")
    logger.info(f"Registering dataset: {DATASET_ID}")

    # Create the Llama Stack client
    client = LlamaStackClient(base_url=base_url)

    rows = []
    with open(dataset_path, "r") as f:
        reader = csv.DictReader(f)
        for r in reader:
            rows.append({
                "input_query": r["input_query"],
                "expected_answer": r["expected_answer"],
                "chat_completion_input": r["chat_completion_input"],
            })
    logger.info(f"Loaded {len(rows)} rows from {dataset_path}")

    try:
        dataset = client.beta.datasets.register(
            purpose="eval/messages-answer",
            source={"type": "rows", "rows": rows},
            dataset_id=DATASET_ID,
        )
    except Exception as exc:
        logger.error(f"Failed to register dataset: {exc}")
        sys.exit(1)

    if dataset is None:
        logger.warning("No dataset returned from registration")
        return

    identifier = getattr(dataset, "identifier", DATASET_ID)
    logger.info(f"Registered dataset: {identifier}")


if __name__ == "__main__":
    main()
