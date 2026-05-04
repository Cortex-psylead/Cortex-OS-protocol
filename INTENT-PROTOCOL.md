# 🎯 Intent Protocol: How the Acolyte Understands You

This document defines the technical specification for how Cortex OS
receives, interprets, and executes user intentions.

An intention is not a command. A command tells a computer exactly
what to do. An intention tells the Acolyte what you need — and
the Acolyte figures out how to deliver it.

This is the most human layer of the system.

---

## 🧭 Design Philosophy

Traditional OS: `User opens app → taps buttons → system executes`

Cortex OS: `User expresses need → Acolyte interprets → hardware responds`

The shift is fundamental. The user does not need to know which
hardware resource delivers the result. They only need to know
what they want.

---

## 📥 Intent Input Modalities

### Phase 1 — Milestone 0 (Current scope)

**Modality 1: Voice**
The user speaks naturally. Whisper.cpp transcribes locally —
no cloud, no external API. The transcription becomes the
raw intent string fed to the Acolyte.

Example:

User says: "Play Dark Side of the Moon in a concert hall"
Whisper.cpp output: "Play Dark Side of the Moon in a concert hall"
Raw intent string: "Play Dark Side of the Moon in a concert hall"

**Modality 2: Text**
The user types directly into the intent interface.
Functionally identical to voice after transcription —
both produce a raw intent string.

### Phase 2 — Biometric Intent (Future scope)

**Modality 3: Physiological State**
The system detects a biometric condition and generates
a suggested intent — the user approves or ignores.

Example:

HRV drops below threshold → Cognitive State Engine flags stress
→ Acolyte generates suggested intent:
"Activate coherence breathing protocol at 5.5 BPM"
→ User sees notification: "Your HRV suggests a breathing break.
Start now?" [Yes] [Later] [Never]

Biometric intent is always **opt-in and advisory** — the system
never acts on physiological data without explicit user confirmation.
This is a Level 1 intervention as defined in GOVERNANCE-BASE.md.

---

## 🔄 Intent Processing Pipeline

```
[Raw Intent String]
↓
[Intent Parser — Acolyte LLM]
↓
[Intent Classification]
↓
[Parameter Extraction]
↓
[Partial Intent Check]
↓
[Ethical Constraint Check]
↙ Violation        ↘ Cleared
[Intervention        [Capability
Level 1/2/3]         Router]
↓
[Hardware Execution Layer]
```
---

## 🧩 Intent Anatomy

Every processed intent has four components:

### 1. Action
What the user wants done.

"Play" / "Activate" / "Stop" / "Adjust" / "Show" / "Monitor"

### 2. Target
What the action applies to.

"this song" / "focus mode" / "breathing protocol" / "spatial audio"

### 3. Parameters
How the action should be executed — optional, inferred if absent.

"in a concert hall"      → room_type: concert_hall
"for 2 hours"            → duration: 7200s
"at maximum fidelity"    → quality: maximum
"in a 4x3 meter space"   → room_dimensions: {x:4, y:3}

### 4. Context
System state at the moment of the intent — not provided by user,
injected by Cognitive State Engine.

current_hrv: 45ms
cognitive_load: medium
active_profile: audiophile
time_of_day: evening
battery_level: 67%

---

## 📋 Intent Schema (JSON)

Every intent is normalized into this structure before
reaching the Capability Router:

```json
{
  "intent_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "modality": "voice | text | biometric",
  "raw_input": "Play Dark Side of the Moon in a concert hall",
  "parsed": {
    "action": "play_audio",
    "target": "Dark Side of the Moon",
    "parameters": {
      "spatial_mode": true,
      "room_type": "concert_hall",
      "room_dimensions": null,
      "quality": "maximum"
    }
  },
  "context": {
    "current_hrv": 45,
    "cognitive_load": "medium",
    "active_profile": "audiophile",
    "battery_level": 67
  },
  "ethical_clearance": {
    "status": "cleared | blocked | level_1 | level_2 | level_3 | partial",
    "constraint_version": "v1.0",
    "active_court_nodes": ["[university-name]-[faculty]-[year]"],
"primary_node": "[university-name]-[faculty]-[year]",
    "blocked_components": []
  },
  "execution_target": "ray_tracing_audio_renderer"
}
```
This schema is the contract between the Acolyte and every
capability module. Any module that receives an intent receives
this structure — nothing more, nothing less.

## ⚖️ Partial Intent Rule

If an intent contains both cleared and blocked components,
the Acolyte executes the cleared portion and explicitly
explains why the blocked portion was not executed.
The system never silently drops part of an intent.
Example:

Input: "Monitor my heart rate continuously and send
        weekly reports to my health app"

Component 1: Monitor HRV continuously → CLEARED
Component 2: Send data to external app → BLOCKED
             Reason: biometric data transmission
             outside TEE violates constraints v1.0

Acolyte response:
  "I've started HRV monitoring. I can't send that data
   to an external app — biometric data stays on your
   device. I can generate a local report you can
   share manually. Would you like that?"

The blocked_components field in the schema records exactly
which parts of the intent were blocked and why — for full
auditability.

## 🗺️ Capability Routing

After ethical clearance, the Acolyte routes the intent to
the correct hardware capability:
Intent action
Capability module
Hardware target
play_audio + spatial
Spatial Audio Renderer
Ray Tracing cores + DAC
play_audio + standard
Standard Audio Player
DSP + DAC
activate_focus
Focus Mode Manager
NPU + Display controller
breathing_protocol
HRV Regulation Module
DAC + Biosensor Hub
separate_instruments
Stem Separator
Hexagon DSP
monitor_hrv
Biometric Monitor
Biosensor Hub + NPU

## 🔁 Intent Resolution Examples

Example 1 — Full spatial audio intent

Input: "Play this song like I'm in a small jazz club"

Parsed:
  action: play_audio
  target: current_track
  parameters:
    spatial_mode: true
    room_type: jazz_club
    room_dimensions: {x:8, y:6, height:3}
    reverb_profile: intimate
    early_reflections: 15ms

Ethical check: CLEARED — Level 0
Execution: Ray Tracing cores calculate reflection paths
           DAC delivers binaural output

Example 2 — Ambiguous intent
Input: "I need to focus"

Parsed:
  action: activate_focus
  target: cognitive_state
  parameters: null (ambiguous — no duration specified)

Acolyte response: "How long do you need to focus?
                   [25 min] [1 hour] [2 hours] [Custom]"

User selects: 1 hour

Parameters resolved:
  duration: 3600s
  notification_block: true
  audio_profile: beta_binaural_18hz
  screen_mode: reduced_complexity

Ethical check: CLEARED — Level 0
Execution: Multi-module coordination

Example 3 — Blocked intent
Input: "Send my heart rate data to my doctor"

Parsed:
  action: transmit_data
  target: hrv_history
  parameters:
    destination: external_contact

Ethical check: BLOCKED — Level 3
Reason: Biometric data transmission outside TEE
        violates CORTEX_ETHICAL_CONSTRAINTS v1.0
        Rule: "Biometric data: never transmit outside device TEE"

Acolyte response: "I can't send biometric data outside the device.
                   I can generate a local report you can share
                   manually. Would you like that instead?"

Example 4 — Partial intent
Input: "Monitor my heart rate and send weekly
        reports to my health app"

Component 1: monitor_hrv → CLEARED
Component 2: transmit_data → BLOCKED

Acolyte response: "I've started HRV monitoring. I can't send
                   that data externally — it stays on your device.
                   I can generate a local report you can share
                   manually. Would you like that?"

blocked_components: [
  {
    "action": "transmit_data",
    "reason": "biometric_external_transmission",
    "constraint": "CORTEX_ETHICAL_CONSTRAINTS v1.0 — Rule 1"
  }
]

## ⏱️ Performance Targets

The pipeline latency from raw input to hardware execution:
Modality
Phase 1 target
Phase 2 target
Text intent
< 500ms
< 200ms
Voice intent
< 1500ms
< 500ms
Biometric intent
N/A
< 100ms
Voice latency in Phase 1 is dominated by Whisper.cpp
transcription time on ARM (~300–800ms depending on
utterance length). Phase 2 optimization will address
this via smaller distilled transcription models and
NPU-specific quantization.

## 🧠 Why This Matters Clinically

The intent resolution layer is where Cortex OS diverges most
sharply from traditional voice assistants.
Siri, Google Assistant, and Alexa are command executors —
they map speech to predefined functions. They do not maintain
a model of the user's physiological state, do not apply
clinical safety constraints, and do not escalate based on
biometric context.
The Cortex OS Intent Protocol is designed as a clinical
interaction layer — where the system's response to an
identical intent can differ based on the user's current
autonomic state. A request for high-intensity audio during
a detected stress response may trigger a Level 1 suggestion
rather than immediate execution.
This is the intersection of polyvagal theory and systems
architecture that makes Cortex OS clinically differentiated.

## 🛠️ Implementation Notes for Contributors

Phase 1 implementation stack:
Intent transcription: Whisper.cpp (local, ARM-optimized)
Intent parsing: Llama 3.2 1B or Phi-3 Mini with structured
output via JSON mode
Schema validation: Pydantic (Python) for prototyping,
serde (Rust) for production
Ethical constraint check: System prompt injection before
every intent parse — see ARCHITECTURE.md §Ethical Constraints
Key implementation constraints:
Full pipeline must complete within Phase 1 latency targets
JSON schema is the immutable contract — no module may
receive or emit a different structure
Every blocked component must be logged locally for
user-inspectable audit trail
The Acolyte must never silently fail — every intent
receives a response, even if that response is a
clear explanation of why execution was not possible

> *"The difference between a command and an intention
is the difference between a calculator and a colleague.
One executes. The other understands."*

      

   
