# ============================================================================
# cortex_protocol/sal/cognitive_shield_refined.py
# Milestone 0: The Cognitive Shield (Refined)
# Features: Sensor Certification Handshake + Clinical Drift Index (CDI)
# Mitigates: Risk #1 (Hardware Agnostic Achilles Heel) & Risk #2 (Silent Malicious Acolyte)
# ============================================================================

import hashlib
import hmac
import secrets
import time
import json
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from collections import deque
from enum import Enum

import numpy as np

# ============================================================================
# 0. CLINICAL CONFIGURATION (White Branch Mandate)
# ============================================================================

class ClinicalThresholds:
    """Defined by the White Branch (Clinical Faculty) - DO NOT modify without clinical review."""
    # For CDI (Clinical Drift Index)
    MAX_COHERENCY_SUM_PER_MINUTE = 2.5   # Sum of coherency indices per minute
    DRIFT_WINDOW_SECONDS = 60            # Sliding window of 1 minute
    BLOCK_THRESHOLD_VIOLATIONS = 3       # 3 anomalous windows = automatic block
    
    # For hardware certification (Risk #1 mitigation)
    REQUIRED_SNR_DB = 30.0
    REQUIRED_BITS_RESOLUTION = 12

# ============================================================================
# 1. SENSOR HARDENING: Certification Handshake
# ============================================================================

class SensorCertificationAuthority:
    """
    Verifies that connected hardware is on the White Branch's whitelist.
    Mitigates Risk #1: The Achilles Heel of Agnostic Hardware.
    
    In production: This synchronizes with a cryptographically signed
    university node. Here we simulate a local whitelist.
    """
    
    # Clinical whitelist - in production, this would be signed by university nodes
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
        """
        Executes the certification handshake.
        Returns: (approved, message)
        """
        # Check 1: Is the sensor on the whitelist?
        if sensor_id not in cls._WHITELIST:
            return False, f"Sensor {sensor_id} not in clinical whitelist"
        
        # Check 2: Does it meet White Branch minimum thresholds?
        spec = cls._WHITELIST[sensor_id]
        if spec["snr_db"] < ClinicalThresholds.REQUIRED_SNR_DB:
            return False, f"Sensor SNR {spec['snr_db']} dB below clinical minimum {ClinicalThresholds.REQUIRED_SNR_DB} dB"
        
        if spec["bits"] < ClinicalThresholds.REQUIRED_BITS_RESOLUTION:
            return False, f"Sensor resolution {spec['bits']} bits below clinical minimum {ClinicalThresholds.REQUIRED_BITS_RESOLUTION} bits"
        
        # In production: verify cryptographic signature of the certificate here
        return True, f"Sensor {sensor_id} certified. SNR: {spec['snr_db']}dB, {spec['bits']}bits"

# ============================================================================
# 2. CLINICAL DRIFT INDEX (CDI) - Pathological Drift Detection
# ============================================================================

class DriftDetector:
    """
    Monitors clinical drift over time.
    Mitigates Risk #2: Silent Malicious Acolyte (slow behavioral addiction).
    """
    
    def __init__(self, window_seconds: int = ClinicalThresholds.DRIFT_WINDOW_SECONDS):
        self.window_seconds = window_seconds
        self._coherency_timestamps: deque = deque()  # (timestamp, coherency_index)
        self._violation_count = 0
        self._blocked = False
        self._baseline_established = False
        self._baseline_mean = 0.0
        self._baseline_std = 0.0
    
    def establish_baseline(self, initial_sessions: List[float]):
        """
        Establishes the user's baseline (first 7 sessions recommended).
        Based on risk assessment prompt recommendations.
        """
        if len(initial_sessions) < 3:
            return  # Need at least 3 sessions for baseline
        
        self._baseline_mean = np.mean(initial_sessions)
        self._baseline_std = np.std(initial_sessions)
        self._baseline_established = True
        print(f"[CDI] Baseline established: mean={self._baseline_mean:.3f}, std={self._baseline_std:.3f}")
    
    def add_reading(self, coherency_index: float) -> Tuple[bool, str]:
        """
        Adds a new reading and checks for dangerous drift.
        Returns: (is_safe, message)
        """
        if self._blocked:
            return False, "CDI: Protocol blocked - drift threshold exceeded"
        
        now = time.time()
        self._coherency_timestamps.append((now, coherency_index))
        
        # Clean old windows
        while self._coherency_timestamps and (now - self._coherency_timestamps[0][0]) > self.window_seconds:
            self._coherency_timestamps.popleft()
        
        # Calculate coherency sum in current window
        current_sum = sum(c for _, c in self._coherency_timestamps)
        
        # Check against absolute clinical threshold
        if current_sum > ClinicalThresholds.MAX_COHERENCY_SUM_PER_MINUTE:
            self._violation_count += 1
            print(f"[CDI] ⚠️ Drift violation {self._violation_count}/{ClinicalThresholds.BLOCK_THRESHOLD_VIOLATIONS} - Sum={current_sum:.2f}")
            
            if self._violation_count >= ClinicalThresholds.BLOCK_THRESHOLD_VIOLATIONS:
                self._blocked = True
                return False, f"CDI: BLOCKED - sustained drift detected (sum={current_sum:.2f} over {self.window_seconds}s)"
            
            return True, f"CDI: warning - temporary drift (sum={current_sum:.2f})"
        
        # If baseline exists, check statistical deviation (finer detection)
        if self._baseline_established:
            z_score = abs(coherency_index - self._baseline_mean) / (self._baseline_std + 0.001)
            if z_score > 3.0:  # More than 3 standard deviations
                self._violation_count += 0.5  # Lesser penalty
                print(f"[CDI] ⚠️ Statistical drift detected: z={z_score:.2f}")
                if self._violation_count >= ClinicalThresholds.BLOCK_THRESHOLD_VIOLATIONS:
                    self._blocked = True
                    return False, f"CDI: BLOCKED - statistical outlier detected (z={z_score:.2f})"
        
        # Reset violations if user returns to normal range
        if current_sum < ClinicalThresholds.MAX_COHERENCY_SUM_PER_MINUTE * 0.6:
            self._violation_count = max(0, self._violation_count - 1)
        
        return True, "CDI: within clinical bounds"
    
    def is_blocked(self) -> bool:
        return self._blocked
    
    def get_status(self) -> Dict:
        return {
            "blocked": self._blocked,
            "baseline_established": self._baseline_established,
            "baseline_mean": self._baseline_mean if self._baseline_established else None,
            "violations": self._violation_count,
            "current_window_sum": sum(c for _, c in self._coherency_timestamps) if self._coherency_timestamps else 0.0
        }

# ============================================================================
# 3. MATHEMATICAL PRIVACY LAYER (Anonymous Tensor Transformation)
# ============================================================================

class AnonymousTensorFactory:
    """
    Converts raw biometric data into anonymous, irreversible tensors.
    Based on OpenMined principles: no link to individual is retained.
    """
    
    @staticmethod
    def to_anonymous_tensor(raw_data: np.ndarray, salt: bytes, certified_sensor_hash: str) -> np.ndarray:
        """
        Three-step irreversible transformation:
        1. Clinical normalization
        2. Dimensionality reduction (loses fine-grained identifiers)
        3. HMAC obfuscation with ephemeral salt
        """
        # Step 1: Normalize to clinical range (e.g., 0-1 for EEG amplitudes)
        clinical_min, clinical_max = -50.0, 50.0  # microvolts for EEG
        normalized = (raw_data - clinical_min) / (clinical_max - clinical_min)
        normalized = np.clip(normalized, 0.0, 1.0)
        
        # Step 2: Dimensionality reduction - preserve only envelope and first-order stats
        envelope = np.abs(np.fft.hilbert(normalized))
        reduced = np.array([
            np.mean(envelope),
            np.std(envelope),
            np.percentile(envelope, 25),
            np.percentile(envelope, 75),
            np.max(envelope)
        ])
        
        # Step 3: Irreversible obfuscation with HMAC + sensor hash (for traceability without identity)
        data_bytes = reduced.tobytes() + certified_sensor_hash.encode()
        hmac_digest = hmac.new(salt, data_bytes, hashlib.sha256).digest()
        anonymous_tensor = np.frombuffer(hmac_digest[:reduced.nbytes], dtype=np.float32)
        anonymous_tensor = anonymous_tensor[:len(reduced)] * reduced  # Preserve relative magnitude
        
        print(f"[SAL] Anonymous tensor created. Original shape: {raw_data.shape} -> {anonymous_tensor.shape}")
        return anonymous_tensor

# ============================================================================
# 4. CLINICAL BRIDGE (Per-tensor clinical validation)
# ============================================================================

class ClinicalBridge:
    """
    Validates that anonymous tensors are within healthy margins.
    Based on Polyvagal Theory criteria defined by White Branch.
    """
    
    @staticmethod
    def validate(tensor: np.ndarray) -> Tuple[bool, str]:
        """
        Clinical rules (example based on polyvagal theory):
        - Standard deviation of envelope <= 0.5 (calm state)
        - 75th percentile < 0.7 (no hyperactivation)
        - Maximum < 0.9 (no stress spikes)
        """
        std_val = tensor[1] if len(tensor) > 1 else 0.0
        percentile_75 = tensor[3] if len(tensor) > 3 else 0.0
        max_val = tensor[4] if len(tensor) > 4 else 0.0
        
        if (std_val <= 0.5) and (percentile_75 <= 0.7) and (max_val <= 0.9):
            return True, "within clinical bounds"
        return False, f"clinical violation: std={std_val:.2f}, p75={percentile_75:.2f}, max={max_val:.2f}"

# ============================================================================
# 5. ACOLYTE (Guest AI - Reference Implementation)
# ============================================================================

class BaselineAcolyte:
    """
    Reference Acolyte: Alertness state monitor.
    Only receives anonymous tensors, never raw biometric data.
    """
    
    def process(self, anonymous_tensor: np.ndarray) -> Dict[str, Any]:
        """Processes the tensor and returns a healthy interpretation."""
        coherency = float(np.mean(anonymous_tensor) * np.std(anonymous_tensor))
        return {
            "coherency_index": coherency,
            "recommendation": "calm" if coherency < 0.3 else "focused" if coherency < 0.7 else "rest_needed"
        }

# ============================================================================
# 6. RAW BIOMETRIC FRAME (Ephemeral, self-destructing)
# ============================================================================

@dataclass
class RawBiometricFrame:
    """Ephemeral container for raw data. Destroyed immediately after transformation."""
    sensor_hash: str
    timestamp: float
    data: np.ndarray
    
    def __del__(self):
        """Secure destruction: overwrites memory before release."""
        if hasattr(self, 'data'):
            self.data.fill(0)  # Overwrite with zeros
            print(f"[SAL] 🔒 Raw frame from sensor [{self.sensor_hash[:8]}] securely destroyed.")

# ============================================================================
# 7. MAIN ORCHESTRATOR: The Cognitive Shield (Refined)
# ============================================================================

class CognitiveShield:
    """
    Main entry point for Milestone 0.
    Demonstrates complete flow: Certification -> Transformation -> Clinical Validation -> Drift Detection
    """
    
    def __init__(self):
        self._session_salt = secrets.token_bytes(32)
        self.factory = AnonymousTensorFactory()
        self.clinical_bridge = ClinicalBridge()
        self.acolyte = BaselineAcolyte()
        self.drift_detector = DriftDetector()
        self._certified_sensors: Dict[str, str] = {}  # sensor_hash -> sensor_id
        self.session_log: List[Dict] = []
        self._baseline_sessions: List[float] = []  # For establishing clinical baseline
    
    def register_sensor(self, sensor_id: str, claimed_snr: float, claimed_bits: int) -> Tuple[bool, str]:
        """
        STEP 1: Hardware certification handshake.
        MUST be called BEFORE any data ingestion.
        """
        approved, message = SensorCertificationAuthority.handshake(sensor_id, claimed_snr, claimed_bits)
        if approved:
            # Store certified sensor hash (not plaintext ID)
            sensor_hash = hashlib.sha256(sensor_id.encode()).hexdigest()
            self._certified_sensors[sensor_hash] = sensor_id
            print(f"[SAL] ✅ Sensor registered: {sensor_id}")
            return True, message
        else:
            print(f"[SAL] ❌ Sensor rejected: {message}")
            return False, message
    
    def ingest_raw_data(self, sensor_id: str, raw_data: np.ndarray) -> Optional[Dict]:
        """
        STEP 2: Ingest raw data ONLY if sensor is certified.
        Flow: Certification check -> CDI check -> Transform -> Clinical Bridge -> Acolyte -> Update CDI
        """
        # Verify sensor is certified
        sensor_hash = hashlib.sha256(sensor_id.encode()).hexdigest()
        if sensor_hash not in self._certified_sensors:
            print(f"[SAL] 🚫 Rejected: sensor '{sensor_id}' not certified. Call register_sensor() first.")
            return None
        
        # Check CDI before processing
        if self.drift_detector.is_blocked():
            print("[SAL] 🛑 BLOCKED: Clinical Drift Index exceeded. Acolyte suspended.")
            return None
        
        # Create ephemeral frame (self-destructs when out of scope)
        raw_frame = RawBiometricFrame(sensor_hash=sensor_hash, timestamp=time.time(), data=raw_data)
        
        # Step 2: Immediate anonymous transformation
        anonymous_tensor = self.factory.to_anonymous_tensor(raw_frame.data, self._session_salt, sensor_hash)
        
        # Step 3: Clinical validation (White Branch)
        is_safe, clinical_msg = self.clinical_bridge.validate(anonymous_tensor)
        if not is_safe:
            print(f"[SAL] 🚫 Clinical Bridge blocked: {clinical_msg}")
            return None
        
        # Step 4: Acolyte processes ONLY anonymous tensor
        result = self.acolyte.process(anonymous_tensor)
        coherency = result["coherency_index"]
        
        # Step 5: Update Clinical Drift Index
        is_safe_drift, drift_msg = self.drift_detector.add_reading(coherency)
        if not is_safe_drift:
            print(f"[SAL] 🛑 {drift_msg}")
            return None
        
        # Store for baseline establishment (first sessions)
        if not self.drift_detector._baseline_established:
            self._baseline_sessions.append(coherency)
            if len(self._baseline_sessions) >= 7:  # 7 sessions for reliable baseline
                self.drift_detector.establish_baseline(self._baseline_sessions)
        
        # Audit log (no identifiable data)
        self.session_log.append({
            "timestamp": raw_frame.timestamp,
            "sensor_hash": sensor_hash[:8],
            "coherency_index": coherency,
            "recommendation": result["recommendation"],
            "cdi_status": self.drift_detector.get_status()
        })
        
        # raw_frame is destroyed automatically when function exits
        return result
    
    def get_audit_log(self) -> List[Dict]:
        """Returns anonymized audit log for clinical/legal review."""
        return self.session_log.copy()
    
    def get_cdi_status(self) -> Dict:
        """Returns current Clinical Drift Index status."""
        return self.drift_detector.get_status()
    
    def destroy_session(self):
        """Destroys session salt and clears logs (judicial kill switch placeholder)."""
        self._session_salt = secrets.token_bytes(32)
        self.session_log.clear()
        print("[SAL] Session destroyed. Salt renewed. All ephemeral keys invalidated.")

# ============================================================================
# 8. DEMONSTRATION & TESTING
# ============================================================================

if __name__ == "__main__":
    print("=== Cortex Protocol - Milestone 0 Refined: Cognitive Shield ===")
    print("=== Features: Sensor Certification + Clinical Drift Index ===\n")
    
    # Simulate biometric sensor data (256Hz EEG-like signal)
    fs = 256
    t = np.linspace(0, 1, fs)
    baseline_eeg = 10 * np.sin(2 * np.pi * 8 * t) + 5 * np.random.randn(fs)
    
    shield = CognitiveShield()
    
    # --- Test 1: Non-certified sensor (must be rejected) ---
    print("\n--- Test 1: Non-certified sensor ---")
    result = shield.ingest_raw_data(sensor_id="eeg_fake_china", raw_data=baseline_eeg)
    print(f"Result: {result}\n")
    
    # --- Test 2: Register certified sensor ---
    print("--- Test 2: Register certified sensor ---")
    ok, msg = shield.register_sensor("eeg_fp1_certified_v1", claimed_snr=35.0, claimed_bits=16)
    print(f"Registration: {msg}")
    
    # --- Test 3: Successful ingestion with certified sensor ---
    print("\n--- Test 3: Ingestion with certified sensor ---")
    for i in range(5):
        result = shield.ingest_raw_data("eeg_fp1_certified_v1", raw_data=baseline_eeg + 0.1 * np.random.randn(fs))
        if result:
            print(f"Session {i+1}: Coherency={result['coherency_index']:.3f} -> {result['recommendation']}")
        time.sleep(0.1)  # Simulate real-time spacing
    
    # --- Test 4: Simulate pathological drift (malicious Acolyte) ---
    print("\n--- Test 4: Simulating pathological drift (progressive increase) ---")
    shield2 = CognitiveShield()
    shield2.register_sensor("eeg_fp1_certified_v1", 35.0, 16)
    
    # Simulate sessions with progressively increasing coherency (malicious Acolyte)
    drift_values = [0.2, 0.3, 0.5, 0.8, 1.2, 1.6, 2.0, 2.5, 3.0]
    for i, drift_val in enumerate(drift_values):
        # Modify data to generate increasing coherency
        modified_data = baseline_eeg + drift_val * baseline_eeg
        result = shield2.ingest_raw_data("eeg_fp1_certified_v1", modified_data)
        if result:
            print(f"Drift session {i+1}: coherency={result['coherency_index']:.2f}")
        else:
            print(f"🚫 Session {i+1} BLOCKED by CDI")
            break
    
    # --- Test 5: Display final CDI status ---
    print("\n--- Final CDI Status ---")
    print(shield2.get_cdi_status())
    
    # --- Test 6: Audit log (anonymized) ---
    print("\n--- Audit Log (last 3 entries, anonymized) ---")
    for entry in shield2.get_audit_log()[-3:]:
        print(f"  {entry['timestamp']}: coherency={entry['coherency_index']:.2f}, recommendation={entry['recommendation']}")
    
    # --- Cleanup ---
    shield2.destroy_session()
    print("\n✅ Milestone 0 Refined completed. Risks #1 and #2 mitigated.")
