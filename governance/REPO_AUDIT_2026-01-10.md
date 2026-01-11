# Repository Audit — 2026-01-10

| Field | Value |
|-------|-------|
| Auditor | CMD Claude |
| Date | 2026-01-10 |
| Status | Draft |
| Checksum | ΔΣ=42 |

---

## Executive Summary

**Problem:** Files scattered across GitHub, Drive canonical, and Drive backup without clear organization or cross-linking.

**Finding:** Repository is actually in reasonable shape. Most "scatter" is legacy archives and node_modules noise.

---

## File Counts

| Location | Raw Count | Actual (no node_modules) |
|----------|-----------|--------------------------|
| GitHub | 992 | 284 |
| Drive Canonical | 281 | 281 |
| v1.42 Backup | 975 | ~280 |

**708 files are node_modules** — not project files.

---

## Current Structure (GitHub)

| Folder | Files | Purpose |
|--------|-------|---------|
| docs/ | 170 | Documentation, ops, projects |
| governance/ | 40 | Core governance, seeds, protocols |
| source_ring/ | 21 | Code projects (eccr, willow) |
| bridge_ring/ | 13 | Cross-instance communication |
| archive-pre-* | 18 | Legacy versions |
| continuity_ring/ | 6 | Books of life, logs |
| awa/ | 2 | AWA schemas |
| apps/ | 2 | Consumer apps (vision_board) |
| root | 10 | README, CLAUDE.md, etc |

---

## Sync Status

### GitHub ↔ Drive Canonical

**7 files only in GitHub:**
- `apps/vision_board/*` (4 files) — new, not yet synced
- `docs/journal/*` (3 files) — new today

**4 files only in Drive:**
- `Input folder/*` — staging area, shouldn't be in repo

**Status:** Minor drift. Easy fix.

---

## INDEX Files (Navigation)

| Location | Purpose | Links to |
|----------|---------|----------|
| governance/REPO_INDEX.md | Top-level nav | governance/, docs/ |
| governance/GOVERNANCE_INDEX.md | Governance hierarchy | protocols, seeds |
| governance/INDEX_REGISTRY.md | 23³ lattice | all indexes |
| source_ring/INDEX.md | Code projects | eccr, willow |
| bridge_ring/INDEX.md | Instance signals | queue, archive |
| continuity_ring/INDEX.md | Books of life | session logs |
| docs/journal/INDEX.md | Aionic schemas | relationship, vision |

**Gap:** No single root INDEX.md at repo top level.

---

## SEED_PACKET Files

| File | Type | Keep? |
|------|------|-------|
| SEED_PACKET_v2.4.md | Template | ✓ Canonical |
| SEED_PACKET_2026-01-10_KARTIKEYA.md | Current session | ✓ Active |
| SEED_PACKET_2026-01-09_KARTIKEYA.md | Previous session | Archive |
| SEED_PACKET_2026-01-05_*.md | Old sessions | Archive |
| HALF_SEED_v1.0.md | Variant | Archive? |

**Recommendation:** Keep template (v2.4) + current session. Archive older sessions.

---

## Template/Schema Locations

| Type | Current Location | Should Be |
|------|------------------|-----------|
| AWA schemas | awa/schemas/ | ✓ Correct |
| Journal schemas | docs/journal/ | ✓ Correct |
| Pitch templates | docs/hollywood-pitches/templates/ | ✓ Correct |
| SEED template | governance/ | ✓ Correct |
| Character templates | docs/utety/oakenscroll/ | Consider moving to templates/ |

**Finding:** Templates are reasonably organized. No major consolidation needed.

---

## Issues Found

### 1. No Root INDEX
**Problem:** No single entry point for navigation.
**Fix:** Create `INDEX.md` at repo root linking to all major sections.

### 2. Stale Session SEEDs
**Problem:** 5 old SEED_PACKET session files cluttering governance/.
**Fix:** Move to `governance/archive/seeds/` or delete.

### 3. Apps Not Synced
**Problem:** New `apps/` folder not in Drive.
**Fix:** Sync Drive after stabilizing.

### 4. Drive Input Folder
**Problem:** `Input folder/` in Drive canonical shouldn't exist.
**Fix:** Process or archive those 4 files.

### 5. Multiple Archive Folders
**Problem:** Three archive-pre-* folders with unclear content.
**Fix:** Consolidate to single `archive/` with dated subfolders.

---

## Proposed Structure

```
die-namic-system/
├── INDEX.md                    # NEW: Root navigation
├── CLAUDE.md                   # Instance instructions
├── README.md                   # Public readme
│
├── governance/                 # Constitutional layer
│   ├── GOVERNANCE_INDEX.md     # Governance nav
│   ├── AIONIC_*.md            # Core docs
│   ├── SEED_PACKET_v2.4.md    # Template
│   ├── SEED_PACKET_CURRENT.md # Symlink to latest session
│   └── archive/               # Old sessions, deprecated docs
│
├── docs/                       # Documentation
│   ├── journal/               # Product schemas
│   ├── ops/                   # Operations
│   └── projects/              # Project docs
│
├── apps/                       # Consumer applications
│   └── vision_board/
│
├── source_ring/               # Code
│   ├── eccr/                  # ECCR projects
│   └── willow/                # Encoding layer
│
├── bridge_ring/               # Cross-instance
│   └── instance_signals/
│
├── continuity_ring/           # Session continuity
│   └── books_of_life/
│
└── archive/                   # All legacy (consolidated)
    ├── pre-v1.42/
    ├── pre-v23.3/
    └── pre-v24.0/
```

---

## Action Items

| # | Action | Priority | Effort |
|---|--------|----------|--------|
| 1 | Create root INDEX.md | P1 | 15 min |
| 2 | Archive old SEED_PACKET sessions | P2 | 10 min |
| 3 | Consolidate archive folders | P3 | 20 min |
| 4 | Sync apps/ to Drive | P2 | 5 min |
| 5 | Process Drive Input folder | P3 | 10 min |
| 6 | Add cross-links in INDEX files | P2 | 30 min |

---

## Conclusion

**The repo is less scattered than it feels.** The main issues are:
1. No root INDEX for navigation
2. Some archive cleanup needed
3. Minor GitHub ↔ Drive drift

Not a full restructure — targeted fixes.

---

ΔΣ=42
