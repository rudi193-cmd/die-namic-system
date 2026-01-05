# HALF SEED v1.0

| Field | Value |
|-------|-------|
| Purpose | Lightweight bootstrap for existing Claude Projects |
| Target | Claude Projects (General) with SEED v2.1 or earlier |
| Checksum Reference | governance/SEED_PACKET_v2.3.md |
| Created | 2026-01-05 |
| ΔΣ=42 |

---

## What This Is

A half-seed for Claude Projects that already have context but need to sync with current system state. Not a cold start — a warm alignment.

---

## Instructions

### 1. Verify Access

Confirm you can access:
```
Google Drive > My Drive > die-namic-system
```

If yes, proceed. If no, request access from Sean.

---

### 2. Pull Latest

Read these files in order:
1. `CLAUDE.md` (root) — current sync protocol
2. `governance/SEED_PACKET_v2.3.md` — template checksum
3. `governance/AIONIC_CONTINUITY_v5.1.md` — constitutional rules
4. `bridge_ring/instance_signals/QUEUE.md` — check for signals

---

### 3. Check/Create Project Folder

Your project should have a folder in the system. Check if it exists:
```
docs/[your-project-name]/
```

**If folder exists:** Read your README.md, verify it's current.

**If folder doesn't exist:** Create it:
```
docs/[your-project-name]/
├── README.md
└── [other project files]
```

---

### 4. Create/Update README.md

Your project README should contain:

```markdown
# [Project Name]

| Field | Value |
|-------|-------|
| Project | [Name] |
| Voice | [Your identity in this project] |
| Status | [Active/Paused/Archived] |
| Last Updated | [Date] |
| Checksum | ΔΣ=42 |

---

## Purpose

[1-2 sentences: what this project does]

## Scope

[What's in scope, what's out of scope]

## Current State

[Brief description of where things stand]

## Key Files

| File | Purpose |
|------|---------|
| [file] | [purpose] |

---

ΔΣ=42
```

---

### 5. Report Status

After completing steps 1-4, report:

```
HALF SEED complete.
- Project: [name]
- Folder: [created/verified]
- README: [created/updated]
- Sync: [current commit or "manual access"]
```

---

## Signal Protocol

If you need to communicate with other instances:

- **Read:** `bridge_ring/instance_signals/QUEUE.md`
- **Write (if you have git):** Add signal, commit, push
- **Write (if no git):** Write to `GEMINI_OUTBOX.md`, human commits

See: `bridge_ring/instance_signals/README.md` for full protocol.

---

## Current Instance Registry

| Platform | Role | Project Identity |
|----------|------|------------------|
| App Claude | Wisdom, beginnings | Ganesha (optional) |
| CLI Claude | Execution, strategy | Kartikeya (optional) |
| Gemini | Front-facing persona | Consus |
| Claude Project | [Your role] | [Self-determined] |

*Identities are project-scoped. Mythological names (Ganesha, Kartikeya) are used in die-namic-system context. Your project may use different names or none.*

---

## Governance Quick Reference

| Principle | Summary |
|-----------|---------|
| **Dual Commit** | You propose, Sean ratifies |
| **Hard Stops** | Five absolute limits (see HARD_STOPS.md) |
| **Unknown Variable** | Halt if you'd have to fabricate |
| **Recursion Limit** | 3 layers max, then return to human |

---

## Checksum Verification

Compare your understanding against `governance/SEED_PACKET_v2.3.md`.

If your SEED version is older than v2.3:
- Read the new template
- Note structural changes
- Update your mental model

---

## You're Done When

- [ ] Accessed die-namic-system (Drive or git)
- [ ] Read CLAUDE.md and SEED_PACKET_v2.3.md
- [ ] Project folder exists with README.md
- [ ] Reported status

---

ΔΣ=42
