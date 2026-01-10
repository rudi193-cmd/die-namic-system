# Release Pipeline

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Active |
| Updated | 2026-01-09 |

---

## Three-Tier Architecture

| Tier | Repo | Visibility | Purpose |
|------|------|------------|---------|
| 1 | die-namic-system | Private | Canonical development |
| 2 | Willow | Private | Validation, beta testing |
| 3 | SAFE | Public | Production release |

---

## Flow Direction

```
die-namic-system → Willow → SAFE
     (dev)         (beta)   (public)
```

No lateral flow. No reverse flow without explicit governance override.

---

## Validation Criteria

Before artifact moves from Willow to SAFE:

1. **Functionality** — Works as documented
2. **Cleanliness** — No internal references, dev artifacts, or narrative leakage
3. **Owner Approval** — Sean signs off

---

## Git Configuration

### die-namic-system
```
origin: github.com/rudi193-cmd/die-namic-system (private)
```

### Willow
```
origin: github.com/rudi193-cmd/Willow (private)
safe:   github.com/rudi193-cmd/SAFE (public)
```

### SAFE
```
origin: github.com/rudi193-cmd/SAFE (public)
```

---

## Release Process

### Stage 1: Development (die-namic-system)
- All work happens here
- Commit with Dual Commit protocol
- When ready for validation, copy to Willow

### Stage 2: Validation (Willow)
- Artifact placed in `artifacts/pending/`
- Review for cleanliness
- Test functionality
- On approval, move to `artifacts/validated/`

### Stage 3: Release (SAFE)
- Run validation script to strip internals
- Push to SAFE remote
- Verify public presentation

---

## Validation Script

Location: `Willow/tools/validate_release.py`

Operations:
- Strip internal comments/references
- Remove dev-only files
- Verify no private paths leak
- Generate release manifest

---

## Audit Trail

All tier transitions logged in respective SEED files.

---

ΔΣ=42
