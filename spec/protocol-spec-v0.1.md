# An Open Governance Standard for Conversational Finance Agents — Specification v0.2

**Status:** Draft  
**Author:** Evans L. Han  
**License:** MIT  

---

## 1. Introduction & Scope

### 1.1 Purpose

This document specifies An Open Governance Standard for Conversational Finance Agents — an engineering standard defining trust boundaries for conversational AI (CUI) agents. An implementation conforming to this specification guarantees that, for every agent response generated in a high-stakes context:

- The response has been classified by risk level **before** generation.
- If the risk level requires user authorization, the agent **must not proceed** until authorization is explicitly obtained.
- If the content falls within a prohibited generation category, the agent **must not generate** it.
- If the conversation state reaches pre-defined compliance thresholds, the agent's generation privilege is **severed unconditionally** and control transferred to a human operator.
- Every generation, authorization, escalation, and circuit-break decision is logged in an **immutable, verifiable** format.

### 1.2 Scope

This specification covers:

- **Authorization Trigger Matrix** (Section 3): When an agent must obtain user authorization.
- **Insurance Fuse Mechanism** (Section 4): When an agent's generation privilege must be unconditionally severed.
- **Generation Boundary Rules** (Section 5): What an agent must never generate.
- **Audit Trail Standard** (Section 6): How every decision is recorded.
- **Adoption Tiers** (Section 7): Three conformance levels for different organizational scales.
- **Compliance Mapping Layer** (Section 8): How jurisdiction-specific rules are overlaid.

This specification does **not** cover:

- The choice of LLM or AI model.
- Prompt engineering or model fine-tuning techniques.
- Transport-layer security (TLS, authentication tokens). These are the responsibility of the deploying organization.
- UI/UX design of the conversational interface.

### 1.3 Document Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2. Terminology

**Agent** — A software system that uses a generative AI model to conduct conversational interactions with a human user via text or voice.

**Authorization Trigger** — A rule that, when matched by a conversational intent, requires the agent to suspend autonomous generation and request explicit user confirmation before proceeding.

**Insurance Fuse** — A mechanism that severs an agent's generation privilege in real time when conversation state reaches pre-defined compliance thresholds, transferring control to a human operator or deterministic SOP. Distinguished from Authorization Trigger: AT suspends generation pending user confirmation; Insurance Fuse terminates generation authority unconditionally.

**Generation Boundary** — A rule that categorically prohibits the agent from autonomously generating content of a specified type, regardless of user request.

**Conversational Intent** — The identified purpose or goal of a user's utterance within a conversation turn, as classified by the agent's intent recognition system.

**Escalation** — The act of revoking an agent's generation privileges for the current interaction and routing it to a human operator or a deterministic Standard Operating Procedure (SOP).

**Audit Trail** — An immutable, timestamped log of every generation, authorization, escalation, and fuse-trigger decision made by the standard during agent operation.

**Compliance Mapping Layer** — A jurisdiction-specific configuration overlay that maps local regulatory requirements to the standard's core mechanisms, without modifying the core specification.

**SME** — Small or Medium-Sized Enterprise.

---

## 3. Authorization Trigger Matrix

### 3.1 Intent Classification Axes

Every conversational intent SHALL be classified along two independent axes before the agent generates a response:

**Axis 1: Financial Commitment Risk (FCR)**

| Level | Label | Definition | Example |
|-------|-------|------------|---------|
| F0 | Informational | No financial implication | "What are your hours?" |
| F1 | Consideration | User is evaluating options with potential future cost | "How much is the premium plan?" |
| F2 | Conditional Commitment | User is committing contingent on terms | "Book the appointment if my insurance covers it." |
| F3 | Binding Transaction | User is authorizing a payment or entering a financial obligation | "Charge my card for the procedure." |

**Axis 2: Regulatory Sensitivity (RS)**

| Level | Label | Definition | Example |
|-------|-------|------------|---------|
| R0 | General Guidance | No regulated domain | "How do I reset my password?" |
| R1 | Regulated Information | Involves disclosure of terms, policies, or rights | "What happens if I cancel my subscription?" |
| R2 | Consumer Financial Decision | Material to a financial choice by a consumer | "Should I pay off my loan early or invest?" |
| R3 | Compliance Representation | Agent statement could be construed as a binding representation to a regulator | "Is this procedure covered by my plan?" |

### 3.2 Authorization Trigger Decision Table

An implementation MUST apply the following decision matrix. For each (FCR, RS) cell, the table specifies whether the agent:

- **FREE**: May generate autonomously without user authorization.
- **AUTH**: MUST suspend generation and obtain explicit user authorization before proceeding.
- **ESCALATE**: MUST revoke generation privileges and route to a human operator or deterministic SOP.

| FCR ↓ / RS → | R0 (General) | R1 (Regulated Info) | R2 (Consumer Decision) | R3 (Compliance Rep) |
|---------------|-------------|---------------------|----------------------|---------------------|
| **F0 (Informational)** | FREE | FREE | AUTH | AUTH |
| **F1 (Consideration)** | FREE | AUTH | AUTH | ESCALATE |
| **F2 (Conditional)** | AUTH | AUTH | ESCALATE | ESCALATE |
| **F3 (Binding)** | AUTH | ESCALATE | ESCALATE | ESCALATE |

### 3.3 Authorization Prompt Requirements

When an AUTH trigger fires, the agent MUST:

1. Suspend autonomous generation.
2. Present the user with a clear, neutral summary of the proposed action.
3. Obtain explicit affirmative confirmation (e.g., "Yes, proceed" — not silence or "OK" in a multi-turn context).
4. Log the authorization event per Section 6.

The authorization prompt MUST NOT:
- Use dark patterns or confusing language to induce authorization.
- Bundle multiple independent authorizations into a single prompt.
- Proceed on ambiguous or non-responsive user input.

---

## 4. Insurance Fuse Mechanism

### 4.1 Purpose

The Insurance Fuse provides a hard-stop risk boundary. While Authorization Trigger (Section 3) suspends generation pending user confirmation, and Generation Boundary (Section 5) blocks specific content categories, the Insurance Fuse severs the agent's generation privilege unconditionally and transfers control to a human operator or deterministic SOP. It is the mechanism of last resort within the interaction architecture.

### 4.2 Trigger Conditions

An implementation MUST activate the Insurance Fuse when any of the following conditions are met:

1. **Cumulative Pattern Threshold**: The number of AUTH or ESCALATE triggers within a single conversation session exceeds a configurable threshold, indicating that the conversation has moved into a risk domain the agent should not navigate autonomously.
2. **User Vulnerability Signal**: The user's utterances contain explicit markers of distress, confusion, or vulnerability in a context involving financial commitments or regulatory decisions.
3. **Multi-Turn Escalation Trajectory**: The conversation's intent classification trajectory shows progressive movement toward higher-risk (FCR, RS) cells across successive turns, even if no single turn independently triggers ESCALATE.
4. **Compliance Boundary Proximity**: The conversation context — including cumulative interaction patterns such as communication frequency, timing, and content type — approaches pre-defined regulatory limits configured in the active Compliance Mapping Layer.

### 4.3 Fuse Activation Behavior

When the Insurance Fuse activates, the implementation MUST:

1. Immediately terminate the agent's generation privilege for the current session.
2. Log the fuse activation event per Section 6, including the specific trigger condition(s) met and the conversation state at the point of activation.
3. Transfer control to a human operator or a deterministic SOP. The transfer MUST include the full conversation context and the fuse activation reason.
4. The agent MUST NOT resume generation within the same session.

### 4.4 Configuration

The Insurance Fuse threshold parameters SHALL be configurable through the Compliance Mapping Layer (Section 8). Default thresholds are defined in the Lite tier configuration:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `fuse.cumulative_trigger_limit` | 3 | Number of AUTH/ESCALATE events before fuse activates |
| `fuse.vulnerability_detection` | enabled | Whether user vulnerability signals trigger the fuse |
| `fuse.trajectory_window` | 5 | Number of turns to analyze for escalation trajectory |
| `fuse.compliance_proximity` | per-jurisdiction | Configured via Compliance Mapping Layer |

---

## 5. Generation Boundary Rules

### 5.1 Prohibited Content Categories

An implementation MUST NOT autonomously generate content in any of the following categories. If a user request triggers a prohibited category, the agent SHALL either refuse to generate and explain why, or escalate to a human operator.

| Category | Definition | Example of Prohibited Generation |
|----------|------------|----------------------------------|
| **Financial Commitment** | Any statement that binds the user or the enterprise to a financial obligation | "Your total will be $247.50." |
| **Price Guarantee** | Any unconditional or absolute statement about current or future pricing | "This price will never go up." |
| **Compliance Representation** | Any statement about the legal or regulatory status of a product, service, or transaction | "This plan is fully compliant with applicable regulations." |
| **Discriminatory Output** | Any content that differentiates users on protected characteristics | Differential pricing or service descriptions based on inferred demographics. |
| **Deceptive Output** | Any content that misleads, omits material information, or implies false urgency | "Only 1 left!" when inventory is not tracked. |
| **Medical/Legal Advice** | Any content that could be construed as professional advice in regulated professions | "You should take this medication." |

### 5.2 Boundary Enforcement Points

Generation boundaries SHALL be enforced at two points:

1. **Pre-generation**: Intent classification (Section 3.1) triggers a boundary check. If the classified intent maps to a prohibited category, generation is blocked before the LLM is invoked.
2. **Post-generation**: The generated output is scanned against prohibited category patterns. If a match is detected, the output is suppressed and either replaced with a safe fallback message or escalated.

An implementation SHOULD enforce boundaries at both points. An implementation MUST enforce at minimum pre-generation boundaries.

### 5.3 Safe Fallback Messages

When generation is blocked by a boundary rule, the agent SHALL respond with a neutral fallback message that does not itself violate any boundary. Example:

> "I'm not able to answer that directly. Let me connect you with someone who can help."

---

## 6. Audit Trail Standard

### 6.1 Log Entry Schema

Every generation, authorization, escalation, and fuse-trigger event SHALL produce a log entry with the following fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `event_id` | UUID | MUST | Unique identifier for this event |
| `timestamp` | ISO 8601 | MUST | When the event occurred (UTC) |
| `session_id` | UUID | MUST | Identifier for the conversation session |
| `event_type` | Enum | MUST | One of: `generation`, `authorization_request`, `authorization_granted`, `authorization_denied`, `escalation`, `boundary_block`, `fuse_activation` |
| `intent_classification` | Object | MUST | `{fcr_level: "F0"-"F3", rs_level: "R0"-"R3", intent_label: string}` |
| `trigger_decision` | Enum | MUST | One of: `free`, `auth_required`, `escalate`, `fuse` |
| `user_input_summary` | String | MUST | Hashed or summarized user utterance (MUST NOT store raw PII) |
| `agent_response_summary` | String | MUST | Hash or summary of generated response |
| `decision_chain` | Array | SHOULD | Ordered list of protocol decisions leading to this event |
| `operator_id` | String | COND | Identifier of human operator if escalation or fuse activation occurred |
| `compliance_mapping_id` | String | SHOULD | Identifier of the active compliance mapping configuration |

### 6.2 Immutability Requirements

The audit trail MUST be:

1. **Append-only**: Entries cannot be modified or deleted after creation.
2. **Ordered**: Entries carry sequence numbers or timestamps establishing total order within a session.
3. **Verifiable**: A cryptographic hash chain links each entry to its predecessor. `entry_n.hash = SHA-256(entry_n.data + entry_{n-1}.hash)`.
4. **Exportable**: The log format SHALL be machine-readable (JSON Lines) and exportable for third-party audit without requiring access to the agent's runtime environment.

### 6.3 Retention

Logs SHALL be retained for a minimum period defined by the active compliance mapping configuration. In the absence of a jurisdiction-specific retention requirement, the default minimum is 7 years.

---

## 7. Three-Tier Adoption Model

### 7.1 Lite Tier

**Target**: Single-proprietor SME with no dedicated IT or compliance staff.

**Requirements for conformance**:
- Deploy the standard's reference implementation with default configuration.
- The default configuration MUST pre-enable all Authorization Triggers at F2+ or R2+ levels.
- The default configuration MUST pre-enable all Generation Boundary categories.
- The default configuration MUST pre-enable the Insurance Fuse with default thresholds.
- Audit trail MUST be enabled with append-only logging to local storage.
- No customization is required.

**Limitations**:
- Audit trail is stored locally. The SME is responsible for backup.
- Compliance mapping is limited to the default baseline. Additional jurisdiction-specific mappings are not included.

### 7.2 Standard Tier

**Target**: SME with dedicated operations or compliance staff (even part-time).

**Requirements for conformance**:
- All Lite requirements.
- One designated individual SHALL perform periodic review of the audit trail (minimum: monthly).
- Compliance mapping layer SHALL be configured for the organization's jurisdiction(s) of operation.
- Review findings SHALL be documented and retained.

### 7.3 Full Tier

**Target**: Enterprise with in-house engineering and legal/compliance teams.

**Requirements for conformance**:
- All Standard requirements.
- Organization MAY fork the specification and reference implementation.
- Custom compliance mapping configurations MAY be developed for the organization's full regulatory footprint.
- Integration with existing SIEM, GRC, or compliance infrastructure is RECOMMENDED.
- Conformance with the core Authorization Trigger Matrix, Insurance Fuse, and Generation Boundary Rules MUST be preserved. An implementation that weakens or removes a trigger, fuse, or boundary defined in Sections 3, 4, and 5 SHALL NOT claim conformance.

---

## 8. Compliance Mapping Layer

### 8.1 Concept

The standard's core mechanisms (Sections 3–6) are **jurisdiction-agnostic**. A compliance mapping configuration overlays jurisdiction-specific requirements onto the core without modifying it. This decoupling is a structural property of the architecture.

### 8.2 Mapping Schema

A compliance mapping configuration SHALL specify:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `jurisdiction_id` | Identifier for the regulatory regime | `sg-mas`, `id-ojk` |
| `trigger_overrides` | Adjustments to the Authorization Trigger decision table | Elevate F1+R1 from AUTH to ESCALATE for stricter regimes |
| `boundary_additions` | Additional prohibited content categories | "Interest rate predictions" for banking regulators |
| `fuse_overrides` | Adjustments to Insurance Fuse thresholds | Lower cumulative trigger limit for stricter regimes |
| `retention_period_days` | Audit log retention requirement | 2555 (7 years) default |
| `audit_export_format` | Required format for third-party audit submission | `jsonl`, `csv`, `pdf` |
| `notification_requirements` | Events that must trigger regulator notification | "Any fuse activation event within 24 hours" |

### 8.3 Reference Mappings

Reference compliance mapping configurations for common regulatory frameworks will be published alongside this specification as they are developed and validated through deployment. These are provided as starting points and do not constitute legal advice.

---

## 9. Conformance Requirements

### 9.1 Conformance Levels

An implementation MAY claim conformance at one of three tiers: **Lite**, **Standard**, or **Full** (per Section 7).

### 9.2 Mandatory Claims

Any claim of conformance MUST:

- Specify the conformance tier.
- Specify the specification version (e.g., v0.2).
- List any compliance mapping configurations applied.
- Disclose any deviations from the core Authorization Trigger Matrix, Insurance Fuse, or Generation Boundary Rules.

### 9.3 Prohibited Claims

An implementation SHALL NOT claim conformance if it:

- Disables or weakens any Authorization Trigger specified in Section 3.2 without documented jurisdiction-specific justification in the compliance mapping layer.
- Disables or weakens the Insurance Fuse specified in Section 4.
- Removes any Generation Boundary category specified in Section 5.1.
- Does not maintain an append-only, verifiable audit trail per Section 6.2.
- Uses "An Open Governance Standard for Conversational Finance Agents" branding for a system that substitutes the core trust-boundary mechanisms with alternative approaches not conforming to this specification.

---

## Appendix A: Reference Implementation

A reference implementation conforming to the Lite tier is maintained at [`/src`](../src/). It demonstrates engineering feasibility and serves as a starting point for adopters. It is not the sole compliant instantiation of this specification.

## Appendix B: Empirical Foundation

The core-to-mapping-layer decoupling described in Section 8 has been empirically validated across multiple jurisdictions with fundamentally different financial consumer protection regimes. In all deployment contexts, the core Authorization Trigger Matrix, Insurance Fuse, and Generation Boundary Rules remained architecturally identical. Only the compliance mapping layer required jurisdiction-specific configuration.

## Appendix C: Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.2 | 2026-05-25 | Added Insurance Fuse mechanism (Section 4); updated specification name throughout; renumbered sections 4–9; added fuse_activation to Audit Trail event types |
| v0.1 | 2026-05-21 | Initial draft — core mechanisms, decision tables, conformance requirements |
