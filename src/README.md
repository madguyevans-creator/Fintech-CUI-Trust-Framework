# Reference Implementation

**Status:** Pre-release (architecture defined, implementation in progress)  
**License:** MIT  

## Overview

This directory will contain the reference implementation of the Human-AI Symbiosis Protocol as defined in [`/spec/protocol-spec-v0.1.md`](../spec/protocol-spec-v0.1.md).

The reference implementation is a deployable middleware that sits between a conversational AI agent and its users, enforcing the protocol's Authorization Triggers, Generation Boundaries, and Audit Trail requirements at runtime. It is not the sole compliant instantiation of the protocol — any implementation conforming to the specification may claim protocol conformance.

## Architecture

```
User → [Agent Runtime] → [Protocol Middleware] → [LLM]
                              │
                        ┌─────┴─────┐
                        │  Intent   │
                        │Classifier │
                        └─────┬─────┘
                              │
                   ┌──────────┴──────────┐
                   │                     │
            ┌──────┴──────┐      ┌──────┴──────┐
            │Authorization│      │ Generation  │
            │  Trigger    │      │  Boundary   │
            │  Engine     │      │  Engine     │
            └──────┬──────┘      └──────┬──────┘
                   │                     │
                   └──────────┬──────────┘
                              │
                        ┌─────┴─────┐
                        │   Audit   │
                        │   Trail   │
                        │   Logger  │
                        └───────────┘
```

### Components

- **Intent Classifier** — Classifies each user utterance along the FCR and RS axes before the agent generates a response.
- **Authorization Trigger Engine** — Applies the Authorization Trigger Decision Table to determine whether generation can proceed freely, requires user authorization, or must escalate.
- **Generation Boundary Engine** — Enforces pre-generation and post-generation content boundaries per Section 4 of the spec.
- **Audit Trail Logger** — Produces immutable, hash-chained JSON Lines log entries for every decision event.

### Deployment Model

The middleware is designed to run as a **sidecar** — deployed alongside the agent runtime, intercepting requests and responses without requiring modification to the agent or LLM provider. This sidecar model is chosen to minimize integration friction for SMEs:

- The agent code doesn't change.
- The LLM provider doesn't change.
- The middleware enforces protocol rules transparently.

## Technology Direction

The reference implementation targets:

- **Language**: Python 3.11+ (initial), with TypeScript/Node.js port planned
- **Deployment**: Docker container, single binary for Lite tier
- **Storage**: SQLite for Lite tier audit logs; PostgreSQL for Standard/Full
- **Configuration**: YAML-based compliance mapping files

## Current State

This directory currently contains only this architecture overview. The reference implementation is under active development and will be published here when ready for early adopters.

## Roadmap

| Milestone | Target | Status |
|-----------|--------|--------|
| Intent Classifier (FCR/RS axes) | — | Planned |
| Authorization Trigger Engine | — | Planned |
| Generation Boundary Engine | — | Planned |
| Audit Trail Logger (hash-chained JSONL) | — | Planned |
| Docker deployment (Lite tier) | — | Planned |
| Compliance mapping YAML loader | — | Planned |
| California DFPI reference mapping | — | Planned |
| New York NYDFS reference mapping | — | Planned |

## License

MIT — see [LICENSE](../LICENSE).
