#!/usr/bin/env python3
"""
Register a benchmark with a Llama Stack server.
"""

import logging
import os
import sys

from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, BadRequestError, NotFoundError

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


def main():
    # Load environment variables from .env file
    load_dotenv()

    base_url = os.getenv("LLAMA_STACK_BASE_URL")
    if not base_url:
        logger.error("LLAMA_STACK_BASE_URL environment variable is not set")
        sys.exit(1)

    logger.info(f"Connecting to Llama Stack server at: {base_url}")

    # Create the Llama Stack client
    client = LlamaStackClient(base_url=base_url)

    provider_id = os.getenv("LLAMA_STACK_BENCHMARK_PROVIDER_ID")
    if provider_id:
        logger.info(f"Using benchmark provider: {provider_id}")

    logger.info("Registering benchmark: my-basic-quality-benchmark")

    benchmark_provider = provider_id or "meta-reference"
    logger.info(f"Using provider_id: {benchmark_provider}")

    try:
        client.alpha.benchmarks.register(
            benchmark_id="my-basic-quality-benchmark",
            dataset_id="basic-subset-of-evals",
            scoring_functions=["basic::subset_of"],
            provider_id=benchmark_provider,
        )
        logger.info("Benchmark registered successfully")
    except BadRequestError as exc:
        if "already exists" in str(exc):
            logger.info("Benchmark 'my-basic-quality-benchmark' already exists, skipping registration")
        else:
            logger.error(f"Failed to register benchmark: {exc}")
            sys.exit(1)
    except NotFoundError as exc:
        logger.error(f"Failed to register benchmark: {exc}")
        logger.error("Benchmark API not found. Enable the eval API in your Llama Stack run.yaml and restart.")
        sys.exit(1)
    except Exception as exc:
        logger.error(f"Failed to register benchmark: {exc}")
        sys.exit(1)


if __name__ == "__main__":
    main()
