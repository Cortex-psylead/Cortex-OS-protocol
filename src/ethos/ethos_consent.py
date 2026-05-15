# ============================================================================
# src/ethos/ethos_consent.py
# ETHOS Module: Dynamic, Physiologically-Grounded Consent
# Dependencies: CORTEX (polyvagal state)
# ============================================================================

import time
import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from enum import Enum
import hashlib

class ConsentCapacity(Enum):
    FULL = "full"          # Ventral vagal — can consent normally
    LIMITED = "limited"    # Sympathetic — requires double confirmation
    NONE = "none"          # Dorsal vagal — cannot consent

class ConsentScope(Enum):
    BIOMETRIC = "biometric"
    AUDIO = "audio"
    LOCATION = "location"
    ACOLYTE_ACCESS = "acolyte_access"

@dataclass
class ConsentRecord:
    """Immutable record of a consent event."""
    id: str
    scope: ConsentScope
    purpose: str
    granted_at: float
    expires_at: float
    user_state_hash: str   # Hash of CORTEX state at time of consent
    revoked: bool = False

class EthosEngine:
    """
    Manages dynamic consent based on physiological capacity.
    Consent is automatically revoked if user leaves the Window of Tolerance.
    """
    
    def __init__(self, cortex_shield):
        self.cortex = cortex_shield
        self._active_consents: Dict[str, ConsentRecord] = {}
        self._consent_log: List[ConsentRecord] = []
    
    def get_consent_capacity(self) -> ConsentCapacity:
        """Determines if user is physiologically capable of consenting."""
        status = self.cortex.get_cdi_status()
        if status.get("blocked", False):
            return ConsentCapacity.NONE
        
        # In a real implementation, we'd read polyvagal_state from CORTEX
        # For now, simulate based on CDI status
        hard_violations = status.get("hard_violations", 0)
        if hard_violations >= 2:
            return ConsentCapacity.LIMITED
        elif hard_violations >= 3:
            return ConsentCapacity.NONE
        return ConsentCapacity.FULL
    
    def request_consent(self, scope: ConsentScope, purpose: str, duration_seconds: int) -> bool:
        """
        Requests consent with physiological capacity check.
        Returns True if consent is granted and recorded.
        """
        capacity = self.get_consent_capacity()
        
        if capacity == ConsentCapacity.NONE:
            print(f"[ETHOS] Consent denied: User in dorsal vagal state (cannot consent)")
            return False
        
        if capacity == ConsentCapacity.LIMITED:
            print(f"[ETHOS] Limited capacity: Requiring double confirmation")
            # In real UI, would show a second confirmation dialog
            confirmed = self._double_confirmation(scope, purpose)
            if not confirmed:
                return False
        
        # Create consent record
        record_id = hashlib.sha256(f"{scope.value}{purpose}{time.time()}".encode()).hexdigest()[:16]
        record = ConsentRecord(
            id=record_id,
            scope=scope,
            purpose=purpose,
            granted_at=time.time(),
            expires_at=time.time() + duration_seconds,
            user_state_hash=self._get_state_hash()
        )
        
        self._active_consents[record_id] = record
        self._consent_log.append(record)
        print(f"[ETHOS] Consent granted: {scope.value} for {purpose} (expires in {duration_seconds}s)")
        return True
    
    def revoke_consent(self, consent_id: str) -> bool:
        """Revokes a specific consent."""
        if consent_id in self._active_consents:
            self._active_consents[consent_id].revoked = True
            print(f"[ETHOS] Consent revoked: {consent_id}")
            return True
        return False
    
    def check_consent(self, scope: ConsentScope) -> bool:
        """Checks if there is an active, unrevoked consent for a scope."""
        now = time.time()
        for record in self._active_consents.values():
            if (record.scope == scope and 
                not record.revoked and 
                record.expires_at > now):
                return True
        return False
    
    def auto_revoke_on_dysregulation(self):
        """Called periodically by CORTEX when user state changes."""
        capacity = self.get_consent_capacity()
        if capacity == ConsentCapacity.NONE:
            # Revoke all consents when user is in dorsal vagal
            for consent_id in list(self._active_consents.keys()):
                self.revoke_consent(consent_id)
            print("[ETHOS] All consents auto-revoked due to physiological dysregulation")
    
    def _double_confirmation(self, scope: ConsentScope, purpose: str) -> bool:
        """Simulates double confirmation for LIMITED capacity state."""
        # In production, this would show a second dialog
        print(f"[ETHOS] Double confirmation required for {scope.value}: {purpose}")
        return True  # Simulate user confirming
    
    def _get_state_hash(self) -> str:
        """Hashes current CORTEX state for audit trail."""
        status = self.cortex.get_cdi_status()
        return hashlib.sha256(str(status).encode()).hexdigest()[:16]
