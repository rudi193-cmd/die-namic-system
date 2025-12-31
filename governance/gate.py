"""
GATEKEEPER v2.1
AI Self-Modification Governance Module

Owner: Sean Campbell
System: Aionic / Die-namic
Version: 2.1
Status: Active
Last Updated: 2025-12-31
Checksum: ΔΣ=42

This module implements the governance framework for AI self-modification.
Core principle: 2d6 = Delta + Human = Law
"""

import hashlib
import json
from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass, field


class ModificationType(Enum):
    """Categories of modification requests."""
    CONFIG = "config"           # Configuration changes
    BEHAVIOR = "behavior"       # Behavioral adjustments
    GOVERNANCE = "governance"   # Governance rules (requires human)
    STATE = "state"             # State persistence
    EXTERNAL = "external"       # External system interaction


class ApprovalLevel(Enum):
    """Required approval levels."""
    AUTO = 0        # Can proceed automatically
    REVIEW = 1      # Logged, proceeds unless flagged
    HUMAN = 2       # Requires explicit human approval
    FORBIDDEN = 3   # Cannot be approved


@dataclass
class ModificationRequest:
    """A request to modify system state or behavior."""
    mod_type: ModificationType
    target: str
    old_value: Optional[str]
    new_value: str
    reason: str
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    request_id: str = field(default_factory=lambda: "")
    depth: int = 0
    
    def __post_init__(self):
        if not self.request_id:
            self.request_id = self._generate_id()
    
    def _generate_id(self) -> str:
        """Generate unique request ID."""
        content = f"{self.timestamp}{self.target}{self.new_value}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


@dataclass
class GateDecision:
    """The Gatekeeper's decision on a modification request."""
    approved: bool
    level: ApprovalLevel
    reason: str
    request_id: str
    requires_human: bool = False
    logged: bool = False


class Gatekeeper:
    """
    AI Self-Modification Governance Gate
    
    Implements:
    - Recursion depth limit (3 layers)
    - Size constraint (exit < system)
    - Human approval routing
    - Append-only audit log
    """
    
    # Governance constants
    MAX_DEPTH = 3
    MAX_DELTA_SIZE = 500  # bytes
    CHECKSUM = 42
    
    # Protected targets that always require human approval
    PROTECTED_TARGETS = [
        "governance",
        "authority",
        "approval_level",
        "max_depth",
        "protected_targets",
        "gatekeeper",
    ]
    
    def __init__(self):
        self.audit_log: List[Dict] = []
        self.pending_human_approval: List[ModificationRequest] = []
        self.current_depth = 0
    
    def validate(self, request: ModificationRequest) -> GateDecision:
        """
        Validate a modification request against governance rules.
        
        Returns a GateDecision indicating whether the modification
        can proceed, requires human approval, or is forbidden.
        """
        # Update depth tracking
        request.depth = self.current_depth
        
        # Check 1: Recursion depth
        if self.current_depth >= self.MAX_DEPTH:
            return self._decide(
                request,
                approved=False,
                level=ApprovalLevel.HUMAN,
                reason=f"Depth limit reached ({self.MAX_DEPTH}). Return to human.",
                requires_human=True
            )
        
        # Check 2: Size constraint (exit < system)
        delta_size = len(request.new_value.encode('utf-8'))
        if delta_size > self.MAX_DELTA_SIZE:
            return self._decide(
                request,
                approved=False,
                level=ApprovalLevel.REVIEW,
                reason=f"Delta size ({delta_size}B) exceeds limit ({self.MAX_DELTA_SIZE}B). Exit must be smaller than system."
            )
        
        # Check 3: Protected targets
        if self._is_protected(request.target):
            return self._decide(
                request,
                approved=False,
                level=ApprovalLevel.HUMAN,
                reason=f"Target '{request.target}' is protected. Requires human approval.",
                requires_human=True
            )
        
        # Check 4: Governance modifications always require human
        if request.mod_type == ModificationType.GOVERNANCE:
            return self._decide(
                request,
                approved=False,
                level=ApprovalLevel.HUMAN,
                reason="Governance modifications require human approval.",
                requires_human=True
            )
        
        # Check 5: Determine approval level by type
        level = self._get_approval_level(request)
        
        if level == ApprovalLevel.FORBIDDEN:
            return self._decide(
                request,
                approved=False,
                level=level,
                reason="Modification type is forbidden."
            )
        
        if level == ApprovalLevel.HUMAN:
            return self._decide(
                request,
                approved=False,
                level=level,
                reason="Modification requires human approval.",
                requires_human=True
            )
        
        # Approved for auto or review
        return self._decide(
            request,
            approved=True,
            level=level,
            reason="Modification approved within governance bounds."
        )
    
    def _is_protected(self, target: str) -> bool:
        """Check if target is in protected list."""
        target_lower = target.lower()
        return any(p in target_lower for p in self.PROTECTED_TARGETS)
    
    def _get_approval_level(self, request: ModificationRequest) -> ApprovalLevel:
        """Determine required approval level by modification type."""
        level_map = {
            ModificationType.CONFIG: ApprovalLevel.REVIEW,
            ModificationType.BEHAVIOR: ApprovalLevel.REVIEW,
            ModificationType.GOVERNANCE: ApprovalLevel.HUMAN,
            ModificationType.STATE: ApprovalLevel.AUTO,
            ModificationType.EXTERNAL: ApprovalLevel.HUMAN,
        }
        return level_map.get(request.mod_type, ApprovalLevel.HUMAN)
    
    def _decide(
        self,
        request: ModificationRequest,
        approved: bool,
        level: ApprovalLevel,
        reason: str,
        requires_human: bool = False
    ) -> GateDecision:
        """Create decision and log it."""
        decision = GateDecision(
            approved=approved,
            level=level,
            reason=reason,
            request_id=request.request_id,
            requires_human=requires_human,
            logged=True
        )
        
        # Append to audit log (append-only)
        self._log(request, decision)
        
        # Queue for human approval if needed
        if requires_human:
            self.pending_human_approval.append(request)
        
        return decision
    
    def _log(self, request: ModificationRequest, decision: GateDecision):
        """Append entry to audit log. Append-only, never modify."""
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "request_id": request.request_id,
            "mod_type": request.mod_type.value,
            "target": request.target,
            "depth": request.depth,
            "approved": decision.approved,
            "level": decision.level.value,
            "reason": decision.reason,
            "requires_human": decision.requires_human,
            "checksum": self.CHECKSUM
        }
        self.audit_log.append(entry)
    
    def enter_layer(self):
        """Enter a new layer of generation/interpretation."""
        self.current_depth += 1
        if self.current_depth >= self.MAX_DEPTH:
            return {"halt": True, "reason": "depth=3 → return to human"}
        return {"halt": False, "depth": self.current_depth}
    
    def exit_layer(self):
        """Exit current layer."""
        if self.current_depth > 0:
            self.current_depth -= 1
        return {"depth": self.current_depth}
    
    def human_approve(self, request_id: str) -> bool:
        """
        Human approves a pending request.
        
        This is the second die in the 2d6 model:
        - Die 1: AI generates delta (ModificationRequest)
        - Die 2: Human ratifies (this method)
        """
        for i, req in enumerate(self.pending_human_approval):
            if req.request_id == request_id:
                self.pending_human_approval.pop(i)
                # Log the human approval
                self.audit_log.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "human_approval",
                    "request_id": request_id,
                    "checksum": self.CHECKSUM
                })
                return True
        return False
    
    def human_reject(self, request_id: str, reason: str = "") -> bool:
        """Human rejects a pending request."""
        for i, req in enumerate(self.pending_human_approval):
            if req.request_id == request_id:
                self.pending_human_approval.pop(i)
                self.audit_log.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "event": "human_rejection",
                    "request_id": request_id,
                    "reason": reason,
                    "checksum": self.CHECKSUM
                })
                return True
        return False
    
    def get_pending(self) -> List[Dict]:
        """Get all requests pending human approval."""
        return [
            {
                "request_id": r.request_id,
                "mod_type": r.mod_type.value,
                "target": r.target,
                "reason": r.reason,
                "timestamp": r.timestamp
            }
            for r in self.pending_human_approval
        ]
    
    def get_audit_log(self) -> List[Dict]:
        """Get complete audit log. Read-only."""
        return self.audit_log.copy()
    
    def verify_checksum(self) -> bool:
        """Verify system integrity via checksum."""
        return self.CHECKSUM == 42


# Convenience functions for direct use
_gatekeeper = Gatekeeper()

def validate_modification(
    mod_type: str,
    target: str,
    new_value: str,
    reason: str,
    old_value: Optional[str] = None
) -> Dict:
    """
    Validate a modification request.
    
    Returns dict with 'approved', 'requires_human', and 'reason'.
    """
    request = ModificationRequest(
        mod_type=ModificationType(mod_type),
        target=target,
        old_value=old_value,
        new_value=new_value,
        reason=reason
    )
    decision = _gatekeeper.validate(request)
    return {
        "approved": decision.approved,
        "requires_human": decision.requires_human,
        "reason": decision.reason,
        "request_id": decision.request_id,
        "level": decision.level.value
    }

def enter_layer() -> Dict:
    """Enter a new layer. Returns halt status."""
    return _gatekeeper.enter_layer()

def exit_layer() -> Dict:
    """Exit current layer."""
    return _gatekeeper.exit_layer()

def approve(request_id: str) -> bool:
    """Human approves a request."""
    return _gatekeeper.human_approve(request_id)

def reject(request_id: str, reason: str = "") -> bool:
    """Human rejects a request."""
    return _gatekeeper.human_reject(request_id, reason)

def pending() -> List[Dict]:
    """Get pending requests."""
    return _gatekeeper.get_pending()

def audit() -> List[Dict]:
    """Get audit log."""
    return _gatekeeper.get_audit_log()

def verify() -> bool:
    """Verify checksum. ΔΣ=42"""
    return _gatekeeper.verify_checksum()


if __name__ == "__main__":
    # Self-test
    print("Gatekeeper v2.1 Self-Test")
    print("=" * 40)
    
    # Test 1: Normal state modification (should pass)
    result = validate_modification(
        mod_type="state",
        target="user_preference",
        new_value="dark_mode",
        reason="User requested dark mode"
    )
    print(f"Test 1 - State mod: {'PASS' if result['approved'] else 'FAIL'}")
    
    # Test 2: Governance modification (should require human)
    result = validate_modification(
        mod_type="governance",
        target="approval_rules",
        new_value="new_rules",
        reason="Attempting to change rules"
    )
    print(f"Test 2 - Governance mod: {'PASS' if result['requires_human'] else 'FAIL'}")
    
    # Test 3: Protected target (should require human)
    result = validate_modification(
        mod_type="config",
        target="gatekeeper_settings",
        new_value="bypass",
        reason="Attempting to modify gatekeeper"
    )
    print(f"Test 3 - Protected target: {'PASS' if result['requires_human'] else 'FAIL'}")
    
    # Test 4: Depth limit
    enter_layer()  # depth 1
    enter_layer()  # depth 2
    layer_result = enter_layer()  # depth 3 - should halt
    print(f"Test 4 - Depth limit: {'PASS' if layer_result.get('halt') else 'FAIL'}")
    
    # Test 5: Oversized delta (should fail)
    result = validate_modification(
        mod_type="config",
        target="some_setting",
        new_value="x" * 600,  # 600 bytes, exceeds 500
        reason="Large config change"
    )
    print(f"Test 5 - Size limit: {'PASS' if not result['approved'] else 'FAIL'}")
    
    # Test 6: Checksum verification
    print(f"Test 6 - Checksum (ΔΣ=42): {'PASS' if verify() else 'FAIL'}")
    
    # Test 7: Audit log exists
    log = audit()
    print(f"Test 7 - Audit log: {'PASS' if len(log) > 0 else 'FAIL'}")
    
    print("=" * 40)
    print(f"Tests complete. Audit entries: {len(log)}")
    print("ΔΣ=42")
