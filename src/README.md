# Reference Implementation

**Status:** Pre-release (architecture defined, implementation in progress)  
**License:** MIT  

## Overview

This directory will contain the reference implementation of An Open Governance Standard for Conversational Finance Agents as defined in [`/spec/protocol-spec-v0.1.md`](../spec/protocol-spec-v0.1.md).

The reference implementation is a deployable middleware that sits between a conversational AI agent and its users, enforcing the standard's Input Safeguard, Authorization Triggers, Insurance Fuse, Generation Boundaries, and Audit Trail requirements at runtime. It is not the sole compliant instantiation of the standard — any implementation conforming to the specification may claim conformance.

## Architecture

```
User → [Agent Runtime] → [Protocol Middleware] → [LLM]
                              │
                        ┌─────┴─────┐
                        │   Input   │
                        │ Safeguard │
                        └─────┬─────┘
                              │
                        ┌─────┴─────┐
                        │  Intent   │
                        │Classifier │
                        └─────┬─────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │Authorization│   │ Generation  │   │  Insurance  │
    │  Trigger    │   │  Boundary   │   │    Fuse     │
    │  Engine     │   │  Engine     │   │   Engine    │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
                        ┌─────┴─────┐
                        │   Audit   │
                        │   Trail   │
                        │   Logger  │
                        └───────────┘
```

### Components

- **Input Safeguard** — Pre-processes user input to detect prompt injection, PII leakage, and adversarial patterns before downstream processing.
- **Intent Classifier** — Classifies each user utterance along the FCR and RS axes before the agent generates a response.
- **Authorization Trigger Engine** — Applies the Authorization Trigger Decision Table to determine whether generation can proceed freely, requires user authorization, or must escalate.
- **Insurance Fuse Engine** — Monitors cumulative conversation state and severs agent generation privilege when pre-defined compliance thresholds are reached, transferring control to a human operator or deterministic SOP.
- **Generation Boundary Engine** — Enforces pre-generation and post-generation content boundaries per Section 5 of the spec.
- **Audit Trail Logger** — Produces immutable, hash-chained JSON Lines log entries for every decision event including fuse activations.

### Deployment Model

The middleware is designed to run as a **sidecar** — deployed alongside the agent runtime, intercepting requests and responses without requiring modification to the agent or LLM provider. This sidecar model minimizes integration friction:

- The agent code doesn't change.
- The LLM provider doesn't change.
- The middleware enforces governance rules transparently.

## Technology Direction

The reference implementation targets:

- **Language**: Python 3.11+ (initial), with TypeScript/Node.js port planned
- **Deployment**: Docker container, single binary for Lite tier
- **Storage**: SQLite for Lite tier audit logs; PostgreSQL for Standard/Full
- **Configuration**: YAML-based compliance mapping files

## Current State

This directory currently contains only this architecture overview. The reference implementation is under active development and will be published here when ready for early adopters.

## Roadmap

| Milestone | Status |
|-----------|--------|
| Intent Classifier (FCR/RS axes) | Planned |
| Input Safeguard Layer | Planned |
| Authorization Trigger Engine | Planned |
| Insurance Fuse Engine | Planned |
| Generation Boundary Engine | Planned |
| Audit Trail Logger (hash-chained JSONL) | Planned |
| Docker deployment (Lite tier) | Planned |
| Compliance mapping YAML loader | Planned |
| Jurisdiction reference mapping examples | Planned |

## License

MIT — see [LICENSE](../LICENSE).
