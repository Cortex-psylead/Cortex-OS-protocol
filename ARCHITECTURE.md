# 🏗️ System Architecture: Cortex Protocol
### Universal Framework for Sovereign & Ethical Computing

This document outlines the technical structure of the **Cortex Protocol**: a hardware-agnostic, intent-centric orchestration layer where a local AI agent — the **Acolyte** — manages system resources under the governance of university-led Ethical Courts.

---

## 🧭 Design Philosophy: From OS to Protocol

Cortex is no longer just a mobile OS; it is a **Universal Protocol**. 

The vision is a **Sovereignty Abstraction Layer (SAL)** that can be implemented on any Linux-based system (Mobile, Desktop, or Edge). The Acolyte is not an app; it is the **System Orchestrator** that translates user intent into hardware execution, ensuring that every cycle of NPU, GPU, or CPU obeys ethical constraints.

The user does not launch applications. The user declares an **Intention**.
The protocol delivers the **Sovereign Result**.

---

## 🛰️ High-Level Topology: The Three Worlds

Cortex integrates three distinct domains into a single trust chain. 

### 1. 🔩 Sovereignty Abstraction Layer (SAL) — *"The Body"*
A hardware-agnostic interface that communicates with diverse architectures:
- **Edge/Mobile (ARM v8/v9):** Direct access to NPUs and Ray Tracing cores for low-latency sensory protection.
- **Desktop/Workstation (x86/GPU):** Leverages local GPU power (e.g., **GTX 1050**) for high-fidelity clinical simulations and LLM inference.
- **Sensor Hub:** Unified access to biometrics (HRV, GSR) and environmental data, processed 100% locally.

### 2. 🤖 Master Agent Core (The Acolyte) — *"The Mind"*
The central intelligence of the protocol, running locally on specialized silicon.
- **Intent Orchestrator:** Maps natural language to hardware capabilities without cloud intermediaries.
- **Cognitive State Engine:** Analyzes real-time sensor data to maintain user homeostasis and prevent sensory overload.
- **Ethical Sandbox:** Every intent is filtered against the digitally signed rulesets from the Ethical Courts before execution.

### 3. ⚖️ Algorithmic Jurisprudence — *"The Governance"*
The human layer that defines the "Constitutional Law" of the device.
- **University Nodes:** Engineering and Psychology faculties (e.g., **Universidad Santiago de Cali**) audit code and define clinical safety thresholds.
- **Signed Constraints:** Ethical rules are compiled into cryptographically signed files that the Acolyte must obey at the hardware level.

---

## 🔄 The Sovereignty Loop (Privacy by Design)

```
[User Intent / Environmental Sensors]
↓
[Acolyte — Local Inference (NPU/GPU)]
↓
[Ethical Court Filter (Signed)]
↙ Violation        ↘ Safe
[Friction/Block]  [Direct Hardware Execution via SAL]
↓
[Result delivered to user / Cognitive Shielding]
```

---

## 🛤️ Roadmap: Universal Progression

### ⚙️ Phase 1 — Framework Foundation *(Current)*
**Goal:** Establish the SAL and the first Clinical Capability Modules.
- **Hardware:** Focus on **Snapdragon 8 Gen 1** (Mobile) and **NVIDIA GTX 1050** (Desktop) as reference points.
- **Milestone 0:** **The Cognitive Shield.** Intercepting environmental stress (noise/light) and applying local hardware-level attenuation signed by a University Node.

### 🔧 Phase 2 — Cross-Platform Integration *(12–24 months)*
**Goal:** Deploy Cortex as a "Sovereign Layer" on top of existing Linux distributions and AOSP.
- **SDK Release:** Tools for developers to build "Cortex-Certified" modules.
- **Hybrid Kernel:** Integration with **PipeWire** and **Mesa** for universal hardware access.

### 🌐 Phase 3 — Global Ethical Standard *(36+ months)*
**Goal:** Full hardware-agnostic distribution and international clinical certification.
- **Universal Governance:** Multiple university nodes globally validating a shared ethical repository.
- **The Cognitive OS:** A complete environment where the Acolyte manages everything from PID 1, replacing traditional desktop/mobile paradigms.

---

## 🧰 Tech Stack (Agnostic & Open Source)

| Layer | Technology | Purpose |
|---|---|---|
| **Inference** | **Llama.cpp / ExecuTorch** | Cross-platform LLM execution (ARM/x86) |
| **Audio/DSP** | **PipeWire / Oboe** | Low-latency, universal audio orchestration |
| **Security** | **OP-TEE / OpenPGP** | Secure storage and Court signature verification |
| **Audit** | **Semgrep / SonarQube** | Continuous university-led code quality audit |
| **Clinical** | **BIDS-Physio** | Universal standard for physiological data |

---

## 🔐 The Trust Chain: From Court to Hardware

The Ethical Courts have **cryptographic authority**. Their GPG keys are the only ones capable of issuing the `ethical_constraints.txt` file.

1. **Faculties** draft and sign the safety thresholds (e.g., "Max audio decibels for sensory protection").
2. **The Protocol** verifies the signature at boot time.
3. **The Acolyte** receives these rules as its "System Prompt," making them physically impossible to bypass during runtime.

> *"The ethics are not a policy. They are the instruction set of the machine."*
