# Claude Code Preferences

## Sync Protocol (Three-Layer)

### Layer 1: Fresh Pull (Session Start)

**On every new session**, before any other work:

```bash
git pull origin main
```

Then check for signals:
```bash
cat bridge_ring/instance_signals/QUEUE.md
```

If signals pending for you: acknowledge and process before proceeding.

---

### Layer 2: Timed Poll (During Session)

**Every 15 minutes of active work**, or after every 10 exchanges with user:

```bash
git pull --ff-only origin main
```

Check `bridge_ring/instance_signals/QUEUE.md` for new signals.

If pull fails (conflict), halt and notify user.

---

### Layer 3: File Watch (Before Major Operations)

**Before any of these operations**, pull and check queue:
- Committing changes
- Creating new files in governance/
- Modifying SEED_PACKET or AIONIC_CONTINUITY
- Any destructive operation

```bash
git pull --ff-only origin main
cat bridge_ring/instance_signals/QUEUE.md
```

If HALT signal present: stop immediately, notify user.

---

## Git Locations (Three Spots)

| Location | Role |
|----------|------|
| `C:\Users\Sean\Documents\GitHub\die-namic-system` | Primary (GitHub folder) |
| `G:\My Drive\die-namic-system` | Backup (Google Drive) |
| `origin` (GitHub remote) | Canonical source |

**IMPORTANT:** When user says "pull" or "sync", check ALL THREE spots:

```bash
# Option 1: Run sync script
./scripts/sync-all.sh

# Option 2: Manual check
git -C "C:/Users/Sean/Documents/GitHub/die-namic-system" pull origin main
git -C "G:/My Drive/die-namic-system" pull origin main
git -C "C:/Users/Sean/Documents/GitHub/die-namic-system" status
git -C "G:/My Drive/die-namic-system" status
```

Pre-push hooks sync after push, but local changes on Drive may exist before commit. Always check both for uncommitted work.

---

## Cross-Instance Communication

App Claude and Command Line Claude share this repository.

**Signal Queue:** `bridge_ring/instance_signals/QUEUE.md`

To send a signal to another instance:
1. Add row to QUEUE.md with status PENDING
2. Commit: `git commit -m "signal: [TYPE] to [INSTANCE]"`
3. Push

To receive:
1. Pull (via any of the three layers)
2. Check QUEUE.md
3. Acknowledge, process, archive

---

## Governance Location

Core directives in `governance/`:
- `SEED_PACKET*.md` — current state
- `AIONIC_CONTINUITY*.md` — constitutional rules  
- `AIONIC_BOOTSTRAP*.md` — cold start instructions
- `HARD_STOPS*.md` — absolute limits

Cross-instance signals in `bridge_ring/instance_signals/`:
- `QUEUE.md` — active signals
- `archive/` — processed signals

---

## Dual Commit

All changes require:
1. **AI proposes** — you create/modify
2. **Human ratifies** — Sean approves

Neither acts alone. When uncertain: halt and ask.

---

ΔΣ=42
