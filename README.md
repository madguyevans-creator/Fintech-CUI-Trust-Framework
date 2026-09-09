# Conversational Finance Governance Framework

> An open-source, model-agnostic, engineering-level governance protocol for conversational AI in financial contexts. Also referred to as An Open Governance Standard for Conversational Finance Agents. MIT Licensed.

**Current specification:** [v0.4](./spec/protocol-spec-v0.4.md)  
**Prior specification:** [v0.3](./spec/protocol-spec-v0.3.md)

## What is this?

The Conversational Finance Governance Framework is an open, MIT-licensed engineering specification that defines the structural governance components a conversational AI agent must implement before being deployed in any Fintech context where its outputs could create financial obligations, regulatory exposure, or consumer harm. It is not a software product. It is a public technical specification — analogous to an RFC — that any organization with engineering resources can implement.

This framework is engineered under the **AI Native Engineering** paradigm: governance is not retrofitted onto AI systems after deployment as an external audit layer. Governance mechanisms — intent classification, action-level authority control, authorization gating, generation boundary enforcement, scoped credentials, circuit-breaking, and audit logging — are embedded as structural components of the interaction architecture.

The framework addresses a structural gap: as systems shift from graphical user interfaces (GUI) to conversational user interfaces (CUI), AI agents make decisions about what to say, what to promise, and what to authorize. No shared, industry-level specification currently defines the **runtime authority** within which these agents must operate.

Scope is **Fintech CUI only**: payments, lending, insurance, collections, KYC/onboarding, BNPL, wallets, and remittance — any conversational surface where an agent can inform, advise, commit, transact, or make a compliance representation. This is not a general-purpose assistant protocol.

## Architecture

```
User → [Agent Runtime] → [Protocol Middleware] → [LLM]
                              │
                        ┌─────┴─────┐
                        │  Intent   │
                        │Classification│
                        │  Matrix   │
                        └─────┬─────┘
                              │
                        ┌─────┴─────┐
                        │  Action   │
                        │  Object   │
                        └─────┬─────┘
                              │
           ┌──────────────────┼──────────────────┐
           │                  │                  │
    ┌──────┴──────┐   ┌──────┴──────┐   ┌──────┴──────┐
    │Authorization│   │ Generation  │   │  Authority  │
    │  Trigger    │   │  Boundary   │   │  Circuit    │
    │ + Scoped    │   │             │   │  Breaker    │
    │ Credential  │   │             │   │             │
    └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
           │                  │                  │
           └──────────────────┼──────────────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
        ┌─────┴─────┐  ┌──────┴──────┐
        │   Audit   │  │  Visible    │
        │   Trail   │  │  Authority  │
        │  Pipeline │  │  State      │
        └───────────┘  └─────────────┘
```

## Five-Layer Architecture (unchanged control plane)

v0.4 does **not** replace the five layers. It adds three runtime objects that the layers operate on.

1. **Intent Classification Matrix** — Classifies each conversational turn along two independent axes: Financial Commitment Risk (F0–F3) and Regulatory Sensitivity (R0–R3), before any response is generated. v0.4 adds a Classification Assurance rule: low-confidence classifications MUST default to the stricter action.
2. **Authorization Trigger** — Applies the Authorization Trigger Decision Table. If the classified action requires authorization, the agent suspends generation and obtains explicit user confirmation before proceeding.
3. **Generation Boundary** — Constrains the model's permissible response space before a user-facing answer is delivered. Enforced at pre-generation and post-generation stages.
4. **Audit Trail Pipeline** — Produces an immutable, hash-chained, machine-readable log of every generation, authorization, escalation, credential issue, and circuit-break decision.
5. **Authority Circuit Breaker** — Severs the agent's generation privilege in real time when conversation state reaches pre-defined thresholds, and transfers control to a human operator or deterministic SOP.

## v0.4 runtime objects

- **Action Object** — The unit of control is no longer “intent” alone. Every turn is bound to one of: `inform`, `advise`, `commit`, `transact`, `represent`. Authority is assigned to the action, not to the model.
- **Scoped Credential** — For `transact` (and any binding `commit` that would execute), the agent MUST NOT receive a durable account or card secret. It MAY receive a single-use, amount-capped, time-bounded credential issued after authorization.
- **Visible Authority State** — The user-facing control surface MUST expose the current action class, which permissions are live, the last authorization, and — if triggered — the circuit-breaker reason.

## Core/Mapping Decoupling

The five layers remain architecturally invariant across Fintech products. Product-line requirements — which actions are free, which require authorization, which must escalate or break — are configured through a Compliance Mapping Layer without modifying the core specification.

Reference mappings (not legal advice):

- [`mappings/payments.yaml`](./mappings/payments.yaml)
- [`mappings/lending.yaml`](./mappings/lending.yaml)
- [`mappings/insurance.yaml`](./mappings/insurance.yaml)
- [`mappings/collections.yaml`](./mappings/collections.yaml)

The same utterance can compile to different authority decisions under different mappings. That is intended.

## Who is this for?

Any organization whose conversational AI agents handle Fintech interactions that touch payments, credit, insurance, collections, onboarding, or other regulated consumer-finance decisions.

## Getting Started

- **Lite** — Read the spec. Run the sidecar against a mapping file. No model required for the control-plane demo.
- **Standard** — Assign periodic audit-trail review. Load a product-line mapping.
- **Full** — Fork the spec and sidecar. Integrate with existing compliance infrastructure. Customize the mapping layer. Do not weaken core triggers, boundaries, or the breaker.

```bash
cd src
python3 -m pip install -r requirements.txt
python3 -m cf_gov.sidecar --mapping ../mappings/payments.yaml --utterance "What's the fee for sending 200 dollars?"
python3 -m cf_gov.sidecar --mapping ../mappings/lending.yaml --utterance "Should I take the loan?"
```

See [`/spec/protocol-spec-v0.4.md`](./spec/protocol-spec-v0.4.md) for the full specification and [`/src`](./src/) for the Lite sidecar.

## Repository Structure

```
├── README.md                 ← You are here
├── LICENSE                   ← MIT
├── spec/                     ← Protocol specification (v0.3, v0.4)
├── src/                      ← Lite sidecar (control plane)
├── mappings/                 ← Product-line mapping examples
├── tests/                    ← Classification gold standard + sidecar tests
└── background/               ← Research foundation documents
```

## Background

- [Concept Paper](./background/concept-paper.pdf) — Academic framing
- [Architecture Whitepaper](./background/architecture-whitepaper.pdf) — Five-layer reference architecture
- [Research Proposal](./background/research-proposal.pdf) — Empirical study design

These documents describe the research framing. The normative artifact is the specification.

## License

MIT — see [LICENSE](./LICENSE).
