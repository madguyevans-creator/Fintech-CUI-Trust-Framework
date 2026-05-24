# An Open Governance Standard for Conversational Finance Agents

> An open-source engineering governance standard defining trust boundaries for conversational AI agents in high-stakes domains. MIT Licensed.

## What is this?

An Open Governance Standard for Conversational Finance Agents is an open, MIT-licensed engineering specification that defines the structural governance components a conversational AI agent must implement before being deployed in any context where its outputs could create financial obligations, regulatory exposure, or consumer harm. It is not a software product. It is a public-domain technical specification — analogous to an RFC — that any enterprise with engineering resources can implement.

This standard is engineered under the **AI Native Engineering** paradigm: governance is not retrofitted onto AI systems after deployment as an external audit layer. Governance mechanisms — intent classification, authorization gating, generation boundary enforcement, circuit-breaking, and audit logging — are embedded as structural components from the first line of code. They are properties of the interaction architecture, not post-hoc content filters.

The standard addresses a structural vacuum: as systems shift from graphical user interfaces (GUI) to conversational user interfaces (CUI), AI agents make decisions about what to say, what to promise, and what to authorize. No shared, industry-level specification currently defines the trust boundaries within which these agents must operate.

## Five-Layer Architecture

The standard defines five structural layers, each enforced at a specific point in the agent's generation pipeline:

1. **Input Safeguard Layer** — Pre-processes user input to detect and neutralize prompt injection, PII leakage, and adversarial input patterns before downstream processing.
2. **Intent Classifier Layer** — Classifies each conversational intent along two independent axes: Financial Commitment Risk (F0–F3) and Regulatory Sensitivity (R0–R3).
3. **Authorization Trigger Layer** — Applies the Authorization Trigger Decision Table. If the classified intent requires authorization, the agent suspends generation and obtains explicit user confirmation before proceeding.
4. **Generation Boundary Layer** — Enforces categorical prohibitions at two points: pre-generation (blocking before LLM invocation) and post-generation (suppressing violating output).
5. **Audit Trail Layer** — Produces an immutable, hash-chained, machine-readable log of every generation, authorization, escalation, and circuit-break decision.

## Core Mechanisms

- **Authorization Trigger** — A structured taxonomy of conversational intents that require explicit user authorization before an AI agent may proceed. Intents are classified along two axes: financial commitment risk (F0–F3) and regulatory sensitivity (R0–R3). The trigger fires before the agent generates any response.
- **Generation Boundary** — A categorical specification of content types an agent must never autonomously generate, including financial commitments, price guarantees, compliance representations, and discriminatory or deceptive outputs. Enforced at both pre-generation and post-generation stages.
- **Insurance Fuse** — A circuit-break mechanism that severs the agent's generation privilege in real time when conversation state reaches pre-defined compliance thresholds. Unlike Authorization Trigger, which suspends generation pending user confirmation, Insurance Fuse terminates generation authority outright and transfers control to a human operator or deterministic SOP. Trigger conditions include: cumulative conversation patterns approaching regulatory limits, user vulnerability signals, and multi-turn escalation trajectories exceeding safe bounds.
- **Audit Trail** — A standardized, immutable log format capturing every generation, authorization, escalation, and fuse-trigger decision with full decision-chain traceability, supporting both internal governance and third-party audit.
- **Three-Tier Adoption Model** — Lite (default configuration, zero customization), Standard (designated audit role), and Full (forkable for enterprise integration). The same specification serves both small organizations and large enterprises.

## Core/Mapping Decoupling

A defining architectural property of this standard is the separation of core governance logic from jurisdiction-specific compliance rules. The five layers remain architecturally invariant across deployment contexts. Jurisdiction-specific requirements — retention periods, notification thresholds, additional prohibited content categories — are configured through a Compliance Mapping Layer without modifying the core specification.

## Who is this for?

Any enterprise whose conversational AI agents handle interactions that touch payments, financial commitments, or regulated consumer decisions — including financial institutions, healthcare booking platforms, legal intake services, education enrollment systems, and retail delivery platforms.

## Getting Started

- **Lite** — Read the spec. Deploy the reference implementation with default configuration. Zero customization required.
- **Standard** — Read the spec. Deploy the reference implementation. Assign one person to periodic audit review.
- **Full** — Fork the spec and reference implementation. Integrate with existing compliance infrastructure. Customize the compliance mapping layer.

See [`/spec`](./spec/) for the full specification.

## Repository Structure

```
├── README.md           ← You are here
├── LICENSE             ← MIT
├── spec/               ← The protocol specification (the core artifact)
├── src/                ← Reference implementation
└── background/         ← Research foundation — concept paper, architecture whitepaper, research proposal
```

## Background

- [Concept Paper](./background/concept-paper.pdf) — Academic framing: AI governance framework and trust mechanisms
- [Architecture Whitepaper](./background/architecture-whitepaper.pdf) — The 5-Layer reference architecture
- [Research Proposal](./background/research-proposal.pdf) — Empirical study design: GenAI as process innovation in organizational contexts

## License

MIT — see [LICENSE](./LICENSE).
