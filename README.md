# 🧠 Cortex Protocol
### Decentralized Infrastructure for Cognitive Sovereignty & Neuro-Privacy

[![Milestone 0: Locked](https://img.shields.io/badge/Milestone-0--Locked-green.svg)](#-milestone-0-the-cognitive-shield)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Branch: Clinical/White](https://img.shields.io/badge/Branch-White%20(Clinical)-blue.svg)](#-the-white-branch)

The **Cortex Protocol** is an open-source framework designed to protect the last frontier of human privacy: the mind. It provides a mathematically guaranteed layer of sovereignty between biometric sensors and Artificial Intelligence agents (Acolytes), ensuring that neural data remains under the exclusive control of its owner—mathematically, clinically, and legally.

---

## 🚀 Quick Start

```bash
git clone https://github.com/Cortex-psylead/Cortex-OS-protocol
pip install numpy matplotlib
python src/sal/cognitive_shield.py
```

The demo runs in under 60 seconds and produces a visual output (`cortex_demo.png`) showing the full protection pipeline in action.

---

## 🛡️ Milestone 0: The Cognitive Shield (Completed)

We have successfully implemented the core protection engine. The **Sovereignty Abstraction Layer (SAL)** is now functional and validated.

**Key Technical Features:**

- **Sensor Hardening:** Automatic rejection of uncertified or low-fidelity hardware via a cryptographic certification handshake. Only devices meeting White Branch clinical standards (SNR ≥ 30 dB, ≥ 12-bit resolution) are permitted.
- **Two-Phase Anonymous Tensor Transformation:** Raw biometric signals pass through a clinical feature extraction phase (interpretable by the Clinical Bridge) followed by irreversible HMAC-SHA256 obfuscation. The Acolyte (AI) receives only the obfuscated tensor—never the raw values.
- **Clinical Drift Index (CDI):** A proactive biometric immune system that monitors for pathological stress or behavioral manipulation by guest AIs using dual-threshold detection (absolute clinical limits + Z-score statistical deviation from personal baseline).
- **Secure Ephemeral Memory:** Raw biometric frames are held in a context manager (`with` block) that guarantees deterministic memory zeroing upon exit—not dependent on garbage collection.

> [!IMPORTANT]
> Full implementation: `src/sal/cognitive_shield.py`
> Each architectural decision is documented in [ARCHITECTURE.md](ARCHITECTURE.md).

---

## 🗂️ Full Project Structure

### Core

| File | Purpose |
| :--- | :--- |
| `src/sal/cognitive_shield.py` | The Cognitive Shield — complete SAL implementation (Milestone 0) |
| `README.md` | This file |

### Clinical & Scientific Foundation

| Document | Purpose |
| :--- | :--- |
| [WHITE_PAPER.md](WHITE_PAPER.md) | Full technical and clinical specification with bibliographic basis |
| [CLINICAL-BRIDGE.md](CLINICAL-BRIDGE.md) | Evidence-based clinical protocols and hardware safety margins |
| [MANIFESTO.md](MANIFESTO.md) | Ethical declaration and statement of neuro-rights |

### Architecture & Technical Specification

| Document | Purpose |
| :--- | :--- |
| [ARCHITECTURE.md](ARCHITECTURE.md) | System layers, hardware topology, and sovereignty loop |
| [MODULE-ISOLATION.md](MODULE-ISOLATION.md) | Zero-trust sandboxing and module isolation protocol |
| [USER-DATA-MODEL.md](USER-DATA-MODEL.md) | Data layers, tensor model, and No-Trace guarantee |
| [SECURITY.md](SECURITY.md) | Threat model, cryptographic governance, and vulnerability reporting |

### Governance & Legal

| Document | Purpose |
| :--- | :--- |
| [GOVERNANCE.md](GOVERNANCE.md) | Governance roles, validation process, and anti-capture provisions |
| [GOVERNANCE-BASE.md](GOVERNANCE-BASE.md) | Constitutional law of the protocol — unalterable foundational principles |
| [INTENT-PROTOCOL.md](INTENT-PROTOCOL.md) | Intent-based interaction model and hardware orchestration |
| [DISCLAIMER.md](DISCLAIMER.md) | Legal framework, safety notice, and scope of the project |

### Community

| Document | Purpose |
| :--- | :--- |
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contributor profiles, validation loop, and how to join |
| [ROADMAP.md](ROADMAP.md) | Strategic milestones from Milestone 0 to 2045 |
| [LEXICON.md](LEXICON.md) | Bilingual glossary of all proprietary and scientific terms |
| [VISION_2045.md](VISION_2045.md) | Long-term vision: The Digital Immune System |
| [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) | Community standards |

---

## 🧘 The White Branch (Clinical Leadership)

This project is founded and governed by mental health professionals. We prioritize the **Window of Tolerance** (Siegel, 1999) over the attention economy. Every Acolyte (AI agent) interacting with Cortex Protocol must pass the Clinical Bridge to ensure it does not cause fatigue, addiction, or emotional distress.

The White Branch holds **veto authority** over any technical implementation. Engineering serves the clinical mandate—not the inverse.

---

## 👥 Two Entry Points

**If you are a clinician or researcher:** Start with [CLINICAL-BRIDGE.md](CLINICAL-BRIDGE.md) and [WHITE_PAPER.md](WHITE_PAPER.md). These documents translate the protocol's technical decisions into the clinical and neurophysiological frameworks you work with.

**If you are a developer or engineer:** Start with [ARCHITECTURE.md](ARCHITECTURE.md) and `src/sal/cognitive_shield.py`. The code is fully documented with the clinical rationale behind each design decision.

---

## 🗺️ Roadmap

- [x] **Milestone 0:** The Cognitive Shield — SAL, CDI, Sensor Certification (complete).
- [ ] **Milestone 1:** The Legal Shield — Judicial Kill Switch & international legal framework.
- [ ] **Milestone 2:** Acolyte SDK — Open API for certified therapeutic AI developers.
- [ ] **Phase 3:** Universal Sovereign Standard — decentralized global Governance Node network.

---

## 🤝 Contributing

We welcome contributions from psychologists, neuroscientists, systems engineers, and legal experts. Read [CONTRIBUTING.md](CONTRIBUTING.md) to understand the three-phase validation loop (Clinical → Legal → Technical) that all contributions must pass.

**Open a `[Proposal]` Issue to begin.** All technical decisions require clinical sign-off from the White Branch before implementation.

---

## ⚖️ License

This project is licensed under the **GNU GPL v3** — see [LICENSE](LICENSE) for details.

*"This ensures that the protocol remains free and open for all humanity, forever."*
