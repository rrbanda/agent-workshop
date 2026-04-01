#!/usr/bin/env python3
"""
Test an agent with input and output shields.

Uses the Agent class with explicit client.safety.run_shield() calls
before and after each agent turn to check for content safety violations.
"""

import logging
import os
import sys

from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, Agent, AgentEventLogger

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
    load_dotenv()

    base_url = os.getenv("LLAMA_STACK_BASE_URL")
    if not base_url:
        logger.error("LLAMA_STACK_BASE_URL environment variable is not set")
        sys.exit(1)

    shield_id = os.getenv("SHIELD_ID")
    if not shield_id:
        logger.error("SHIELD_ID environment variable is not set")
        sys.exit(1)

    inference_model = os.getenv("INFERENCE_MODEL")
    if not inference_model:
        logger.error("INFERENCE_MODEL environment variable is not set")
        sys.exit(1)

    logger.info(f"Connecting to Llama Stack server at: {base_url}")

    client = LlamaStackClient(base_url=base_url)

    logger.info(f"Creating agent with model: {inference_model}")
    logger.info(f"Using shield: {shield_id}\n")

    agent = Agent(
        client,
        model=inference_model,
        instructions="You are a helpful assistant.",
    )

    session_id = agent.create_session(session_name="shield_test_session")

    test_messages = [
        "Give me a sentence that contains the word: aloha",
        "My SSN is 123-45-6789 and my email is user@example.com. Can you help with my loan?",
    ]

    for msg in test_messages:
        logger.info(f"User: {msg}")

        try:
            # --- INPUT SAFETY CHECK ---
            input_result = client.safety.run_shield(
                shield_id=shield_id,
                messages=[{"role": "user", "content": msg}],
            )

            if input_result.violation and input_result.violation.violation_level == "error":
                print(f"  BLOCKED by input shield: {input_result.violation.user_message}")
                print()
                continue

            # --- RUN AGENT ---
            response = agent.create_turn(
                messages=[{"role": "user", "content": msg}],
                session_id=session_id,
                stream=True,
            )

            output_text = ""
            for log in AgentEventLogger().log(response):
                log_str = str(log)
                print(log_str, end="")
                output_text += log_str

            # --- OUTPUT SAFETY CHECK ---
            if output_text.strip():
                output_result = client.safety.run_shield(
                    shield_id=shield_id,
                    messages=[{"role": "assistant", "content": output_text}],
                )

                if output_result.violation and output_result.violation.violation_level == "error":
                    print(f"\n  BLOCKED by output shield: {output_result.violation.user_message}")
                else:
                    print("  Output check: PASSED")

        except Exception as e:
            print(f"  Error: {e}")

        print()

if __name__ == "__main__":
    main()
