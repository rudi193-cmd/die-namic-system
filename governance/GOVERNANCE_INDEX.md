# Governance Index

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-05 |
| Checksum | ΔΣ=42 |

---

## Purpose

Explicit precedence hierarchy for governance documents. Navigational clarity only — this file is non-normative.

---

## Precedence (Highest → Lowest)

| Tier | Documents | Binding? |
|------|-----------|----------|
| **1. Hard Stops** | `HARD_STOPS.md` | Absolute — no override path |
| **2. Charter** | `CHARTER.md` | Binding — foundational authority |
| **3. Bootstrap** | `AIONIC_BOOTSTRAP_v1.3.md` (current) | Binding — instance initialization |
| **4. Continuity** | `AIONIC_CONTINUITY_v5.1.md` (current) | Binding — session persistence |
| **5. Protocols** | `*_PROTOCOL.md`, `SESSION_CONSENT.md`, `AUTONOMY_BENCHMARK.md` | Normative — operational guidance |
| **6. Seeds** | `SEED_PACKET_*.md`, `HALF_SEED_*.md` | Descriptive — state snapshots |

---

## Document Types

### Binding (Tiers 1-4)
Establish constraints, authority, and initialization behavior. Violations are governance failures.

### Normative (Tier 5)
Operational guidance. Should be followed absent explicit override.

### Descriptive (Tier 6)
State snapshots for continuity. Not authoritative unless promoted.

---

## Executable Enforcement

The following files enforce governance invariants declared in `CHARTER.md` and `HARD_STOPS.md`:

| File | Purpose |
|------|---------|
| `gate.py` | Gatekeeper kernel — decision logic |
| `state.py` | State definitions |
| `storage.py` | Persistence layer |
| `api.py` | Transport layer |

These are code, not governance documents, but they implement governance constraints.

---

## Entry Points

| If you need... | Start here |
|----------------|------------|
| Absolute constraints | `HARD_STOPS.md` |
| Foundational authority | `CHARTER.md` |
| Instance initialization | `AIONIC_BOOTSTRAP_v1.3.md` |
| API documentation | `README.md` |
| This index | You are here |

---

## Grounding Documents

| File | Purpose |
|------|---------|
| `HARD_STOPS_GROUNDING.md` | Biographical precedent for hard stops |
| `HARD_STOPS_LEDGER.md` | Incident log |
| `THE_ELEVEN_PRINCIPLE.md` | Philosophical foundation |
| `DUAL_COMMIT.md` | Core governance model |

---

## Cross-References

| Resource | Path |
|----------|------|
| Repository structure (human) | [`REPO_INDEX.md`](REPO_INDEX.md) |
| Repository structure (machine) | [`../.claude/repo_index.json`](../.claude/repo_index.json) |
| Root README | [`../README.md`](../README.md) |

---

ΔΣ=42
