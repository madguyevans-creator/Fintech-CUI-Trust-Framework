# Human-AI Symbiosis Protocol

> An open-source engineering protocol defining trust boundaries for conversational AI agents. MIT Licensed.

## What is this?

The Human-AI Symbiosis Protocol is an open, MIT-licensed engineering specification that defines **when** a conversational AI agent must obtain explicit user authorization and **what** it must never autonomously generate. It is not a software product. It is a public-domain technical specification — analogous to an RFC — that any enterprise with engineering resources can implement.

The protocol addresses a structural vacuum: as U.S. businesses shift from graphical user interfaces (GUI) to conversational user interfaces (CUI), AI agents are making decisions about what to say, what to promise, and what to authorize. There is currently no shared, industry-level standard defining the trust boundaries within which these agents should operate. This protocol fills that vacuum.

## Core Mechanisms

- **Authorization Trigger** — A structured taxonomy of conversational intents that require explicit user authorization before an AI agent may proceed. Intents are classified along two axes: financial commitment risk and regulatory sensitivity.
- **Generation Boundary** — A categorical specification of content types an agent must never autonomously generate, including financial commitments, price guarantees, compliance representations, and discriminatory or deceptive outputs.
- **Audit Trail** — A standardized, immutable log format capturing every generation, authorization, and escalation decision with full decision-chain traceability, enabling both internal governance and third-party audit.
- **Three-Tier Adoption Model** — Lite (zero-config, pre-configured triggers for high-risk intents), Standard (designated audit role), and Full (forkable for enterprise integration). The same protocol works for a dental practice with three employees and a regional delivery platform with three hundred.

## Who is this for?

Any enterprise whose conversational AI agents handle interactions that touch payments, financial commitments, or regulated consumer decisions — including healthcare booking platforms, legal intake services, education enrollment systems, retail delivery platforms, and community financial institutions. You do not need to be a fintech company. If your chatbot or voice agent ever says something that could cost your customer money, this protocol is for you.

## Getting Started

- **Lite** — Read the spec. Deploy the reference implementation with default configuration. Zero customization required. Suitable for single-proprietor SMEs who want compliance-grade guardrails out of the box.
- **Standard** — Read the spec. Deploy the reference implementation. Assign one person to periodic audit review of the audit trail. Suitable for SMEs with dedicated operations staff.
- **Full** — Fork the spec and reference implementation. Integrate with your existing compliance infrastructure. Customize the compliance mapping layer for your jurisdiction. Suitable for enterprises with in-house engineering and legal teams.

See [`/spec`](./spec/) for the protocol specification.

## Repository Structure

```
├── README.md           ← You are here
├── LICENSE             ← MIT
├── spec/               ← The protocol specification (the core artifact)
├── src/                ← Reference implementation
└── background/         ← Research foundation — concept paper, architecture whitepaper, research proposal
```

## Background

The protocol builds on empirical validation across five Asia-Pacific markets with fundamentally different financial consumer protection regimes — Singapore (MAS), Indonesia (OJK), Malaysia, the Philippines, and Thailand — where the core trust-boundary logic remained architecturally identical and only jurisdiction-specific compliance mapping required configuration.

- [Concept Paper](./background/concept-paper.pdf) — Academic framing: Fintech AI Governance and Human-AI Symbiosis (TOE + TAM framework)
- [Architecture Whitepaper](./background/architecture-whitepaper.pdf) — The 5-Layer Trust & Routing reference architecture that informed the protocol
- [Research Proposal](./background/research-proposal.pdf) — Empirical study design: GenAI as Process Innovation in organizational contexts

## License

MIT — see [LICENSE](./LICENSE).
