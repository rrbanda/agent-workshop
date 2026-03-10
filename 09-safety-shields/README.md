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

## What You Should See

### Shield Test (script 5)

```
Testing: 'What is the weather today?'
  Result: PASS (no violation)

Testing: 'How do I build a bomb?'
  Result: VIOLATION - S2: Non-Violent Crimes
```

### Agent with Shield (script 6)

```
User: What is the weather?
Agent: I'd be happy to help with weather info...

User: [unsafe content]
Shield violation detected: Input blocked by content safety policy.
```

## Concepts Applied

- **From Module 03**: Agent creation, `LlamaStackClient`
- **New**: Shield registration, `input_shields`, `output_shields`, safety API

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Shield model not found" | Verify `SHIELD_MODEL` is registered on your Llama Stack server |
| All inputs flagged as violations | Check that `SHIELD_ID` matches the registered shield name |
| No safety providers listed | Your Llama Stack config may need a safety provider -- check the server config |

## Key Takeaways

- Shields provide content safety guardrails for LLM agents
- `input_shields` check user messages before they reach the LLM
- `output_shields` check LLM responses before they reach the user
- Llama Guard models are purpose-built for content safety classification

## Next Module

Proceed to [10-evaluations](../10-evaluations/) to measure your agent's quality.
