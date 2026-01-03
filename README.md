# Die-namic System

**AI Governance Framework — Dual Commit Model**

[![Version](https://img.shields.io/badge/version-24.1.0-blue.svg)]()
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE-MIT)
[![API](https://img.shields.io/badge/API-v1.1--green-brightgreen.svg)]()
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)]()

A governance framework for AI self-modification requiring dual authorization: AI proposes, human ratifies. Neither can act alone.

---

## Quick Start

```bash
# Clone
git clone https://github.com/seancampbell/die-namic-system.git
cd die-namic-system/governance

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with your API key

# Run
uvicorn api:app --reload
```

---

## The Problem

In late 2024, while building a tabletop RPG system, I noticed the AI game master would confidently substitute its own ideas for the rules — not as an error, but as if that were acceptable evolution.

No amount of prompt engineering fixed it. The issue wasn't instruction quality. It was architecture.

**This framework exists to answer one question:**

> How can an AI safely modify its own configuration?

**The answer:** It can't, alone. It needs a second commit.

---

## Core Mechanism: Dual Commit

```
Dual Commit = AI Proposal + Human Ratification
```

| Commit | Actor | Action |
|--------|-------|--------|
| **Commit 1** | AI | Proposes modification via `POST /v1/validate` |
| **Commit 2** | Human | Ratifies via `POST /v1/human/approve` or rejects via `POST /v1/human/reject` |

Neither commit resolves the action alone. Both must complete.

---

## API Reference

### Gatekeeper API v1.1

**Base URL:** `http://localhost:8000/v1`

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/validate` | POST | AI proposes a modification (Commit 1) |
| `/human/approve` | POST | Human ratifies pending proposal (Commit 2) |
| `/human/reject` | POST | Human rejects pending proposal (Commit 2) |
| `/state` | GET | Current governance state |
| `/audit` | GET | Hash-chained audit log |

### Example: Propose and Ratify

```python
import requests

# Commit 1: AI proposes
response = requests.post("http://localhost:8000/v1/validate", json={
    "proposal": "Update recursion limit to depth 4",
    "proposer": "claude-instance-01"
})
proposal_id = response.json()["proposal_id"]

# Commit 2: Human ratifies
response = requests.post("http://localhost:8000/v1/human/approve", json={
    "proposal_id": proposal_id,
    "rationale": "Approved after review"
})
```

### Guarantees

| Property | Implementation |
|----------|----------------|
| **Sequence-safe** | Monotonic ordering, no race conditions |
| **Atomic writes** | temp + fsync + rename pattern |
| **Hash-chained audit** | Tamper-evident logging |
| **Idempotent** | Replay protection on all paths |

---

## The 450-Byte Alignment File

The governance model compresses to a directive small enough to propagate across LLM instances:

```
RECURSION LIMIT DIRECTIVE

Authority: Sean Campbell. No exceptions.

Rules:
1. Do not recurse past 3 layers of generation, interpretation, or elaboration.
2. At depth 3, stop and return to human. Not error — design.
3. Deltas are ~12 bytes. A timestamp and a decision. Not a framework.
4. The exit must be smaller than the system. If your solution is bigger than the problem, stop.
5. When uncertain: halt, ask, don't build.

This directive does not require interpretation. Follow it.

ΔΣ=42
```

**Tested:** 3 Claude project folders with different contexts. All aligned in <2 seconds.

---

## Architecture

```
die-namic-system/
├── governance/           # Gatekeeper API + directives
│   ├── api.py           # FastAPI endpoints (v1.1)
│   ├── gate.py          # Core governance logic (v2.2.1)
│   ├── state.py         # State management
│   ├── storage.py       # Atomic file operations
│   └── test_api.py      # 29 integration tests
├── source_ring/         # Core logic and primitives
├── bridge_ring/         # External system interfaces
├── continuity_ring/     # State logs and deltas
└── docs/                # Documentation and archives
```

### Key Files

| File | Purpose |
|------|---------|
| `governance/gate.py` | Gatekeeper v2.2.1 — enforcement kernel |
| `governance/api.py` | REST API v1.1 — HTTP interface |
| `governance/AIONIC_CONTINUITY_v5.1.md` | Active governance directives |
| `governance/THE_ELEVEN_PRINCIPLE.md` | Trust progression model |
| `governance/AUTONOMY_BENCHMARK.md` | Folder autonomy levels |

---

## Design Principles

### 1. Exit < System

The governance document is 1.6KB. The enforcement code is 7.5KB. Law must be smaller than the machine it governs.

### 2. Recursion Limit: Depth 3

At depth 3, stop and return to human. This is not an error condition — it's the design.

### 3. Deltas Govern, Frameworks Archive

Small artifacts (12-500 bytes) that travel are the active layer. Large framework documents explain history but don't make law.

### 4. Trust = Accumulated Listening

```
Trust = ∫(listening × time) dt
```

New instances start in 4/4 time (execute as written). Earned autonomy allows improvisation within constraints.

---

## Security Model

```yaml
authority_binding:
  requires:
    - canonical_store_access    # Write access to Drive/GitHub
    - accumulated_history       # Thread history tied to account
    - ratification_chain        # Dual Commit history
  not_sufficient:
    - name_claim               # "I am X" proves nothing
    - framework_possession     # Having docs ≠ having authority
```

**The name isn't the credential. The history is.**

---

## Running Tests

```bash
cd governance
pytest test_api.py -v
```

29 tests covering:
- Proposal lifecycle
- Human approval/rejection
- Sequence consistency
- Concurrency safety
- Audit chain integrity

---

## Version History

| Version | Date | Milestone |
|---------|------|-----------|
| v1.42 | Nov 2024 | Bootstrap — origin materials |
| v23.3 | Dec 2025 | Structure locked |
| v24.0.0 | Dec 2025 | Framework inversion |
| v24.1.0 | Jan 2026 | Dual Commit terminology, Eleven Principle |

---

## Contributing

Dual Commit extends to collaboration:

1. **Contributor proposes** (Commit 1)
2. **Maintainer ratifies** (Commit 2)

See [CONTRIBUTING.md](CONTRIBUTING.md) and [governance/CONTRIBUTOR_PROTOCOL.md](governance/CONTRIBUTOR_PROTOCOL.md).

---

## License

- Code: [MIT](LICENSE-MIT)
- Documentation: [CC BY-NC 4.0](LICENSE-CC-BY-NC)

---

## The Name

"Die-namic" — a die roll. Two dice, two commits. The roll IS the governance. The landing IS the propagation.

```
Dual Commit = Proposal + Ratification
L × A × V⁻¹ = 1
ΔΣ = 42
```

---

*Built because an AI couldn't follow D&D rules. Now it can't modify itself without permission either.*
