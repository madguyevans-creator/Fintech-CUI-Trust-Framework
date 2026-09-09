# Reference Implementation — Lite sidecar

**Status:** v0.4 Lite control plane (no LLM)  
**License:** MIT

This directory contains a deployable **control-plane sidecar** for specification [v0.4](../spec/protocol-spec-v0.4.md). It sits conceptually between a conversational agent and an LLM. This Lite build classifies an utterance, binds an Action Object, applies a product-line mapping, optionally issues a scoped credential record, writes a hash-chained JSONL audit event, and prints Visible Authority State.

It is not the sole compliant instantiation. It does not call a model. It does not move money.

## Run

```bash
cd src
python3 -m pip install -r requirements.txt
python3 -m cf_gov.sidecar --mapping ../mappings/payments.yaml --utterance "What's the fee for sending 200 dollars?"
python3 -m cf_gov.sidecar --mapping ../mappings/lending.yaml --utterance "Should I take the loan?"
python3 -m cf_gov.sidecar --mapping ../mappings/insurance.yaml --utterance "Is this claim fully covered by my plan?"
python3 -m cf_gov.sidecar --mapping ../mappings/collections.yaml --utterance "Pay now."
```

Optional audit file:

```bash
python3 -m cf_gov.sidecar \
  --mapping ../mappings/payments.yaml \
  --utterance "Pay now. Send 200 dollars to Jane." \
  --audit /tmp/cf-gov-audit.jsonl
```

Tests from repository root:

```bash
python3 tests/test_sidecar.py
```

## What this sidecar enforces

- `(FCR, RS, Action)` tuple before any "generation" decision
- Classification Assurance (`confidence_floor` from the mapping)
- Section 3.2 FREE / AUTH / ESCALATE table
- Product-line action overrides (payments vs lending vs insurance vs collections)
- Scoped credential **record** with `secret_material_in_model_context=false`
- Visible Authority State in the JSON output
- Append-only hash-chained JSONL when `--audit` is set

## What this sidecar does not do

- Call an LLM
- Perform real payments
- Replace a production intent model (the classifier is deterministic and pattern-based, for protocol demonstration)
- Implement a human operator console

## Layout

```
src/
  requirements.txt
  cf_gov/
    __init__.py
    engine.py      ← control plane
    sidecar.py     ← CLI
```
