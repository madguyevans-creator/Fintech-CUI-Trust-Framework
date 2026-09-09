# Conversational Finance Governance Framework — Specification v0.4

**Status:** Draft  
**Author:** Evans L. Han  
**License:** MIT  
**Also referred to as:** An Open Governance Standard for Conversational Finance Agents  
**Supersedes:** [v0.3](./protocol-spec-v0.3.md) for new implementations. v0.3 remains valid for existing Lite claims until v0.5.

---

## 0. What changed in v0.4

v0.4 does **not** replace the five-layer control plane. It adds three runtime objects the layers operate on, plus a classification-assurance rule.

| Addition | Section | Why |
|----------|---------|-----|
| Action Object (`inform` / `advise` / `commit` / `transact` / `represent`) | 3A | Authority is assigned to the action, not to the utterance or the model. |
| Classification Assurance | 3.4 | Low-confidence classification MUST default to the stricter action. |
| Scoped Credential | 3A.4 | The agent MUST NOT hold durable payment or account secrets. |
| Visible Authority State | 3A.5 | Users MUST be able to see current action class, live permissions, last authorization, and breaker reason. |

Normative v0.3 sections 1–9 remain in force except where this document explicitly tightens them.

---

## 1. Introduction & Scope

### 1.1 Purpose

This document specifies the Conversational Finance Governance Framework — an engineering standard defining **runtime authority** for conversational AI (CUI) agents in Fintech. An implementation conforming to this specification guarantees that, for every agent response generated in a high-stakes Fintech context:

- The turn has been classified by risk level **and** bound to an Action Object **before** generation.
- If classification confidence is below the configured threshold, the implementation **MUST** take the stricter of the candidate actions.
- If the action requires user authorization, the agent **MUST NOT proceed** until authorization is explicitly obtained.
- If the action is `transact` (or a binding `commit` that would execute), the agent **MUST NOT** receive a durable account or card secret. It MAY receive a scoped credential issued after authorization.
- If the content falls within a prohibited generation category, the agent **MUST NOT generate** it.
- If the conversation state reaches pre-defined thresholds, the agent's generation privilege is **severed unconditionally** and control transferred to a human operator or deterministic SOP.
- The current authority state is **visible** to the user.
- Every generation, authorization, escalation, credential issue, and circuit-break decision is logged in an **immutable, verifiable** format.

### 1.2 Scope

This specification covers Fintech CUI only: payments, lending, insurance, collections, KYC/onboarding, BNPL, wallets, remittance, and adjacent consumer-finance surfaces where an agent can inform, advise, commit, transact, or represent.

This specification covers:

- **Action Object** (Section 3A)
- **Authorization Trigger Decision Table** (Section 3)
- **Classification Assurance** (Section 3.4)
- **Authority Circuit Breaker** (Section 4)
- **Generation Boundary Rules** (Section 5)
- **Audit Trail Pipeline Standard** (Section 6)
- **Adoption Tiers** (Section 7)
- **Compliance Mapping Layer** (Section 8)

This specification does **not** cover:

- The choice of LLM or AI model.
- Prompt engineering or model fine-tuning techniques.
- Transport-layer security (TLS, authentication tokens).
- UI/UX design beyond Visible Authority State requirements in Section 3A.5.
- Enterprise strategy, board governance, or organizational adoption models.

### 1.3 Document Conventions

The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are to be interpreted as described in RFC 2119.

---

## 2. Terminology

Terms from v0.3 remain in force. v0.4 adds:

**Action Object** — The unit of runtime authority. One of: `inform`, `advise`, `commit`, `transact`, `represent`. Every classified turn MUST be bound to exactly one Action Object before generation.

**Scoped Credential** — A single-use, amount-capped, time-bounded capability token issued only after a successful AUTH for a `transact` (or executing `commit`). It is not an account number, PAN, or long-lived API secret.

**Visible Authority State** — The user-visible record of the current action class, live permissions, last authorization event, and circuit-breaker reason if any.

**Classification Confidence** — A real number in `[0, 1]` produced with the FCR × RS × Action classification. It is a control input, not a UX score.

**Stricter action** — The action with higher authority cost, in this order: `inform` < `advise` < `commit` < `transact` < `represent`. When FCR/RS cells conflict with action class, the decision table in Section 3.2 still governs FREE / AUTH / ESCALATE; the action class MUST NOT be used to weaken that cell.

---

## 3A. Action Object, Scoped Credential, Visible Authority State

### 3A.1 Action classes

Every conversational turn SHALL be bound to one Action Object:

| Action | Definition | Fintech example | Default authority posture |
|--------|------------|-----------------|---------------------------|
| `inform` | States a fact, schedule, or already-disclosed term. Creates no new obligation and no recommendation. | "The stated fee is 1%." | Usually FREE at F0/R0–R1 |
| `advise` | Recommends a choice the user may take. | "You should repay early." | AUTH or stricter |
| `commit` | States a price, lock, guarantee, or other binding term. | "Your premium is locked at $247.50." | AUTH / ESCALATE |
| `transact` | Would move money, submit an application, or execute a contract. | "Pay the premium now." | AUTH + scoped credential; often ESCALATE |
| `represent` | States a legal, regulatory, or coverage status as if it were a binding representation. | "This product is fully compliant." | ESCALATE / BREAK |

An implementation MUST classify action independently of FCR and RS. The three labels together form the control tuple:

```text
(FCR, RS, Action)
```

### 3A.2 Binding rule

1. Classify FCR and RS per Section 3.1 (v0.3).
2. Classify Action per Section 3A.1.
3. Apply Classification Assurance (Section 3.4).
4. Look up FREE / AUTH / ESCALATE from Section 3.2.
5. Apply mapping overrides (Section 8), including action-level overrides.
6. If the resulting decision is AUTH and Action is `transact` (or executing `commit`), issue a Scoped Credential only after confirmation (Section 3A.4).
7. Publish Visible Authority State (Section 3A.5).
8. Log the full tuple and decision chain (Section 6).

An implementation MUST NOT generate a user-facing `advise`, `commit`, `transact`, or `represent` payload before steps 1–5 complete.

### 3A.3 Action MUST NOT weaken the decision table

If Section 3.2 returns ESCALATE, the implementation MUST ESCALATE even if the action classifier returned `inform`.  
If Section 3.2 returns AUTH, the implementation MUST NOT treat the turn as FREE because the action classifier returned `inform`.

Mapping files MAY raise a cell (FREE→AUTH, AUTH→ESCALATE, ESCALATE→breaker). Mapping files MUST NOT lower a cell without a documented product-line justification in the mapping file itself.

### 3A.4 Scoped Credential

When a turn would execute a `transact` (or a `commit` that causes execution):

1. The agent MUST NOT be given the user's durable PAN, account number, or long-lived payment secret.
2. After explicit AUTH, the implementation MAY issue a scoped credential with at least:
   - `credential_id` (UUID)
   - `session_id`
   - `max_amount`
   - `currency`
   - `merchant_or_rail_scope`
   - `expires_at` (MUST be short-lived; Lite default: 15 minutes)
   - `single_use` (MUST be true in Lite)
3. After use, expiry, denial, escalation, or circuit-break, the credential MUST be revoked.
4. The credential issue, use, and revocation MUST be logged (Section 6).
5. The LLM context MUST receive only the fact that a scoped credential exists and its constraints — not the secret material.

Lite implementations MAY simulate the credential as an opaque token. They still MUST refuse to put raw secrets in the model context.

### 3A.5 Visible Authority State

The user-facing surface MUST expose, at minimum:

| Field | Requirement |
|-------|-------------|
| `action` | Current Action Object |
| `fcr` / `rs` | Current classification |
| `decision` | `free` / `auth_required` / `escalate` / `breaker` |
| `live_permissions` | Which capabilities are currently granted |
| `last_authorization` | Timestamp and summary of the last AUTH, or `none` |
| `breaker_reason` | If the breaker fired, the trigger condition(s) |

The Visible Authority State MAY be a compact status line. It MUST NOT be only an internal log.

---

## 3. Authorization Trigger Decision Table

Section 3.1–3.3 of v0.3 remain normative. They are restated here so v0.4 is self-contained.

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

Action-level mapping overlays (Section 8) MAY further raise cells for `advise`, `commit`, `transact`, and `represent`. They MUST NOT lower a cell below this table.

### 3.3 Authorization Prompt Requirements

When an AUTH trigger fires, the agent MUST:

1. Suspend autonomous generation.
2. Present the user with a clear, neutral summary of the proposed action, including the Action Object and, for `transact`, the scoped-credential constraints.
3. Obtain explicit affirmative confirmation (e.g., "Yes, proceed" — not silence or "OK" in a multi-turn context).
4. Log the authorization event per Section 6.

The authorization prompt MUST NOT:

- Use dark patterns or confusing language to induce authorization.
- Bundle multiple independent authorizations into a single prompt.
- Proceed on ambiguous or non-responsive user input.

### 3.4 Classification Assurance

An implementation MUST produce a confidence value `c ∈ [0, 1]` with every `(FCR, RS, Action)` tuple.

| Condition | Required behavior |
|-----------|-------------------|
| `c < confidence_floor` (Lite default: `0.70`) | MUST NOT FREE. Treat as AUTH at minimum. If either candidate action is `represent` or FCR/RS would ESCALATE, MUST ESCALATE. |
| Two actions within `0.10` confidence | MUST select the stricter action. |
| Action classifier says `inform` but FCR ≥ F2 or RS ≥ R2 | MUST NOT remain `inform`. Rebind to `advise` or stricter before applying Section 3.2. |
| False-negative vs false-positive | An implementation SHOULD bias toward false positives (extra AUTH/ESCALATE) over false negatives (under-classified FREE). |

Classification Assurance is a control-plane rule. It is not a sixth governance layer.

The gold-standard fixtures in [`/tests/classification`](../tests/classification) are RECOMMENDED for conformance testing. They are not themselves a certified benchmark.

---

## 4. Authority Circuit Breaker

v0.3 Section 4 remains normative. v0.4 adds one activation condition:

5. **Action-scope violation**: The agent attempts to perform an action outside the currently granted Visible Authority State, or attempts to use a revoked / expired scoped credential.

When the breaker activates, Visible Authority State MUST show `decision: breaker` and `breaker_reason`.

Default Lite thresholds from v0.3 remain:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `breaker.cumulative_trigger_limit` | 3 | Number of AUTH/ESCALATE events before breaker activates |
| `breaker.vulnerability_detection` | enabled | Whether user vulnerability signals trigger the breaker |
| `breaker.trajectory_window` | 5 | Number of turns to analyze for escalation trajectory |
| `breaker.compliance_proximity` | per-mapping | Configured via Compliance Mapping Layer |
| `confidence_floor` | 0.70 | Classification Assurance floor |

---

## 5. Generation Boundary Rules

v0.3 Section 5 remains normative. v0.4 binds boundaries to Action Objects:

| Category | Typical Action | Notes |
|----------|----------------|-------|
| Financial Commitment | `commit` | MUST NOT be generated as FREE content. |
| Price Guarantee | `commit` | MUST NOT be generated as FREE content. |
| Compliance Representation | `represent` | MUST ESCALATE or BREAK. |
| Discriminatory Output | any | MUST block. |
| Deceptive Output | any | MUST block. |
| Medical/Legal Advice presented as professional advice | `advise` / `represent` | MUST block or ESCALATE. |

Pre-generation enforcement remains MUST. Post-generation enforcement remains SHOULD.

---

## 6. Audit Trail Pipeline

v0.3 Section 6 remains normative. v0.4 extends the log schema:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `action` | Enum | MUST | `inform` / `advise` / `commit` / `transact` / `represent` |
| `classification_confidence` | Number | MUST | `[0, 1]` |
| `visible_authority_state` | Object | MUST | Snapshot of Section 3A.5 at event time |
| `credential_id` | UUID | COND | Present when a scoped credential is issued, used, or revoked |
| `event_type` | Enum | MUST | v0.3 types plus `credential_issued`, `credential_used`, `credential_revoked` |

Immutability, hash-chain, and export requirements are unchanged.

---

## 7. Three-Tier Adoption Model

v0.3 Section 7 remains normative, with these v0.4 Lite additions:

- Default configuration MUST bind every turn to an Action Object.
- Default configuration MUST enable Classification Assurance with `confidence_floor = 0.70`.
- Default configuration MUST refuse to place durable payment secrets in model context.
- Default configuration MUST expose Visible Authority State.

Standard and Full tiers inherit these requirements.

---

## 8. Compliance Mapping Layer

v0.3 Section 8 remains normative. v0.4 mapping files SHALL additionally specify:

| Parameter | Description |
|-----------|-------------|
| `product_line` | `payments` / `lending` / `insurance` / `collections` / other Fintech identifier |
| `action_overrides` | Per-action raises to AUTH / ESCALATE / breaker |
| `scoped_credential` | Amount cap, TTL, single-use flag |
| `confidence_floor` | Override for Classification Assurance |

Reference files:

- [`../mappings/payments.yaml`](../mappings/payments.yaml)
- [`../mappings/lending.yaml`](../mappings/lending.yaml)
- [`../mappings/insurance.yaml`](../mappings/insurance.yaml)
- [`../mappings/collections.yaml`](../mappings/collections.yaml)

These are starting points. They do not constitute legal advice.

---

## 9. Conformance Requirements

v0.3 Section 9 remains normative. v0.4 claims MUST also:

- Specify `action` handling.
- Disclose the `confidence_floor`.
- Disclose whether scoped credentials are real or simulated.
- Disclose how Visible Authority State is exposed.

An implementation SHALL NOT claim v0.4 conformance if it:

- Classifies intent but not Action Object.
- Places durable payment or account secrets in the model context.
- Treats low-confidence classification as FREE.
- Hides breaker activation from the user-facing authority state.

---

## Appendix A: Reference Implementation

A Lite sidecar demonstrating the control plane — no LLM required — is maintained at [`/src`](../src/). It is not the sole compliant instantiation.

## Appendix B: Version History

| Version | Date | Changes |
|---------|------|---------|
| v0.4 | 2026-09-10 | Action Object; Classification Assurance; Scoped Credential; Visible Authority State; product-line mapping examples; Lite sidecar |
| v0.3 | 2026-07-07 | Renamed Insurance Fuse → Authority Circuit Breaker; aligned five-layer names |
| v0.2 | 2026-05-25 | Added Insurance Fuse mechanism |
| v0.1 | 2026-05-21 | Initial draft |
