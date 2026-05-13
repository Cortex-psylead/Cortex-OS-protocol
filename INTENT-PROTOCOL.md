# 🏗️ System Architecture: Cortex Protocol Framework

This document outlines the technical structure of the **Cortex Protocol**: a hardware-agnostic, intent-centric orchestration layer. It enables a local AI agent — the **Acolyte** — to manage hardware resources following strict clinical and ethical governance.

---

## 🧭 Design Philosophy: From OS to Protocol

Cortex is not a traditional Operating System; it is a **Sovereign Abstraction Layer (SAL)**. 

The vision is a protocol that sits between the hardware and the user. Whether running on a mobile device, a high-end workstation, or a local server, the Acolyte orchestrates resources (NPU, GPU, DSP, biometric sensors) in response to user intent, under the supervision of independent **Ethical Governance Nodes**.

The user does not "open apps." The user declares an **Intention**.
The Protocol delivers the **Result** while ensuring **Cognitive Sovereignty**.

---

## 🛰️ High-Level Topology

Three fundamental layers interact in real time. Biometric and personal data never leave the device.

### 1. 🔩 Sovereignty Abstraction Layer (SAL) — *"The Body"*

This layer interfaces with any available hardware architecture (ARM, x86, RISC-V), prioritizing:

- **Local Inference Units (NPU/GPU):** 100% dedicated to local Acolyte execution. No cloud dependency.
- **Hardware Acceleration:** Repurposing specialized cores (e.g., Ray Tracing or Parallel Compute) for real-time physiological tasks like 3D spatial audio mapping.
- **Biosensor Hub:** Low-latency access to HRV, GSR, and environmental sensors.
- **Sovereign Audio Path:** Direct hardware output to ensure high-fidelity delivery of therapeutic frequencies.

### 2. 🤖 Master Agent Core (The Acolyte) — *"The Mind"*

The central nervous system of the Protocol. Built on local Small Language Models (SLMs) optimized for edge silicon.

- **Intent Orchestrator:** Identifies user intent and allocates hardware resources without intermediate app layers.
- **Cognitive State Engine:** Analyzes sensor data locally to determine mental load (Flow, Stress, Overload).
- **Ethical Sandbox:** Every Acolyte decision is cross-referenced against the digitally signed rulesets from **Ethical Governance Nodes** before execution.

### 3. 🖥️ Sovereign Neural Interface (SNI) — *"The Senses"*

The interface is dynamic and intent-driven, replacing static grids with adaptive environments.

- **Adaptive UX:** Visual complexity adjusts based on detected cognitive load.
- **Sensory Buffer:** Hardware-level filters modulating screen Hz, blue light, and audio frequencies to maintain homeostasis.
- **Kill-Switch:** Human sovereignty is non-negotiable. The user can override any Protocol decision at any time.

---

## 🔄 The Sovereignty Loop (Privacy by Design)

```[User Intent / Biometric Sensors]
↓
[Acolyte — Local Compute Inference]
↓
[Ethical Governance Filter]
↙ Violation        ↘ Cleared
[Friction/Alert]  [Direct Hardware Execution]
↓
[Result delivered to user]`
```
All processing is local. All data stays on the device.

---

## 🛤️ Roadmap: Universal Evolution

### ⚙️ Milestone 0 — The Clinical Proof of Concept
**Goal:** Prove that intent-based orchestration works on existing hardware.
- Implementation of the **Acolyte** as a high-level service.
- **Milestone 0:** Real-time 3D spatial audio rendered via local acceleration, triggered by natural language, running 100% locally.

### 🔧 Phase 2 — Hardware Abstraction Layer (SAL) Integration
**Goal:** Establish the Protocol as a universal standard.
- Deployment of the **Sovereignty Abstraction Layer** across multiple architectures (Mobile & Desktop).
- Formal integration of **Ethical Governance Nodes** for ruleset signing.

### 🌐 Phase 3 — The Sovereign Ecosystem
**Goal:** Cortex as a hardware-agnostic distribution.
- Full independence from proprietary cloud dependencies.
- Global network of Independent Governance Nodes (Universities, Research Centers) providing auditable ethical manifests.

---

## 🧰 Technical Stack (Agnostic & Open Source)

| Component | Library / Tool | Purpose |
|---|---|---|
| **Inference** | Llama.cpp / ExecuTorch | High-performance local LLM/SLM execution. |
| **Audio** | PipeWire / Oboe | Low-latency, universal audio orchestration. |
| **Spatial Rendering** | Resonance Audio / libmysofa | 3D sound field rendering for therapeutic use. |
| **Governance** | GPG / OpenPGP | Digital signatures for ethical rulesets. |
| **Privacy** | OP-TEE / Trusted Execution | Secure local storage of sensitive manifests. |

---

## 🔐 Ethical Constraints: The Governance Mechanism

The Ethical Governance Nodes do not only audit documents; they control what the Acolyte can physically do at runtime.

- **Constitutional System Prompts:** Ethical constraints are loaded into the Acolyte's context as "Constitutional Law" before processing intent.
- **Signed Manifests:** Constraints are structured text files, validated and digitally signed by **Governance Nodes**.
- **Hardware Enforcement:** The SAL verifies the GPG signature at boot/launch. If the signature is invalid, the Protocol refuses to load the capability module.

---

> *"The hardware is yours. The protocol gives it back to you. The ethics make sure it stays that way."*
