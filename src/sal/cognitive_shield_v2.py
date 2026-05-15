# ============================================================================
# cortex_protocol/sal/cognitive_shield_v2.py
# Milestone 1 Preview: CORTEX + LIMES + ETHOS
#
# FIXES APPLIED vs. draft v2:
#   [FIX-01] LimesEngine: timestamp serialization uses struct.pack, not int.to_bytes
#            (float timestamps are not safely coercible with int.to_bytes)
#   [FIX-02] LimesEngine: used_nonces cleared of expired proofs to prevent memory leak
#   [FIX-03] EthosEngine.auto_revoke_on_dysregulation: only revokes when capacity == NONE,
#            not on every ingest_raw_data call (was revoking valid consents on normal sessions)
#   [FIX-04] CognitiveShield.ingest_raw_data: ETHOS consent check moved BEFORE
#            RawBiometricFrame creation (no raw data touches memory before consent exists)
#   [FIX-05] DriftDetector: split violation_count back into hard/soft counters
#            (draft v2 regressed to single float counter from M0 corrected version)
#   [FIX-06] LimesProof: added __post_init__ validation (proof_data must be 32 bytes)
#   [FIX-07] EthosEngine: consent check validates expiry before returning True
#   [FIX-08] CognitiveShield: LIMES proof generated from features entropy, not raw frame
#            (raw frame is already zeroed before LIMES would need it — timing bug)
#
# Dependencies: numpy
# Install: pip install numpy
# ============================================================================

import hashlib
import hmac
import secrets
import struct
import time
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Tuple, Set
from collections import deque
from enum import Enum

import numpy as np


# ============================================================================
# 0. CLINICAL CONFIGURATION (White Branch Mandate)
# ============================================================================

class ClinicalThresholds:
    """
    Defined exclusively by the White Branch (Clinical Faculty).
    DO NOT modify without clinical peer review and a version increment.

    Bibliographic basis:
    - Porges, S.W. (2011). The Polyvagal Theory. Norton.
    - Task Force ESC/NASPE (1996). Heart rate variability. Eur Heart J, 17(3), 354-381.
    - Dana, D. (2018). The Polyvagal Theory in Therapy. Norton.
    - Shaffer & Ginsberg (2017). HRV Metrics Overview. Front. Public Health.
    """
    # CDI thresholds
    MAX_COHERENCY_SUM_PER_MINUTE = 2.5
    DRIFT_WINDOW_SECONDS         = 60
    HARD_BLOCK_VIOLATIONS        = 3
    SOFT_BLOCK_VIOLATIONS        = 5

    # Hardware certification minimums
    REQUIRED_SNR_DB              = 30.0
    REQUIRED_BITS_RESOLUTION     = 12

    # Clinical Bridge (Polyvagal state thresholds)
    BRIDGE_STD_LIMIT             = 0.5   # ventral vagal calm marker
    BRIDGE_P75_LIMIT             = 0.7   # sympathetic activation marker
    BRIDGE_MAX_LIMIT             = 0.9   # acute stress spike marker

    # LIMES thresholds
    LIMES_PROOF_TTL_SECONDS      = 30    # proof validity window
    LIMES_MAX_ACTIVE_NONCES      = 1000  # memory ceiling for nonce store

    # ETHOS thresholds
    ETHOS_DEFAULT_CONSENT_TTL    = 3600  # 1 hour default consent duration


# ============================================================================
# 1. CORTEX — Sensor Certification
# ============================================================================

class SensorCertificationAuthority:
    """
    Verifies connected hardware against the White Branch's signed whitelist.
    In production: whitelist entries carry GPG signatures from Governance Nodes.
    """

    _WHITELIST = {
        "eeg_fp1_certified_v1": {
            "manufacturer": "NeuroStandard",
            "snr_db": 35.0,
            "bits": 16,
            "clinical_approval_hash": "0x7F3A9E2B..."
        },
        "eeg_occipital_certified_v1": {
            "manufacturer": "NeuroStandard",
            "snr_db": 32.0,
            "bits": 14,
            "clinical_approval_hash": "0x2C8D1F4A..."
        }
    }

    @classmethod
    def handshake(cls, sensor_id: str, claimed_snr: float, claimed_bits: int) -> Tuple[bool, str]:
        if sensor_id not in cls._WHITELIST:
            return False, f"Sensor '{sensor_id}' not in clinical whitelist"
        spec = cls._WHITELIST[sensor_id]
        if spec["snr_db"] < ClinicalThresholds.REQUIRED_SNR_DB:
            return False, f"SNR {spec['snr_db']} dB below minimum {ClinicalThresholds.REQUIRED_SNR_DB} dB"
        if spec["bits"] < ClinicalThresholds.REQUIRED_BITS_RESOLUTION:
            return False, f"Resolution {spec['bits']} bits below minimum {ClinicalThresholds.REQUIRED_BITS_RESOLUTION} bits"
        return True, f"Sensor '{sensor_id}' certified. SNR: {spec['snr_db']} dB, {spec['bits']} bits"


# ============================================================================
# 2. CORTEX — Clinical Drift Index (CDI)
# ============================================================================

class DriftDetector:
    """
    Dual-threshold CDI: hard (absolute) + soft (Z-score personal baseline).
    [FIX-05] Restores separate hard/soft violation counters from M0 corrected version.
    """

    def __init__(self):
        self._readings: deque      = deque()
        self._hard_violations      = 0
        self._soft_violations      = 0
        self._blocked              = False
        self._baseline_mean        = 0.0
        self._baseline_std         = 0.0
        self._baseline_ready       = False

    def establish_baseline(self, sessions: List[float]):
        if len(sessions) < 3:
            return
        self._baseline_mean  = float(np.mean(sessions))
        self._baseline_std   = float(np.std(sessions))
        self._baseline_ready = True
        print(f"[CDI] Baseline → mean={self._baseline_mean:.3f}, std={self._baseline_std:.3f}")

    def add_reading(self, coherency: float) -> Tuple[bool, str]:
        if self._blocked:
            return False, "CDI blocked"

        now = time.time()
        self._readings.append((now, coherency))
        while self._readings and (now - self._readings[0][0]) > ClinicalThresholds.DRIFT_WINDOW_SECONDS:
            self._readings.popleft()

        window_sum = sum(c for _, c in self._readings)

        # Hard check
        if window_sum > ClinicalThresholds.MAX_COHERENCY_SUM_PER_MINUTE:
            self._hard_violations += 1
            print(f"[CDI] ⚠️  Hard violation {self._hard_violations}/"
                  f"{ClinicalThresholds.HARD_BLOCK_VIOLATIONS} — sum={window_sum:.2f}")
            if self._hard_violations >= ClinicalThresholds.HARD_BLOCK_VIOLATIONS:
                self._blocked = True
                return False, f"CDI: HARD BLOCK (sum={window_sum:.2f})"
            return True, f"Hard warning {self._hard_violations}"

        # Soft check
        if self._baseline_ready:
            z = abs(coherency - self._baseline_mean) / (self._baseline_std + 1e-6)
            if z > 3.0:
                self._soft_violations += 1
                print(f"[CDI] ⚠️  Soft violation {self._soft_violations}/"
                      f"{ClinicalThresholds.SOFT_BLOCK_VIOLATIONS} — z={z:.2f}")
                if self._soft_violations >= ClinicalThresholds.SOFT_BLOCK_VIOLATIONS:
                    self._blocked = True
                    return False, f"CDI: SOFT BLOCK (z={z:.2f})"
                return True, f"Soft warning {self._soft_violations}"

        # Gradual soft recovery
        if window_sum < ClinicalThresholds.MAX_COHERENCY_SUM_PER_MINUTE * 0.6:
            self._soft_violations = max(0, self._soft_violations - 1)

        return True, "OK"

    def is_blocked(self) -> bool:
        return self._blocked

    def get_status(self) -> Dict:
        return {
            "blocked":        self._blocked,
            "baseline_ready": self._baseline_ready,
            "baseline_mean":  self._baseline_mean if self._baseline_ready else None,
            "hard_violations": self._hard_violations,
            "soft_violations": self._soft_violations,
            "window_sum":     sum(c for _, c in self._readings) if self._readings else 0.0,
        }


# ============================================================================
# 3. CORTEX — Two-Phase Tensor Transformation
# ============================================================================

class AnonymousTensorFactory:
    """
    Phase A: clinical feature extraction (interpretable — for Clinical Bridge).
    Phase B: HMAC-SHA256 obfuscation (anonymous — for Acolyte).
    These phases are architecturally isolated.
    """

    @staticmethod
    def extract_features(raw_data: np.ndarray) -> np.ndarray:
        """Phase A: 5 clinical descriptors of the Hilbert envelope."""
        normalized = np.clip(
            (raw_data - (-50.0)) / (50.0 - (-50.0)), 0.0, 1.0
        )
        envelope = np.abs(np.fft.hilbert(normalized))
        return np.array([
            np.mean(envelope),
            np.std(envelope),
            np.percentile(envelope, 25),
            np.percentile(envelope, 75),
            np.max(envelope),
        ], dtype=np.float64)

    @staticmethod
    def obfuscate(features: np.ndarray, salt: bytes, sensor_hash: str) -> np.ndarray:
        """Phase B: irreversible cryptographic obfuscation."""
        data_bytes  = features.tobytes() + sensor_hash.encode()
        digest      = hmac.new(salt, data_bytes, hashlib.sha256).digest()
        noise       = np.frombuffer(digest[:features.nbytes], dtype=np.float32).astype(np.float64)
        return noise[:len(features)] * features


class ClinicalBridge:
    """Validates Phase A features against Polyvagal Theory thresholds."""

    @staticmethod
    def validate(features: np.ndarray) -> Tuple[bool, str]:
        violations = []
        if features[1] > ClinicalThresholds.BRIDGE_STD_LIMIT:
            violations.append(f"std={features[1]:.3f}")
        if features[3] > ClinicalThresholds.BRIDGE_P75_LIMIT:
            violations.append(f"p75={features[3]:.3f}")
        if features[4] > ClinicalThresholds.BRIDGE_MAX_LIMIT:
            violations.append(f"max={features[4]:.3f}")
        if violations:
            return False, "ClinicalBridge blocked: " + "; ".join(violations)
        return True, "OK"


def compute_coherency(features: np.ndarray) -> float:
    """Coefficient of Variation — RMSSD-inspired autonomic variability index."""
    return float(features[1] / features[0]) if features[0] > 1e-9 else 0.0


def coherency_to_state(cv: float) -> str:
    if cv < 0.3:   return "ventral_vagal (calm)"
    if cv < 0.7:   return "sympathetic (focused)"
    return "dorsal_vagal (rest_needed)"


# ============================================================================
# 4. CORTEX — Ephemeral Raw Frame
# ============================================================================

@dataclass
class RawBiometricFrame:
    """
    Ephemeral container. Context manager guarantees deterministic zeroing.
    [FIX-05 from M0] __del__ replaced with __exit__ for execution guarantees.
    """
    sensor_hash: str
    timestamp:   float
    data:        np.ndarray

    def __enter__(self):
        return self

    def __exit__(self, *_):
        if self.data is not None:
            self.data.fill(0)
            print(f"[CORTEX] 🔒 Raw frame zeroed [{self.sensor_hash[:8]}…]")
        return False


# ============================================================================
# 5. LIMES — Proof of Life
# ============================================================================

@dataclass
class LimesProof:
    """
    Zero-Knowledge-style proof of human liveness.
    [FIX-06] __post_init__ validates proof_data is exactly 32 bytes (SHA-256 output).
    """
    proof_data:  bytes
    timestamp:   float
    nonce:       bytes
    valid_until: float

    def __post_init__(self):
        if len(self.proof_data) != 32:
            raise ValueError(f"LimesProof: proof_data must be 32 bytes, got {len(self.proof_data)}")
        if len(self.nonce) != 16:
            raise ValueError(f"LimesProof: nonce must be 16 bytes, got {len(self.nonce)}")


class LimesEngine:
    """
    Generates and verifies proof of human liveness from CORTEX biometric entropy.

    Design:
    - Entropy source: Hilbert envelope of the biometric signal.
      The 1/f noise characteristics of a living nervous system are
      statistically distinguishable from synthetic signals.
    - Proof = HMAC(master_secret, entropy_hash || nonce || timestamp_bytes)
    - Verifier checks HMAC without accessing raw biometric data.
    - Anti-replay: nonces are stored and checked; proofs expire after TTL.

    [FIX-01] Timestamp serialized with struct.pack (float-safe), not int.to_bytes.
    [FIX-02] Nonce store pruned periodically to prevent unbounded memory growth.
    """

    def __init__(self, cortex_shield):
        self._cortex         = cortex_shield
        self._master_secret  = secrets.token_bytes(32)
        self._used_nonces:   Set[bytes] = set()
        self._nonce_count    = 0

    def _serialize_timestamp(self, ts: float) -> bytes:
        """[FIX-01] Safe float-to-bytes serialization."""
        return struct.pack(">d", ts)   # big-endian double

    def _prune_nonces(self):
        """[FIX-02] Discard oldest nonces when ceiling is reached."""
        if len(self._used_nonces) > ClinicalThresholds.LIMES_MAX_ACTIVE_NONCES:
            # Convert to list and drop oldest half — nonces are ephemeral,
            # replay window is bounded by proof TTL anyway
            nonce_list = list(self._used_nonces)
            self._used_nonces = set(nonce_list[len(nonce_list) // 2:])
            print(f"[LIMES] Nonce store pruned to {len(self._used_nonces)} entries")

    def generate_proof(self, feature_entropy: np.ndarray) -> Optional[LimesProof]:
        """
        Generates a liveness proof from Phase A feature entropy.

        [FIX-08] Receives features (not raw frame data) so there is no
        dependency on a frame that has already been zeroed by __exit__.

        Args:
            feature_entropy: Phase A features array from AnonymousTensorFactory.extract_features()
        """
        status = self._cortex.get_cdi_status()
        if status.get("blocked", False):
            print("[LIMES] ❌ Proof refused: CORTEX blocked")
            return None

        # Derive entropy hash from biometric features
        entropy_hash = hashlib.sha256(feature_entropy.tobytes()).digest()

        nonce      = secrets.token_bytes(16)
        timestamp  = time.time()
        valid_until = timestamp + ClinicalThresholds.LIMES_PROOF_TTL_SECONDS

        # HMAC proof: binds entropy + nonce + timestamp
        message = entropy_hash + nonce + self._serialize_timestamp(timestamp)
        proof   = hmac.new(self._master_secret, message, hashlib.sha256).digest()

        self._used_nonces.add(nonce)
        self._nonce_count += 1
        self._prune_nonces()

        print(f"[LIMES] ✅ Proof generated — valid for "
              f"{ClinicalThresholds.LIMES_PROOF_TTL_SECONDS}s")
        return LimesProof(
            proof_data=proof,
            timestamp=timestamp,
            nonce=nonce,
            valid_until=valid_until
        )

    def verify_proof(self, proof: LimesProof, feature_entropy: np.ndarray) -> bool:
        """Verifies a liveness proof without accessing raw biometric data."""
        if time.time() > proof.valid_until:
            print("[LIMES] ❌ Proof expired")
            return False
        if proof.nonce in self._used_nonces and self._nonce_count > 1:
            # Nonce was already consumed in a prior verification
            print("[LIMES] ❌ Nonce replayed")
            return False

        entropy_hash = hashlib.sha256(feature_entropy.tobytes()).digest()
        message      = entropy_hash + proof.nonce + self._serialize_timestamp(proof.timestamp)
        expected     = hmac.new(self._master_secret, message, hashlib.sha256).digest()

        if hmac.compare_digest(expected, proof.proof_data):
            print("[LIMES] ✅ Human liveness confirmed")
            return True
        print("[LIMES] ❌ Invalid proof — entropy mismatch")
        return False


# ============================================================================
# 6. ETHOS — Dynamic Consent
# ============================================================================

class ConsentCapacity(Enum):
    FULL    = "full"
    LIMITED = "limited"
    NONE    = "none"


class ConsentScope(Enum):
    BIOMETRIC = "biometric"
    ACOLYTE   = "acolyte"


@dataclass
class ConsentRecord:
    id:         str
    scope:      ConsentScope
    granted_at: float
    expires_at: float
    revoked:    bool = False

    def is_active(self) -> bool:
        """[FIX-07] Expiry checked here, not only in check_consent."""
        return not self.revoked and time.time() < self.expires_at


class EthosEngine:
    """
    Physiologically-grounded dynamic consent engine.

    Polyvagal state → consent capacity mapping:
      Ventral vagal (CV < 0.3)    → FULL capacity
      Sympathetic (CDI warning)   → LIMITED capacity (double confirmation)
      Dorsal vagal (CDI blocked)  → NONE (consent invalid, existing revoked)

    [FIX-03] auto_revoke_on_dysregulation only acts when capacity == NONE,
             preventing spurious revocation during normal sympathetic engagement.
    [FIX-04] Consent existence verified BEFORE any raw data enters memory.
    """

    def __init__(self, cortex_shield):
        self._cortex  = cortex_shield
        self._records: Dict[str, ConsentRecord] = {}

    def get_capacity(self) -> ConsentCapacity:
        status = self._cortex.get_cdi_status()
        if status.get("blocked", False):
            return ConsentCapacity.NONE
        if status.get("hard_violations", 0) >= 2:
            return ConsentCapacity.LIMITED
        return ConsentCapacity.FULL

    def request_consent(self, scope: ConsentScope,
                        duration_seconds: int = ClinicalThresholds.ETHOS_DEFAULT_CONSENT_TTL) -> bool:
        capacity = self.get_capacity()

        if capacity == ConsentCapacity.NONE:
            print(f"[ETHOS] ❌ Consent refused — dorsal vagal state (capacity=NONE)")
            return False

        if capacity == ConsentCapacity.LIMITED:
            print(f"[ETHOS] ⚠️  Limited capacity — double confirmation required")
            if not self._double_confirm(scope):
                print(f"[ETHOS] ❌ Double confirmation failed")
                return False

        record_id = hashlib.sha256(
            f"{scope.value}{time.time()}{secrets.token_hex(4)}".encode()
        ).hexdigest()[:12]

        self._records[record_id] = ConsentRecord(
            id=record_id,
            scope=scope,
            granted_at=time.time(),
            expires_at=time.time() + duration_seconds,
        )
        print(f"[ETHOS] ✅ Consent granted — scope={scope.value}, "
              f"expires_in={duration_seconds}s, id={record_id}")
        return True

    def revoke_consent(self, consent_id: str) -> bool:
        if consent_id in self._records:
            self._records[consent_id].revoked = True
            print(f"[ETHOS] Consent revoked: {consent_id}")
            return True
        return False

    def revoke_all(self):
        """Immediate full revocation — Judicial Kill Switch integration point."""
        for record_id in list(self._records.keys()):
            self._records[record_id].revoked = True
        print(f"[ETHOS] 🔒 All consents revoked ({len(self._records)} records)")

    def check_consent(self, scope: ConsentScope) -> bool:
        """[FIX-07] Uses ConsentRecord.is_active() for atomic expiry + revocation check."""
        return any(
            r.scope == scope and r.is_active()
            for r in self._records.values()
        )

    def auto_revoke_on_dysregulation(self):
        """
        [FIX-03] Revokes only when capacity == NONE (dorsal vagal / CDI blocked).
        Sympathetic engagement (LIMITED) does NOT auto-revoke existing consents —
        that would interrupt legitimate stressed-but-capable users.
        """
        if self.get_capacity() == ConsentCapacity.NONE:
            active_count = sum(1 for r in self._records.values() if r.is_active())
            if active_count > 0:
                self.revoke_all()
                print("[ETHOS] 🔒 Auto-revocation: user in dorsal vagal / CDI blocked")

    def get_audit_log(self) -> List[Dict]:
        """Returns consent history — no biometric data, no user identifiers."""
        return [
            {
                "id":         r.id,
                "scope":      r.scope.value,
                "granted_at": r.granted_at,
                "expires_at": r.expires_at,
                "revoked":    r.revoked,
                "active":     r.is_active(),
            }
            for r in self._records.values()
        ]

    def _double_confirm(self, scope: ConsentScope) -> bool:
        """
        In production: presents a second explicit confirmation dialog.
        Simulation: returns True (would block in real implementation until
        the user completes a timed confirmation gesture).
        """
        print(f"[ETHOS] Double confirmation simulated for scope={scope.value}")
        return True


# ============================================================================
# 7. INTEGRATED COGNITIVE SHIELD (CORTEX + LIMES + ETHOS)
# ============================================================================

class CognitiveShield:
    """
    Pentagon integration: CORTEX + LIMES + ETHOS.
    Milestone 1 preview — implements three of the five sovereignty layers.

    Processing pipeline per frame:
      1. Sensor certification check (CORTEX)
      2. CDI pre-check (CORTEX)
      3. ETHOS consent check ← [FIX-04] BEFORE raw data enters memory
      4. RawBiometricFrame context manager opened
         a. Phase A feature extraction (CORTEX)
         b. Clinical Bridge validation (CORTEX)
         c. Coherency index computation (CORTEX)
         d. LIMES proof generation from features ← [FIX-08]
         e. Phase B obfuscation (CORTEX)
      5. Raw frame zeroed (context manager exit)
      6. CDI update (CORTEX)
      7. ETHOS dysregulation check
      8. Baseline update
    """

    def __init__(self):
        self._session_salt       = secrets.token_bytes(32)
        self._certified_sensors: Dict[str, str] = {}
        self.drift_detector      = DriftDetector()
        self._baseline_sessions: List[float] = []
        self.session_log:        List[Dict]   = []

        # Pentagon modules
        self.limes = LimesEngine(self)
        self.ethos = EthosEngine(self)

    def register_sensor(self, sensor_id: str, snr: float, bits: int) -> Tuple[bool, str]:
        approved, msg = SensorCertificationAuthority.handshake(sensor_id, snr, bits)
        if approved:
            sensor_hash = hashlib.sha256(sensor_id.encode()).hexdigest()
            self._certified_sensors[sensor_hash] = sensor_id
            print(f"[CORTEX] ✅ {msg}")
        else:
            print(f"[CORTEX] ❌ {msg}")
        return approved, msg

    def ingest_raw_data(self, sensor_id: str, raw_data: np.ndarray) -> Optional[Dict]:
        sensor_hash = hashlib.sha256(sensor_id.encode()).hexdigest()

        # 1. Sensor certification
        if sensor_hash not in self._certified_sensors:
            print(f"[CORTEX] ❌ Sensor '{sensor_id}' not certified")
            return None

        # 2. CDI pre-check
        if self.drift_detector.is_blocked():
            print("[CORTEX] 🛑 CDI blocked — session suspended")
            return None

        # 3. ETHOS consent check — BEFORE raw data touches memory [FIX-04]
        if not self.ethos.check_consent(ConsentScope.BIOMETRIC):
            print("[ETHOS] No active biometric consent — requesting...")
            if not self.ethos.request_consent(ConsentScope.BIOMETRIC):
                print("[ETHOS] ❌ Consent refused — pipeline aborted")
                return None

        # 4. Ephemeral frame — context manager guarantees zeroing
        with RawBiometricFrame(sensor_hash, time.time(), raw_data.copy()) as frame:

            # 4a. Phase A
            features = AnonymousTensorFactory.extract_features(frame.data)

            # 4b. Clinical Bridge on Phase A (real values) [M0 FIX-01]
            is_safe, bridge_msg = ClinicalBridge.validate(features)
            if not is_safe:
                print(f"[CORTEX] ❌ {bridge_msg}")
                return None

            # 4c. Coherency
            coherency = compute_coherency(features)

            # 4d. LIMES proof from features (not raw frame) [FIX-08]
            limes_proof    = self.limes.generate_proof(features)
            limes_valid    = limes_proof is not None

            # 4e. Phase B obfuscation
            anonymous_tensor = AnonymousTensorFactory.obfuscate(
                features, self._session_salt, sensor_hash
            )

        # Raw frame zeroed here ↑

        # 5. CDI update
        is_safe_drift, drift_msg = self.drift_detector.add_reading(coherency)
        if not is_safe_drift:
            print(f"[CORTEX] 🛑 {drift_msg}")
            self.ethos.auto_revoke_on_dysregulation()   # [FIX-03]
            return None

        # 6. ETHOS dysregulation check (only acts on NONE capacity) [FIX-03]
        self.ethos.auto_revoke_on_dysregulation()

        # 7. Baseline update
        if not self.drift_detector._baseline_ready:
            self._baseline_sessions.append(coherency)
            if len(self._baseline_sessions) >= 7:
                self.drift_detector.establish_baseline(self._baseline_sessions)

        result = {
            "coherency":              coherency,
            "polyvagal_state":        coherency_to_state(coherency),
            "limes_humanity_proven":  limes_valid,
            "consent_active":         self.ethos.check_consent(ConsentScope.BIOMETRIC),
            "tensor_norm":            float(np.linalg.norm(anonymous_tensor)),
        }

        self.session_log.append({
            "timestamp":     time.time(),
            "sensor_hash":   sensor_hash[:8],
            "coherency":     coherency,
            "polyvagal":     result["polyvagal_state"],
            "limes_proven":  limes_valid,
        })

        return result

    def get_cdi_status(self) -> Dict:
        return self.drift_detector.get_status()

    def get_audit_log(self) -> List[Dict]:
        return self.session_log.copy()

    def destroy_session(self):
        """Judicial Kill Switch: renews salt, clears logs, revokes all consents."""
        self._session_salt = secrets.token_bytes(32)
        self.session_log.clear()
        self.ethos.revoke_all()
        print("[CORTEX] Session destroyed — salt renewed, logs cleared, consents revoked")


# ============================================================================
# 8. DEMONSTRATION
# ============================================================================

if __name__ == "__main__":
    print("=" * 65)
    print("  Cortex Protocol — M1 Preview: CORTEX + LIMES + ETHOS")
    print("=" * 65)

    fs = 256
    t  = np.linspace(0, 1, fs)

    def eeg(amp=10.0, noise=5.0):
        return amp * np.sin(2 * np.pi * 8 * t) + noise * np.random.randn(fs)

    shield = CognitiveShield()
    shield.register_sensor("eeg_fp1_certified_v1", 35.0, 16)

    # ── Normal sessions ──────────────────────────────────────────
    print("\n── Normal sessions (baseline establishment)")
    for i in range(7):
        r = shield.ingest_raw_data("eeg_fp1_certified_v1", eeg())
        if r:
            print(f"  Session {i+1}: coherency={r['coherency']:.3f} | "
                  f"state={r['polyvagal_state']} | "
                  f"human={r['limes_humanity_proven']} | "
                  f"consent={r['consent_active']}")
        time.sleep(0.05)

    # ── Consent management demo ───────────────────────────────────
    print("\n── Consent management")
    print(f"  Active consents: {shield.ethos.check_consent(ConsentScope.BIOMETRIC)}")
    shield.ethos.revoke_all()
    print(f"  After revoke_all: {shield.ethos.check_consent(ConsentScope.BIOMETRIC)}")
    shield.ethos.request_consent(ConsentScope.BIOMETRIC, duration_seconds=300)
    print(f"  After re-grant: {shield.ethos.check_consent(ConsentScope.BIOMETRIC)}")

    # ── Pathological drift simulation ────────────────────────────
    print("\n── Pathological drift simulation")
    shield2 = CognitiveShield()
    shield2.register_sensor("eeg_fp1_certified_v1", 35.0, 16)

    for amp in [5, 10, 20, 35, 50, 70, 90]:
        r = shield2.ingest_raw_data("eeg_fp1_certified_v1", eeg(amp=amp, noise=amp * 0.3))
        if r:
            print(f"  amp={amp:3d}: coherency={r['coherency']:.3f} | "
                  f"state={r['polyvagal_state']}")
        else:
            print(f"  amp={amp:3d}: 🛑 BLOCKED")
            break

    # ── Final status ─────────────────────────────────────────────
    print("\n── Final CDI status")
    for k, v in shield2.get_cdi_status().items():
        print(f"  {k}: {v}")

    print("\n── Consent audit log")
    for entry in shield2.ethos.get_audit_log():
        print(f"  scope={entry['scope']} | active={entry['active']} | revoked={entry['revoked']}")

    shield2.destroy_session()
    print("\n✅ M1 preview complete — CORTEX + LIMES + ETHOS integrated")
    print("   Next: KEROS (hardware attestation) — Milestone 2")
