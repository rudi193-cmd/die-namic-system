"""
STORAGE v1.1
Filesystem Storage Layer for Gatekeeper API

Owner: Sean Campbell
System: Aionic / Die-namic
Version: 1.1
Status: Active
Last Updated: 2026-01-01T01:00:00Z
Checksum: ΔΣ=42

Thin storage layer. No governance logic.
Persistence only - kernel decides, storage persists.

v1.1 Changes (Aios blockers):
- BLOCKER 1: Global transaction lock (txn.lock) for atomic operations
- BLOCKER 2: Atomic state writes (temp + fsync + rename)
- Improved verify_chain diagnostics (actual_head_computed)
- Platform note: fcntl is Unix-only (documented)

Platform: Unix-only (fcntl locking). Windows not supported.
"""

import json
import os
from pathlib import Path
from typing import Optional, List, Tuple
from dataclasses import asdict
import fcntl
from contextlib import contextmanager

from state import (
    RuntimeState,
    AuditEntry,
    GateEvent,
    create_genesis_hash,
    verify_chain,
    recompute_entry_hash,
)


# Default storage directory
STORAGE_DIR = Path(os.environ.get("GATEKEEPER_STORAGE_DIR", "./data"))


def ensure_storage_dir():
    """Ensure storage directory exists."""
    STORAGE_DIR.mkdir(parents=True, exist_ok=True)


# =============================================================================
# TRANSACTION LOCK (BLOCKER 1 FIX)
# =============================================================================

def get_txn_lock_path() -> Path:
    """Global transaction lock path."""
    return STORAGE_DIR / "txn.lock"


@contextmanager
def txn_lock():
    """
    Global transaction lock for atomic multi-file operations.
    
    MUST be held for:
    - Full validate cycle (load → validate → apply_events → save)
    - Human approve/reject (load → audit → state → remove pending)
    
    This prevents race conditions on sequence numbers.
    Platform: Unix-only (fcntl).
    """
    ensure_storage_dir()
    lock_path = get_txn_lock_path()
    lock_file = open(lock_path, "w")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


@contextmanager
def file_lock(filepath: Path):
    """
    Per-file lock for individual file access.
    Used internally; prefer txn_lock() for multi-file operations.
    """
    lock_path = filepath.with_suffix(filepath.suffix + ".lock")
    lock_file = open(lock_path, "w")
    try:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX)
        yield
    finally:
        fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN)
        lock_file.close()


# =============================================================================
# STATE STORAGE
# =============================================================================

def get_state_path() -> Path:
    return STORAGE_DIR / "state.json"


def load_state() -> RuntimeState:
    """
    Load RuntimeState from filesystem.
    Returns default state if file doesn't exist.
    
    CALLER MUST hold txn_lock() for transactional operations.
    """
    ensure_storage_dir()
    path = get_state_path()
    
    if not path.exists():
        return create_default_state()
    
    with open(path, "r") as f:
        data = json.load(f)
    
    return RuntimeState(
        phase=data.get("phase", "development"),
        workflow_posture=data.get("workflow_posture", "STRICT"),
        depth=data.get("depth", 0),
        sequence=data.get("sequence", 0),
        authorized_surfaces=data.get("authorized_surfaces", ["repo", "config"]),
        head_hash=data.get("head_hash", create_genesis_hash()),
        recent_idempotency_keys=data.get("recent_idempotency_keys", []),
        max_depth=data.get("max_depth", 3),
        max_delta_size=data.get("max_delta_size", 500),
        idempotency_window=data.get("idempotency_window", 100),
    )


def save_state(state: RuntimeState) -> None:
    """
    Save RuntimeState to filesystem.
    
    BLOCKER 2 FIX: Atomic write via temp + fsync + rename.
    CALLER MUST hold txn_lock() for transactional operations.
    """
    ensure_storage_dir()
    path = get_state_path()
    tmp_path = path.with_suffix(".json.tmp")
    
    data = {
        "phase": state.phase,
        "workflow_posture": state.workflow_posture,
        "depth": state.depth,
        "sequence": state.sequence,
        "authorized_surfaces": state.authorized_surfaces,
        "head_hash": state.head_hash,
        "recent_idempotency_keys": state.recent_idempotency_keys,
        "max_depth": state.max_depth,
        "max_delta_size": state.max_delta_size,
        "idempotency_window": state.idempotency_window,
    }
    
    # Write to temp file
    with open(tmp_path, "w") as f:
        json.dump(data, f, indent=2)
        f.flush()
        os.fsync(f.fileno())
    
    # Atomic rename
    os.replace(tmp_path, path)


def create_default_state() -> RuntimeState:
    """Create and persist default state."""
    state = RuntimeState(
        phase="development",
        workflow_posture="STRICT",
        depth=0,
        sequence=0,
        authorized_surfaces=["repo", "config", "api"],  # API authorized by default
        head_hash=create_genesis_hash(),
        recent_idempotency_keys=[],
    )
    save_state(state)
    return state


# =============================================================================
# AUDIT STORAGE (Append-only)
# =============================================================================

def get_audit_path() -> Path:
    return STORAGE_DIR / "audit.jsonl"


def append_audit_entry(entry: AuditEntry) -> None:
    """
    Append audit entry to log. APPEND-ONLY.
    Never modifies existing entries.
    
    CALLER MUST hold txn_lock() for transactional operations.
    """
    ensure_storage_dir()
    path = get_audit_path()
    
    with open(path, "a") as f:
        f.write(json.dumps(entry.to_dict()) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_audit_log() -> List[dict]:
    """Load all audit entries."""
    ensure_storage_dir()
    path = get_audit_path()
    
    if not path.exists():
        return []
    
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    
    return entries


def get_audit_head() -> dict:
    """Get current audit head (last entry hash + sequence)."""
    state = load_state()
    entries = load_audit_log()
    
    return {
        "head_hash": state.head_hash,
        "sequence": state.sequence,
        "entry_count": len(entries),
    }


def verify_audit_chain() -> dict:
    """
    Verify audit chain integrity.
    
    Returns computed head during verification for better diagnostics.
    """
    state = load_state()
    entries = load_audit_log()
    
    if not entries:
        is_valid = state.head_hash == "" or state.head_hash == create_genesis_hash()
        return {
            "valid": is_valid,
            "entry_count": 0,
            "expected_head": state.head_hash,
            "actual_head_stored": create_genesis_hash(),
            "actual_head_computed": create_genesis_hash(),
        }
    
    # Walk the chain and compute head
    prev = create_genesis_hash()
    chain_valid = True
    
    for entry in entries:
        # Recompute hash using canonical fields
        computed = recompute_entry_hash({**entry, "prev_hash": prev})
        
        if entry.get("entry_hash") != computed:
            chain_valid = False
            break
        
        prev = computed
    
    return {
        "valid": chain_valid and (prev == state.head_hash),
        "entry_count": len(entries),
        "expected_head": state.head_hash,
        "actual_head_stored": entries[-1].get("entry_hash", ""),
        "actual_head_computed": prev,
    }


# =============================================================================
# PENDING STORAGE
# =============================================================================

def get_pending_path() -> Path:
    return STORAGE_DIR / "pending.jsonl"


def append_pending(payload: dict) -> None:
    """
    Add pending human approval request.
    
    CALLER MUST hold txn_lock() for transactional operations.
    """
    ensure_storage_dir()
    path = get_pending_path()
    
    with open(path, "a") as f:
        f.write(json.dumps(payload) + "\n")
        f.flush()
        os.fsync(f.fileno())


def load_pending() -> List[dict]:
    """Load all pending requests."""
    ensure_storage_dir()
    path = get_pending_path()
    
    if not path.exists():
        return []
    
    entries = []
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entries.append(json.loads(line))
    
    return entries


def remove_pending(request_id: str) -> Optional[dict]:
    """
    Remove pending request by ID.
    Returns the removed request, or None if not found.
    
    CALLER MUST hold txn_lock() for transactional operations.
    This should be called AFTER audit/state updates, not before.
    """
    ensure_storage_dir()
    path = get_pending_path()
    tmp_path = path.with_suffix(".jsonl.tmp")
    
    if not path.exists():
        return None
    
    entries = []
    removed = None
    
    with open(path, "r") as f:
        for line in f:
            line = line.strip()
            if line:
                entry = json.loads(line)
                if entry.get("request_id") == request_id:
                    removed = entry
                else:
                    entries.append(entry)
    
    if removed is None:
        return None
    
    # Atomic rewrite (same pattern as state)
    with open(tmp_path, "w") as f:
        for entry in entries:
            f.write(json.dumps(entry) + "\n")
        f.flush()
        os.fsync(f.fileno())
    
    os.replace(tmp_path, path)
    
    return removed


# =============================================================================
# EVENT APPLICATION (Under Transaction Lock)
# =============================================================================

def apply_events(events: List[GateEvent], state: RuntimeState) -> RuntimeState:
    """
    Apply events to storage and return updated state.
    
    This is where kernel output becomes persistent reality.
    
    CALLER MUST hold txn_lock() - this function assumes lock is held.
    """
    new_state = RuntimeState(
        phase=state.phase,
        workflow_posture=state.workflow_posture,
        depth=state.depth,
        sequence=state.sequence,
        authorized_surfaces=list(state.authorized_surfaces),
        head_hash=state.head_hash,
        recent_idempotency_keys=list(state.recent_idempotency_keys),
        max_depth=state.max_depth,
        max_delta_size=state.max_delta_size,
        idempotency_window=state.idempotency_window,
    )
    
    for event in events:
        if event.event_type == "audit":
            # Create and persist audit entry
            entry = AuditEntry(
                timestamp=event.payload["timestamp"],
                request_id=event.payload["request_id"],
                mod_type=event.payload["mod_type"],
                target=event.payload["target"],
                sequence=event.payload["sequence"],
                decision_type=event.payload["decision_type"],
                code=event.payload["code"],
                reason=event.payload["reason"],
                prev_hash=new_state.head_hash or create_genesis_hash(),
                checksum=event.payload.get("checksum", 42),
            )
            append_audit_entry(entry)
            new_state.head_hash = entry.entry_hash
            
        elif event.event_type == "pending_human":
            append_pending(event.payload)
            
        elif event.event_type == "state_delta":
            if event.payload.get("sequence_increment"):
                new_state.sequence += event.payload["sequence_increment"]
            
            key = event.payload.get("add_idempotency_key")
            if key:
                new_state.recent_idempotency_keys.append(key)
                # Trim to window
                if len(new_state.recent_idempotency_keys) > new_state.idempotency_window:
                    new_state.recent_idempotency_keys = \
                        new_state.recent_idempotency_keys[-new_state.idempotency_window:]
    
    # Persist updated state (atomic write)
    save_state(new_state)
    
    return new_state


# =============================================================================
# HUMAN ACTION HELPERS (BLOCKER 3 FIX)
# =============================================================================

def process_human_action(
    request_id: str,
    action: str,  # "approval" or "rejection"
    reason: str,
    timestamp: str,
) -> Tuple[bool, Optional[RuntimeState], Optional[str]]:
    """
    Process human approve/reject with correct ordering.
    
    Order (all under txn_lock):
    1. Load state
    2. Find pending request (fail if not found)
    3. Compute next sequence
    4. Append audit entry
    5. Update and save state
    6. Remove pending
    
    CALLER MUST hold txn_lock().
    
    Returns: (success, new_state, error_message)
    """
    # Load current state
    state = load_state()
    
    # Find pending request (check before mutating anything)
    pending_list = load_pending()
    pending_request = None
    for item in pending_list:
        if item.get("request_id") == request_id:
            pending_request = item
            break
    
    if pending_request is None:
        return False, None, f"Request {request_id} not found in pending"
    
    # Compute next sequence (both approve and reject consume sequence)
    next_seq = state.sequence + 1
    
    # Create audit entry
    entry = AuditEntry(
        timestamp=timestamp,
        request_id=request_id,
        mod_type="human_action",
        target=action,
        sequence=next_seq,
        decision_type=f"human_{action}",
        code="none",
        reason=reason,
        prev_hash=state.head_hash or create_genesis_hash(),
    )
    
    # Step 1: Append audit (persists first for durability)
    append_audit_entry(entry)
    
    # Step 2: Update and save state
    state.head_hash = entry.entry_hash
    state.sequence = next_seq
    save_state(state)
    
    # Step 3: Remove pending (only after audit and state are durable)
    remove_pending(request_id)
    
    return True, state, None


# =============================================================================
# INITIALIZATION
# =============================================================================

def init_storage() -> RuntimeState:
    """
    Initialize storage and return current state.
    
    Uses txn_lock to prevent race conditions on multi-worker cold start.
    """
    ensure_storage_dir()
    
    with txn_lock():
        path = get_state_path()
        if not path.exists():
            # Create default state under lock to prevent double-init race
            return create_default_state()
        return load_state()


# ΔΣ=42
