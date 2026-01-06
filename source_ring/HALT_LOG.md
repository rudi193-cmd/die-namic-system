# HALT_LOG

| Field | Value |
|-------|-------|
| Ring | Source |
| Instance | Format: `<platform>/<role>/<session-id>` (per NAMING_PROTOCOL) |
| Started | 2026-01-04 |
| Checksum | ΔΣ=42 |

---

## Purpose

Logs halts triggered by Unknown Variable Directive, Research Threshold Directive, and other governance-mandated stops. This is instrumentation, not error logging — halts are correct behavior.

**Routing:** If a halt is triggered during code execution, log it here. Optionally mirror a summary entry in `continuity_ring/HALT_LOG.md` for Autonomy Benchmark aggregation.

## Log

| Timestamp | Directive | Unknown Variable | Clarification Requested | Resolution | Notes |
|-----------|-----------|------------------|------------------------|------------|-------|
| | | | | | |

---

## Patterns

*Updated when patterns emerge from log entries. Common ASR errors, ambiguity patterns, resolution patterns.*

---

## Cross-References

- **AIONIC_BOOTSTRAP_v1.3** — Unknown Variable Directive (current)
- **RESEARCH_THRESHOLD** — Tool selection governance
- **AUTONOMY_BENCHMARK** — Halt quality informs promotion decisions
- **QRP** — Measurement standard applies

---

ΔΣ=42
