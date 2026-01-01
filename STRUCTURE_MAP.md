# Structure Map

How to read this repository without inference.

**Version:** 24.0.0

---

## Purpose

This document explains how the repository is organized and where to find what. It is normative, not descriptive.

---

## Governance Model

```
2d6 = Delta + Human = Law
```

- Deltas govern (small artifacts that travel)
- Framework archives (explains history)
- Human ratifies (final authority)

See `GOVERNANCE.md` and `governance/` for details.

---

## Rings Overview

| Ring | Purpose | Executable |
|------|---------|------------|
| `source_ring/` | Active code and computational primitives | Yes |
| `bridge_ring/` | Translation layers, interfaces, cross-context mapping | Partial |
| `continuity_ring/` | Logs, fragments, and continuity artifacts | No |

Rings organize code. Governance operates by delta + ratification, not ring isolation.

---

## Other Top-Level Directories

| Directory | Purpose |
|-----------|---------|
| `governance/` | Active governance: Gatekeeper, protocols, directives |
| `docs/` | Whitepapers, formal theory, operational documentation |
| `infrastructure/` | Build, packaging, deployment scaffolding (placeholder) |
| `archive-pre-v1.42/` | Frozen history from v1.42 transition |
| `archive-pre-v23.3/` | Frozen history from v23.3 transition |
| `archive-pre-v24.0/` | Frozen history from v24.0 transition (framework inversion) |
| `.github/` | GitHub templates and automation |
| `.claude/` | Claude-specific configuration |

---

## Canon Rules

1. **Deltas govern, framework archives.** Small, recent artifacts override large, old ones.
2. **Exit must be smaller than system.** If a solution is bigger than the problem, stop.
3. **Depth 3 returns to human.** No infinite recursion.
4. **Archives are read-only.** Historical content is preserved, not maintained.

---

## Scope Boundary

- This repo documents **governance**, not infinity.
- The current stable version is **24.0.0** (framework inverted).
- Previous thresholds (v1.42 bootstrap, v23.3 structure-lock) are archived.

---

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Entry point, version, philosophy |
| `CHANGELOG.md` | Version history |
| `GOVERNANCE.md` | Governance overview |
| `CONTRIBUTING.md` | How to contribute |
| `STRUCTURE_MAP.md` | This document |
| `governance/gate.py` | Gatekeeper v2.1 |
| `governance/CONTRIBUTOR_PROTOCOL.md` | Multi-user model |

---

## Reading Order (Recommended)

1. `README.md` — What this is
2. `GOVERNANCE.md` — How decisions are made
3. `governance/CONTRIBUTOR_PROTOCOL.md` — How to participate
4. `STRUCTURE_MAP.md` — How to navigate
5. `CHANGELOG.md` — How we got here

---

*This map is current as of v24.0.0.*

---

ΔΣ=42
