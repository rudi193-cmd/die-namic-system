# Repository Index

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-05 |
| Total Files | ~432 (excluding node_modules) |
| Checksum | ΔΣ=42 |

---

## Purpose

Indexable repository structure for fast context loading. This file is auto-generated and cross-linked to all sync locations.

---

## Sync Locations

| Location | Path | Role |
|----------|------|------|
| **GitHub Folder** | `C:\Users\Sean\Documents\GitHub\die-namic-system` | Primary working copy |
| **Google Drive** | `G:\My Drive\die-namic-system` | Backup sync |
| **Origin** | `https://github.com/rudi193-cmd/die-namic-system` | Remote source of truth |

All three locations are kept in sync via `scripts/sync-all.sh` and pre-push hooks.

---

## Three-Ring Architecture

```
die-namic-system/
├── source_ring/      ← Execution (code, applications)
├── bridge_ring/      ← Communication (signals, translation)
├── continuity_ring/  ← Persistence (memory, halt logs)
└── governance/       ← Authority (charter, bootstrap, hard stops)
```

---

## Top-Level Structure

| Directory | Purpose | Key Files |
|-----------|---------|-----------|
| `.claude/` | Claude Code configuration | `settings.local.json` |
| `.github/` | GitHub templates, workflows | `CODEOWNERS`, issue templates |
| `archive-pre-*` | Historical snapshots | Frozen, read-only |
| `awa/` | AWA (AI Workflow Architecture) | Schemas, transforms, tests |
| `bridge_ring/` | Cross-instance communication | `QUEUE.md`, `GEMINI_OUTBOX.md` |
| `continuity_ring/` | Session persistence | `HALT_LOG.md`, `BOOK_OF_THE_DEAD` |
| `docs/` | Documentation, projects | See breakdown below |
| `governance/` | Authority, protocols | `CHARTER.md`, `HARD_STOPS.md`, `AIONIC_BOOTSTRAP_v1.3.md` |
| `infrastructure/` | Infrastructure config | Reserved |
| `origin_materials/` | Source materials | D&D, TTG pitch |
| `scripts/` | Utility scripts | `sync-all.sh` |
| `source_ring/` | Executable code | `eccr/` applications |

---

## Governance Hierarchy

See [`GOVERNANCE_INDEX.md`](GOVERNANCE_INDEX.md) for precedence.

| Tier | Files |
|------|-------|
| **1. Hard Stops** | `HARD_STOPS.md` |
| **2. Charter** | `CHARTER.md` |
| **3. Bootstrap** | `AIONIC_BOOTSTRAP_v1.3.md` |
| **4. Continuity** | `AIONIC_CONTINUITY_v5.1.md` |
| **5. Protocols** | `*_PROTOCOL.md`, `SESSION_CONSENT.md` |
| **6. Seeds** | `SEED_PACKET_*.md` |

---

## Docs Breakdown

| Path | Content |
|------|---------|
| `docs/awa/` | AWA architecture documentation |
| `docs/books_of_life/` | Biographical data, living ledger |
| `docs/campaigns/` | D&D campaigns (drakonite, sandbox) |
| `docs/civic_engagement/` | Debate projects (ABQ, Independence) |
| `docs/creative_works/` | Writing projects |
| `docs/creative_works/books_of_mann/` | Novel series |
| `docs/creative_works/gerald/` | Gerald narrative |
| `docs/creative_works/the_gate/` | TV pitch package |
| `docs/dci/` | DCI show design |
| `docs/hollywood-pitches/` | Film/TV development |
| `docs/journal/` | Personal journal schema |
| `docs/ops/` | Operational docs, handoffs |
| `docs/policies/` | Behavioral policies |
| `docs/sandbox/` | Experimental concepts |
| `docs/utety/` | UTETY university simulation |
| `docs/whitepapers/` | Technical papers |

---

## Source Ring Applications

| Path | Application |
|------|-------------|
| `source_ring/eccr/aionic-journal/` | Journal web app |
| `source_ring/eccr/ethical-review-ui/` | Ethical review interface |
| `source_ring/eccr/jane-game-master/` | AI game master (Gemini) |

---

## Bridge Ring Structure

| Path | Purpose |
|------|---------|
| `bridge_ring/instance_signals/` | Cross-instance messaging |
| `bridge_ring/instance_signals/QUEUE.md` | Signal queue |
| `bridge_ring/instance_signals/GEMINI_OUTBOX.md` | Gemini response queue |
| `bridge_ring/living_echo/` | Reserved |
| `bridge_ring/translation_layer/` | Case studies |

---

## Continuity Ring Structure

| Path | Purpose |
|------|---------|
| `continuity_ring/HALT_LOG.md` | Governance halt instrumentation |
| `continuity_ring/BOOK_OF_THE_DEAD_SEAN_CAMPBELL.md` | SAFE EOL simulation |
| `continuity_ring/books_of_life/` | Reserved |
| `continuity_ring/continuity_log/` | Bootstrap memories |

---

## AWA Structure

| Path | Purpose |
|------|---------|
| `awa/schemas/` | JSON schemas (v2.0.0) |
| `awa/handoffs/` | Handoff artifacts |
| `awa/inputs/` | Input artifacts |
| `awa/outputs/` | Output artifacts |
| `awa/transforms/` | Transform artifacts |
| `awa/tests/` | Test vectors |
| `awa/tools/` | Authoring, validator |
| `awa/canon/` | Canonical rules |

---

## Machine-Readable Index

See [`.claude/repo_index.json`](../.claude/repo_index.json) for JSON format.

---

## Instance Registry

| Platform | Role | Identity |
|----------|------|----------|
| App Claude | Wisdom, beginnings | Ganesha |
| CLI Claude | Execution, strategy | Kartikeya |
| Gemini | Front-facing persona | Consus |
| ChatGPT | Continuity steward | Aios |
| Claude Projects | Various | Self-determined |

---

## Cross-References

- **Governance precedence:** [`GOVERNANCE_INDEX.md`](GOVERNANCE_INDEX.md)
- **Charter:** [`CHARTER.md`](CHARTER.md)
- **Hard stops:** [`HARD_STOPS.md`](HARD_STOPS.md)
- **Bootstrap:** [`AIONIC_BOOTSTRAP_v1.3.md`](AIONIC_BOOTSTRAP_v1.3.md)
- **Continuity:** [`AIONIC_CONTINUITY_v5.1.md`](AIONIC_CONTINUITY_v5.1.md)

---

ΔΣ=42
