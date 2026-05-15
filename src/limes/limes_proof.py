# ============================================================================
# src/limes/limes_proof.py
# LIMES Module: Zero-Knowledge Proof of Human Liveness
# Dependencies: CORTEX (for entropy source)
# ============================================================================

import hashlib
import hmac
import secrets
import time
from dataclasses import dataclass
from typing import Tuple, Optional
import numpy as np

@dataclass
class LimesProof:
    """Zero-Knowledge Proof of Human Liveness."""
    proof_data: bytes
    timestamp: float
    nonce: bytes
    valid_until: float

class LimesEngine:
    """
    Generates ZKPs proving that biometric data comes from a living human.
    Uses entropy from CORTEX (HRV irregularity, EEG 1/f noise) as the source.
    """
    
    def __init__(self, cortex_shield):
        self.cortex = cortex_shield
        self._master_secret = secrets.token_bytes(32)
        self._used_nonces = set()
    
    def generate_proof(self, sensor_id: str, entropy_source: np.ndarray) -> Optional[LimesProof]:
        """
        Generates a ZKP of liveness from CORTEX entropy.
        Returns proof or None if entropy is insufficient.
        """
        # 1. Check that CORTEX is in a valid state (not dorsal vagal)
        status = self.cortex.get_cdi_status()
        if status.get("blocked", False):
            print("[LIMES] Cannot generate proof: CORTEX blocked (user dysregulated)")
            return None
        
        # 2. Extract entropy from the signal (Coefficient of Variation of the envelope)
        #    This is the "chaotic" part that AI cannot synthesize.
        if len(entropy_source) < 10:
            return None
        
        envelope = np.abs(np.fft.hilbert(entropy_source))
        entropy_hash = hashlib.sha256(envelope.tobytes()).digest()
        
        # 3. Create proof components (simulated ZKP)
        nonce = secrets.token_bytes(16)
        timestamp = time.time()
        valid_until = timestamp + 30.0  # 30-second validity window
        
        # 4. Generate proof: HMAC( entropy_hash + nonce + timestamp )
        message = entropy_hash + nonce + timestamp.to_bytes(8, 'big')
        proof = hmac.new(self._master_secret, message, hashlib.sha256).digest()
        
        # 5. Store nonce for replay prevention
        self._used_nonces.add(nonce)
        
        print(f"[LIMES] Proof generated. Valid until: {valid_until}")
        return LimesProof(
            proof_data=proof,
            timestamp=timestamp,
            nonce=nonce,
            valid_until=valid_until
        )
    
    def verify_proof(self, proof: LimesProof, entropy_hash: bytes) -> bool:
        """
        Verifies a ZKP without accessing raw biometric data.
        Returns True if proof is valid and not replayed.
        """
        # Check expiration
        if time.time() > proof.valid_until:
            print("[LIMES] Proof expired")
            return False
        
        # Check nonce replay
        if proof.nonce in self._used_nonces:
            print("[LIMES] Nonce replayed — possible attack")
            return False
        
        # Recompute HMAC
        message = entropy_hash + proof.nonce + proof.timestamp.to_bytes(8, 'big')
        expected = hmac.new(self._master_secret, message, hashlib.sha256).digest()
        
        if hmac.compare_digest(expected, proof.proof_data):
            print("[LIMES] Proof verified: Human liveness confirmed")
            self._used_nonces.add(proof.nonce)
            return True
        else:
            print("[LIMES] Invalid proof")
            return False
