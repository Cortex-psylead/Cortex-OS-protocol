# 📊 User Data Model: Sovereign Physiological Data

This document defines how Cortex OS stores, structures, and
protects user data locally — and how that data can be used
for research without ever leaving the device or exposing
user identity.

---

## 🧭 Design Philosophy

User data in Cortex OS follows three absolute principles:

1. **Local by default** — all data lives on the device,
   encrypted, under user-only key control
2. **Ephemeral by default** — no session data persists
   beyond the current session unless the user explicitly
   enables history
3. **Interoperable by design** — data structures follow
   open international standards so researchers and
   Ethical Court nodes can work with them without
   learning proprietary formats

---

## 📐 Base Standard: BIDS-Physio

Cortex OS adopts the **Brain Imaging Data Structure (BIDS)**
as its foundational data organization standard — specifically
the **BIDS-Physio** extension for physiological signals.

BIDS is the universal open standard for neuroscientific data,
maintained by the global neuroimaging community and endorsed
by major research institutions worldwide.

**Why BIDS for Cortex OS:**

- Any university researcher in the world already knows this format
- Ethical Court nodes can audit physiological data without
  learning a proprietary schema
- Research collaborations with universities require zero
  format conversion
- Future integration with clinical institutions (OpenEMR,
  hospital systems) is straightforward
- The project becomes interoperable with the entire global
  neuroscience research community from day one

---

## 🗂️ Data Structure

Following BIDS-Physio conventions, local user data is
organized as follows:

```
/cortex_data/
├── sub-local/                    ← User (never identified externally)
│   ├── ses-[session_id]/         ← Each session is independent
│   │   ├── physio/
│   │   │   ├── sub-local_ses-[id]_physio.tsv      ← Raw signal data
│   │   │   └── sub-local_ses-[id]_physio.json     ← Metadata
│   │   ├── func/
│   │   │   ├── intents.jsonl     ← Intent history (this session)
│   │   │   └── states.jsonl      ← ANS state log (this session)
│   │   └── constraints/
│   │       └── active_constraints.txt  ← GPG-signed ethical constraints
│   └── profile/
│       ├── user_preferences.json ← Capability profiles (audiophile, etc.)
│       └── consent.json          ← What the user has explicitly enabled
└── .cortex_meta/
├── dataset_description.json  ← BIDS required metadata
└── participants.tsv          ← Local only — never transmitted
```
---

## 📋 Physiological Signal Schema (BIDS-Physio)

Following the BIDS-Physio specification for each session:

**physio.tsv** — tab-separated values, one row per sample:
cardiac    respiratory    gsr    timestamp
0.82       0.23           0.41   0.000
0.83       0.23           0.41   0.004
0.81       0.22           0.40   0.008

**physio.json** — metadata for the signal file:
```json
{
  "SamplingFrequency": 250,
  "StartTime": 0,
  "Columns": ["cardiac", "respiratory", "gsr"],
  "cardiac": {
    "Description": "Photoplethysmography signal for HRV analysis",
    "Units": "normalized",
    "SamplingFrequency": 250
  },
  "respiratory": {
    "Description": "Accelerometer-derived respiratory rate",
    "Units": "normalized",
    "SamplingFrequency": 50
  },
  "gsr": {
    "Description": "Galvanic skin response",
    "Units": "microsiemens",
    "SamplingFrequency": 10
  }
}
```
🔐 Encryption Architecture
All data in /cortex_data/ is encrypted at rest:
```
[Raw physiological signal]
        ↓
[AES-256-GCM encryption]
        ↓
[Stored in /cortex_data/]
        ↓
[Key derived from user credentials]
        ↓
[Key stored in ARM TrustZone TEE]
        ↓
[Only accessible to Acolyte with user authorization]
```
Key principles:
Encryption keys never exist in normal world memory
Keys are derived per-session — a compromised session
key does not expose historical data
User can delete all data with cryptographic certainty —
deleting the key makes all encrypted data permanently
unreadable

🔄 Data Lifecycle
```
[Session starts — user grants intent]
        ↓
[New session folder created with unique ID]
        ↓
[Physiological signals sampled → encrypted → stored]
        ↓
[Intent log updated per INTENT-PROTOCOL.md schema]
        ↓
[ANS state log updated every 30 seconds]
        ↓
[Session ends]
        ↓
[User choice:]
   ↙ Delete (default)    ↘ Keep (explicit opt-in)
[Key deleted —          [Data retained —
 data unreadable]        encrypted at rest]
```
Default behavior is always deletion.
Retention requires explicit, per-session user consent.

🎓 Research Use: Federated Learning Without Exposure
When the user opts into contributing to research
(explicit consent required, always reversible):
```
[Local session data — stays on device]
        ↓
[Local model training via PySyft/OpenMined]
        ↓
[Only model gradients leave the device]
        ↓
[Gradients are anonymized and aggregated]
        ↓
[No raw physiological data ever transmitted]
        ↓
[Ethical Court nodes verify process integrity]
[without accessing any user data]
```
This is attestation without exposure —
the court knows the system works correctly
without knowing what it knows about the user.

📊 Derived Metrics (Non-Raw Storage)
The Acolyte stores derived metrics, not raw signals,
for the cognitive state model:
```
{
  "session_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "duration_seconds": 1847,
  "hrv_metrics": {
    "mean_rmssd": 42.3,
    "mean_lf_hf_ratio": 1.8,
    "coherence_score": 0.73,
    "dominant_state": "ventral_vagal"
  },
  "cognitive_load": {
    "mean": "medium",
    "peak": "high",
    "duration_high_load_seconds": 340
  },
  "interventions_offered": 2,
  "interventions_accepted": 1,
  "active_profile": "audiophile"
}
```
Raw signals are ephemeral. Derived metrics are what
the Acolyte uses to personalize future sessions —
and even these are deleted by default.

🛠️ Implementation Notes for Contributors
Phase 1 implementation:
Local storage: SQLCipher — encrypted SQLite for Android
BIDS compliance: pybids (Python) for validation,
custom Kotlin implementation for production
Key management: Android Keystore + OP-TEE for
TEE-backed key storage
Data deletion: cryptographic erasure via key deletion,
not file overwrite
BIDS validation:
All data written to /cortex_data/ must pass BIDS
validator before being considered stored. This ensures
permanent interoperability with the research community.
Reference:
BIDS specification: bids.neuroimaging.io
BIDS-Physio extension: bids-specification.readthedocs.io
OpenMined/PySyft: openmined.org

"Your data is yours. Not because we promise it.
Because the mathematics make it impossible
for it to be anyone else's."
