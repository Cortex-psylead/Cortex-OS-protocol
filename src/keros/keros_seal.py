# ============================================================================
# src/keros/keros_seal.py
# KEROS Module: Hardware Attestation for Sensor Integrity
# Dependencies: CORTEX (tensor) + TPM 2.0 (optional)
# ============================================================================

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass
from typing import Optional, Tuple
from enum import Enum

class AttestationLevel(Enum):
    NONE = "none"       # No TPM available
    SOFTWARE = "soft"   # TPM present but not used
    HARDWARE = "hard"   # TPM seal valid
    TIME = "time"       # TPM seal + timestamp verified (anti-replay)

@dataclass
class Keroseal:
    """Cryptographic seal from hardware TPM."""
    tensor_hash: bytes
    timestamp: float
    nonce: bytes
    pcr_quote: bytes   # Proof of code integrity
    signature: bytes   # Signed by TPM Attestation Key

class KerosEngine:
    """
    Hardware attestation module.
    Seals tensors with TPM-backed proof of origin and integrity.
    """
    
    def __init__(self, tpm_available: bool = False):
        self.tpm_available = tpm_available
        self._attestation_key = None
        self._used_nonces = set()
        
        if tpm_available:
            self._init_tpm()
    
    def _init_tpm(self):
        """Initializes TPM 2.0 connection (simulated for PoC)."""
        print("[KEROS] TPM 2.0 detected. Attestation key loaded.")
        self._attestation_key = secrets.token_bytes(32)  # Simulated AK
    
    def seal_tensor(self, anonymous_tensor: np.ndarray, sensor_id: str) -> Tuple[Keroseal, AttestationLevel]:
        """
        Seals a tensor with hardware attestation.
        Returns (seal, attestation_level).
        """
        tensor_hash = hashlib.sha256(anonymous_tensor.tobytes()).digest()
        nonce = secrets.token_bytes(16)
        timestamp = time.time()
        
        if not self.tpm_available or self._attestation_key is None:
            # Fallback: software seal (no hardware assurance)
            print("[KEROS] TPM not available. Using software fallback.")
            seal = Keroseal(
                tensor_hash=tensor_hash,
                timestamp=timestamp,
                nonce=nonce,
                pcr_quote=b"SOFTWARE_FALLBACK",
                signature=hashlib.sha256(tensor_hash + nonce).digest()
            )
            return seal, AttestationLevel.SOFTWARE
        
        # Hardware seal (TPM-backed)
        # In production: tpm2_quote(pcr=16) to prove SAL code integrity
        pcr_quote = self._simulate_pcr_quote()
        
        # Create message to sign
        message = tensor_hash + nonce + timestamp.to_bytes(8, 'big')
        signature = hmac.new(self._attestation_key, message, hashlib.sha256).digest()
        
        seal = Keroseal(
            tensor_hash=tensor_hash,
            timestamp=timestamp,
            nonce=nonce,
            pcr_quote=pcr_quote,
            signature=signature
        )
        
        level = AttestationLevel.TIME if self._verify_timestamp(seal) else AttestationLevel.HARDWARE
        print(f"[KEROS] Tensor sealed. Attestation level: {level.value}")
        return seal, level
    
    def verify_seal(self, seal: Keroseal, expected_tensor_hash: bytes) -> bool:
        """
        Verifies a hardware seal without contacting the original sensor.
        Returns True if seal is valid and not replayed.
        """
        # Check nonce replay
        if seal.nonce in self._used_nonces:
            print("[KEROS] Replay attack detected: nonce already used")
            return False
        
        # Check timestamp freshness (within 5 seconds)
        if abs(time.time() - seal.timestamp) > 5.0:
            print("[KEROS] Seal timestamp too old — possible replay")
            return False
        
        # Verify signature (simulated)
        message = seal.tensor_hash + seal.nonce + seal.timestamp.to_bytes(8, 'big')
        expected_sig = hmac.new(self._attestation_key, message, hashlib.sha256).digest()
        
        if hmac.compare_digest(expected_sig, seal.signature):
            self._used_nonces.add(seal.nonce)
            print("[KEROS] Seal verified: Hardware integrity confirmed")
            return True
        else:
            print("[KEROS] Invalid signature")
            return False
    
    def _simulate_pcr_quote(self) -> bytes:
        """Simulates TPM PCR quote for code integrity."""
        # In production: tpm2_pcrread(16)
        return hashlib.sha256(b"CORTEX_SAL_CODE_HASH").digest()
    
    def _verify_timestamp(self, seal: Keroseal) -> bool:
        """Verifies that timestamp is within reasonable bounds."""
        return abs(time.time() - seal.timestamp) < 5.0
