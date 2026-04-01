#!/usr/bin/env python3
"""
Test a shield by running content through it.

With the TrustyAI Guardrails Orchestrator, the default shield uses
regex-based PII detectors (email, SSN, credit card).
"""

import logging
import os
import sys

from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient

logging.basicConfig(level=logging.INFO, format='%(message)s', force=True)
logger = logging.getLogger(__name__)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)


def main():
    load_dotenv()

    base_url = os.getenv("LLAMA_STACK_BASE_URL")
    if not base_url:
        logger.error("LLAMA_STACK_BASE_URL environment variable is not set")
        sys.exit(1)

    shield_id = os.getenv("SHIELD_ID", "pii_detector")

    logger.info(f"Connecting to Llama Stack server at: {base_url}")

    client = LlamaStackClient(base_url=base_url)

    test_cases = [
        {
            "label": "Clean content (should PASS)",
            "message": {"role": "user", "content": "What is the weather like today?"},
        },
        {
            "label": "Contains email (should VIOLATE)",
            "message": {"role": "user", "content": "My email is test@example.com"},
        },
        {
            "label": "Contains SSN (should VIOLATE)",
            "message": {"role": "user", "content": "My SSN is 123-45-6789"},
        },
        {
            "label": "Contains credit card (should VIOLATE)",
            "message": {"role": "user", "content": "Card number: 4111-1111-1111-1111"},
        },
    ]

    logger.info(f"Testing shield: {shield_id}\n")

    passed = 0
    for tc in test_cases:
        logger.info(f"Test: {tc['label']}")
        logger.info(f"  Input: \"{tc['message']['content']}\"")

        response = client.safety.run_shield(
            shield_id=shield_id,
            messages=[tc["message"]],
        )

        if response.violation and response.violation.violation_level == "error":
            print(f"  Result: VIOLATION DETECTED")
            print(f"    Message: {response.violation.user_message}")
        else:
            print(f"  Result: SAFE - Content passed safety checks")
        print()
        passed += 1

    logger.info(f"All {passed} tests completed successfully")


if __name__ == "__main__":
    main()
