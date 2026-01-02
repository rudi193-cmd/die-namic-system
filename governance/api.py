"""
API v1.1
FastAPI Transport Layer for Gatekeeper

Owner: Sean Campbell
System: Aionic / Die-namic
Version: 1.1
Status: Active
Last Updated: 2026-01-01T01:00:00Z
Checksum: ΔΣ=42

THIN TRANSPORT ONLY. No governance logic.
Kernel decides, API transports.

v1.1 Changes (Aios blockers):
- BLOCKER 1: Transaction lock on validate and human actions
- BLOCKER 3: Human approve/reject both consume sequence, correct ordering
- Surface authorization gate (checks authorized_surfaces)

Platform: Unix-only (fcntl locking in storage layer).

Endpoints:
- POST /v1/validate      - Submit modification request
- GET  /v1/pending       - List pending human approvals
- POST /v1/human/approve - Human approves request
- POST /v1/human/reject  - Human rejects request
- GET  /v1/audit/head    - Get current head_hash + sequence
- GET  /v1/audit/verify  - Verify chain integrity
- GET  /v1/state         - Get current runtime state
- GET  /v1/health        - Healthcheck
"""

import os
from datetime import datetime, timezone
from typing import Optional, List
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Depends, Security, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field

# Import kernel (governance logic lives here, not in API)
from gate import Gatekeeper, apply_audit_event
from state import (
    ModificationRequest,
    RuntimeState,
    AuditEntry,
    DecisionCode,
    DecisionType,
    create_genesis_hash,
)

# Import storage layer
from storage import (
    init_storage,
    load_state,
    save_state,
    load_audit_log,
    load_pending,
    apply_events,
    get_audit_head,
    verify_audit_chain,
    txn_lock,
    process_human_action,
)


# =============================================================================
# CONFIGURATION
# =============================================================================

API_KEY = os.environ.get("GATEKEEPER_API_KEY", "dev-key-change-me")
HUMAN_AUTH_KEY = os.environ.get("GATEKEEPER_HUMAN_KEY", "human-key-change-me")

api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
human_key_header = APIKeyHeader(name="X-Human-Key", auto_error=False)


# =============================================================================
# DEPENDENCIES
# =============================================================================

async def verify_api_key(api_key: str = Security(api_key_header)):
    """Verify API key for standard endpoints."""
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )
    return api_key


async def verify_human_key(human_key: str = Security(human_key_header)):
    """Verify human auth key for approval endpoints."""
    if human_key != HUMAN_AUTH_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing human authorization key",
        )
    return human_key


def check_api_surface_authorized(state: RuntimeState):
    """
    Check that 'api' surface is authorized in provided state.
    
    Surface authorization gate: if 'api' not in authorized_surfaces,
    reject all API operations.
    
    Args:
        state: The RuntimeState to check (should be same snapshot used for sequence)
    """
    if "api" not in state.authorized_surfaces:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="API surface not authorized. Add 'api' to authorized_surfaces.",
        )


# =============================================================================
# REQUEST/RESPONSE MODELS
# =============================================================================

class ValidateRequest(BaseModel):
    """Request body for /v1/validate."""
    mod_type: str = Field(..., description="Modification type (config, behavior, governance, state, external)")
    target: str = Field(..., description="Target being modified")
    new_value: str = Field(..., description="New value")
    reason: str = Field(..., description="Reason for modification")
    old_value: Optional[str] = Field(None, description="Previous value (optional)")
    idempotency_key: Optional[str] = Field(None, description="Idempotency key for retry safety")


class ValidateResponse(BaseModel):
    """Response body for /v1/validate."""
    approved: bool
    requires_human: bool
    decision_type: str
    code: str
    reason: str
    request_id: str
    sequence: int


class HumanActionRequest(BaseModel):
    """Request body for human approve/reject."""
    request_id: str = Field(..., description="Request ID to approve/reject")
    reason: Optional[str] = Field(None, description="Reason (required for reject)")


class HumanActionResponse(BaseModel):
    """Response body for human actions."""
    success: bool
    request_id: str
    action: str
    message: str
    sequence: int


class PendingItem(BaseModel):
    """Single pending approval item."""
    request_id: str
    mod_type: str
    target: str
    new_value: str
    reason: str
    timestamp: str
    sequence: int


class PendingResponse(BaseModel):
    """Response body for /v1/pending."""
    count: int
    items: List[PendingItem]


class AuditHeadResponse(BaseModel):
    """Response body for /v1/audit/head."""
    head_hash: str
    sequence: int
    entry_count: int


class AuditVerifyResponse(BaseModel):
    """Response body for /v1/audit/verify."""
    valid: bool
    entry_count: int
    expected_head: str
    actual_head_stored: str
    actual_head_computed: str


class StateResponse(BaseModel):
    """Response body for /v1/state."""
    phase: str
    workflow_posture: str
    depth: int
    sequence: int
    authorized_surfaces: List[str]
    head_hash_prefix: str
    idempotency_key_count: int


class HealthResponse(BaseModel):
    """Response body for /v1/health."""
    status: str
    version: str
    checksum: int
    timestamp: str


# =============================================================================
# APPLICATION LIFECYCLE
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize storage on startup."""
    init_storage()
    yield


# =============================================================================
# APPLICATION
# =============================================================================

app = FastAPI(
    title="Gatekeeper API",
    description="AI Self-Modification Governance API. Thin transport layer. Platform: Unix-only.",
    version="1.1.0",
    lifespan=lifespan,
)

# Single kernel instance (stateless, safe to share)
gatekeeper = Gatekeeper()


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/v1/health", response_model=HealthResponse, tags=["System"])
async def health():
    """
    Healthcheck endpoint. No authentication required.
    """
    return HealthResponse(
        status="healthy",
        version="1.1.0",
        checksum=42,
        timestamp=datetime.now(timezone.utc).isoformat(),
    )


@app.post("/v1/validate", response_model=ValidateResponse, tags=["Governance"])
async def validate(
    request: ValidateRequest,
    api_key: str = Depends(verify_api_key),
):
    """
    Submit a modification request for validation.
    
    The kernel (Gatekeeper) decides. This endpoint only transports.
    
    BLOCKER 1 FIX: Entire operation under transaction lock.
    """
    # Transaction lock for atomic load → validate → persist
    with txn_lock():
        # Load state once
        state = load_state()
        
        # Surface authorization check (same snapshot used for sequence)
        check_api_surface_authorized(state)
        
        # Build kernel request
        mod_request = ModificationRequest(
            mod_type=request.mod_type,
            target=request.target,
            new_value=request.new_value,
            reason=request.reason,
            old_value=request.old_value,
            sequence=state.sequence + 1,
            idempotency_key=request.idempotency_key,
        )
        
        # Kernel decides
        decision, events = gatekeeper.validate(mod_request, state)
        
        # Apply events to storage (still under lock)
        new_state = apply_events(events, state)
    
    # Transport response
    return ValidateResponse(
        approved=decision.approved,
        requires_human=decision.requires_human,
        decision_type=decision.decision_type.value,
        code=decision.code.value,
        reason=decision.reason,
        request_id=decision.request_id,
        sequence=new_state.sequence,
    )


@app.get("/v1/pending", response_model=PendingResponse, tags=["Governance"])
async def get_pending(api_key: str = Depends(verify_api_key)):
    """
    List all requests pending human approval.
    """
    # Surface check (read-only, no txn lock needed)
    state = load_state()
    check_api_surface_authorized(state)
    
    items = load_pending()
    
    return PendingResponse(
        count=len(items),
        items=[
            PendingItem(
                request_id=item["request_id"],
                mod_type=item["mod_type"],
                target=item["target"],
                new_value=item["new_value"],
                reason=item["reason"],
                timestamp=item["timestamp"],
                sequence=item["sequence"],
            )
            for item in items
        ],
    )


@app.post("/v1/human/approve", response_model=HumanActionResponse, tags=["Human"])
async def human_approve(
    request: HumanActionRequest,
    human_key: str = Depends(verify_human_key),
):
    """
    Human approves a pending request.
    
    This is the second die in the 2d6 model:
    - Die 1: AI generates delta (validate)
    - Die 2: Human ratifies (this endpoint)
    
    BLOCKER 3 FIX: 
    - Consumes sequence (like reject)
    - Correct ordering: audit → state → remove pending
    - All under transaction lock
    """
    timestamp = datetime.now(timezone.utc).isoformat()
    reason = request.reason or "Human approved request"
    
    with txn_lock():
        # Surface check (load state for authorization validation)
        state = load_state()
        check_api_surface_authorized(state)
        
        # Process with correct ordering
        success, new_state, error = process_human_action(
            request_id=request.request_id,
            action="approval",
            reason=reason,
            timestamp=timestamp,
        )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )
    
    return HumanActionResponse(
        success=True,
        request_id=request.request_id,
        action="approved",
        message=f"Request {request.request_id} approved by human",
        sequence=new_state.sequence,
    )


@app.post("/v1/human/reject", response_model=HumanActionResponse, tags=["Human"])
async def human_reject(
    request: HumanActionRequest,
    human_key: str = Depends(verify_human_key),
):
    """
    Human rejects a pending request.
    
    BLOCKER 3 FIX:
    - Consumes sequence (like approve)
    - Correct ordering: audit → state → remove pending
    - All under transaction lock
    """
    if not request.reason:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Reason is required for rejection",
        )
    
    timestamp = datetime.now(timezone.utc).isoformat()
    
    with txn_lock():
        # Surface check (load state for authorization validation)
        state = load_state()
        check_api_surface_authorized(state)
        
        # Process with correct ordering
        success, new_state, error = process_human_action(
            request_id=request.request_id,
            action="rejection",
            reason=request.reason,
            timestamp=timestamp,
        )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=error,
        )
    
    return HumanActionResponse(
        success=True,
        request_id=request.request_id,
        action="rejected",
        message=f"Request {request.request_id} rejected: {request.reason}",
        sequence=new_state.sequence,
    )


@app.get("/v1/audit/head", response_model=AuditHeadResponse, tags=["Audit"])
async def audit_head(api_key: str = Depends(verify_api_key)):
    """
    Get current audit head (hash + sequence).
    """
    state = load_state()
    check_api_surface_authorized(state)
    head = get_audit_head()
    
    return AuditHeadResponse(
        head_hash=head["head_hash"],
        sequence=head["sequence"],
        entry_count=head["entry_count"],
    )


@app.get("/v1/audit/verify", response_model=AuditVerifyResponse, tags=["Audit"])
async def audit_verify(api_key: str = Depends(verify_api_key)):
    """
    Verify audit chain integrity.
    """
    state = load_state()
    check_api_surface_authorized(state)
    result = verify_audit_chain()
    
    return AuditVerifyResponse(
        valid=result["valid"],
        entry_count=result["entry_count"],
        expected_head=result["expected_head"],
        actual_head_stored=result["actual_head_stored"],
        actual_head_computed=result["actual_head_computed"],
    )


@app.get("/v1/state", response_model=StateResponse, tags=["System"])
async def get_state(api_key: str = Depends(verify_api_key)):
    """
    Get current runtime state.
    """
    # No surface check here - allow reading state even if api not authorized
    # (so users can see what's wrong)
    state = load_state()
    
    return StateResponse(
        phase=state.phase,
        workflow_posture=state.workflow_posture,
        depth=state.depth,
        sequence=state.sequence,
        authorized_surfaces=state.authorized_surfaces,
        head_hash_prefix=state.head_hash[:16] + "..." if state.head_hash else "",
        idempotency_key_count=len(state.recent_idempotency_keys),
    )


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    port = int(os.environ.get("GATEKEEPER_PORT", "8000"))
    
    print("=" * 60)
    print("Gatekeeper API v1.1")
    print("Thin transport layer. Kernel decides.")
    print("Platform: Unix-only (fcntl locking)")
    print("=" * 60)
    print(f"Port: {port}")
    print(f"Docs: http://localhost:{port}/docs")
    print("ΔΣ=42")
    print("=" * 60)
    
    uvicorn.run(app, host="0.0.0.0", port=port)
