# 🛣️ Roadmap: Cortex OS Protocol

This document shows the current state of the project and what comes next.
It is a living document — updated as the community grows and milestones are reached.

> **Current status: Declaration of Intent — Open RFC.**
> No production code exists yet. We are building the foundation.

---

## 🧭 Where We Are Now

| Area | Status |
|---|---|
| Vision & protocol documents | ✅ Complete |
| Clinical-technical framework | ✅ Complete |
| Ethical governance structure | ✅ Complete |
| Security architecture | ✅ Defined |
| First technical collaborator | 🔍 Seeking |
| First university node | 🔍 Seeking |
| Any working code | ⏳ Pending Milestone 0 |

---

## 🎯 Milestone 0 — Proof of Concept
**Target: 2025–2026 | Status: 🔍 Seeking collaborators**

> Demonstrate that the Ray Tracing cores of a Snapdragon 8 Gen 1
> can render a user-defined 3D spatial sound field,
> running completely local, with no external services.

**What needs to happen:**
- Android dev with AAudio / Oboe / Hexagon DSP experience joins the project
- 3D spatial audio prototype running on Xiaomi 12 Pro (reference device)
- Local voice intent recognition via Whisper.cpp — user says what they want,
  the agent delivers it
- First commit of executable code in the repository

**This milestone proves the core thesis:** underutilized mobile hardware
can be orchestrated by a local AI agent for real user benefit.

---

## ⚙️ Phase 1 — AOSP Foundation
**Target: 12–18 months after Milestone 0 | Status: ⏳ Not started**

- AOSP base with Google Services removed
- Acolyte running as privileged system service
- HRV monitoring module — local NPU processing
- Therapeutic audio module — Hexagon DSP synthesis
- Neurodivergence sensory buffer — real-time environmental load scoring
- First Ethical Court university node formally affiliated
- Clinical validation protocol designed by psychology semillero

**Exit criteria:** A working AOSP build where the user can speak an intent
and the system delivers a hardware response — locally, privately, ethically.

---

## 🔧 Phase 2 — Hybrid Linux Kernel
**Target: 18–36 months after Phase 1 | Status: ⏳ Not started**

- Migration to Linux mainline kernel with Android patches
- PipeWire replacing Android audio HAL
- OP-TEE fully integrated for biometric data isolation
- Acolyte promoted to core system daemon
- Ethical Courts formally constituted with technical, clinical,
  and legal university nodes
- First academic paper published from clinical-technical collaboration

**Exit criteria:** Cortex OS running on Linux kernel with all Phase 1
modules functional and Ethical Courts actively auditing contributions.

---

## 🌐 Phase 3 — Sovereign Linux Mobile OS
**Target: 36+ months after Phase 2 | Status: ⏳ Not started**

- Full Linux kernel — no Android layer
- Acolyte as system orchestrator from boot
- Vendor-agnostic: Snapdragon, Dimensity, Exynos ARM v8/v9
- All proprietary blobs replaced or reverse-engineered under
  open source legal frameworks
- Cortex OS as a complete, distributable Linux mobile OS
- International university governance network established

**Exit criteria:** A person can flash Cortex OS on a supported device
and have full hardware sovereignty from first boot.

---

## 🤝 How to Move This Forward

The fastest way to advance the roadmap is:

1. **If you are an Android audio / DSP developer** — open an Issue
   tagged `[milestone-0]` and let's build the proof of concept together
2. **If you are a university researcher** — open an Issue tagged
   `[court-node-proposal]` and read GOVERNANCE.md
3. **If you are anyone else** — star the repository, share it,
   open Issues with ideas and questions

Every conversation moves this forward.

---

> *"A roadmap is not a promise. It is a direction.
> The community decides how fast we walk."*
