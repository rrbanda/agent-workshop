# Module 09: Safety Shields

## Learning Objectives

- Register safety shields (Llama Guard) with Llama Stack
- Test content safety directly via the safety API
- Integrate input and output shields into agents

## Prerequisites

- [Module 03: Llama Stack Basics](../03-llama-stack-basics/) completed
- A safety model (e.g., Llama-Guard-3-1B) available on your Llama Stack server

## Scripts

| Script | What It Does |
|--------|--------------|
| `1_list_models.py` | List all available models |
| `2_list_safety_providers.py` | List safety providers |
| `3_list_shields.py` | List registered shields |
| `4_register_shield.py` | Register a Llama Guard shield |
| `5_test_shield.py` | Test shield with safe and unsafe messages |
| `6_agent_shield.py` | Create an agent with input and output shields |

## Step-by-Step

### 1. Register a Shield

```bash
python 4_register_shield.py
```

### 2. Test the Shield

```bash
python 5_test_shield.py
```

Expected: "What is the weather?" passes; harmful content is flagged as a violation.

### 3. Agent with Shields

```bash
python 6_agent_shield.py
```

The agent blocks unsafe inputs and filters unsafe outputs.

## Key Takeaways

- Shields provide content safety guardrails for LLM agents
- `input_shields` check user messages before they reach the LLM
- `output_shields` check LLM responses before they reach the user
- Llama Guard models are purpose-built for content safety classification

## Next Module

Proceed to [10-evaluations](../10-evaluations/) to measure your agent's quality.
