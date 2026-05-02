# 🧠 Clinical-Technical Bridge: Evidence-Based Protocols for Cortex OS

This document establishes the scientific foundation for Cortex OS capability
modules that interface with human physiology. It serves two audiences equally:
**engineers** who need to translate clinical protocols into hardware parameters,
and **researchers** who need to verify the evidence base behind each intervention.

Every module in Cortex OS that touches biometric data or delivers physiological
stimuli must have a corresponding section in this document.

---

## 📐 How to Read This Document

Each section follows the same structure:

- **Clinical basis** — the validated science behind the intervention
- **Key parameters** — the specific values engineers need to implement
- **Hardware mapping** — how those parameters translate to Snapdragon hardware
- **Safety boundaries** — the limits the Ethical Courts must enforce
- **References** — peer-reviewed sources, not opinion

---

## ❤️ Module 1: HRV & Cardiac Coherence

### Clinical Basis

Heart Rate Variability (HRV) is the variation in time between successive
heartbeats. It is the most validated non-invasive biomarker of autonomic
nervous system balance. High HRV correlates with parasympathetic dominance,
emotional regulation capacity, and cognitive flexibility. Low HRV correlates
with chronic stress, anxiety, and poor executive function.

**Cardiac coherence** is a specific HRV state characterized by a rhythmic,
sine-wave-like oscillation at approximately 0.1 Hz (one breath cycle every
10 seconds). In this state, heart, brain, and respiratory system synchronize,
producing measurable improvements in cortical function and emotional regulation.

Key validated protocols:
- **HeartMath Institute coherence protocol:** 5.5 breaths/minute (inhale
  5s, exhale 5s) produces optimal HRV coherence in most adults.
- **Lecomte & Servant (2014):** Cardiac coherence at 0.1 Hz produces
  significant reduction in cortisol and improvement in HRV indices (SDNN,
  RMSSD) after 4 weeks of daily practice.
- **McCraty et al. (2009):** HRV biofeedback produces lasting autonomic
  regulation improvements measurable via frequency domain analysis
  (LF/HF ratio normalization).

### Key Parameters for Engineers

| Parameter | Value | Clinical source |
|---|---|---|
| Coherence frequency | 0.1 Hz | HeartMath, McCraty 2009 |
| Optimal breath rate | 5.5 breaths/min | Lecomte & Servant 2014 |
| Inhale/exhale ratio | 1:1 (5s / 5s) | HeartMath protocol |
| Minimum session duration | 5 minutes | Servant-Schreiber 2004 |
| Coherence score threshold | LF/HF ratio ≥ 2.0 | McCraty et al. 2009 |
| Sampling rate for HRV | ≥ 250 Hz | Task Force ESC/NASPE 1996 |

### Hardware Mapping (Snapdragon 8 Gen 1)

- **Biosensor input:** Heart rate sensor sampled at ≥ 250 Hz via Biosensor
  Hub low-power core
- **Visual pacing guide:** Breathing pacer rendered at coherence frequency
  (0.1 Hz) via adaptive UI layer — smooth sine-wave animation, not
  mechanical timer
- **Audio pacing:** Optional binaural tone at 0.1 Hz delivered via
  high-fidelity DAC, bypassing generic audio stack
- **Real-time analysis:** HRV frequency domain analysis (FFT) executed
  on NPU — LF/HF ratio calculated every 30 seconds
- **Coherence feedback:** Haptic + visual confirmation when coherence
  threshold is reached

### Safety Boundaries (Ethical Court Mandate)

- Session duration hard cap: 60 minutes without user confirmation to continue
- Minimum inter-session interval: 30 minutes
- Contraindication flag: Users with cardiac arrhythmia must receive
  explicit disclaimer before first use
- No HRV data leaves the device under any circumstances

---

## 🎵 Module 2: Therapeutic Audio & Frequencies

### Clinical Basis

Sound directly modulates the autonomic nervous system through two primary
pathways: the **acoustic-vagal pathway** (the vagus nerve responds to
specific frequency ranges in the human voice and music) and **entrainment**
(the brain's tendency to synchronize its oscillatory activity to external
rhythmic stimuli).

**Polyvagal Theory (Porges, 1994, 2011)** establishes that the middle ear
muscles are directly innervated by the vagus nerve, and that frequencies
between 500–2000 Hz — the prosodic range of the human voice — activate
the ventral vagal complex, producing feelings of safety and social engagement.
Frequencies below 500 Hz activate defensive responses (mobilization or
shutdown).

**Binaural beats** are an auditory processing artifact: when two tones of
slightly different frequencies are presented separately to each ear, the
brain perceives a third tone equal to the difference. This perceived tone
can entrain cortical oscillations:

| Beat frequency | Brainwave band | Clinical effect |
|---|---|---|
| 1–4 Hz | Delta | Deep sleep induction |
| 4–8 Hz | Theta | Deep relaxation, creativity |
| 8–12 Hz | Alpha | Calm focus, stress reduction |
| 12–30 Hz | Beta | Alert focus, cognitive performance |
| 40 Hz | Gamma | Attention, working memory |

**Key references:**
- Porges, S.W. (2011). *The Polyvagal Theory.* Norton.
- Oster, G. (1973). Auditory beats in the brain. *Scientific American.*
- Jirakittayakorn & Wongsawat (2017): 6 Hz binaural beats significantly
  reduce anxiety scores (STAI) vs. control — randomized controlled trial.
- Huang & Charyton (2008): Meta-analysis confirming entrainment effects
  of binaural beats on EEG oscillations.

### Key Parameters for Engineers

| Use case | Carrier frequency | Beat frequency | Duration |
|---|---|---|---|
| Stress reduction | 200 Hz | 10 Hz (Alpha) | 15–20 min |
| Deep focus | 200 Hz | 18 Hz (Beta) | 25–50 min |
| Sleep induction | 150 Hz | 3 Hz (Delta) | 20–30 min |
| Creativity / flow | 200 Hz | 6 Hz (Theta) | 15–30 min |
| Anxiety reduction | 200 Hz | 6 Hz (Theta) | 20 min |
| Vagal activation | 500–2000 Hz | N/A | Continuous |

**3D Spatial Audio (Ray Tracing application):**
- Room size directly affects perceived safety. Larger virtual spaces
  (concert hall acoustic profile) reduce threat response vs. small
  enclosed spaces (Palomäki et al., 2005).
- Optimal therapeutic spatial profile: medium room, 25–40 ms early
  reflections, RT60 between 0.8–1.2 seconds.
- Ray Tracing cores calculate reflection paths in real time based on
  user-defined room dimensions.

### Hardware Mapping (Snapdragon 8 Gen 1)

- **Binaural rendering:** Left/right channel separation via high-fidelity
  DAC — requires headphone output, not speaker
- **Carrier tone generation:** Synthesized on Hexagon DSP — zero latency,
  no CPU load
- **3D spatial profile:** Ray Tracing cores calculate acoustic reflections
  per user-defined room geometry
- **Frequency safety filter:** Hardware-level low-pass filter prevents
  delivery of frequencies above 20 kHz or below 20 Hz at therapeutic
  amplitudes

### Safety Boundaries (Ethical Court Mandate)

- Maximum volume for binaural sessions: 60 dB SPL (WHO safe listening)
- Binaural beats require headphones — speaker delivery is ineffective
  and must be flagged to user
- Contraindications to flag: epilepsy (entrainment risk), tinnitus
  (carrier frequency sensitivity), first trimester pregnancy
- No binaural beat session longer than 60 minutes without break

---

## 🛡️ Module 3: Neurodivergence Support (ASD / ADHD)

### Clinical Basis

**Autism Spectrum Disorder (ASD)** is characterized, among other features,
by atypical sensory processing — hyper or hyposensitivity to auditory,
visual, tactile, and proprioceptive stimuli. The DSM-5 includes sensory
processing differences as a diagnostic criterion (Criterion B4).

**ADHD** involves dysregulation of the dopaminergic and noradrenergic
systems, producing difficulties in sustained attention, impulse control,
and working memory. Environmental stimulation load directly modulates
symptom severity.

**Safe and Sound Protocol (SSP, Porges & Unyte):** A clinically validated
auditory intervention that filters music through a algorithm emphasizing
the 500–2000 Hz prosodic range, directly stimulating middle ear muscles
and the ventral vagal complex. Five hours of intervention showed significant
reduction in auditory hypersensitivity and social anxiety in ASD
(Porges et al., 2014 — published in *Frontiers in Integrative Neuroscience*).

**Sensory load model (Miller et al., 2007):** Sensory overload in ASD
follows a cumulative threshold model — small stimuli accumulate until
a regulatory breakdown occurs. Real-time monitoring and preemptive
attenuation can prevent overload episodes.

### Key Parameters for Engineers

| Parameter | ASD hypersensitivity | ADHD overstimulation |
|---|---|---|
| Screen Hz reduction | 60 Hz → 30 Hz | No change |
| Blue light filter | Activate above stress threshold | Activate after 8 PM |
| Audio frequency filter | Attenuate < 500 Hz and > 2000 Hz | Attenuate > 3000 Hz |
| Notification batching | Group, never interrupt | Max 3 per hour in focus |
| Transition warnings | 5-minute advance alert | 2-minute advance alert |
| Sensory load score | Calculated every 60 seconds | Calculated every 120 seconds |

### Hardware Mapping (Snapdragon 8 Gen 1)

- **Sensory load monitoring:** Ambient sound level (microphone) +
  screen brightness + notification frequency → composite load score
  calculated on NPU every 60 seconds
- **Preemptive attenuation:** Hexagon DSP applies real-time EQ filter
  (parametric) to all audio output when load score exceeds threshold
- **Screen modulation:** Display Hz and color temperature adjusted via
  hardware display controller — not software overlay
- **Transition system:** Acolyte delivers advance warnings before
  calendar events, app closures, or context switches

### Safety Boundaries (Ethical Court Mandate)

- Sensory profile is user-defined — the system never auto-classifies
  a user as neurodivergent
- All interventions are opt-in per session, not permanent by default
- Sensory load score and profile data never leave the device
- Override is always one tap — no confirmation dialogs during
  sensory crisis

---

## 🫀 Module 4: Autonomic Nervous System Regulation

### Clinical Basis

The Autonomic Nervous System (ANS) regulates involuntary physiological
functions through two primary branches: the **sympathetic** (mobilization,
threat response) and the **parasympathetic** (restoration, social engagement).

**Polyvagal Theory (Porges, 1994)** extends this model with a third
circuit: the **ventral vagal complex**, a phylogenetically recent
myelinated vagal pathway that supports social engagement, emotional
regulation, and felt safety. Technology interaction that triggers
threat responses (social comparison, infinite scroll, notification
anxiety) chronically activates the sympathetic branch, suppressing
the ventral vagal state.

Cortex OS positions itself as the first OS designed to actively
maintain ventral vagal dominance during device use.

**Key physiological markers of ANS state:**

| ANS State | HRV | Respiratory rate | Skin conductance |
|---|---|---|---|
| Ventral vagal (safe) | High | 12–18 rpm | Low, stable |
| Sympathetic (threat) | Low | > 20 rpm | High, rising |
| Dorsal vagal (shutdown) | Very low | < 10 rpm | Low, flat |

**References:**
- Porges, S.W. (1994). Vagal tone: A physiologic marker of stress
  vulnerability. *Pediatrics.*
- Thayer, J.F. & Lane, R.D. (2009). Claude Bernard and the heart-brain
  connection. *Neuroscience & Biobehavioral Reviews.*
- Laborde, S. et al. (2017). Heart rate variability and cardiac vagal
  tone in psychophysiological research. *Frontiers in Psychology.*

### Key Parameters for Engineers

| Marker | Ventral vagal | Sympathetic | Dorsal vagal |
|---|---|---|---|
| RMSSD | > 40 ms | 20–40 ms | < 20 ms |
| LF/HF ratio | 1.5–2.5 | > 3.0 | < 0.5 |
| Respiratory rate | 12–18 rpm | > 20 rpm | < 10 rpm |
| Acolyte response | No intervention | Level 1 nudge | Level 2 alert |

### Hardware Mapping (Snapdragon 8 Gen 1)

- **Continuous ANS monitoring:** HRV (heart rate sensor) + respiratory
  rate (accelerometer breathing detection) + optional GSR
  — all processed locally on NPU
- **State classification:** 3-state model (ventral/sympathetic/dorsal)
  updated every 30 seconds
- **Graduated response:**
  - Ventral vagal → system operates normally
  - Sympathetic → Acolyte offers breathing protocol or audio intervention
    (user can ignore with one tap)
  - Dorsal vagal → Acolyte delivers Level 2 alert, offers pre-agreed
    intervention if configured in Level 2 mode (see GOVERNANCE-BASE.md)

### Safety Boundaries (Ethical Court Mandate)

- ANS state classification is advisory only — never used to restrict
  device functionality without explicit user consent
- Dorsal vagal state (shutdown/dissociation) triggers human-directed
  alert if user has pre-configured an emergency contact
- All physiological data is ephemeral by default — not stored beyond
  the current session unless user explicitly enables history
- System never interprets physiological data as diagnostic — it is
  a regulation support tool, not a medical device

---

## 📚 Master Reference List

- HeartMath Institute. (2015). *Science of the Heart, Vol. 2.*
- Jirakittayakorn, N. & Wongsawat, Y. (2017). Brain responses to
  6-Hz binaural beats. *Frontiers in Neuroscience.*
- Laborde, S. et al. (2017). HRV and cardiac vagal tone in
  psychophysiological research. *Frontiers in Psychology.*
- Lecomte, J. & Servant, D. (2014). Cardiac coherence training.
  *Journal of Psychosomatic Research.*
- McCraty, R. et al. (2009). The coherent heart. *Integral Review.*
- Miller, L.J. et al. (2007). Concept evolution in sensory integration.
  *American Journal of Occupational Therapy.*
- Oster, G. (1973). Auditory beats in the brain. *Scientific American.*
- Palomäki, K. et al. (2005). Spatial sound perception and room acoustics.
  *JASA.*
- Porges, S.W. (1994). Vagal tone as physiologic marker. *Pediatrics.*
- Porges, S.W. (2011). *The Polyvagal Theory.* Norton.
- Porges, S.W. et al. (2014). Reducing auditory hypersensitivities in
  autistic spectrum disorder. *Frontiers in Integrative Neuroscience.*
- Task Force ESC/NASPE. (1996). HRV standards of measurement.
  *Circulation.*
- Thayer, J.F. & Lane, R.D. (2009). Heart-brain connection.
  *Neuroscience & Biobehavioral Reviews.*

---

> *"The body keeps the score. The OS should help keep it safe."*
>
> — Inspired by Bessel van der Kolk (2014)
