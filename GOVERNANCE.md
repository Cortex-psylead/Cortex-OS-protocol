# 🏛️ Protocol Governance
**Cortex Protocol — Governance Framework v1.1**

This document defines how the Cortex Protocol is governed as an open standard. It establishes the roles, validation processes, and anti-capture mechanisms that ensure no single entity controls the clinical safety parameters of the protocol.

For the foundational constitutional principles, see [GOVERNANCE-BASE.md](GOVERNANCE-BASE.md). For the technical enforcement of governance at runtime, see [ARCHITECTURE.md](ARCHITECTURE.md).

---

## Governance Philosophy

The Cortex Protocol is a decentralized open standard, not a corporate product. Its governance model is designed around a single principle: **clinical safety parameters are maintained by the institutions best qualified to define them — clinical and research institutions — not by the organizations that have commercial incentives to compromise them.**

This is enforced architecturally (through signed Clinical Capability Modules) and institutionally (through the three-body governance structure below).

---

## The Three Governance Bodies

### 1. ⚕️ White Branch (Clinical Authority)

**Composition:** Licensed mental health professionals, neuropsychologists, and neuroscience researchers.

**Authority:** The White Branch holds exclusive, non-delegable authority over:
- All numerical thresholds in `ClinicalThresholds` and `ClinicalBridge`
- Approval or rejection of any Clinical Capability Module (CCM)
- Definition of the CDI reset protocol
- Any modification to the Clinical Bridge validation logic

**How authority is exercised technically:** Commits modifying `ClinicalThresholds`, `ClinicalBridge`, or any document in the clinical specification require a GPG signature from a registered White Branch member key. Unsigned modifications to these files are rejected by the contribution process.

**What the White Branch does NOT control:** Implementation choices that do not affect clinical safety margins (e.g., code architecture, programming language, performance optimizations).

---

### 2. 🛡️ Protocol Stewards (Technical Branch)

**Composition:** Engineers, systems architects, and open-source contributors.

**Authority:** The Technical Branch is responsible for:
- Implementing the SAL, CDI, and Clinical Bridge as specified by the White Branch
- Maintaining the reference implementation and SDK
- Reviewing pull requests for technical correctness, security, and hardware-agnosticism
- Publishing and versioning the standard specification

**Constraint:** The Technical Branch cannot override a White Branch clinical decision. If a clinical threshold creates a technical challenge, the Technical Branch raises it as a proposal to the White Branch — it does not implement a unilateral override.

---

### 3. ⚖️ Legal Validator (Adscribed to the White Branch)

**Composition:** Legal professionals specializing in health data law, AI regulation, and digital rights.

**Authority:** The Legal Validator provides:
- Legal signature certifying that Clinical Capability Modules comply with applicable law (GDPR, Ley 1581/2012, AI Act, neuro-rights legislation)
- Review of the DISCLAIMER and USER-DATA-MODEL for jurisdictional accuracy
- Advisory opinions on regulatory developments affecting the standard

**Constraint:** The Legal Validator has no authority over clinical methodology or safety threshold values. Legal risk management does not override clinical judgment.

---

## Governance Nodes: The Institutional Layer

Governance Nodes are the external institutional partners that give the protocol its independence and credibility. They are the mechanism by which the standard becomes decentralized.

**A Governance Node is:** A university faculty, professional association, or research center that has formally joined the Cortex Protocol governance network and has been issued a GPG keypair for signing Clinical Capability Modules.

**What a Governance Node does:**
1. Issues signed Clinical Capability Modules authorizing specific protocol capabilities.
2. Participates in the Annual Review Cycle, submitting peer-reviewed evidence for threshold updates.
3. Maintains a hardware whitelist of certified sensors for their deployment context.
4. Provides institutional credibility for grant applications, regulatory submissions, and academic publications.

**What a Governance Node does NOT do:**
- Govern the core standard specification (that is the White Branch's role).
- Hold veto power over other nodes' decisions.
- Represent commercial interests in the governance process.

**How to become a Governance Node:** Open an Issue tagged `[Governance-Node-Application]`. The application must include: institutional affiliation, field of expertise, proposed scope of clinical oversight, and willingness to participate in the Annual Review Cycle. Acceptance requires White Branch approval.

**Current Governance Nodes:** *(None yet — Milestone 1 objective)*

---

## The Validation Loop: From Evidence to Code

Every new capability, threshold modification, or protocol extension must pass through the Validation Loop before being merged into the standard.

```
[Proposal submitted as Issue]
         ↓
[Phase 1: Clinical Audit — White Branch]
  ↙ Rejected              ↘ Approved
[Closed]         [Phase 2: Legal Validation — Legal Validator]
                   ↙ Legal issue         ↘ Cleared
               [Revised]      [Phase 3: Technical Review — Protocol Stewards]
                                ↙ Technical issue    ↘ Approved
                           [Revised]          [Merged + Version increment]
```

**Phase 1 is mandatory and cannot be bypassed.** A proposal rejected for clinical reasons is closed. It may be resubmitted with new peer-reviewed evidence, but the Clinical Audit gate cannot be circumvented by appealing to technical necessity or commercial interest.

---

## Annual Review Cycle

The protocol's clinical safety parameters are reviewed annually. The review process:

1. **Call for Evidence (Month 1):** The White Branch publishes a call for new peer-reviewed research relevant to existing thresholds.
2. **Governance Node Submissions (Months 2–3):** Active Governance Nodes submit proposals for threshold updates, supported by literature.
3. **White Branch Review (Month 4):** The White Branch evaluates submissions and votes on threshold modifications.
4. **Public Comment Period (Month 5):** Proposed changes are published for 30-day community comment.
5. **Standard Update (Month 6):** Approved changes are merged with a MINOR version increment and full changelog.

**Signed manifests are time-limited.** Clinical Capability Modules issued by Governance Nodes expire after 12 months. Renewal requires participation in the Annual Review Cycle, ensuring that no outdated clinical evidence governs an active deployment.

---

## Anti-Capture Provisions

These rules are permanent and cannot be modified by any single governance body. Changes require consensus from the White Branch, at least two active Governance Nodes, and a MAJOR version increment.

**1. No cloud processing of biometric data.**
Any contribution requiring cloud-based processing of raw biometric or cognitive data is automatically rejected, regardless of the justification.

**2. Clinical Supremacy.**
Commercial application logic, engagement optimization, and performance targets cannot override a signed Clinical Capability Module. The SAL enforces this at runtime, not by policy.

**3. Evidence Transparency.**
Every clinical threshold in the protocol must link to a publicly accessible, peer-reviewed reference. Thresholds without citation are invalid.

**4. Hardware Independence.**
No hardware manufacturer may hold a governance role in any body that certifies their own products. No contribution may create dependency on a specific hardware vendor.

**5. User Sovereignty is Unconditional.**
No governance decision may remove or restrict the user's ability to override the protocol (the Kill Switch defined in GOVERNANCE-BASE.md). The protocol serves the user — it is never its master.

---

## Conflict Resolution

When the White Branch and Technical Branch disagree on whether a technical implementation satisfies a clinical requirement:

1. The Technical Branch documents the conflict as an Issue tagged `[Governance-Conflict]`.
2. The White Branch has 14 days to respond with a written clinical justification.
3. If no resolution is reached, an active Governance Node is asked to provide an independent clinical opinion.
4. The Governance Node's opinion is binding for the specific dispute.

When two Governance Nodes disagree on a threshold update:

1. The conflicting positions are published in the Annual Review Cycle for community comment.
2. The White Branch makes a final determination based on the weight of peer-reviewed evidence.
3. The dissenting Node's position is documented in the changelog.

---

*This document is maintained by the Protocol Stewards under White Branch oversight. Modifications to the Anti-Capture Provisions require the consensus process defined in Section 5.*
