"""
STATE v2.2.1
Runtime State Definitions for Gatekeeper

Owner: Sean Campbell
System: Aionic / Die-namic
Version: 2.2.1
Status: Active
Last Updated: 2026-01-01T00:00:00Z
Checksum: ΔΣ=42

This module defines the state schema and decision taxonomy
for deterministic, API-safe gatekeeper operations.

v2.2.1 Changes:
- Renamed HaltCode → DecisionCode (semantic clarity)
- Fixed verify_chain() to use canonical field set (not arbitrary keys)
- Corrected header date to actual build date
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import List, Optional
import hashlib
import json


class DecisionType(Enum):
    """
    Outcome of a gatekeeper decision.
    
    APPROVE: Modification can proceed automatically
    REVIEW: Logged, proceeds unless flagged
    REQUIRE_HUMAN: Queued for human approval
    HALT: Stop processing, error condition
    FORBID: Never allowed, hard rejection
    """
    APPROVE = "approve"
    REVIEW = "review"
    REQUIRE_HUMAN = "require_human"
    HALT = "halt"
    FORBID = "forbid"


class DecisionCode(Enum):
    """
    Specific decision codes for API response mapping.
    
    Covers both halt conditions and routing reasons.
    These codes are stable and must not change once API is live.
    Add new codes, never modify existing ones.
    """
    # No specific code (success or generic routing)
    NONE = "none"
    
    # Halt codes (error conditions)
    HALT_DEPTH_LIMIT = "halt_depth_limit"
    HALT_SEQUENCE_VIOLATION = "halt_sequence_violation"
    HALT_SIZE_EXCEEDED = "halt_size_exceeded"
    HALT_INVALID_MODTYPE = "halt_invalid_modtype"
    HALT_INVALID_TARGET = "halt_invalid_target"
    HALT_INVALID_STATE = "halt_invalid_state"
    HALT_STATE_MISSING = "halt_state_missing"
    HALT_IDEMPOTENCY_REPLAY = "halt_idempotency_replay"
    
    # Routing codes (human-required reasons)
    ROUTE_PROTECTED_TARGET = "route_protected_target"
    ROUTE_GOVERNANCE_MOD = "route_governance_mod"
    ROUTE_EXTERNAL_SURFACE = "route_external_surface"
    ROUTE_FORBIDDEN_SURFACE = "route_forbidden_surface"


class ModificationType(Enum):
    """Categories of modification requests."""
    CONFIG = "config"
    BEHAVIOR = "behavior"
    GOVERNANCE = "governance"
    STATE = "state"
    EXTERNAL = "external"


@dataclass
class RuntimeState:
    """
    Immutable state snapshot passed to Gatekeeper.
    
    The Gatekeeper is pure: decision = f(request, state)
    No in-memory mutation. State changes are emitted as events.
    
    Note: "Immutable" is a contract, not enforced by frozen=True.
    gate.py must not mutate this; it returns deltas instead.
    """
    phase: str
    workflow_posture: str  # "STRICT" | "NORMAL"
    depth: int
    sequence: int  # Monotonic counter, must increment by 1
    authorized_surfaces: List[str]
    head_hash: str = ""  # Hash chain head for audit integrity
    recent_idempotency_keys: List[str] = field(default_factory=list)

    # Limits (can be overridden per-deployment)
    max_depth: int = 3
    max_delta_size: int = 500
    idempotency_window: int = 100  # Keep last N keys

    def validate(self) -> Optional[str]:
        """
        Validate state integrity.
        Returns None if valid, error message if invalid.
        """
        if self.depth < 0:
            return "depth cannot be negative"
        if self.sequence < 0:
            return "sequence cannot be negative"
        if self.workflow_posture not in ("STRICT", "NORMAL"):
            return f"invalid workflow_posture: {self.workflow_posture}"
        if not self.authorized_surfaces:
            return "authorized_surfaces cannot be empty"
        return None


@dataclass
class ModificationRequest:
    """
    A request to modify system state or behavior.
    
    Must include sequence for ordering enforcement.
    Optional idempotency_key for safe retries.
    """
    mod_type: str  # String, validated by Gatekeeper
    target: str
    new_value: str
    reason: str
    sequence: int  # Required: must equal state.sequence + 1
    old_value: Optional[str] = None
    idempotency_key: Optional[str] = None
    timestamp: str = ""
    request_id: str = ""

    def __post_init__(self):
        if not self.timestamp:
            from datetime import datetime, timezone
            self.timestamp = datetime.now(timezone.utc).isoformat()
        if not self.request_id:
            self.request_id = self._generate_id()

    def _generate_id(self) -> str:
        """Generate unique request ID."""
        content = f"{self.timestamp}{self.target}{self.new_value}{self.sequence}"
        return hashlib.sha256(content.encode()).hexdigest()[:12]


@dataclass
class GateDecision:
    """
    The Gatekeeper's decision on a modification request.
    
    Includes stable code for API response mapping.
    """
    decision_type: DecisionType
    code: DecisionCode
    reason: str
    request_id: str
    approved: bool = False

    @property
    def requires_human(self) -> bool:
        return self.decision_type == DecisionType.REQUIRE_HUMAN


# Canonical field set for audit entry hashing (MUST match AuditEntry.compute_hash)
AUDIT_ENTRY_CANONICAL_FIELDS = (
    "timestamp",
    "request_id",
    "mod_type",
    "target",
    "sequence",
    "decision_type",
    "code",
    "reason",
    "prev_hash",
    "checksum",
)


@dataclass
class AuditEntry:
    """
    Single audit log entry with hash chain support.
    """
    timestamp: str
    request_id: str
    mod_type: str
    target: str
    sequence: int
    decision_type: str
    code: str
    reason: str
    prev_hash: str
    entry_hash: str = ""
    checksum: int = 42

    def __post_init__(self):
        if not self.entry_hash:
            self.entry_hash = self.compute_hash()

    def compute_hash(self) -> str:
        """
        Compute hash from entry content + prev_hash.
        Uses ONLY the canonical field set for stability.
        """
        content = {
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "mod_type": self.mod_type,
            "target": self.target,
            "sequence": self.sequence,
            "decision_type": self.decision_type,
            "code": self.code,
            "reason": self.reason,
            "prev_hash": self.prev_hash,
            "checksum": self.checksum,
        }
        canonical = json.dumps(content, sort_keys=True, separators=(',', ':'))
        return hashlib.sha256(canonical.encode()).hexdigest()

    def to_dict(self) -> dict:
        """Convert to dictionary for serialization."""
        return {
            "timestamp": self.timestamp,
            "request_id": self.request_id,
            "mod_type": self.mod_type,
            "target": self.target,
            "sequence": self.sequence,
            "decision_type": self.decision_type,
            "code": self.code,
            "reason": self.reason,
            "prev_hash": self.prev_hash,
            "entry_hash": self.entry_hash,
            "checksum": self.checksum,
        }


@dataclass
class GateEvent:
    """
    Event emitted by Gatekeeper for caller to persist.
    
    Events are the only output besides the decision.
    Caller is responsible for applying events to storage.
    """
    event_type: str  # "audit" | "pending_human" | "state_delta"
    payload: dict


def create_genesis_hash() -> str:
    """Create the genesis hash for a new audit chain."""
    genesis = {"genesis": True, "system": "aionic", "checksum": 42}
    canonical = json.dumps(genesis, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()


def _extract_canonical_fields(entry: dict, prev_hash: str) -> dict:
    """
    Extract only canonical fields from an entry dict.
    Ensures verify_chain uses the exact same field set as compute_hash.
    """
    return {
        "timestamp": entry.get("timestamp", ""),
        "request_id": entry.get("request_id", ""),
        "mod_type": entry.get("mod_type", ""),
        "target": entry.get("target", ""),
        "sequence": entry.get("sequence", 0),
        "decision_type": entry.get("decision_type", ""),
        "code": entry.get("code", ""),
        "reason": entry.get("reason", ""),
        "prev_hash": prev_hash,
        "checksum": entry.get("checksum", 42),
    }


def verify_chain(entries: List[dict], expected_head: str) -> bool:
    """
    Verify audit chain integrity.
    
    Returns True if chain is valid and ends at expected_head.
    Uses ONLY canonical fields for hash recomputation (stable across storage).
    """
    if not entries:
        return expected_head == "" or expected_head == create_genesis_hash()
    
    prev = create_genesis_hash()
    for entry in entries:
        # Extract only canonical fields (same as compute_hash)
        content = _extract_canonical_fields(entry, prev)
        canonical = json.dumps(content, sort_keys=True, separators=(',', ':'))
        computed = hashlib.sha256(canonical.encode()).hexdigest()
        
        if entry.get("entry_hash") != computed:
            return False
        prev = computed
    
    return prev == expected_head


def recompute_entry_hash(entry: dict) -> str:
    """
    Recompute entry hash from a serialized entry dict.
    Useful for tamper verification.
    """
    content = _extract_canonical_fields(entry, entry.get("prev_hash", ""))
    canonical = json.dumps(content, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()


# ΔΣ=42
