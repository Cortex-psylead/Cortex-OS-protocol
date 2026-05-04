# 🔒 Module Isolation Protocol: Inter-Module Sandboxing

This document defines how Cortex OS isolates capability modules
from each other, preventing a compromised or malfunctioning module
from accessing data or hardware resources belonging to another module.

Isolation is not optional. It is structural.

---

## 🧭 Design Philosophy

In a traditional OS, apps are isolated from each other but share
system services freely. In Cortex OS, isolation goes deeper —
every capability module is treated as an untrusted component
by default, even if it passed Ethical Court certification.

**The principle: a compromised audio module must never be able
to read HRV data. A compromised biometric module must never
be able to inject audio. No exceptions.**

This is zero-trust applied not between users and system,
but between modules within the system itself.

---

## 🛤️ Isolation Evolution by Phase

Isolation is implemented progressively across the three
architectural phases of Cortex OS, matching the available
infrastructure at each stage.

---

## ⚙️ Phase 1 — Linux Process Isolation (AOSP)

### Mechanism
Each capability module runs as an **independent Linux process**
with its own unique UID assigned by the Android kernel.

This is the same isolation model Android uses for apps —
mature, battle-tested, and requiring no kernel modifications.

### How it works

```
[Acolyte Core Process — UID 1000]
↓ IPC via Binder/AIDL
┌───────────────────────────────────────┐
│  [Audio Module — UID 1001]            │
│  [HRV Monitor — UID 1002]             │
│  [Focus Manager — UID 1003]           │
│  [Stem Separator — UID 1004]          │
└───────────────────────────────────────┘
↑
Kernel enforces UID boundaries
No cross-UID memory access permitted
```

### Communication between modules
Modules never communicate directly with each other.
All inter-module communication routes through the Acolyte:

[Module A] → [Acolyte] → [Module B]

The Acolyte acts as the sole message broker. It validates
every inter-module message against the active ethical
constraints before forwarding.

### Inter-process communication stack
- **Binder** — Android's native IPC mechanism, kernel-level
- **AIDL** — Interface Definition Language for type-safe
  cross-process calls
- **Intent schema** — every message between modules uses
  the structure defined in INTENT-PROTOCOL.md

### Known limitations in Phase 1
Process isolation protects against direct memory access
but does not fully protect against **side-channel attacks** —
a malicious module could potentially infer information
from another module by measuring CPU timing or cache behavior.

This is a known limitation, documented here for transparency.
It is addressed in Phase 2 and Phase 3.

---

## 🔧 Phase 2 — Linux Namespaces + cgroups

### Mechanism
Each capability module runs inside its own **Linux namespace**,
providing deeper isolation than process boundaries alone.

Android already uses cgroups internally for battery and
process priority management. Phase 2 extends this existing
infrastructure to provide per-module resource isolation.

### What namespaces provide per module

| Namespace | What it isolates |
|---|---|
| **PID namespace** | Module cannot see processes outside its namespace |
| **Network namespace** | Module has no network access by default |
| **Mount namespace** | Module sees only its own filesystem slice |
| **IPC namespace** | Module cannot access shared memory of other modules |
| **User namespace** | Module has its own user/group ID mapping |

### cgroups per module

Each module has enforced resource limits:
Module: audio_spatial_renderer
cgroup limits:
cpu.max: 30% of 2 performance cores
memory.max: 256MB
io.max: read-only access to /audio/assets
devices: DAC + Ray Tracing cores only

A module that exceeds its resource limits is throttled —
not terminated. The user is notified if a module is
consistently hitting its limits.

### Communication in Phase 2
Same Acolyte-as-broker model as Phase 1, but now enforced
at namespace boundary level — a module physically cannot
open a socket to another module without routing through
the Acolyte's defined interface.

### What Phase 2 adds over Phase 1
- Side-channel resistance improved via namespace isolation
- Network access completely removed from modules by default
- Filesystem access scoped to module-specific directories
- Resource exhaustion attacks (one module starving others)
  prevented by cgroup limits

---

## 🌐 Phase 3 — ARM CCA Confidential Compute (ARMv9)

### Mechanism
ARM Confidential Compute Architecture (CCA) introduces
**Realms** — hardware-enforced confidential execution
environments that are isolated from the normal OS,
the hypervisor, and from each other at the silicon level.

Available on ARMv9 architecture — the Phase 3 target
of Cortex OS (Snapdragon 8 Gen 2+ / Dimensity 9200+).

### What ARM CCA Realms provide

```
┌─────────────────────────────────────────────┐
│              ARM TrustZone                  │
│  ┌─────────────┐    ┌──────────────────┐   │
│  │ Secure World│    │   Normal World   │   │
│  │  (OP-TEE)  │    │  ┌────────────┐  │   │
│  │            │    │  │   Realm 1  │  │   │
│  │ Ethical    │    │  │ Audio Mod  │  │   │
│  │ Constraints│    │  ├────────────┤  │   │
│  │ GPG Keys   │    │  │   Realm 2  │  │   │
│  │ Biometric  │    │  │ HRV Module │  │   │
│  │ Raw Data   │    │  ├────────────┤  │   │
│  └─────────────┘   │  │   Realm 3  │  │   │
│                    │  │ Focus Mgr  │  │   │
│                    │  └────────────┘  │   │
│                    └──────────────────┘   │
└─────────────────────────────────────────────┘
```

Each capability module runs in its own Realm. A Realm is:
- **Hardware-isolated** — even the OS kernel cannot read
  a Realm's memory
- **Attestable** — the Realm can cryptographically prove
  its identity and integrity to the Acolyte
- **Independently destroyable** — a compromised Realm
  can be terminated and restarted without affecting others

### What Phase 3 adds over Phase 2
- Isolation enforced at silicon level — no software can
  bypass it, including a compromised kernel
- Each module can prove it has not been tampered with
  via hardware attestation
- Biometric data processed inside Realm never exists
  in normal world memory — not even for microseconds
- A fully compromised OS cannot access module data

### Known requirement
ARM CCA requires ARMv9 hardware. Phase 1 and Phase 2
run on ARMv8 (Snapdragon 8 Gen 1). Phase 3 requires
migration to ARMv9 devices as specified in ARCHITECTURE.md.

---

## 📊 Isolation Comparison

| Property | Phase 1 | Phase 2 | Phase 3 |
|---|---|---|---|
| Memory isolation | ✅ Process | ✅ Namespace | ✅ Hardware Realm |
| Network isolation | ⚠️ Partial | ✅ Namespace | ✅ Hardware Realm |
| Filesystem isolation | ⚠️ Partial | ✅ Mount namespace | ✅ Hardware Realm |
| Side-channel resistance | ⚠️ Limited | ✅ Improved | ✅ Hardware enforced |
| Resource limits | ⚠️ OS-level | ✅ cgroups | ✅ Realm quotas |
| Kernel compromise | ❌ Not protected | ❌ Not protected | ✅ Protected |
| Implementation complexity | Low | Medium | High |

---

## 🔄 Module Lifecycle

Regardless of phase, every module follows the same lifecycle:

```
[Court-certified module package received]
↓
[Acolyte verifies GPG signature]
↓
[Isolation environment provisioned]
(Process / Namespace / Realm depending on phase)
↓
[Module loaded with minimum required permissions]
↓
[Module active — receives intents from Acolyte only]
↓
[Intent processed — result returned to Acolyte]
↓
[Module idle — resources released to cgroup limits]
↓
[Module terminated on user request or Acolyte decision]
↓
[Isolation environment destroyed — memory zeroed]
```
**Memory zeroing on termination is mandatory.**
No module may leave residual data in memory after termination.

---

## 🚨 Breach Response Protocol

If the Acolyte detects anomalous behavior from a module
— unexpected resource usage, attempted cross-module
communication, failed attestation in Phase 3 —
the response is graduated:

| Severity | Detection | Response |
|---|---|---|
| Low | Unusual CPU spike | Log + notify user |
| Medium | Attempted boundary crossing | Terminate module + notify user |
| High | Attestation failure (Phase 3) | Terminate + quarantine + Court alert |
| Critical | Multiple simultaneous anomalies | Full system safe mode |

Safe mode: only Acolyte core and ethical constraints
remain active. All capability modules suspended until
user reviews and confirms restart.

---

## 🛠️ Implementation Notes for Contributors

**Phase 1 stack:**
- Process isolation: Android UID system — no additional libraries
- IPC: **Binder / AIDL** — native Android
- Message broker: Acolyte core process
- Schema: INTENT-PROTOCOL.md JSON structure

**Phase 2 additions:**
- Namespace management: **libcontainer** or direct kernel
  namespace syscalls
- Resource limits: **cgroups v2** — available in Android
  kernel since Android 12
- Monitoring: **eBPF** probes for anomaly detection

**Phase 3 additions:**
- Realm management: **ARM CCA SDK** (public specification)
- Attestation: **RATS architecture** (RFC 9334)
- Requires ARMv9 device and updated OP-TEE

---

> *"Trust no module. Verify everything.
> Isolate by default. Connect only with purpose."*
