"""List available embedding models on the Llama Stack server."""

import os
import logging
import sys
from dotenv import load_dotenv
from llama_stack_client import LlamaStackClient
from llama_stack_client import APIConnectionError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    force=True
)
logger = logging.getLogger(__name__)

# Suppress httpx and llama_stack_client INFO logs
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

# Load environment variables
load_dotenv()

# Get configuration from environment
LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL", "http://localhost:8321")

logger.info("=" * 80)
logger.info("Available Embedding Models on Llama Stack Server")
logger.info("=" * 80)
logger.info(f"Server: {LLAMA_STACK_BASE_URL}")
logger.info("-" * 80)

# Initialize client
try:
    client = LlamaStackClient(base_url=LLAMA_STACK_BASE_URL)
except Exception as e:
    logger.error(f"Failed to initialize client: {e}")
    sys.exit(1)

# List all models
try:
    logger.info("\nFetching available models...")
    models = client.models.list()

    model_list = list(models)

    if not model_list:
        logger.warning("No models found on the server")
        logger.info("\nYou need to register models using client.models.register()")
        sys.exit(0)

    embedding_models = []
    for model in model_list:
        meta = getattr(model, 'custom_metadata', {}) or {}
        if meta.get('model_type') == 'embedding':
            embedding_models.append(model)

    if embedding_models:
        logger.info(f"\nFound {len(embedding_models)} embedding model(s):\n")
        for i, model in enumerate(embedding_models, 1):
            meta = getattr(model, 'custom_metadata', {}) or {}
            logger.info(f"{i}. {model.id}")
            logger.info(f"   Provider: {meta.get('provider_id', 'unknown')}")
            logger.info(f"   Resource ID: {meta.get('provider_resource_id', 'unknown')}")
            dim = meta.get('embedding_dimension', 'unknown')
            logger.info(f"   Dimension: {dim}")
            logger.info("")
    else:
        logger.warning("\n⚠ No embedding models found!")
        logger.info("You need an embedding model for vector stores.")
        logger.info("Run: python 0_register_embedding_model.py")

    logger.info("=" * 80)

except APIConnectionError as e:
    logger.error(f"Cannot connect to server at {LLAMA_STACK_BASE_URL}")
    logger.error("Make sure the server is running")
    sys.exit(1)
except Exception as e:
    logger.error(f"Error listing models: {e}")
    sys.exit(1)
