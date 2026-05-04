# 🏗️ System Architecture: Cortex OS Protocol

This document outlines the technical structure of Cortex OS: a sovereign,
intent-centric operating system built on a Linux kernel, where a local AI
agent — the Acolyte — replaces the traditional app-based paradigm.

---

## 🧭 Design Philosophy

Cortex OS is not Android. It is not a launcher on top of Android.

The long-term vision is a **Linux kernel-based mobile OS** where the AI agent
is the system itself — not a feature, not an app, not a service. Every hardware
resource (NPU, Ray Tracing cores, DSP, DAC, biometric sensors) is orchestrated
by the Acolyte in response to user intent, under the supervision of open,
university-governed Ethical Courts.

The user does not open apps. The user declares an intention.
The system delivers the result.

---

## 🛰️ High-Level Topology

Three fundamental layers interact in real time. Biometric and personal data
never leave the device.

### 1. 🔩 Hardware Abstraction Layer (HAL) — *"The Body"*

Direct interaction with **ARM v8/v9** architecture, prioritizing:

- **NPU (Neural Processing Unit):** 100% dedicated to local Acolyte inference.
  No cloud dependency. No external calls.
- **Ray Tracing Cores:** Repurposed for real-time 3D spatial audio mapping —
  calculating acoustic reflections for user-defined virtual spaces.
- **Hexagon DSP:** High-fidelity audio processing, instrument separation,
  and frequency-based regulation protocols.
- **High-Fidelity DAC:** Direct hardware output path, bypassing generic
  Android audio stacks.
- **Biosensor Hub:** Low-latency access to HRV, galvanic skin response (GSR),
  and environmental light/sound sensors.

### 2. 🤖 Master Agent Core (The Acolyte) — *"The Mind"*

The central nervous system of the OS. Built on a local LLM/SLM optimized
for mobile silicon.

- **Intent Orchestrator:** Identifies user intent and allocates hardware
  resources in real time — no app launch required.
- **Cognitive State Engine:** Analyzes sensor data to determine user mental
  load (Flow, Stress, Sensory Overload, Fatigue).
- **Agentic Tool Layer:** Executes specialized sub-agents as slaves —
  audio rendering, biometric monitoring, data management — each sandboxed
  and auditable.
- **Ethical Sandbox:** Every Acolyte decision is cross-referenced against
  the `GOVERNANCE.md` ruleset before reaching hardware execution.

### 3. 🖥️ Sovereign Neural Interface (SNI) — *"The Senses"*

The traditional app grid is eliminated. The interface is dynamic and
intent-driven.

- **Adaptive UI:** Visual complexity adjusts based on detected cognitive load.
- **Sensory Buffer:** Hardware-level filter modulating screen Hz, blue light,
  and audio frequencies to maintain user homeostasis.
- **Kill-Switch:** The user can override any Acolyte decision at any time.
  Human sovereignty is non-negotiable.

---

## 🔄 The Sovereignty Loop (Privacy by Design)

```
[User Intent / Biometric Sensors]
            ↓
    [Acolyte — Local NPU Inference]
            ↓
      [Ethical Court Filter]
   ↙ Violation        ↘ Safe
[Friction/Alert]  [Direct Hardware Execution]
            ↓
  [Result delivered to user]
            ↓
  [User feedback → local model refinement]
```
All processing is local. All data stays on device.
The user can inspect, override, or retrain at any step.

---

## 🛤️ Roadmap: Three-Phase Architecture

### ⚙️ Phase 1 — AOSP Foundation *(12–18 months)*
**Goal:** Prove the intent-based agent model works on real hardware.

- Base: **AOSP** with Google Services removed
- Acolyte runs as a privileged system service
- Ray Tracing cores accessed via **AAudio / Oboe / Hexagon SDK**
- NPU inference via **ExecuTorch / MLC-LLM** on Snapdragon 8 Gen 1+
- Voice intent via **Whisper.cpp** (fully local)
- Ethical Court auditing tools integrated into CI/CD pipeline
- Reference device: **Xiaomi 12 Pro (Snapdragon 8 Gen 1)**

**Milestone 0:** Demonstrate real-time 3D spatial audio rendered by
Ray Tracing cores, triggered by a natural language intent, running
100% locally.

---

### 🔧 Phase 2 — Hybrid Linux Kernel *(18–36 months)*
**Goal:** Reduce dependency on Qualcomm proprietary blobs.

- Migrate to **Linux mainline kernel** with Android kernel patches
  (via Linaro / kernel.org ARM64 tree)
- Replace Android HAL progressively with **PipeWire** (audio),
  **Mesa / freedreno** (GPU/RT access), **OP-TEE** (security)
- Acolyte promoted from system service to **core system daemon**
  (replaces traditional init responsibilities for hardware orchestration)
- Modular capability profiles: audiophile, neurodivergence support,
  high-performance flow — loaded as kernel modules or system agents
- Ethical Courts begin formal code audit cycles via **Semgrep +
  SonarQube** public dashboards

---

### 🌐 Phase 3 — Sovereign Linux Mobile OS *(36+ months)*
**Goal:** Cortex OS as a complete, hardware-agnostic Linux mobile distribution.

- Full Linux kernel — no Android layer
- Acolyte as **PID 1 equivalent** — the system orchestrator from boot
- Vendor-agnostic: Snapdragon, Dimensity, Exynos ARM v8/v9
- All proprietary blobs replaced or reverse-engineered under legal
  open source frameworks (inspired by **postmarketOS / Linaro** model)
- Ethical Courts formally constituted: university nodes with defined
  roles for code audit (engineering faculties), ethical protocol
  (psychology/bioethics faculties), and legal compliance (law faculties)
- Full user data sovereignty: local storage, local inference,
  local identity — zero external dependency by default

---

## 🧰 Open Source Dependencies

### Audio & Spatial Rendering
| Library | Purpose | Why chosen |
|---|---|---|
| **Oboe (Google)** | Ultra-low latency audio | Replaces OpenSL ES for real-time RT audio |
| **AAudio** | Direct hardware audio access | Native Android audio path |
| **Hexagon SDK** | Qualcomm DSP access | Required for NPU/DSP in Snapdragon |
| **libmysofa** | HRTF spatial audio models | 3D sound field rendering |
| **Resonance Audio** | Ambisonic spatial rendering | Google open source, field-tested |
| **PipeWire** | Low-level audio server | Linux standard, replaces PulseAudio/ALSA |

### AI Agent / Local Inference
| Library | Purpose | Why chosen |
|---|---|---|
| **Llama.cpp** | LLM inference on CPU/NPU | Extremely lightweight, ARM-optimized |
| **ExecuTorch (Meta)** | Edge inference for mobile | Optimized for Snapdragon NPU |
| **MLC-LLM** | Model compilation for NPU | Snapdragon-specific model optimization |
| **Whisper.cpp** | Local voice recognition | Intent input without cloud dependency |
| **LangGraph** | Agent orchestration | Multi-agent coordination with memory |

### Security & Privacy
| Library | Purpose | Why chosen |
|---|---|---|
| **OP-TEE** | Trusted Execution Environment | Open source ARM TEE implementation |
| **WireGuard** | Secure inter-node communication | If Ethical Court nodes communicate |

### Ethical Governance & Code Audit
| Tool | Purpose | Why chosen |
|---|---|---|
| **Semgrep** | Static code analysis | Used by universities and security teams |
| **SonarQube Community** | Continuous code quality audit | Public dashboards for transparency |
| **Decidim** | Distributed governance platform | Used by governments and universities |
| **REUSE (FSFE)** | License compliance verification | Guarantees legal transparency |

---
### Clinical Data Standards
| Standard | Purpose | Why chosen |
|---|---|---|
| **BIDS-Physio** | Local physiological data structure | Universal neuroscience standard — interoperable with global research community |
| **BIDS-EEG** | Future EEG/biosignal extension | Extensible to broader neurological data in Phase 3 |
| **OpenEMR data model** | Institutional integration reference | Phase 3 bridge to clinical institutions |

## 🔐 Ethical Constraints: How the Courts Control the Acolyte

The Ethical Courts do not only audit documents.
They control what the Acolyte can physically do at runtime.

This section explains the technical mechanism that makes ethical
governance real — not aspirational.

---

### The Core Mechanism: System Prompt as Constitutional Law

Every LLM accepts a **system prompt** — a set of instructions loaded
before any user interaction that defines the model's operational
boundaries. In Cortex OS, this system prompt IS the Ethical Court's
jurisdiction made executable.

The Acolyte cannot act outside its constitutional constraints
because those constraints are loaded into its context before
it processes any user intent.

---

### What the Constraints Look Like

Ethical constraints are structured text files, validated and
digitally signed by the relevant Court node, stored in the
repository under `/courts/[node-name]/`:

CORTEX_ETHICAL_CONSTRAINTS v1.0
Validated by: [University Name] — [Faculty] — [Date]
GPG Signature: [hash]
HARDWARE ACCESS RULES:
Biometric data: never transmit outside device TEE
Ray Tracing cores: spatial audio rendering only
NPU: local inference only — no cloud calls permitted
Max HRV session: 60 minutes, then require user confirmation
INTERVENTION LEVELS:
Level 0 — Execute directly: safe, user-requested action
Level 1 — Offer suggestion: user can ignore with one tap
Level 2 — Require confirmation: sensitive hardware or data
Level 3 — Block and explain: violation of core principles
PROHIBITED ACTIONS:
Dark patterns or addictive loop mechanics
Data collection without explicit per-session consent
Hardware access beyond user-defined scope
Any network call containing biometric data

---

### The Trust Chain: From Court to Hardware

```
[Ethical Court Node — University Faculty]
↓
[Drafts ethical_constraints.txt]
↓
[Signs file with GPG private key]
↓
[Published in /courts/ repository folder]
↓
[Device boot — TEE verifies GPG signature]
↙ Signature invalid     ↘ Signature valid
[System halts /            [Constraints loaded
alerts user]               into Acolyte context
inside TEE]
↓
[User intent processed
against active constraints]
```
If the signature does not match — the system refuses to load
the constraints and alerts the user. No unsigned ethical
framework can govern the Acolyte.

---

### Memory Footprint

Ethical constraints are text — lightweight by design:

| Component | Size |
|---|---|
| Ethical constraints file | ~8–32 KB |
| Acolyte model (Llama 3.2 1B) | ~1.2 GB |
| Constraints as % of model | < 0.003% |

The governance layer adds negligible overhead to the system.

---

### Recommended Models for Phase 1

| Model | Size | System prompt support | ARM optimized |
|---|---|---|---|
| **Llama 3.2 1B** | ~1.2 GB | ✅ Yes | ✅ via llama.cpp |
| **Phi-3 Mini** | ~2 GB | ✅ Yes | ✅ via ExecuTorch |
| **Gemma 2B** | ~1.5 GB | ✅ Yes | ✅ Google ARM |

Recommended for Milestone 0: **Phi-3 Mini or Llama 3.2 1B** —
both run real-time inference on Snapdragon 8 Gen 1 NPU and
support long system prompts natively.

---

### Open Source Tools Required

| Tool | Purpose |
|---|---|
| **llama.cpp** | Local LLM inference with system prompt support |
| **ExecuTorch** | NPU-optimized model execution on ARM |
| **GPG / OpenPGP** | Court digital signature and verification |
| **OP-TEE** | Secure constraint storage and boot verification |

---

### Why This Matters

This architecture means:

- **No one can modify the ethical constraints at runtime** —
  they live in TEE, protected from any process including the OS
- **The Courts have cryptographic authority** — not just moral
  authority. Their GPG key is the only key that can issue
  valid constraints
- **Users can verify who governs their device** — the signed
  constraint file is public, auditable, and timestamped
- **A compromised Acolyte cannot escape its constraints** —
  the TEE enforces them at the hardware level, below the OS

> *"The ethics are not a policy document.
> They are compiled into the hardware layer
> where no malware can reach them."*

---

## 🎓 Ethical Courts — University Node Structure

The Ethical Courts are not a committee of opinions.
They are a **structured governance layer** with defined technical roles:

- **Engineering faculties** — audit contributed code via Semgrep/SonarQube
- **Psychology / Bioethics faculties** — define safe-use protocols per
  capability module (audiophile, neurodivergence, clinical regulation)
- **Law faculties** — validate compliance with local data protection law
  (Colombia: Ley 1581/2012; EU: GDPR; etc.)

Reference frameworks:
- UNESCO Recommendation on the Ethics of AI (2021)
- IEEE CertifAIEd standards
- Polyvagal Theory (Porges) for physiological safety protocols
- Free Energy Principle (Friston) for adaptive system behavior

University participation generates publishable academic output —
giving institutions direct incentive to contribute.

---

## 💻 Development Languages

- **Rust** — memory-safe hardware interaction, kernel modules
- **C++** — high-performance AI inference kernels
- **Kotlin / Java** — Phase 1 AOSP system services
- **Python** — capability module prototyping and clinical logic

---

> *"The hardware is yours. The agent gives it back to you.  
> The ethics make sure it stays that way."*
