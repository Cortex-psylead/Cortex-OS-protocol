# 🤝 Contributing to Cortex OS Protocol

Thank you for being here. Cortex OS is an open project, for humanity,
with no commercial owner. Every contribution — code, research, documentation,
or ethical oversight — moves us closer to a world where people have real
sovereignty over their own hardware.

This document tells you everything you need to know to contribute effectively.

---

## 🧭 Before You Start

Read these two documents first. They are not bureaucracy — they define
what this project is and is not:

- [README.md](./README.md) — The vision and origin of the project
- [GOVERNANCE-BASE.md](./GOVERNANCE-BASE.md) — The unalterable ethical
  principles every contribution must respect

One rule above all others: **user sovereignty is non-negotiable.**
No contribution that limits a user's access to their own hardware or data
will be accepted, for any reason.

---

## 🔍 What We Need Right Now

This is an early-stage project. The most valuable contributions at this
moment are not necessarily the most complex ones.

### 🔊 Priority 1 — Android Audio / DSP Engineer
**This is the most critical role for Milestone 0.**

We need someone who can demonstrate that the Ray Tracing cores of a
Snapdragon 8 Gen 1 can render a user-defined 3D spatial sound field
locally. If you have experience with any of the following, you are
exactly who we are looking for:

- AAudio or Oboe (Google) for ultra-low latency audio
- OpenSL ES or Android audio HAL
- Hexagon DSP SDK (Qualcomm)
- Spatial audio / ambisonics / HRTF processing
- libmysofa or Resonance Audio

Reference device available for testing: **Xiaomi 12 Pro (Snapdragon 8 Gen 1+)**

---

### 🤖 Priority 2 — Local AI / Edge Inference Engineer
We need someone to prototype the Acolyte agent running fully locally on
ARM. Relevant experience:

- Llama.cpp or ExecuTorch on mobile ARM
- MLC-LLM for Snapdragon NPU
- Whisper.cpp for local voice intent recognition
- LangGraph or similar agent orchestration

---

### 🔐 Priority 3 — ARM / Android Security Engineer
For the privacy and TEE layer. Relevant experience:

- OP-TEE (open source ARM Trusted Execution Environment)
- Android Keystore / Strongbox
- Biometric data isolation on mobile

---

### 🎓 Priority 4 — University Researchers
We are actively seeking university nodes for the Ethical Courts structure.
If you are affiliated with a university (public or private) and your
faculty works in any of the following areas, we want to hear from you:

- Computer science / systems engineering (code audit role)
- Psychology / bioethics / neuroscience (ethical protocol role)
- Law / data protection (legal compliance role)

See [GOVERNANCE.md](./GOVERNANCE.md) for the full court structure and
how to formally propose your institution.

---

### 📝 Always Welcome
- Documentation improvements in English or Spanish
- Translation of documents to other languages
- Research references for capability modules
- Bug reports and Issue triage

---

## 🛠️ How to Contribute

### Step 1 — Find or open an Issue
Before writing any code, check if there is already an open Issue for
what you want to do. If not, open one. This avoids duplicate work and
lets the community give early feedback.

Issue tags to know:
- `[milestone-0]` — work related to the first proof of concept
- `[capability-proposal]` — new hardware feature or user profile
- `[protocol-change]` — changes to core documents
- `[court-node-proposal]` — university node application
- `[good-first-issue]` — suitable for first-time contributors
- `[help-wanted]` — actively seeking contributors
- `[security-patch]` — security fixes (fast-track process)

### Step 2 — Fork and branch
git clone https://github.com/Cortex-psylead/Cortex-OS-protocol
git checkout -b feature/your-feature-name

Branch naming convention:
- `feature/` — new capability or module
- `fix/` — bug fix
- `docs/` — documentation only
- `research/` — research or protocol proposal

### Step 3 — Follow the code principles

**Rust** for hardware interaction and kernel-level components — memory
safety is mandatory at this layer.

**C++** for AI inference kernels where performance is critical.

**Kotlin / Java** for Phase 1 AOSP system services.

**Python** for capability module prototyping only — not for production
system components.

Every function that touches hardware must include:
- A comment explaining which hardware resource it accesses
- A reference to the GOVERNANCE-BASE.md principle it respects
- An explicit user override path (the Kill-Switch must always exist)

### Step 4 — Open a Pull Request

PR title format: `[scope] Brief description`

Examples:
- `[audio] Implement HRTF spatial renderer via Oboe`
- `[agent] Whisper.cpp intent recognition prototype`
- `[docs] Update ARCHITECTURE.md Phase 2 milestones`

Your PR description must include:
- What it does
- Which Issue it closes (`Closes #N`)
- Which hardware it was tested on (if applicable)
- Any open questions or known limitations

---

## ⚖️ Code of Conduct

Cortex OS is built on respect — for users, for contributors, and for
the communities this technology will serve.

**We do not accept:**
- Code that exfiltrates user data outside the device
- Code that implements dark patterns or addictive mechanics
- Code that hides hardware capabilities from the user
- Disrespectful behavior toward any contributor

**We actively welcome:**
- Contributors from any country, background, or discipline
- Non-technical contributions (research, translation, documentation)
- Critical feedback and honest disagreement — done respectfully
- Questions from people new to open source or hardware development

Violations of this code of conduct should be reported by opening a
private Issue or contacting the Protocol Steward directly.

---

## 🌍 Language Policy

The official language of this repository is **English** for all
technical documents, code comments, and Pull Requests.

**Spanish** is welcome in Issues and community discussion — this project
was born in Latin America and that community matters.

Translations of core documents into other languages are a valued
contribution and follow the standard PR process.

---

## 📋 Contribution Checklist

Before submitting a PR, confirm:

- [ ] I have read GOVERNANCE-BASE.md
- [ ] My code does not exfiltrate any user data
- [ ] My code includes a user override path where applicable
- [ ] I have tested on real ARM hardware if possible
- [ ] I have linked the relevant Issue
- [ ] My branch follows the naming convention
- [ ] My PR description answers: what, why, and tested on what

---

> *"The best contribution is the one that gives a person more control
> over their own device than they had yesterday."*
