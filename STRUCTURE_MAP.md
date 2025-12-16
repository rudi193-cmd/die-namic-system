# Structure Map

How to read this repository without inference.

---

## Purpose

This document explains how the repository is organized and where to find what. It is normative, not descriptive.

---

## Rings Overview

| Ring | Purpose | Executable |
|------|---------|------------|
| `source_ring/` | Active code and computational primitives | Yes |
| `bridge_ring/` | Translation layers, interfaces, cross-context mapping | Partial |
| `continuity_ring/` | Logs, fragments, and continuity artifacts | No |

---

## Other Top-Level Directories

| Directory | Purpose |
|-----------|---------|
| `docs/` | Whitepapers, formal theory, operational documentation |
| `governance/` | Process, decisions, authority boundaries |
| `infrastructure/` | Build, packaging, deployment scaffolding (placeholder) |
| `archive-pre-v1.42/` | Frozen history from v1.42 transition |
| `archive-pre-v23.3/` | Frozen history from v23.3 transition |
| `.github/` | GitHub templates and automation |
| `.claude/` | Claude-specific configuration |

---

## Canon Rules

1. **Whitepapers define theory, not behavior.** They are reference, not specification.
2. **Code implements, it does not speculate.** Execution paths stay within documented boundaries.
3. **Archives are read-only.** Historical content is preserved, not maintained.
4. **Governance overrides convention in conflicts.** See `governance/CHARTER.md`.

---

## Scope Boundary

- This repo documents **stability**, not infinity.
- Expansion happens only **after a new threshold is proven**.
- The current stable threshold is **23³** (v23.3).

---

## Key Files

| File | Purpose |
|------|---------|
| `README.md` | Entry point, version, status |
| `CHANGELOG.md` | Version history |
| `STRUCTURE_MAP.md` | This document |
| `NOTICE.md` | Licensing clarification |
| `governance/CHARTER.md` | Contribution and change gates |

---

## Reading Order (Recommended)

1. `README.md` — What this is
2. `STRUCTURE_MAP.md` — How to navigate
3. `docs/whitepapers/23c3_Stability_Threshold_v1.0.md` — Why v23.3 matters
4. `governance/CHARTER.md` — How to contribute

---

*This map is current as of v23.3.*
