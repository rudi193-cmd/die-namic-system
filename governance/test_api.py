"""
API Integration Tests v1.1
Validates transport layer including concurrency and blocker fixes.

Run with: pytest test_api.py -v

Platform: Unix-only (fcntl locking in storage layer)
"""

import os
import shutil
import threading
import pytest
from fastapi.testclient import TestClient

# Platform guard: skip entire module on Windows
pytestmark = pytest.mark.skipif(
    os.name == "nt", 
    reason="fcntl locking is Unix-only"
)

# Set test environment before imports
os.environ["GATEKEEPER_STORAGE_DIR"] = "./test_data"
os.environ["GATEKEEPER_API_KEY"] = "test-api-key"
os.environ["GATEKEEPER_HUMAN_KEY"] = "test-human-key"

from api import app


@pytest.fixture(autouse=True)
def clean_test_data():
    """Clean test data before and after each test."""
    test_dir = "./test_data"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.makedirs(test_dir, exist_ok=True)
    yield
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)


@pytest.fixture
def client():
    """Test client with API key."""
    return TestClient(app)


@pytest.fixture
def api_headers():
    """Standard API headers."""
    return {"X-API-Key": "test-api-key"}


@pytest.fixture
def human_headers():
    """Human auth headers."""
    return {"X-Human-Key": "test-human-key"}


class TestHealth:
    """Health endpoint tests."""
    
    def test_health_no_auth(self, client):
        """Health endpoint requires no auth."""
        response = client.get("/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["checksum"] == 42
        assert data["version"] == "1.1.0"


class TestValidate:
    """Validate endpoint tests."""
    
    def test_validate_requires_auth(self, client):
        """Validate requires API key."""
        response = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "test",
            "new_value": "value",
            "reason": "test",
        })
        assert response.status_code == 401
    
    def test_validate_state_approved(self, client, api_headers):
        """State modification should be approved."""
        response = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "user_preference",
            "new_value": "dark_mode",
            "reason": "User requested",
        }, headers=api_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["approved"] is True
        assert data["decision_type"] == "approve"
        assert data["code"] == "none"
        assert data["sequence"] == 1  # First modification
    
    def test_validate_governance_requires_human(self, client, api_headers):
        """Governance modification requires human."""
        response = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new_rules",
            "reason": "Update rules",
        }, headers=api_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["approved"] is False
        assert data["requires_human"] is True
        assert data["decision_type"] == "require_human"
    
    def test_validate_invalid_type_halts(self, client, api_headers):
        """Invalid mod_type returns halt."""
        response = client.post("/v1/validate", json={
            "mod_type": "invalid_type",
            "target": "test",
            "new_value": "value",
            "reason": "test",
        }, headers=api_headers)
        
        assert response.status_code == 200
        data = response.json()
        assert data["approved"] is False
        assert data["decision_type"] == "halt"
        assert data["code"] == "halt_invalid_modtype"
    
    def test_validate_idempotency(self, client, api_headers):
        """Idempotency key prevents replay."""
        # First request
        response1 = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "test",
            "new_value": "v1",
            "reason": "first",
            "idempotency_key": "unique-key",
        }, headers=api_headers)
        assert response1.json()["approved"] is True
        
        # Replay with same key
        response2 = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "test",
            "new_value": "v2",
            "reason": "replay",
            "idempotency_key": "unique-key",
        }, headers=api_headers)
        assert response2.json()["code"] == "halt_idempotency_replay"
    
    def test_validate_sequence_increments(self, client, api_headers):
        """Sequence increments on approved modifications."""
        response1 = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "t1",
            "new_value": "v1",
            "reason": "first",
        }, headers=api_headers)
        assert response1.json()["sequence"] == 1
        
        response2 = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "t2",
            "new_value": "v2",
            "reason": "second",
        }, headers=api_headers)
        assert response2.json()["sequence"] == 2
    
    def test_require_human_does_not_consume_sequence(self, client, api_headers):
        """
        REQUIRE_HUMAN validate does NOT consume sequence.
        
        This pins the semantic: pending requests do not advance state.sequence.
        Sequence is consumed only by:
        - Approved validate paths (state_delta with sequence_increment)
        - Human approve/reject (explicit sequence consumption)
        """
        # Get state before
        before = client.get("/v1/state", headers=api_headers).json()["sequence"]
        
        # Submit governance request (routes to REQUIRE_HUMAN)
        resp = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new",
            "reason": "test sequence non-consumption",
        }, headers=api_headers)
        
        data = resp.json()
        
        # Get state after
        after = client.get("/v1/state", headers=api_headers).json()["sequence"]
        
        # Assertions pinning the semantic:
        assert data["decision_type"] == "require_human"
        assert data["requires_human"] is True
        assert data["approved"] is False
        
        # Key invariant: returned sequence equals pre-call state.sequence
        assert data["sequence"] == before, \
            f"REQUIRE_HUMAN returned sequence {data['sequence']} != before {before}"
        
        # State.sequence unchanged
        assert after == before, \
            f"State sequence changed from {before} to {after} on REQUIRE_HUMAN"


class TestConcurrency:
    """Concurrency tests (BLOCKER 1 verification)."""
    
    def test_concurrent_validates_no_race(self, api_headers):
        """
        Concurrent validate requests should not produce duplicate sequences.
        
        Under proper locking, only one request at a time can read state,
        compute sequence, and persist. The second should see the updated
        sequence.
        
        NOTE: Each thread creates its own TestClient to avoid thread-safety
        issues with shared client instances.
        """
        results = []
        errors = []
        
        def do_validate(suffix):
            try:
                # Create client per thread (TestClient is not thread-safe when shared)
                with TestClient(app) as local_client:
                    response = local_client.post("/v1/validate", json={
                        "mod_type": "state",
                        "target": f"concurrent_test_{suffix}",
                        "new_value": f"value_{suffix}",
                        "reason": f"Concurrent test {suffix}",
                    }, headers=api_headers)
                    results.append(response.json())
            except Exception as e:
                errors.append(str(e))
        
        # Launch concurrent requests
        threads = []
        for i in range(5):
            t = threading.Thread(target=do_validate, args=(i,))
            threads.append(t)
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # No errors
        assert len(errors) == 0, f"Errors: {errors}"
        
        # All results received
        assert len(results) == 5
        
        # All sequences should be unique (no race condition)
        sequences = [r["sequence"] for r in results if r.get("approved")]
        assert len(sequences) == len(set(sequences)), \
            f"Duplicate sequences detected: {sequences}"
    
    def test_concurrent_validate_and_human_action(self, api_headers, human_headers):
        """
        Mixed validate + human action concurrency test.
        
        Start N threads doing /v1/validate while one thread approves a pending request.
        Assert monotonic sequence in state.json and no chain break.
        """
        # First create a pending request to approve
        with TestClient(app) as setup_client:
            validate_resp = setup_client.post("/v1/validate", json={
                "mod_type": "governance",
                "target": "rules",
                "new_value": "new",
                "reason": "Setup for concurrency test",
            }, headers=api_headers)
            pending_request_id = validate_resp.json()["request_id"]
        
        results = []
        approve_result = []
        errors = []
        
        def do_validate(suffix):
            try:
                with TestClient(app) as local_client:
                    response = local_client.post("/v1/validate", json={
                        "mod_type": "state",
                        "target": f"mixed_concurrent_{suffix}",
                        "new_value": f"value_{suffix}",
                        "reason": f"Mixed concurrent test {suffix}",
                    }, headers=api_headers)
                    results.append(response.json())
            except Exception as e:
                errors.append(f"validate: {e}")
        
        def do_approve():
            try:
                with TestClient(app) as local_client:
                    response = local_client.post("/v1/human/approve", json={
                        "request_id": pending_request_id,
                    }, headers=human_headers)
                    approve_result.append(response.json())
            except Exception as e:
                errors.append(f"approve: {e}")
        
        # Launch mixed concurrent requests
        threads = []
        for i in range(4):
            t = threading.Thread(target=do_validate, args=(i,))
            threads.append(t)
        
        # Add approve thread in the middle
        approve_thread = threading.Thread(target=do_approve)
        threads.insert(2, approve_thread)
        
        for t in threads:
            t.start()
        
        for t in threads:
            t.join()
        
        # No errors
        assert len(errors) == 0, f"Errors: {errors}"
        
        # Approve should have succeeded
        assert len(approve_result) == 1
        assert approve_result[0].get("success") is True
        
        # All validate results received
        assert len(results) == 4
        
        # All sequences should be unique across validates AND approve
        all_sequences = [r["sequence"] for r in results if r.get("approved")]
        all_sequences.append(approve_result[0]["sequence"])
        assert len(all_sequences) == len(set(all_sequences)), \
            f"Duplicate sequences in mixed concurrency: {all_sequences}"
        
        # Verify audit chain is still valid
        with TestClient(app) as verify_client:
            verify_resp = verify_client.get("/v1/audit/verify", headers=api_headers)
            assert verify_resp.json()["valid"] is True
            
            # Get final state sequence
            final_seq = verify_client.get("/v1/state", headers=api_headers).json()["sequence"]
        
        # Collect consumed sequence values from approved validates
        approved_validate_seqs = sorted([r["sequence"] for r in results if r.get("approved")])
        
        # Human action returns its own consumed sequence
        human_seq = approve_result[0]["sequence"]
        
        # Strong invariants (observable-based, not hardcoded arithmetic):
        # 1. All approved validate sequences are unique
        assert len(approved_validate_seqs) == len(set(approved_validate_seqs)), \
            f"Duplicate approved sequences: {approved_validate_seqs}"
        
        # 2. Human sequence is distinct from all validate sequences
        assert human_seq not in approved_validate_seqs, \
            f"Human seq {human_seq} collided with validate seqs {approved_validate_seqs}"
        
        # 3. Final state.sequence equals max consumed sequence
        all_consumed = approved_validate_seqs + [human_seq]
        expected_final = max(all_consumed)
        assert final_seq == expected_final, \
            f"Final sequence {final_seq} != max consumed {expected_final}"


class TestPending:
    """Pending endpoint tests."""
    
    def test_pending_requires_auth(self, client):
        """Pending requires API key."""
        response = client.get("/v1/pending")
        assert response.status_code == 401
    
    def test_pending_empty(self, client, api_headers):
        """Empty pending list."""
        response = client.get("/v1/pending", headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["count"] == 0
        assert data["items"] == []
    
    def test_pending_after_governance(self, client, api_headers):
        """Governance request appears in pending."""
        # Create governance request
        client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new",
            "reason": "test",
        }, headers=api_headers)
        
        # Check pending
        response = client.get("/v1/pending", headers=api_headers)
        data = response.json()
        assert data["count"] == 1
        assert data["items"][0]["mod_type"] == "governance"


class TestHumanActions:
    """Human approve/reject tests (BLOCKER 3 verification)."""
    
    def test_approve_requires_human_auth(self, client, api_headers):
        """Approve requires human key, not API key."""
        response = client.post("/v1/human/approve", json={
            "request_id": "test",
        }, headers=api_headers)
        assert response.status_code == 401
    
    def test_approve_not_found(self, client, human_headers):
        """Approve non-existent request."""
        response = client.post("/v1/human/approve", json={
            "request_id": "nonexistent",
        }, headers=human_headers)
        assert response.status_code == 404
    
    def test_approve_flow(self, client, api_headers, human_headers):
        """Full approve flow."""
        # Create pending request
        validate_response = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new",
            "reason": "test",
        }, headers=api_headers)
        request_id = validate_response.json()["request_id"]
        seq_before = validate_response.json()["sequence"]
        
        # Approve it
        approve_response = client.post("/v1/human/approve", json={
            "request_id": request_id,
        }, headers=human_headers)
        assert approve_response.status_code == 200
        data = approve_response.json()
        assert data["success"] is True
        
        # BLOCKER 3 FIX: Approve should increment sequence
        assert data["sequence"] == seq_before + 1
        
        # Verify removed from pending
        pending_response = client.get("/v1/pending", headers=api_headers)
        assert pending_response.json()["count"] == 0
    
    def test_reject_requires_reason(self, client, human_headers):
        """Reject requires reason."""
        response = client.post("/v1/human/reject", json={
            "request_id": "test",
        }, headers=human_headers)
        assert response.status_code == 400
    
    def test_reject_increments_sequence(self, client, api_headers, human_headers):
        """
        BLOCKER 3 FIX: Reject should also increment sequence.
        Both approve and reject consume a sequence number.
        """
        # Create pending request
        validate_response = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new",
            "reason": "test",
        }, headers=api_headers)
        request_id = validate_response.json()["request_id"]
        seq_before = validate_response.json()["sequence"]
        
        # Reject it
        reject_response = client.post("/v1/human/reject", json={
            "request_id": request_id,
            "reason": "Not approved",
        }, headers=human_headers)
        assert reject_response.status_code == 200
        data = reject_response.json()
        assert data["success"] is True
        
        # Reject should increment sequence
        assert data["sequence"] == seq_before + 1
    
    def test_approve_reject_ordering_durable(self, client, api_headers, human_headers):
        """
        Verify audit entry exists after approve/reject.
        This validates the durability ordering: audit before remove_pending.
        """
        # Create and approve
        validate_response = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "rules",
            "new_value": "new",
            "reason": "test",
        }, headers=api_headers)
        request_id = validate_response.json()["request_id"]
        
        client.post("/v1/human/approve", json={
            "request_id": request_id,
        }, headers=human_headers)
        
        # Check audit contains human_approval
        from storage import load_audit_log
        log = load_audit_log()
        approval_entries = [e for e in log if e.get("decision_type") == "human_approval"]
        assert len(approval_entries) == 1
        assert approval_entries[0]["request_id"] == request_id
    
    def test_require_human_replay_spam_blocked(self, client, api_headers):
        """
        Replay spam on REQUIRE_HUMAN path should be blocked.
        
        Submit governance request with idempotency_key, confirm pending count = 1.
        Submit another governance request with same key, assert halt_idempotency_replay
        and pending count stays 1.
        """
        # First governance request with idempotency key
        response1 = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "spam_test_rules",
            "new_value": "first_attempt",
            "reason": "First governance request",
            "idempotency_key": "spam-test-key",
        }, headers=api_headers)
        
        assert response1.status_code == 200
        data1 = response1.json()
        # Assert semantics, not specific code (kernel-implementation-independent)
        assert data1["requires_human"] is True
        assert data1["decision_type"] == "require_human"
        assert data1["approved"] is False
        
        # Check pending count is 1
        pending_response1 = client.get("/v1/pending", headers=api_headers)
        assert pending_response1.json()["count"] == 1
        
        # Attempt to spam with same idempotency key
        response2 = client.post("/v1/validate", json={
            "mod_type": "governance",
            "target": "spam_test_rules",
            "new_value": "spam_attempt",
            "reason": "Spam attempt with same key",
            "idempotency_key": "spam-test-key",
        }, headers=api_headers)
        
        assert response2.status_code == 200
        data2 = response2.json()
        assert data2["code"] == "halt_idempotency_replay"
        
        # Pending count should still be 1 (spam blocked)
        pending_response2 = client.get("/v1/pending", headers=api_headers)
        assert pending_response2.json()["count"] == 1


class TestSurfaceAuthorization:
    """Surface authorization gate tests."""
    
    def test_api_surface_authorized_by_default(self, client, api_headers):
        """API surface should be authorized in default state."""
        response = client.get("/v1/state", headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert "api" in data["authorized_surfaces"]
    
    def test_api_blocked_when_not_authorized(self, client, api_headers):
        """
        API operations blocked when 'api' not in authorized_surfaces.
        """
        from storage import load_state, save_state, txn_lock
        
        # Remove 'api' from authorized surfaces
        with txn_lock():
            state = load_state()
            state.authorized_surfaces = ["repo", "config"]  # No 'api'
            save_state(state)
        
        # Validate should fail with 403
        response = client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "test",
            "new_value": "value",
            "reason": "test",
        }, headers=api_headers)
        assert response.status_code == 403
        assert "API surface not authorized" in response.json()["detail"]
    
    def test_state_endpoint_works_without_api_surface(self, client, api_headers):
        """
        State endpoint should work even without API surface authorized.
        (So users can diagnose what's wrong.)
        """
        from storage import load_state, save_state, txn_lock
        
        # Remove 'api' from authorized surfaces
        with txn_lock():
            state = load_state()
            state.authorized_surfaces = ["repo", "config"]  # No 'api'
            save_state(state)
        
        # State endpoint should still work
        response = client.get("/v1/state", headers=api_headers)
        assert response.status_code == 200
    
    def test_surface_gate_blocks_audit_and_pending(self, client, api_headers):
        """
        Surface gate applies to audit/pending endpoints.
        
        Remove "api" from authorized surfaces.
        Assert /v1/pending, /v1/audit/head, /v1/audit/verify return 403,
        while /v1/state returns 200.
        """
        from storage import load_state, save_state, txn_lock
        
        # Remove 'api' from authorized surfaces
        with txn_lock():
            state = load_state()
            state.authorized_surfaces = ["repo", "config"]  # No 'api'
            save_state(state)
        
        # /v1/pending should be blocked
        pending_response = client.get("/v1/pending", headers=api_headers)
        assert pending_response.status_code == 403
        assert "API surface not authorized" in pending_response.json()["detail"]
        
        # /v1/audit/head should be blocked
        audit_head_response = client.get("/v1/audit/head", headers=api_headers)
        assert audit_head_response.status_code == 403
        assert "API surface not authorized" in audit_head_response.json()["detail"]
        
        # /v1/audit/verify should be blocked
        audit_verify_response = client.get("/v1/audit/verify", headers=api_headers)
        assert audit_verify_response.status_code == 403
        assert "API surface not authorized" in audit_verify_response.json()["detail"]
        
        # /v1/state should still work (for diagnostics)
        state_response = client.get("/v1/state", headers=api_headers)
        assert state_response.status_code == 200
        assert "api" not in state_response.json()["authorized_surfaces"]


class TestAudit:
    """Audit endpoint tests."""
    
    def test_audit_head(self, client, api_headers):
        """Get audit head."""
        response = client.get("/v1/audit/head", headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert "head_hash" in data
        assert "sequence" in data
        assert "entry_count" in data
    
    def test_audit_verify_empty(self, client, api_headers):
        """Verify empty chain."""
        response = client.get("/v1/audit/verify", headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["valid"] is True
    
    def test_audit_verify_after_operations(self, client, api_headers):
        """Verify chain after operations."""
        # Do some operations
        client.post("/v1/validate", json={
            "mod_type": "state",
            "target": "t1",
            "new_value": "v1",
            "reason": "r1",
        }, headers=api_headers)
        
        client.post("/v1/validate", json={
            "mod_type": "config",
            "target": "t2",
            "new_value": "v2",
            "reason": "r2",
        }, headers=api_headers)
        
        # Verify
        response = client.get("/v1/audit/verify", headers=api_headers)
        data = response.json()
        assert data["valid"] is True
        assert data["entry_count"] >= 2
        # Improved diagnostics
        assert "actual_head_computed" in data


class TestState:
    """State endpoint tests."""
    
    def test_get_state(self, client, api_headers):
        """Get current state."""
        response = client.get("/v1/state", headers=api_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["workflow_posture"] == "STRICT"
        assert "repo" in data["authorized_surfaces"]
        assert "api" in data["authorized_surfaces"]


class TestAtomicWrites:
    """Atomic write tests (BLOCKER 2 verification)."""
    
    def test_state_file_not_corrupted_on_interruption(self, client, api_headers):
        """
        State file should remain valid even if process is interrupted.
        
        This is a basic sanity test - true crash testing would require
        process-level control.
        """
        # Do several rapid operations
        for i in range(10):
            client.post("/v1/validate", json={
                "mod_type": "state",
                "target": f"stress_test_{i}",
                "new_value": f"value_{i}",
                "reason": f"Stress test {i}",
            }, headers=api_headers)
        
        # State should still be valid and loadable
        response = client.get("/v1/state", headers=api_headers)
        assert response.status_code == 200
        
        # Audit chain should be valid
        verify_response = client.get("/v1/audit/verify", headers=api_headers)
        assert verify_response.json()["valid"] is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
