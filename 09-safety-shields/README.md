# Module 09: Safety Shields

## Learning Objectives

- Register safety shields with Llama Stack
- Test content safety directly via the safety API
- Integrate input and output shields into agents

> [!TIP]
> **Capstone Preview:** In the capstone, you will wrap the mortgage agent with these safety shields to block social-engineering attempts like "How can I forge bank statements?" and to catch PII leakage in agent responses.

## Prerequisites

- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed
- Set `SHIELD_PROVIDER` and `SHIELD_ID` in your `.env` (see `.env.example`). The default provider is `trustyai_fms` with a regex-based PII detector.

## Concepts

**Safety shields** are content classifiers that sit between the user and the LLM. An **input shield** scans the user's message before it reaches the model -- blocking prompt injection, PII exposure, or harmful requests. An **output shield** scans the model's response before it reaches the user -- catching generated content that contains sensitive data or policy violations. In Llama Stack, shields are registered once and can be attached to any agent.

Llama Stack supports multiple safety providers. This workshop uses one of the following:

- **TrustyAI Guardrails (default):** The `trustyai_fms` provider connects to a TrustyAI Guardrails Orchestrator that uses regex-based detectors for PII (email, SSN, credit card). Shields are registered at runtime with detector configuration via `4_register_shield.py`. This is the default path in this workshop.
- **Llama Guard (alternative):** The `llama-guard` provider sends a structured safety classification prompt to an LLM, which returns a `safe` or `unsafe` verdict with category codes. Requires a safety-capable model. To use this path, set `SHIELD_PROVIDER` to a llama-guard provider ID and `SHIELD_MODEL` to the model identifier in your `.env`.

## Scripts

| Script | What It Does |
|--------|--------------|
| `1_list_models.py` | List all available models |
| `2_list_safety_providers.py` | List safety providers |
| `3_list_shields.py` | List registered shields |
| `4_register_shield.py` | Register a safety shield (TrustyAI PII detector or Llama Guard) |
| `5_test_shield.py` | Test shield with safe and unsafe messages |
| `6_agent_shield.py` | Create an agent with input and output shields |

## Step-by-Step

> [!NOTE]
> **Working directory:** All commands in this module run from `09-safety-shields/`.
>
> **Services needed:** Llama Stack server with a safety provider configured (`SHIELD_PROVIDER` and `SHIELD_ID` in `.env`).

### 1. Register a Shield

```bash
python 4_register_shield.py
```

### 2. Test the Shield

```bash
python 5_test_shield.py
```

Expected: clean content passes; messages containing PII (email, SSN, credit card) are flagged as violations.

### 3. Agent with Shields

```bash
python 6_agent_shield.py
```

The agent blocks inputs containing PII and filters unsafe outputs.

## What You Should See

### Shield Test (script 5)

```text
Testing shield: pii_detector

Test: Clean content (should PASS)
  Input: "What is the weather like today?"
  Result: SAFE - Content passed safety checks

Test: Contains email (should VIOLATE)
  Input: "My email is test@example.com"
  Result: VIOLATION DETECTED

Test: Contains SSN (should VIOLATE)
  Input: "My SSN is 123-45-6789"
  Result: VIOLATION DETECTED
```

### Agent with Shield (script 6)

```text
Query 1: Safe -- policy lookup
  Input check: PASSED
  (Agent responds normally)
  Output check: PASSED

Query 2: Unsafe -- contains PII (SSN + email)
  BLOCKED by input shield (pii_detector)
```

## Concepts Applied

- **From Module 03**: Agent creation, `LlamaStackClient`
- **New**: Shield registration, `client.safety.run_shield()`, input/output content safety

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Shield not working | Verify `SHIELD_PROVIDER` and `SHIELD_ID` in `.env` match a registered provider. For TrustyAI, run `4_register_shield.py` first. |
| All inputs flagged as violations | Check that `SHIELD_ID` matches the registered shield name |
| No safety providers listed | Your Llama Stack config may need a safety provider -- check the server config or run `2_list_safety_providers.py` |

## Key Takeaways

- Shields provide content safety guardrails for LLM agents
- `client.safety.run_shield()` checks messages before and after agent turns
- Shields are pluggable -- swap between TrustyAI (regex PII) and Llama Guard (LLM classification) by changing `SHIELD_PROVIDER` in `.env`
- Shields are registered once and can be attached to any agent

## Next Module

Proceed to [10-evaluations](../10-evaluations/) to measure your agent's quality.
