# Gatekeeper API v1.1

AI Self-Modification Governance API  
**Thin transport layer. Kernel decides.**

**Platform: Unix-only** (fcntl locking)

## v1.1 Changes (Aios Blocker Fixes)

| Blocker | Issue | Fix |
|---------|-------|-----|
| **#1** | No atomic transaction lock | Global `txn_lock()` for all validate/human operations |
| **#2** | Non-atomic state writes | Temp file + fsync + atomic rename pattern |
| **#3** | Human endpoints inconsistent | Both approve/reject consume sequence, correct ordering |

Additional:
- Surface authorization gate (`api` must be in `authorized_surfaces`)
- Improved audit verification diagnostics (`actual_head_computed`)
- Extended test coverage (29 tests including concurrency)

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      API Layer (api.py)                     │
│                    Thin transport only                      │
│   ┌─────────────────────────────────────────────────────┐   │
│   │              with txn_lock():                        │   │
│   │    Parse → Load State → Kernel → Persist → Respond   │   │
│   └─────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Kernel (gate.py v2.2.1)                  │
│                  All governance logic                       │
│     Deterministic │ Sequence-safe │ Hash-chained audit      │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                   Storage (storage.py v1.1)                 │
│              Filesystem persistence layer                   │
│   ┌─────────────────────────────────────────────────────┐   │
│   │  txn.lock │ state.json │ audit.jsonl │ pending.jsonl │   │
│   └─────────────────────────────────────────────────────┘   │
│              Atomic writes │ Global transaction lock         │
└─────────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your keys

# Run server
python api.py

# Or with uvicorn directly
uvicorn api:app --reload
```

## Endpoints

| Method | Path | Purpose | Auth |
|--------|------|---------|------|
| GET | `/v1/health` | Healthcheck | None |
| POST | `/v1/validate` | Submit modification request | API Key |
| GET | `/v1/pending` | List pending approvals | API Key |
| POST | `/v1/human/approve` | Human approves | Human Key |
| POST | `/v1/human/reject` | Human rejects | Human Key |
| GET | `/v1/audit/head` | Current head hash | API Key |
| GET | `/v1/audit/verify` | Verify chain | API Key |
| GET | `/v1/state` | Runtime state | API Key* |

*State endpoint works even without API surface authorized (for diagnostics).

## Authentication

Two key types:
- `X-API-Key`: For standard operations (validate, pending, audit)
- `X-Human-Key`: For human approval actions only

## Surface Authorization

The API checks that `api` is in `authorized_surfaces` before allowing operations.
If not authorized, returns `403 Forbidden`.

Default authorized surfaces: `["repo", "config", "api"]`

## Transaction Safety

All state-modifying operations use a global transaction lock:

```python
with txn_lock():
    state = load_state()
    # ... kernel decides ...
    apply_events(events, state)
```

This prevents race conditions on concurrent requests.

## Atomic Writes

State persistence uses atomic rename:

```python
# Write to temp
with open("state.json.tmp", "w") as f:
    json.dump(data, f)
    f.flush()
    os.fsync(f.fileno())

# Atomic rename
os.replace("state.json.tmp", "state.json")
```

## Human Action Ordering

Both approve and reject follow the same durable ordering:

1. Append audit entry (fsync)
2. Update and save state (atomic rename)
3. Remove from pending (atomic rename)

This ensures audit is never lost even on crash.

## Testing

```bash
# Run all tests
pytest test_api.py -v

# Tests are Unix-only (will skip on Windows)
```

### Test Coverage (29 tests):

| Category | Tests |
|----------|-------|
| Authentication | API key, Human key |
| Validate | approve, require_human, halt codes, idempotency, sequence semantics |
| Concurrency | sequence race, mixed validate+human action |
| Human actions | approve/reject sequence, durability, replay spam |
| Surface authorization | default, blocked, audit/pending gate |
| Audit | head, verify empty/populated |
| Atomic writes | stress test |

### New in v1.1:
- `test_concurrent_validates_no_race` (per-thread client)
- `test_concurrent_validate_and_human_action` (mixed operations, observable-based monotonicity)
- `test_require_human_does_not_consume_sequence` (pins sequence semantic)
- `test_require_human_replay_spam_blocked` (idempotency on REQUIRE_HUMAN)
- `test_surface_gate_blocks_audit_and_pending` (403 on all protected endpoints)

## Files

| File | Version | Purpose |
|------|---------|---------|
| `api.py` | 1.1 | FastAPI transport (8 endpoints) |
| `storage.py` | 1.1 | Filesystem persistence with txn lock |
| `gate.py` | 2.2.1 | Gatekeeper kernel (certified) |
| `state.py` | 2.2.1 | State definitions (certified) |
| `test_api.py` | 1.1 | 29 integration tests |
| `requirements.txt` | - | Dependencies |
| `.env.example` | - | Environment template |

## Platform Requirements

- **Unix-only**: Uses `fcntl` for file locking
- **Python 3.10+**: Dataclasses, type hints
- **FastAPI 0.109+**: Lifespan context manager

Windows is not supported due to `fcntl` dependency.

## Kernel Guarantees

- **Deterministic**: Same input → same output
- **Sequence-safe**: Monotonic ordering enforced
- **Replay-protected**: Idempotency keys tracked
- **Hash-chained audit**: Tamper-evident logging
- **Total validation**: No uncaught exceptions

## Core Principle: Dual Commit

**Dual Commit**: Governance requiring both AI proposal and human ratification before any change takes effect.

- **Commit 1**: AI proposes modification (`POST /v1/validate`)
- **Commit 2**: Human ratifies or rejects (`POST /v1/human/approve` or `/reject`)

Neither party can effect change unilaterally. Both commits must complete for the action to resolve.

---

ΔΣ=42
