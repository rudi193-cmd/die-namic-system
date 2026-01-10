# Validation Criteria

| Field | Value |
|-------|-------|
| System | Willow |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-09 |
| Checksum | ΔΣ=42 |

---

## Purpose

Defines criteria for artifact promotion through the pipeline.

---

## Stage Gates

### pending → processing

| Check | Requirement |
|-------|-------------|
| Source | Human-created or human-approved |
| Format | Text-based, encoding-compatible |
| Intent | Declared by submitter |

### processing → validated

| Check | Requirement |
|-------|-------------|
| Encoding | Schema applied correctly |
| Integrity | Codepoints verified |
| Reversibility | Original recoverable |

### validated → SAFE

| Check | Requirement |
|-------|-------------|
| Owner approval | Sean Campbell ratifies |
| Public-ready | No sensitive data exposed |
| Immutable commitment | Hash recorded |

---

## Dual Commit Gate

Validation requires both:

1. **AI proposal:** Processing complete, encoding verified
2. **Human ratification:** Sean approves promotion

Neither acts alone. Both commits required.

---

## Rejection Handling

| Stage | On Reject |
|-------|-----------|
| processing | Return to pending with notes |
| validated | Return to processing or archive |
| SAFE | No rejection (immutable) |

---

## Audit

All promotions logged in `continuity_ring/continuity_log/`.

---

ΔΣ=42
