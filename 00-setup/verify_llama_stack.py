#!/usr/bin/env python3
"""
Llama Stack Workshop Readiness Check

Verifies that a Llama Stack server has all capabilities the
ACME Agent Workshop requires:

  [1/6] Models ........... inference + embedding models exist
  [2/6] Chat ............. test prompt returns a response
  [3/6] Embedding ........ generates a vector of expected dimension
  [4/6] Vector Store ..... create / search / delete
  [5/6] Safety ........... safety provider available (llama-guard or trustyai_fms)
  [6/6] Tool Runtime ..... rag-runtime + model-context-protocol providers

Usage:
  python 00-setup/verify_llama_stack.py

Reads LLAMA_STACK_BASE_URL, INFERENCE_MODEL, and EMBEDDING_MODEL from .env.
"""

import logging
import os
import sys

from dotenv import find_dotenv, load_dotenv

logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("llama_stack_client").setLevel(logging.WARNING)

load_dotenv(find_dotenv())

LLAMA_STACK_BASE_URL = os.getenv("LLAMA_STACK_BASE_URL")
if not LLAMA_STACK_BASE_URL:
    print(
        f"{FAIL}: LLAMA_STACK_BASE_URL is not set.\n"
        "Set it in your .env file or export it before running this script.\n"
        "Example: export LLAMA_STACK_BASE_URL=https://llamastack.apps.example.com"
    )
    sys.exit(1)
LLAMA_STACK_API_KEY = os.getenv("LLAMA_STACK_API_KEY", "fake")
INFERENCE_MODEL = os.getenv("INFERENCE_MODEL", "vllm-inference/gpt-oss-120b")
EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL", "vllm-embedding/nomic-embed-text-v1-5"
)
EXPECTED_EMBEDDING_DIM = int(os.getenv("EMBEDDING_DIMENSION", "768"))

PASS = "\033[92mPASS\033[0m"
FAIL = "\033[91mFAIL\033[0m"
WARN = "\033[93mWARN\033[0m"

passed = 0
failed = 0
warnings = 0


def banner():
    print()
    print("Llama Stack Workshop Readiness Check")
    print(f"Server: {LLAMA_STACK_BASE_URL}")
    print("=" * 56)


def result_line(idx, name, status, detail=""):
    global passed, failed, warnings
    dots = "." * (24 - len(name))
    tag = PASS if status == "pass" else (FAIL if status == "fail" else WARN)
    if status == "pass":
        passed += 1
    elif status == "fail":
        failed += 1
    else:
        warnings += 1
    msg = f" ({detail})" if detail else ""
    print(f"[{idx}/6] {name} {dots} {tag}{msg}")


def get_client():
    try:
        from llama_stack_client import LlamaStackClient

        return LlamaStackClient(
            base_url=LLAMA_STACK_BASE_URL,
            api_key=LLAMA_STACK_API_KEY,
        )
    except ImportError:
        print(
            f"{FAIL}: llama-stack-client not installed. "
            "Run: pip install 'llama-stack-client==0.5.0'"
        )
        sys.exit(1)
    except Exception as e:
        print(f"{FAIL}: Cannot connect to {LLAMA_STACK_BASE_URL}: {e}")
        sys.exit(1)


# ── Check 1: Models ──────────────────────────────────────────────────────────
def check_models(client):
    try:
        models = client.models.list()
        model_ids = [m.id for m in models]

        inf_ok = INFERENCE_MODEL in model_ids
        emb_ok = EMBEDDING_MODEL in model_ids

        details = []
        if inf_ok:
            details.append(f"inference: {INFERENCE_MODEL}")
        else:
            details.append(f"MISSING inference: {INFERENCE_MODEL}")
        if emb_ok:
            details.append(f"embedding: {EMBEDDING_MODEL}")
        else:
            details.append(f"MISSING embedding: {EMBEDDING_MODEL}")

        status = "pass" if (inf_ok and emb_ok) else "fail"
        result_line(1, "Models", status, "; ".join(details))
        return inf_ok, emb_ok
    except Exception as e:
        result_line(1, "Models", "fail", str(e))
        return False, False


# ── Check 2: Chat Completion ─────────────────────────────────────────────────
def check_chat(client, model_available):
    if not model_available:
        result_line(2, "Chat", "fail", "skipped -- inference model not found")
        return

    try:
        response = client.chat.completions.create(
            model=INFERENCE_MODEL,
            messages=[{"role": "user", "content": "Say hello in exactly 5 words."}],
        )
        text = response.choices[0].message.content
        if isinstance(text, list):
            text = text[0] if text else ""
        tokens = len(str(text).split())
        result_line(2, "Chat", "pass", f"response received, ~{tokens} words")
    except Exception as e:
        result_line(2, "Chat", "fail", str(e)[:120])


# ── Check 3: Embedding ───────────────────────────────────────────────────────
def check_embedding(client, model_available):
    if not model_available:
        result_line(3, "Embedding", "fail", "skipped -- embedding model not found")
        return

    try:
        response = client.embeddings.create(
            model=EMBEDDING_MODEL,
            input=["test embedding for workshop verification"],
        )
        dim = len(response.data[0].embedding)
        dim_ok = dim == EXPECTED_EMBEDDING_DIM
        status = "pass" if dim_ok else "warn"
        detail = f"dimension: {dim}"
        if not dim_ok:
            detail += f" (expected {EXPECTED_EMBEDDING_DIM})"
        result_line(3, "Embedding", status, detail)
    except Exception as e:
        result_line(3, "Embedding", "fail", str(e)[:120])


# ── Check 4: Vector Store ────────────────────────────────────────────────────
def check_vector_store(client, emb_available):
    if not emb_available:
        result_line(
            4, "Vector Store", "fail", "skipped -- embedding model not found"
        )
        return

    test_name = "workshop-verify-test"
    vs_id = None
    steps_done = []
    try:
        providers = client.providers.list()
        vec_providers = [p for p in providers if getattr(p, "api", None) == "vector_io"]
        provider_id = vec_providers[0].provider_id if len(vec_providers) == 1 else "faiss"

        vs = client.vector_stores.create(
            name=test_name,
            metadata={"embedding_model": EMBEDDING_MODEL},
            extra_body={"provider_id": provider_id},
        )
        vs_id = vs.id
        steps_done.append("create")

        results = client.vector_stores.search(
            vector_store_id=vs_id,
            query="What is ACME?",
            max_num_results=1,
        )
        steps_done.append("search")

        client.vector_stores.delete(vector_store_id=vs_id)
        steps_done.append("delete")
        vs_id = None

        result_line(4, "Vector Store", "pass", "/".join(steps_done))
    except Exception as e:
        if vs_id:
            try:
                client.vector_stores.delete(vector_store_id=vs_id)
            except Exception:
                pass
        result_line(
            4,
            "Vector Store",
            "fail",
            f"failed at {'/'.join(steps_done) or 'start'}: {str(e)[:80]}",
        )


# ── Check 5: Safety ──────────────────────────────────────────────────────────
def check_safety(client):
    try:
        providers = client.providers.list()
        safety_providers = [
            p for p in providers if getattr(p, "api", None) == "safety"
        ]
        provider_ids = [p.provider_id for p in safety_providers]

        known_safety = {"llama-guard", "trustyai_fms"}
        found_known = [p for p in provider_ids if p in known_safety]
        if found_known:
            result_line(5, "Safety", "pass", f"{', '.join(found_known)} provider available")
        elif safety_providers:
            result_line(
                5,
                "Safety",
                "warn",
                f"providers: {', '.join(provider_ids)} (expected llama-guard or trustyai_fms)",
            )
        else:
            result_line(5, "Safety", "fail", "no safety providers found")
    except Exception as e:
        result_line(5, "Safety", "fail", str(e)[:120])


# ── Check 6: Tool Runtime ────────────────────────────────────────────────────
def check_tool_runtime(client):
    try:
        providers = client.providers.list()
        tr_providers = [
            p for p in providers if getattr(p, "api", None) == "tool_runtime"
        ]
        provider_ids = [p.provider_id for p in tr_providers]

        has_rag = "rag-runtime" in provider_ids
        has_mcp = "model-context-protocol" in provider_ids

        details = []
        if has_rag:
            details.append("rag-runtime")
        if has_mcp:
            details.append("model-context-protocol")

        if has_rag and has_mcp:
            result_line(6, "Tool Runtime", "pass", " + ".join(details))
        elif details:
            missing = []
            if not has_rag:
                missing.append("rag-runtime")
            if not has_mcp:
                missing.append("model-context-protocol")
            result_line(
                6,
                "Tool Runtime",
                "warn",
                f"found: {', '.join(details)}; missing: {', '.join(missing)}",
            )
        else:
            result_line(
                6,
                "Tool Runtime",
                "fail",
                f"no rag-runtime or model-context-protocol (found: {', '.join(provider_ids) or 'none'})",
            )
    except Exception as e:
        result_line(6, "Tool Runtime", "fail", str(e)[:120])


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    banner()
    client = get_client()

    inf_ok, emb_ok = check_models(client)
    check_chat(client, inf_ok)
    check_embedding(client, emb_ok)
    check_vector_store(client, emb_ok)
    check_safety(client)
    check_tool_runtime(client)

    print("=" * 56)

    total = passed + failed + warnings
    if failed == 0 and warnings == 0:
        print(f"Result: {passed}/{total} checks passed -- server is ready for the workshop")
    elif failed == 0:
        print(
            f"Result: {passed}/{total} passed, {warnings} warnings -- "
            "review warnings above"
        )
    else:
        print(
            f"Result: {passed}/{total} passed, {failed} FAILED -- "
            "fix failures before starting the workshop"
        )

    print()
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
