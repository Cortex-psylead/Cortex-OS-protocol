# 🏛️ Protocol Governance
**Cortex Protocol — Governance Framework v1.2**

This document defines how the Cortex Protocol is governed as an open standard. It establishes roles, validation processes, anti-capture mechanisms, and — critically — the limits of what governance can guarantee.

For foundational constitutional principles, see [GOVERNANCE-BASE.md](GOVERNANCE-BASE.md). For technical enforcement at runtime, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Governance Philosophy

The Cortex Protocol is a decentralized open standard, not a corporate product. Its governance rests on a single principle: **clinical safety parameters are maintained by the institutions best qualified to define them, not by those with commercial incentives to compromise them.**

But governance is not a complete solution. This document is explicit about what governance can and cannot guarantee — because a governance framework that overstates its own power is itself a form of capture.

---

## The Three Governance Bodies

### 1. ⚕️ White Branch (Clinical Authority)

**Composition:** Licensed mental health professionals, neuropsychologists, and neuroscience researchers.

**Authority:** Exclusive, non-delegable authority over:
- All numerical thresholds in `ClinicalThresholds` and `ClinicalBridge`
- Approval or rejection of any Clinical Capability Module (CCM)
- CDI reset protocol and Voluntary Activation Mode parameters
- Any modification to Clinical Bridge validation logic
- Annual review of LIMES entropy assumptions (see DISCLAIMER §4.1)

**Technical enforcement:** Commits modifying clinical threshold files require a GPG signature from a registered White Branch member key. Unsigned modifications are rejected.

**White Branch accountability:** Every threshold must carry a peer-reviewed bibliographic citation. Every modification must be versioned, publicly documented, and open to 30-day community comment before merging. The White Branch has authority because it shows its work — not because it declares authority.

**What the White Branch does NOT control:** Implementation architecture, programming language choices, or performance optimizations that do not affect clinical safety margins.

---

### 2. 🛡️ Protocol Stewards (Technical Branch)

**Composition:** Engineers, systems architects, open-source contributors.

**Authority:**
- Implementing the SAL, CDI, and Clinical Bridge as specified by the White Branch
- Maintaining the reference implementation and module SDK
- Reviewing pull requests for technical correctness, security, and hardware-agnosticism
- Publishing and versioning the standard specification
- Implementing the User-Verifiable Audit Protocol (Milestone 2)

**Constraint:** The Technical Branch cannot override a White Branch clinical decision. Technical necessity does not justify modifying clinical thresholds.

---

### 3. ⚖️ Legal Validator (Adscribed to the White Branch)

**Composition:** Legal professionals specializing in health data law, AI regulation, and digital rights.

**Authority:**
- Legal certification that CCMs comply with applicable law
- Review of DISCLAIMER and USER-DATA-MODEL for jurisdictional accuracy
- Advisory opinions on regulatory developments
- Annual review of the operator risk model (Section 5)

**Constraint:** No authority over clinical methodology. Legal risk management does not override clinical judgment.

---

## Governance Nodes: The Institutional Layer

Governance Nodes are the external institutional partners that distribute the protocol's authority across independent institutions.

**A Governance Node is:** A university faculty, professional association, or research center formally joined to the governance network, holding a GPG keypair for signing Clinical Capability Modules.

**What a Governance Node does:**
- Issues signed CCMs authorizing specific protocol capabilities
- Participates in the Annual Review Cycle with peer-reviewed evidence
- Maintains a hardware whitelist for their deployment context
- Provides institutional credibility for regulatory submissions

**What a Governance Node does NOT do:**
- Hold veto power over other nodes' decisions
- Represent commercial interests in governance processes
- Self-certify products it manufactures or sells

**Current Governance Nodes:** *(None — Milestone 1 objective)*

---

## The Validation Loop

```
[Proposal submitted as Issue]
         ↓
[Phase 1: Clinical Audit — White Branch]
  ↙ Rejected              ↘ Approved with citation
[Closed]         [Phase 2: Legal Validation]
                   ↙ Legal issue    ↘ Cleared
               [Revised]    [Phase 3: Technical Review]
                              ↙ Issue    ↘ Approved
                          [Revised]  [30-day public comment]
                                            ↓
                                    [Merged + Version increment]
```

Phase 1 is mandatory and cannot be bypassed.

---

## Annual Review Cycle

1. **Month 1:** Call for evidence — including LIMES entropy assumptions and LOGOS thresholds
2. **Months 2–3:** Governance Node submissions with bibliographic support
3. **Month 4:** White Branch review and vote
4. **Month 5:** 30-day public comment
5. **Month 6:** Standard update with MINOR version increment

Signed manifests expire after 12 months. Renewal requires Annual Review participation.

---

## Anti-Capture Provisions

Permanent. Changes require White Branch consensus, ≥ 2 active Governance Nodes, and a MAJOR version increment.

**1. No cloud processing of biometric data.**
Automatically rejected regardless of justification.

**2. Clinical Supremacy.**
Commercial logic, engagement optimization, and performance targets cannot override a signed CCM.

**3. Evidence Transparency.**
Every clinical threshold must link to a publicly accessible peer-reviewed reference. Thresholds without citation are invalid.

**4. Hardware Independence.**
No manufacturer may hold a governance role certifying their own products. No contribution may create vendor dependency.

**5. User Sovereignty is Unconditional.**
No governance decision may restrict the user's Kill Switch. The protocol serves the user.

**6. Module Boundary Discipline.**

| Module | Owns | SHALL NOT include |
| :--- | :--- | :--- |
| **CORTEX** | Biological safety | Identity, consent, hardware attestation, cognitive monitoring |
| **LIMES** | Human liveness proof | Health monitoring, consent records, hardware sealing, cognitive tracking |
| **ETHOS** | Dynamic consent | Liveness proofs, biometric analysis, hardware attestation, delegation tracking |
| **KEROS** | Hardware attestation | Biological monitoring, identity proofs, consent records, cognitive metrics |
| **LOGOS** | Cognitive integrity | Biometric monitoring, identity proofs, consent records, hardware sealing |

A proposal merging two modules requires peer-reviewed clinical justification that separation causes measurable patient harm.

---

## The Operator Threat Model

The Anti-Capture Provisions protect against AI systems acting against user interests. They do not automatically protect against human operators who deploy the protocol in bad faith. This section names that risk explicitly.

### Identified Operator Risk Vectors

**Workplace surveillance:** An institution requiring employees to use Cortex-certified devices and using CDI data as a performance or compliance metric without employees understanding this.

**Clinical boundary violations:** A clinical operator accessing session audit logs beyond their declared purpose, or sharing data outside the consent scope.

**Threshold manipulation:** A platform claiming compliance while running non-standard threshold configurations that reduce CDI sensitivity to avoid blocking engagement-driven features.

**Consent theater:** An implementation presenting consent requests to users in states of limited capacity and recording the consent as valid.

### Current Mitigations and Their Limits

The Anti-Capture Provisions reduce operator risk. They do not eliminate it. Current mitigations are institutional — they depend on the integrity of the White Branch, the independence of Governance Nodes, and the good faith of implementers. None of these can be cryptographically enforced at present.

This is an acknowledged gap. The protocol names it because a governance framework that presents itself as a complete solution when it is not is a form of the problem it claims to solve.

### User-Verifiable Audit Protocol (Planned — Milestone 2)

The long-term solution is a mechanism by which the user — not the Governance Node, not the operator — can independently verify that the active implementation operates within the parameters declared to them.

The User-Verifiable Audit Protocol (UVAP) will allow any user to:
- Query the active threshold configuration and compare it against the signed standard
- Verify that consent records match what they authorized
- Confirm that no data has been transmitted beyond declared boundaries

UVAP is a Milestone 2 deliverable and a prerequisite for Level 3 (Full Pentagon Compliant) certification.

---

## Voluntary Activation Mode (VAM)

The CDI monitors autonomic arousal as a proxy for pathological stress. High arousal can also indicate voluntary high-intensity cognitive engagement — flow states, deliberate focused work. The CDI does not currently distinguish between these states.

**VAM allows a user to explicitly declare a high-intensity session** where CDI thresholds are elevated with documented consent:
- Requires explicit user activation — not the default state
- Records activation in audit log with timestamp and declared duration
- Does not disable monitoring — recalibrates it to the user's declared context
- Auto-expires at declared duration end
- Cannot be activated when ETHOS capacity is NONE (dorsal vagal state)

VAM parameters are defined by the White Branch in domain-specific CIT specifications. They are not user-configurable beyond declared presets.

---

## Conflict Resolution

**White Branch vs. Technical Branch:** Technical Branch documents conflict as `[Governance-Conflict]` Issue. White Branch has 14 days to respond with written clinical justification. If unresolved, an active Governance Node provides a binding independent opinion.

**Between Governance Nodes:** Conflicting positions published in Annual Review Cycle. White Branch makes final determination based on weight of evidence. Dissenting Node's position documented in changelog.

---

*Governance Framework v1.2 — Protocol Stewards under White Branch oversight.*
*Modifications to Anti-Capture Provisions require the consensus process defined above.*
