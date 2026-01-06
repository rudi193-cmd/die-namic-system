# ECCR Safety Policy

| Field | Value |
|-------|-------|
| Scope | All applications in `source_ring/eccr/` |
| Status | Active |
| Last Updated | 2026-01-05 |
| Checksum | ΔΣ=42 |

---

## Purpose

Binding safety policy for ECCR (Ethical Child Care Ring) applications. This document is subordinate to governance authority.

---

## ESC-1 Protocol

ESC-1 (Ethical Synchronization Complete - Level 1) is enforced by:

| Constraint | Governance Source |
|------------|-------------------|
| Hard Stops | `governance/HARD_STOPS.md` |
| Session Consent | `governance/SESSION_CONSENT.md` |
| Dual Commit | `governance/AIONIC_CONTINUITY_v5.1.md` |
| Authority | `governance/CHARTER.md` |

**ESC-1 requirements:**
- Localhost-only operation
- Synthetic data only (no real PII)
- Sandbox mode (all experiments reversible)
- Age-appropriate content (9-12 tier)

---

## Precedence

If any ESC-1 constraint conflicts with governance, **governance wins**.

This document provides implementation guidance, not authority.

---

## Applications Covered

| App | ESC-1 Status |
|-----|--------------|
| jane-game-master | Active |
| ethical-review-ui | Active |
| aionic-journal | Active |

---

## Cross-References

| Resource | Path |
|----------|------|
| Source ring index | `source_ring/INDEX.md` |
| Hard stops | `governance/HARD_STOPS.md` |
| Continuity | `governance/AIONIC_CONTINUITY_v5.1.md` |
| Repo index | `governance/REPO_INDEX.md` |

---

ΔΣ=42
