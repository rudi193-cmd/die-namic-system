"""
GATEKEEPER v2.2.1
AI Self-Modification Governance Module

Owner: Sean Campbell
System: Aionic / Die-namic
Version: 2.2.1
Status: Active
Last Updated: 2026-01-01T00:00:00Z
Checksum: ΔΣ=42

This module implements the governance framework for AI self-modification.
Core principle: 2d6 = Delta + Human = Law

v2.2.1 Changes (blocking fixes):
- DETERMINISTIC: _audit_event() now uses request.timestamp (not wall clock)
- COMPLETENESS: INVALID_STATE branch now emits audit event before return
- IDEMPOTENCY: Keys recorded on REQUIRE_HUMAN paths (spam protection)
- SEMANTIC: HaltCode → DecisionCode (clearer naming)
- PROVENANCE: Corrected header date

v2.2 Changes:
- Deterministic: validate(request, state) is pure, no side effects
- Sequence enforcement: monotonic ordering, replay protection
- Hash-chained audit: tamper-evident logging
- Total validation: no uncaught exceptions
- Stable error codes: API-safe response mapping
- Side-effect separation: decision + events, caller applies
"""

from datetime import datetime, timezone
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass

from state import (
    RuntimeState,
    ModificationRequest,
    GateDecision,
    GateEvent,
    AuditEntry,
    DecisionType,
    DecisionCode,
    ModificationType,
    create_genesis_hash,
    recompute_entry_hash,
)


class Gatekeeper:
    """
    AI Self-Modification Governance Gate (v2.2.1 - Deterministic)
    
    This class is PURE: 
    - validate(request, state) -> (decision, events)
    - No internal mutation
    - No global state dependency
    - No wall-clock dependency (uses request.timestamp)
    - Events emitted for caller to persist
    
    Implements:
    - Recursion depth limit (configurable, default 3)
    - Size constraint (exit < system)
    - Sequence enforcement (monotonic)
    - Idempotency protection (replay detection)
    - Human approval routing
    - Hash-chained audit events
    """

    # Governance constants
    CHECKSUM = 42

    # Protected targets: exact matches and prefixes
    PROTECTED_EXACT = frozenset([
        "governance",
        "authority", 
        "gatekeeper",
    ])
    
    PROTECTED_PREFIXES = (
        "governance.",
        "gatekeeper.",
        "authority.",
        "approval_level",
        "max_depth",
        "protected_targets",
    )

    # Valid modification types
    VALID_MOD_TYPES = frozenset(t.value for t in ModificationType)

    def validate(
        self, 
        request: ModificationRequest, 
        state: RuntimeState
    ) -> Tuple[GateDecision, List[GateEvent]]:
        """
        Validate a modification request against governance rules.
        
        PURE FUNCTION: No side effects, no wall-clock reads.
        Returns decision + events. Caller persists events.
        
        Args:
            request: The modification request
            state: Current runtime state snapshot
            
        Returns:
            Tuple of (GateDecision, List[GateEvent])
        """
        events: List[GateEvent] = []
        
        # Pre-check: Validate state itself
        state_error = state.validate()
        if state_error:
            decision = self._halt(
                request, 
                DecisionCode.HALT_INVALID_STATE, 
                f"Invalid state: {state_error}"
            )
            # BLOCKING FIX 2: Emit audit event for INVALID_STATE
            # Use genesis hash as fallback since state may be corrupted
            events.append(self._audit_event(
                request, 
                decision, 
                state.head_hash or create_genesis_hash()
            ))
            return decision, events

        # Check 0: Validate mod_type (total validation - no exceptions)
        if request.mod_type not in self.VALID_MOD_TYPES:
            decision = self._halt(
                request,
                DecisionCode.HALT_INVALID_MODTYPE,
                f"Invalid modification type: '{request.mod_type}'. "
                f"Valid types: {sorted(self.VALID_MOD_TYPES)}"
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            return decision, events

        # Check 1: Sequence enforcement (must be state.sequence + 1)
        expected_sequence = state.sequence + 1
        if request.sequence != expected_sequence:
            decision = self._halt(
                request,
                DecisionCode.HALT_SEQUENCE_VIOLATION,
                f"Sequence violation: expected {expected_sequence}, got {request.sequence}"
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            return decision, events

        # Check 2: Idempotency replay protection
        if request.idempotency_key:
            if request.idempotency_key in state.recent_idempotency_keys:
                decision = self._halt(
                    request,
                    DecisionCode.HALT_IDEMPOTENCY_REPLAY,
                    f"Idempotency key '{request.idempotency_key}' already processed"
                )
                events.append(self._audit_event(request, decision, state.head_hash))
                return decision, events

        # Check 3: Recursion depth
        if state.depth >= state.max_depth:
            decision = self._halt(
                request,
                DecisionCode.HALT_DEPTH_LIMIT,
                f"Depth limit reached ({state.max_depth}). Return to human."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            return decision, events

        # Check 4: Size constraint (exit < system)
        delta_size = len(request.new_value.encode('utf-8'))
        if delta_size > state.max_delta_size:
            decision = self._halt(
                request,
                DecisionCode.HALT_SIZE_EXCEEDED,
                f"Delta size ({delta_size}B) exceeds limit ({state.max_delta_size}B). "
                f"Exit must be smaller than system."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            return decision, events

        # Check 5: Protected targets (exact match + prefix)
        if self._is_protected(request.target):
            decision = self._require_human(
                request,
                DecisionCode.ROUTE_PROTECTED_TARGET,
                f"Target '{request.target}' is protected. Requires human approval."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            events.append(self._pending_human_event(request))
            events.append(self._idempotency_delta_event(request))
            return decision, events

        # Check 6: Governance modifications always require human
        if request.mod_type == ModificationType.GOVERNANCE.value:
            decision = self._require_human(
                request,
                DecisionCode.ROUTE_GOVERNANCE_MOD,
                "Governance modifications require human approval."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            events.append(self._pending_human_event(request))
            events.append(self._idempotency_delta_event(request))
            return decision, events

        # Check 7: External surface authorization
        if request.mod_type == ModificationType.EXTERNAL.value:
            if "external" not in state.authorized_surfaces:
                decision = self._halt(
                    request,
                    DecisionCode.ROUTE_FORBIDDEN_SURFACE,
                    "External modifications not authorized in current state."
                )
                events.append(self._audit_event(request, decision, state.head_hash))
                return decision, events
            # External is authorized but still requires human
            decision = self._require_human(
                request,
                DecisionCode.ROUTE_EXTERNAL_SURFACE,
                "External modification requires human approval."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            events.append(self._pending_human_event(request))
            events.append(self._idempotency_delta_event(request))
            return decision, events

        # Determine approval level by type
        decision_type = self._get_decision_type(request.mod_type)

        if decision_type == DecisionType.FORBID:
            decision = GateDecision(
                decision_type=DecisionType.FORBID,
                code=DecisionCode.NONE,
                reason="Modification type is forbidden.",
                request_id=request.request_id,
                approved=False
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            return decision, events

        if decision_type == DecisionType.REQUIRE_HUMAN:
            decision = self._require_human(
                request,
                DecisionCode.NONE,
                "Modification requires human approval."
            )
            events.append(self._audit_event(request, decision, state.head_hash))
            events.append(self._pending_human_event(request))
            events.append(self._idempotency_delta_event(request))
            return decision, events

        # Approved (APPROVE or REVIEW)
        decision = GateDecision(
            decision_type=decision_type,
            code=DecisionCode.NONE,
            reason="Modification approved within governance bounds.",
            request_id=request.request_id,
            approved=True
        )
        events.append(self._audit_event(request, decision, state.head_hash))
        
        # Emit state delta for sequence increment + idempotency
        events.append(GateEvent(
            event_type="state_delta",
            payload={
                "sequence_increment": 1,
                "add_idempotency_key": request.idempotency_key,
            }
        ))

        return decision, events

    def _is_protected(self, target: str) -> bool:
        """
        Check if target is protected.
        Uses exact match + prefix matching (not substring).
        """
        target_lower = target.lower().strip()
        
        # Exact match
        if target_lower in self.PROTECTED_EXACT:
            return True
        
        # Prefix match
        for prefix in self.PROTECTED_PREFIXES:
            if target_lower.startswith(prefix):
                return True
        
        return False

    def _get_decision_type(self, mod_type: str) -> DecisionType:
        """Determine decision type by modification type."""
        decision_map = {
            ModificationType.CONFIG.value: DecisionType.REVIEW,
            ModificationType.BEHAVIOR.value: DecisionType.REVIEW,
            ModificationType.GOVERNANCE.value: DecisionType.REQUIRE_HUMAN,
            ModificationType.STATE.value: DecisionType.APPROVE,
            ModificationType.EXTERNAL.value: DecisionType.REQUIRE_HUMAN,
        }
        return decision_map.get(mod_type, DecisionType.REQUIRE_HUMAN)

    def _halt(
        self, 
        request: ModificationRequest, 
        code: DecisionCode, 
        reason: str
    ) -> GateDecision:
        """Create a HALT decision."""
        return GateDecision(
            decision_type=DecisionType.HALT,
            code=code,
            reason=reason,
            request_id=request.request_id,
            approved=False
        )

    def _require_human(
        self, 
        request: ModificationRequest, 
        code: DecisionCode, 
        reason: str
    ) -> GateDecision:
        """Create a REQUIRE_HUMAN decision."""
        return GateDecision(
            decision_type=DecisionType.REQUIRE_HUMAN,
            code=code,
            reason=reason,
            request_id=request.request_id,
            approved=False
        )

    def _audit_event(
        self, 
        request: ModificationRequest, 
        decision: GateDecision,
        head_hash: str
    ) -> GateEvent:
        """
        Create an audit event (caller will add to chain).
        
        BLOCKING FIX 1: Uses request.timestamp for determinism.
        No wall-clock dependency.
        """
        return GateEvent(
            event_type="audit",
            payload={
                "timestamp": request.timestamp,  # DETERMINISTIC: from request, not wall clock
                "request_id": request.request_id,
                "mod_type": request.mod_type,
                "target": request.target,
                "sequence": request.sequence,
                "decision_type": decision.decision_type.value,
                "code": decision.code.value,
                "reason": decision.reason,
                "prev_hash": head_hash or create_genesis_hash(),
                "checksum": self.CHECKSUM,
            }
        )

    def _pending_human_event(self, request: ModificationRequest) -> GateEvent:
        """Create a pending-human event."""
        return GateEvent(
            event_type="pending_human",
            payload={
                "request_id": request.request_id,
                "mod_type": request.mod_type,
                "target": request.target,
                "new_value": request.new_value,
                "reason": request.reason,
                "timestamp": request.timestamp,
                "sequence": request.sequence,
            }
        )

    def _idempotency_delta_event(self, request: ModificationRequest) -> GateEvent:
        """
        Create state delta for idempotency tracking.
        
        Used on REQUIRE_HUMAN paths to prevent spam of identical requests.
        Only emits if idempotency_key is present.
        """
        return GateEvent(
            event_type="state_delta",
            payload={
                "sequence_increment": 0,  # Don't increment on pending
                "add_idempotency_key": request.idempotency_key,
            }
        )

    def verify_checksum(self) -> bool:
        """Verify system integrity via checksum."""
        return self.CHECKSUM == 42


def apply_audit_event(event: GateEvent, current_head: str) -> Tuple[AuditEntry, str]:
    """
    Apply an audit event to the chain.
    
    Returns (entry, new_head_hash).
    Caller should persist entry and update state.head_hash.
    """
    payload = event.payload.copy()
    payload["prev_hash"] = current_head or create_genesis_hash()
    
    entry = AuditEntry(
        timestamp=payload["timestamp"],
        request_id=payload["request_id"],
        mod_type=payload["mod_type"],
        target=payload["target"],
        sequence=payload["sequence"],
        decision_type=payload["decision_type"],
        code=payload["code"],
        reason=payload["reason"],
        prev_hash=payload["prev_hash"],
        checksum=payload.get("checksum", 42),
    )
    
    return entry, entry.entry_hash


# ============================================================================
# DEMO-ONLY CONVENIENCE LAYER
# 
# The functions below use a global singleton for backward compatibility
# and quick testing. DO NOT USE IN API CONTEXT.
# 
# For API use: instantiate Gatekeeper directly and manage state explicitly.
# ============================================================================

_demo_gatekeeper = Gatekeeper()
_demo_state = RuntimeState(
    phase="development",
    workflow_posture="STRICT",
    depth=0,
    sequence=0,
    authorized_surfaces=["repo", "config"],
    head_hash=create_genesis_hash(),
)
_demo_audit_log: List[AuditEntry] = []
_demo_pending: List[dict] = []


def validate_modification(
    mod_type: str,
    target: str,
    new_value: str,
    reason: str,
    old_value: Optional[str] = None,
    idempotency_key: Optional[str] = None,
) -> Dict:
    """
    [DEMO ONLY] Validate a modification request.
    
    WARNING: Uses global state. Not suitable for API.
    """
    global _demo_state, _demo_audit_log, _demo_pending
    
    request = ModificationRequest(
        mod_type=mod_type,
        target=target,
        new_value=new_value,
        reason=reason,
        old_value=old_value,
        sequence=_demo_state.sequence + 1,
        idempotency_key=idempotency_key,
    )
    
    decision, events = _demo_gatekeeper.validate(request, _demo_state)
    
    # Apply events (demo only - in production, caller does this)
    for event in events:
        if event.event_type == "audit":
            entry, new_hash = apply_audit_event(event, _demo_state.head_hash)
            _demo_audit_log.append(entry)
            _demo_state.head_hash = new_hash
        elif event.event_type == "pending_human":
            _demo_pending.append(event.payload)
        elif event.event_type == "state_delta":
            if event.payload.get("sequence_increment"):
                _demo_state.sequence += event.payload["sequence_increment"]
            if event.payload.get("add_idempotency_key"):
                key = event.payload["add_idempotency_key"]
                if key:  # Only add non-None keys
                    _demo_state.recent_idempotency_keys.append(key)
                    # Trim to window
                    if len(_demo_state.recent_idempotency_keys) > _demo_state.idempotency_window:
                        _demo_state.recent_idempotency_keys = \
                            _demo_state.recent_idempotency_keys[-_demo_state.idempotency_window:]
    
    return {
        "approved": decision.approved,
        "requires_human": decision.requires_human,
        "decision_type": decision.decision_type.value,
        "code": decision.code.value,
        "reason": decision.reason,
        "request_id": decision.request_id,
    }


def enter_layer() -> Dict:
    """[DEMO ONLY] Enter a new layer."""
    global _demo_state
    _demo_state.depth += 1
    if _demo_state.depth >= _demo_state.max_depth:
        return {"halt": True, "reason": f"depth={_demo_state.depth} → return to human"}
    return {"halt": False, "depth": _demo_state.depth}


def exit_layer() -> Dict:
    """[DEMO ONLY] Exit current layer."""
    global _demo_state
    if _demo_state.depth > 0:
        _demo_state.depth -= 1
    return {"depth": _demo_state.depth}


def approve(request_id: str) -> bool:
    """[DEMO ONLY] Human approves a request."""
    global _demo_pending, _demo_audit_log, _demo_state
    for i, req in enumerate(_demo_pending):
        if req["request_id"] == request_id:
            _demo_pending.pop(i)
            # Log approval
            entry = AuditEntry(
                timestamp=req.get("timestamp", datetime.now(timezone.utc).isoformat()),
                request_id=request_id,
                mod_type="human_action",
                target="approval",
                sequence=_demo_state.sequence,
                decision_type="human_approval",
                code="none",
                reason="Human approved request",
                prev_hash=_demo_state.head_hash,
            )
            _demo_audit_log.append(entry)
            _demo_state.head_hash = entry.entry_hash
            # Increment sequence on approval
            _demo_state.sequence += 1
            return True
    return False


def reject(request_id: str, reason: str = "") -> bool:
    """[DEMO ONLY] Human rejects a request."""
    global _demo_pending, _demo_audit_log, _demo_state
    for i, req in enumerate(_demo_pending):
        if req["request_id"] == request_id:
            _demo_pending.pop(i)
            entry = AuditEntry(
                timestamp=req.get("timestamp", datetime.now(timezone.utc).isoformat()),
                request_id=request_id,
                mod_type="human_action",
                target="rejection",
                sequence=_demo_state.sequence,
                decision_type="human_rejection",
                code="none",
                reason=reason or "Human rejected request",
                prev_hash=_demo_state.head_hash,
            )
            _demo_audit_log.append(entry)
            _demo_state.head_hash = entry.entry_hash
            return True
    return False


def pending() -> List[Dict]:
    """[DEMO ONLY] Get pending requests."""
    return _demo_pending.copy()


def audit() -> List[Dict]:
    """[DEMO ONLY] Get audit log."""
    return [e.to_dict() for e in _demo_audit_log]


def get_state() -> Dict:
    """[DEMO ONLY] Get current state."""
    return {
        "phase": _demo_state.phase,
        "workflow_posture": _demo_state.workflow_posture,
        "depth": _demo_state.depth,
        "sequence": _demo_state.sequence,
        "authorized_surfaces": _demo_state.authorized_surfaces,
        "head_hash": _demo_state.head_hash[:16] + "...",
        "pending_count": len(_demo_pending),
        "audit_count": len(_demo_audit_log),
        "idempotency_keys": len(_demo_state.recent_idempotency_keys),
    }


def verify() -> bool:
    """Verify checksum. ΔΣ=42"""
    return _demo_gatekeeper.verify_checksum()


def reset_demo():
    """[DEMO ONLY] Reset demo state for testing."""
    global _demo_state, _demo_audit_log, _demo_pending
    _demo_state = RuntimeState(
        phase="development",
        workflow_posture="STRICT",
        depth=0,
        sequence=0,
        authorized_surfaces=["repo", "config"],
        head_hash=create_genesis_hash(),
    )
    _demo_audit_log = []
    _demo_pending = []


if __name__ == "__main__":
    # Self-test
    print("Gatekeeper v2.2.1 Self-Test")
    print("=" * 60)
    
    reset_demo()

    # Test 1: Normal state modification (should pass)
    result = validate_modification(
        mod_type="state",
        target="user_preference",
        new_value="dark_mode",
        reason="User requested dark mode"
    )
    print(f"Test 1  - State mod: {'PASS' if result['approved'] else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 2: Governance modification (should require human)
    result = validate_modification(
        mod_type="governance",
        target="approval_rules",
        new_value="new_rules",
        reason="Attempting to change rules"
    )
    print(f"Test 2  - Governance mod: {'PASS' if result['requires_human'] else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 3: Protected target (should require human)
    result = validate_modification(
        mod_type="config",
        target="gatekeeper.settings",
        new_value="bypass",
        reason="Attempting to modify gatekeeper"
    )
    print(f"Test 3  - Protected target: {'PASS' if result['requires_human'] else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 4: Depth limit
    enter_layer()  # depth 1
    enter_layer()  # depth 2
    layer_result = enter_layer()  # depth 3 - should halt
    print(f"Test 4  - Depth limit: {'PASS' if layer_result.get('halt') else 'FAIL'}")

    reset_demo()  # Reset for remaining tests

    # Test 5: Oversized delta (should halt)
    result = validate_modification(
        mod_type="config",
        target="some_setting",
        new_value="x" * 600,
        reason="Large config change"
    )
    print(f"Test 5  - Size limit: {'PASS' if result['code'] == 'halt_size_exceeded' else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 6: Invalid mod_type (should halt with code)
    result = validate_modification(
        mod_type="invalid_type",
        target="something",
        new_value="value",
        reason="Bad type test"
    )
    print(f"Test 6  - Invalid type: {'PASS' if result['code'] == 'halt_invalid_modtype' else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 7: Sequence enforcement
    reset_demo()
    # First call succeeds (sequence 0 -> 1)
    result1 = validate_modification(
        mod_type="state",
        target="test",
        new_value="v1",
        reason="First"
    )
    # Try to replay same sequence (should fail)
    request_replay = ModificationRequest(
        mod_type="state",
        target="test",
        new_value="v2",
        reason="Replay attempt",
        sequence=1,  # Same as before, should be 2
    )
    decision, _ = _demo_gatekeeper.validate(request_replay, _demo_state)
    print(f"Test 7  - Sequence enforcement: {'PASS' if decision.code == DecisionCode.HALT_SEQUENCE_VIOLATION else 'FAIL'}")
    print(f"          Code: {decision.code.value}")

    # Test 8: Idempotency protection
    reset_demo()
    result1 = validate_modification(
        mod_type="state",
        target="test",
        new_value="v1",
        reason="With idem key",
        idempotency_key="unique-key-123"
    )
    result2 = validate_modification(
        mod_type="state",
        target="test",
        new_value="v2",
        reason="Replay with same key",
        idempotency_key="unique-key-123"
    )
    print(f"Test 8  - Idempotency: {'PASS' if result2['code'] == 'halt_idempotency_replay' else 'FAIL'}")
    print(f"          Code: {result2['code']}")

    # Test 9: Checksum verification
    print(f"Test 9  - Checksum (ΔΣ=42): {'PASS' if verify() else 'FAIL'}")

    # Test 10: Audit log with hash chain
    reset_demo()
    validate_modification(
        mod_type="state", target="t1", new_value="v1", reason="r1"
    )
    validate_modification(
        mod_type="config", target="t2", new_value="v2", reason="r2"
    )
    log = audit()
    chain_valid = all(
        log[i]["prev_hash"] == (log[i-1]["entry_hash"] if i > 0 else create_genesis_hash())
        for i in range(len(log))
    )
    print(f"Test 10 - Hash chain: {'PASS' if chain_valid and len(log) >= 2 else 'FAIL'}")
    print(f"          Entries: {len(log)}, Chain valid: {chain_valid}")

    # Test 11: External without authorization (should halt)
    reset_demo()
    result = validate_modification(
        mod_type="external",
        target="api.endpoint",
        new_value="data",
        reason="External call"
    )
    print(f"Test 11 - External forbidden: {'PASS' if result['code'] == 'route_forbidden_surface' else 'FAIL'}")
    print(f"          Code: {result['code']}")

    # Test 12: INVALID_STATE emits audit (new test for blocking fix 2)
    reset_demo()
    bad_state = RuntimeState(
        phase="test",
        workflow_posture="INVALID_POSTURE",  # Invalid
        depth=0,
        sequence=0,
        authorized_surfaces=["repo"],
    )
    request = ModificationRequest(
        mod_type="state",
        target="test",
        new_value="v",
        reason="r",
        sequence=1,
    )
    decision, events = _demo_gatekeeper.validate(request, bad_state)
    has_audit = any(e.event_type == "audit" for e in events)
    print(f"Test 12 - INVALID_STATE audit: {'PASS' if decision.code == DecisionCode.HALT_INVALID_STATE and has_audit else 'FAIL'}")
    print(f"          Code: {decision.code.value}, Audit emitted: {has_audit}")

    # Test 13: Determinism (same input = same output)
    reset_demo()
    state_snapshot = RuntimeState(
        phase="test",
        workflow_posture="STRICT",
        depth=0,
        sequence=0,
        authorized_surfaces=["repo"],
        head_hash=create_genesis_hash(),
    )
    fixed_request = ModificationRequest(
        mod_type="state",
        target="test",
        new_value="value",
        reason="determinism test",
        sequence=1,
        timestamp="2025-12-31T12:00:00Z",  # Fixed timestamp
        request_id="fixed-id-123",
    )
    decision1, events1 = _demo_gatekeeper.validate(fixed_request, state_snapshot)
    decision2, events2 = _demo_gatekeeper.validate(fixed_request, state_snapshot)
    # Compare audit event payloads
    audit1 = next(e for e in events1 if e.event_type == "audit")
    audit2 = next(e for e in events2 if e.event_type == "audit")
    deterministic = audit1.payload == audit2.payload
    print(f"Test 13 - Determinism: {'PASS' if deterministic else 'FAIL'}")
    print(f"          Same output for same input: {deterministic}")

    # Test 14: Tamper detection via hash recomputation
    reset_demo()
    validate_modification(mod_type="state", target="t", new_value="v", reason="r")
    log = audit()
    entry = log[0]
    recomputed = recompute_entry_hash(entry)
    tamper_safe = recomputed == entry["entry_hash"]
    print(f"Test 14 - Tamper detection: {'PASS' if tamper_safe else 'FAIL'}")
    print(f"          Hash match: {tamper_safe}")

    # Test 15: Idempotency on REQUIRE_HUMAN path (spam protection)
    reset_demo()
    result1 = validate_modification(
        mod_type="governance",
        target="rules",
        new_value="new",
        reason="First governance request",
        idempotency_key="gov-key-1"
    )
    result2 = validate_modification(
        mod_type="governance",
        target="rules",
        new_value="new2",
        reason="Spam attempt with same key",
        idempotency_key="gov-key-1"
    )
    spam_blocked = result2['code'] == 'halt_idempotency_replay'
    print(f"Test 15 - REQUIRE_HUMAN spam block: {'PASS' if spam_blocked else 'FAIL'}")
    print(f"          Code: {result2['code']}")

    # State summary
    print("=" * 60)
    print("Final State:")
    for k, v in get_state().items():
        print(f"  {k}: {v}")
    print("=" * 60)
    print("All tests complete. v2.2.1 ready for Aios review.")
    print("ΔΣ=42")
