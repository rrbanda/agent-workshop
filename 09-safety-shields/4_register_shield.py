#!/usr/bin/env python3
"""
Register a safety shield with the TrustyAI Guardrails Orchestrator.

On RHOAI, shields use the trustyai_fms provider backed by the
GuardrailsOrchestrator (regex PII detectors, HAP models, etc.).
Shields are registered at runtime via the /v1/shields API with
detector configuration in the params field.
"""

import logging
import os
import sys

import httpx
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient, BadRequestError

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
    shield_provider = os.getenv("SHIELD_PROVIDER", "trustyai_fms")

    logger.info(f"Connecting to Llama Stack server at: {base_url}")
    logger.info(f"Registering shield '{shield_id}' with provider: {shield_provider}")

    if shield_provider == "trustyai_fms":
        payload = {
            "shield_id": shield_id,
            "provider_shield_id": shield_id,
            "provider_id": shield_provider,
            "params": {
                "type": "content",
                "confidence_threshold": 0.5,
                "verify_ssl": False,
                "message_types": ["system", "user"],
                "detectors": {
                    "regex": {
                        "detector_params": {
                            "regex": [
                                "email",
                                "us-social-security-number",
                                "credit-card",
                            ]
                        }
                    }
                },
            },
        }

        url = f"{base_url}/v1/shields"
        try:
            resp = httpx.post(url, json=payload, timeout=30)
            if resp.status_code == 200:
                logger.info(f"Shield '{shield_id}' registered successfully")
            elif resp.status_code == 400 and "already exists" in resp.text:
                logger.info(f"Shield '{shield_id}' already exists, skipping registration")
            else:
                logger.error(f"Failed to register shield: {resp.status_code} {resp.text}")
                sys.exit(1)
        except httpx.ConnectError as e:
            logger.error(f"Cannot connect to Llama Stack at {base_url}: {e}")
            sys.exit(1)
    else:
        client = LlamaStackClient(base_url=base_url)
        shield_model = os.getenv("SHIELD_MODEL", "")
        logger.info(f"Using llama-guard style registration with model: {shield_model}")
        try:
            client.shields.register(
                shield_id=shield_id,
                provider_id=shield_provider,
                provider_shield_id=shield_model,
            )
            logger.info(f"Shield '{shield_id}' registered successfully")
        except BadRequestError as e:
            if "already exists" in str(e):
                logger.info(f"Shield '{shield_id}' already exists, skipping registration")
            else:
                raise

    logger.info("")
    logger.info("Next step: run 5_test_shield.py to verify the shield works")


if __name__ == "__main__":
    main()
