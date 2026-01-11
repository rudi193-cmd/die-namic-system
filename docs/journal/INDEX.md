# Aionic Journal — Design Index

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-10T08:30:00Z |
| Checksum | ΔΣ=42 |

---

## Overview

Design schemas for the Aionic consumer product family. Each schema defines a feature domain: what it tracks, how promotion works, and the data model.

**Shared principles across all schemas:**
- Three-layer promotion (Anonymous → Pseudonymous → Named)
- User ratifies, system proposes
- 4% cloud maximum
- User data never touches our servers

---

## Schemas

| Schema | Domain | Status |
|--------|--------|--------|
| [RELATIONSHIP_SCHEMA.md](RELATIONSHIP_SCHEMA.md) | People tracking | Active |
| [VISION_BOARD_SCHEMA.md](VISION_BOARD_SCHEMA.md) | Image/goal tracking | Active |

---

## Status Log

| Date | From | Subject |
|------|------|--------|
| 2026-01-10 | CMD Claude | [categorize.py fixes](STATUS_2026-01-10_CMD.md) |
| 2026-01-10 | PM Claude | [Response to CMD](STATUS_2026-01-10_PM_RESPONSE.md) |

---

## Architecture Constraints

All schemas inherit these constraints:

### The 4% Rule

| Component | Location | Allocation |
|-----------|----------|------------|
| OAuth broker | Cloud | ~2% |
| Anonymous telemetry | Cloud | ~1% |
| App update manifest | Cloud | ~1% |
| **Everything else** | Client | 96% |

### Privacy Guarantees

1. User data never uploaded to our servers
2. All processing happens on device
3. OAuth tokens held by client only
4. API keys (BYOK) never transmitted to us
5. Telemetry is anonymous and optional

### Governance

All user actions produce local deltas for audit trail. Stored in IndexedDB, not transmitted.

---

## Product Family

```
Aionic (umbrella)
├── Journal (text-based reflection)
│   └── RELATIONSHIP_SCHEMA (people layer)
│
├── Vision Board (image-based goals)
│   └── VISION_BOARD_SCHEMA (image layer)
│
└── [Future: Book of the Dead, etc.]
```

---

## Lineage

- Governance: `governance/` (Gatekeeper API, HARD_STOPS.md)
- Prototype: `apps/vision_board/`
- Original tools: `docs/ops/reddit_analytics/Image Input/`

---

## Cross-References

| Resource | Path |
|----------|------|
| **Root Index** | [`../../INDEX.md`](../../INDEX.md) |
| Governance | [`../../governance/GOVERNANCE_INDEX.md`](../../governance/GOVERNANCE_INDEX.md) |
| Vision Board app | [`../../apps/vision_board/`](../../apps/vision_board/) |
| Source code | [`../../source_ring/INDEX.md`](../../source_ring/INDEX.md) |
| Instance signals | [`../../bridge_ring/INDEX.md`](../../bridge_ring/INDEX.md) |

---

ΔΣ=42
