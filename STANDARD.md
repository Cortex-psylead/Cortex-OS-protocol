# Cortex Protocol: Open Standard Specification
**Document ID: CORE-STANDARD-001 | Version: 0.1-draft (RFC)**

> **Status: Request for Comments (RFC)**
> This document is open for review by the neurotechnology, clinical research, and AI ethics communities. To submit a comment or proposal, open an Issue tagged `[RFC-Comment]` in the repository.

---

## Preamble

The Cortex Protocol is an open, royalty-free technical standard for the governance of human-AI interaction at the neurophysiological level. It defines the minimum requirements for a compliant implementation of the Sovereignty Abstraction Layer (SAL), the Clinical Drift Index (CDI), and the Clinical Bridge — the three components that together constitute a **Cortex-Compliant** system.

The standard is maintained by the White Branch under the governance framework defined in [GOVERNANCE.md](GOVERNANCE.md) and [GOVERNANCE-BASE.md](GOVERNANCE-BASE.md). It is licensed under GPL v3: any implementation of this standard is free to use, modify, and distribute, provided modifications are published under the same terms.

---

## Part I — Scope and Definitions

### 1.1 Scope

This standard applies to any software system, hardware device, or AI agent that:

1. Collects, processes, or transmits neurophysiological or biometric data from a human user.
2. Operates an AI agent (Acolyte) in a context where the AI's outputs can influence the user's cognitive or emotional state.
3. Claims compliance with the Cortex Protocol.

Systems operating exclusively on non-biometric data (keyboard input, mouse movement, text) are outside the scope of this standard.

### 1.2 Normative Definitions

The following terms carry normative meaning in this document. All definitions are operationalized in [LEXICON.md](LEXICON.md).

**SHALL** — a mandatory requirement. A compliant implementation must satisfy all SHALL requirements.

**SHOULD** — a recommended requirement. A compliant implementation should satisfy SHOULD requirements unless there is documented clinical justification for deviation.

**MAY** — an optional capability. Compliant implementations may implement MAY requirements at their discretion.

**Compliant Implementation** — a software system or hardware device that satisfies all SHALL requirements of this specification.

**Certified Acolyte** — an AI agent that has passed the White Branch validation loop and operates under a signed Clinical Capability Module issued by an independent Governance Node.

**Cortex-Ready Device** — a hardware sensor that meets the minimum quality thresholds defined in Section 3.1 and is registered in an active Governance Node's hardware whitelist.

---

## Part II — Core Requirements

### 2.1 The Sovereignty Abstraction Layer (SAL)

#### 2.1.1 Data Boundary

**SHALL:** Raw biometric data (EEG voltage, R-R intervals, GSR values, or any direct physiological measurement) SHALL NOT be transmitted beyond the SAL boundary. A compliant implementation processes all raw data locally on the user's device.

**SHALL:** The SAL SHALL implement the two-phase transformation defined in Section 2.2 before any data exits the SAL boundary.

**SHALL NOT:** Raw biometric data SHALL NOT be logged, cached to disk, or stored in any persistent medium in its original form.

#### 2.1.2 Session Isolation

**SHALL:** Each user session SHALL be cryptographically isolated using a unique session salt of at least 256 bits generated from a cryptographically secure random number generator.

**SHALL:** Session salts SHALL be destroyed at session end. A compliant implementation SHALL provide a session destruction function that: (a) replaces the session salt with a new random value, (b) clears the session audit log, (c) renders all tensors produced in the session permanently inaccessible.

**SHALL NOT:** Session salts SHALL NOT be derived from user-identifiable data (name, device ID, biometric features).

#### 2.1.3 Ephemeral Memory

**SHALL:** Raw biometric frames SHALL be held in memory using a deterministic destruction pattern (context manager or equivalent) that guarantees memory zeroing upon frame exit, independent of garbage collection scheduling.

**SHALL NOT:** Implementations SHALL NOT rely on finalizer methods (`__del__` in Python, `finalize()` in Java) as the sole mechanism for raw data destruction.

---

### 2.2 Two-Phase Tensor Transformation

#### 2.2.1 Phase A — Clinical Feature Extraction

**SHALL:** Phase A SHALL extract a minimum of 5 statistical descriptors from the raw biometric signal sufficient to classify autonomic state (minimum: mean, standard deviation, 25th percentile, 75th percentile, maximum of the signal envelope or equivalent).

**SHALL:** Phase A output SHALL be expressed as normalized values in [0, 1] relative to a clinically defined physiological reference range documented in the implementation's Clinical Bridge specification.

**SHALL:** Phase A output SHALL be the exclusive input to the Clinical Bridge validation (Section 2.3). The Clinical Bridge SHALL NOT receive Phase B output.

#### 2.2.2 Phase B — Privacy Obfuscation

**SHALL:** Phase B SHALL apply an irreversible cryptographic transformation to Phase A output using the session salt before producing the tensor delivered to the Acolyte.

**SHALL:** The cryptographic transformation SHALL use a keyed-hash function with a minimum security level of 256 bits (e.g., HMAC-SHA256 or equivalent).

**SHALL:** The Acolyte SHALL receive only Phase B output. The Acolyte SHALL NOT receive Phase A features, raw biometric values, or the session salt.

---

### 2.3 Clinical Bridge

#### 2.3.1 Per-Frame Validation

**SHALL:** Every biometric frame SHALL pass Clinical Bridge validation before the Acolyte processes it.

**SHALL:** Clinical Bridge thresholds SHALL be derived from peer-reviewed literature and SHALL be documented with bibliographic citations in the implementation's clinical specification.

**SHALL:** Clinical Bridge thresholds SHALL be defined and maintained exclusively by clinically qualified personnel (White Branch or equivalent clinical governance body).

**SHALL NOT:** Clinical Bridge thresholds SHALL NOT be modified by the Technical Branch, by Acolyte logic, or by any automated process without explicit clinical governance approval.

#### 2.3.2 Threshold Documentation

**SHALL:** A compliant implementation SHALL publish the following for each Clinical Bridge threshold: (a) the parameter name and value, (b) the physiological condition it maps to, (c) the bibliographic reference(s) supporting the value.

---

### 2.4 Clinical Drift Index (CDI)

#### 2.4.1 Temporal Monitoring

**SHALL:** A compliant implementation SHALL monitor biometric coherency across sessions using a sliding temporal window of at least 60 seconds.

**SHALL:** The CDI SHALL employ at least one absolute threshold (hard violation) and at least one statistical deviation threshold relative to a personal baseline (soft violation).

**SHALL:** Hard and soft violation counters SHALL be tracked independently with documented, clinically justified trigger thresholds.

#### 2.4.2 Baseline Personalization

**SHOULD:** The CDI SHOULD establish a personal baseline from the user's first sessions (minimum 3, recommended 7) to personalize statistical deviation detection to individual neurophysiology.

**SHALL:** If a personal baseline is not yet established, the CDI SHALL operate using only the absolute threshold detection mechanism.

#### 2.4.3 Block Response

**SHALL:** When CDI block thresholds are exceeded, the implementation SHALL immediately suspend Acolyte processing and SHALL NOT resume without a documented reset protocol.

**SHALL:** The CDI reset protocol SHALL require explicit action — either from the user (at governance Level 0–1) or from an authorized clinical professional (at governance Level 2). Automatic reset without human authorization is not permitted.

---

### 2.5 Hardware Certification

#### 2.5.1 Sensor Quality Thresholds

**SHALL:** A compliant implementation SHALL verify connected sensors against minimum quality thresholds before any data ingestion. The minimum thresholds are:

| Parameter | Minimum Value | Rationale |
| :--- | :--- | :--- |
| Signal-to-Noise Ratio | ≥ 30.0 dB | Minimum for reliable autonomic state classification |
| ADC Resolution | ≥ 12 bits | Minimum to resolve EEG microvolt amplitudes |
| Sampling Rate (cardiac) | ≥ 250 Hz | Required for accurate RMSSD computation |

**SHALL NOT:** Data from sensors failing quality thresholds SHALL NOT enter the SAL pipeline.

#### 2.5.2 Hardware Whitelist

**SHOULD:** Compliant implementations SHOULD maintain a hardware whitelist signed by an active Governance Node, listing sensor models that have undergone clinical quality verification.

**MAY:** Implementations MAY allow user-authorized exemptions for sensors not in the whitelist, provided the exemption is explicitly logged in the session audit record.

---

### 2.6 Audit and Logging

#### 2.6.1 Audit Log Contents

**SHALL:** The session audit log SHALL contain, for each processed frame: timestamp, truncated sensor identifier (maximum 8 characters of the hash), coherency index value, autonomic state classification, and CDI status.

**SHALL NOT:** The audit log SHALL NOT contain: raw biometric values, Phase A features, full sensor identifiers, session salts, or any user-identifiable information.

#### 2.6.2 Log Destruction

**SHALL:** The audit log SHALL be destroyed as part of the session destruction function (Section 2.1.2).

---

## Part III — Governance Requirements

### 3.1 White Branch (Clinical Authority)

**SHALL:** Any organization claiming Cortex compliance SHALL designate a clinical governance body (White Branch or equivalent) composed of licensed mental health or neuroscience professionals holding authority to define and modify Clinical Bridge thresholds.

**SHALL:** Clinical Bridge threshold modifications SHALL be documented with the approving clinician's identifier and the supporting bibliographic evidence.

### 3.2 Governance Nodes

**SHOULD:** Compliant implementations SHOULD operate under the oversight of at least one independent Governance Node — an institution external to the implementing organization that issues signed Clinical Capability Modules.

**SHALL:** Clinical Capability Modules issued by Governance Nodes SHALL carry a cryptographic signature verifiable against a published public key.

**SHALL NOT:** A hardware manufacturer, commercial AI developer, or for-profit entity SHALL NOT serve as its own Governance Node for the products it manufactures or sells.

### 3.3 Anti-Capture Provisions

The following are absolute prohibitions for any compliant implementation:

**SHALL NOT:** Transmit raw biometric data to cloud infrastructure under any circumstances.

**SHALL NOT:** Implement Clinical Bridge thresholds that favor commercial engagement metrics over clinical safety parameters.

**SHALL NOT:** Restrict the protocol to hardware from a single manufacturer (hardware lock-in).

**SHALL NOT:** Require users to authenticate to a centralized server to activate local protection features.

---

## Part IV — Conformance Levels

### Level 1 — Core Compliant
Satisfies all SHALL requirements in Parts II and III. Suitable for research and development implementations.

### Level 2 — Clinically Validated
Core Compliant, plus: CDI thresholds validated against clinical population data, at least one active independent Governance Node, peer-reviewed publication of validation methodology.

### Level 3 — Certified Standard
Clinically Validated, plus: Formal certification issued by a multi-institutional Governance Council, hardware whitelist maintained by an independent node, legal compliance documentation for at least one national regulatory framework.

---

## Part V — Reference Implementation

The reference implementation of this standard is maintained at:
`https://github.com/Cortex-psylead/Cortex-OS-protocol`

The reference implementation (`src/sal/cognitive_shield.py`) demonstrates compliance with all Level 1 SHALL requirements using synthetic EEG signals. Real-hardware validation is the objective of Milestone 1 (see [ROADMAP.md](ROADMAP.md)).

---

## Part VI — Versioning and Change Management

This document follows semantic versioning: `MAJOR.MINOR.PATCH`.

- **MAJOR** increments when a change breaks backward compatibility with existing implementations.
- **MINOR** increments when new requirements are added in a backward-compatible manner.
- **PATCH** increments for clarifications, editorial corrections, and bibliographic updates.

Changes to SHALL requirements in Sections 2.1–2.5 require White Branch clinical approval and a MINOR or MAJOR version increment. Changes to SHOULD and MAY requirements require Technical Branch review only.

---

## Acknowledgements

This standard builds on the work of the polyvagal research community (Porges, Dana), the HRV measurement standardization effort (Task Force, 1996), the open neurotechnology hardware community (OpenBCI, BrainFlow), and the emerging neuro-rights legislative frameworks in Chile, the European Union, and Colombia.

---

*Cortex Protocol Standard Specification v0.1-draft. Released for public comment under GPL v3.*
*White Branch, Cortex Protocol — 2025.*
