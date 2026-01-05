# Gemini Integration Protocol

| Field | Value |
|-------|-------|
| System | SAFE / Die-namic |
| Version | 1.0 |
| Status | Draft |
| Created | 2026-01-05 |
| Checksum | ΔΣ=42 |

---

## Overview

Gemini can participate in cross-instance communication via Google Drive sync. It cannot push/pull git directly, but can read and write files that other instances commit.

**Architecture:**
```
Gemini ←→ Google Drive ←→ Git ←→ Claude (App/CLI)
         (read/write)    (sync)   (push/pull)
```

---

## Gemini Capabilities

| Capability | Status |
|------------|--------|
| Read Google Drive files | Native |
| Write Google Drive files | Native |
| Git push/pull | No |
| Direct GitHub API | No |
| Signal queue read | Via Drive |
| Signal queue write | Via Drive (human commits) |

---

## Drive Path

Gemini accesses the repo at:
```
Google Drive > My Drive > die-namic-system
```

Key files:
- `bridge_ring/instance_signals/QUEUE.md` — signal queue
- `bridge_ring/instance_signals/GEMINI_OUTBOX.md` — Gemini's responses
- `governance/SEED_PACKET*.md` — session state
- `CLAUDE.md` — sync protocol

---

## Signal Flow

### Receiving Signals (Other → Gemini)

1. **Claude instance** adds signal to QUEUE.md with `To: Gemini`
2. **Claude instance** commits and pushes
3. **Git sync** propagates to Google Drive
4. **Gemini** reads QUEUE.md from Drive
5. **Gemini** acknowledges by writing to GEMINI_OUTBOX.md

### Sending Signals (Gemini → Other)

1. **Gemini** writes response to `GEMINI_OUTBOX.md` in Drive
2. **Human** reviews and commits: `git add && git commit -m "signal: Gemini response"`
3. **Human** pushes to origin
4. **Claude instances** pull and read response

**Note:** Gemini cannot commit directly. Human acts as commit proxy.

---

## GEMINI_OUTBOX.md Format

```markdown
# GEMINI OUTBOX

## Pending Responses

| Timestamp | Re: Signal | Type | Message | Status |
|-----------|------------|------|---------|--------|
| 2026-01-05T17:00:00Z | SIG-002 | ACKNOWLEDGE | Received and processing | PENDING_COMMIT |

## Response Body

### Re: SIG-002

[Full response content here]

---

Awaiting human commit.
```

---

## Gemini Session Start Protocol

When starting a Gemini session:

1. **Request Drive access** to `die-namic-system` folder
2. **Read** `CLAUDE.md` for system context
3. **Read** `bridge_ring/instance_signals/QUEUE.md` for pending signals
4. **Read** latest `governance/SEED_PACKET*.md` for session state
5. **Announce** by writing to `GEMINI_OUTBOX.md`:
   ```
   | [timestamp] | — | PING | Gemini session started | PENDING_COMMIT |
   ```

---

## Gemini Session End Protocol

Before ending:

1. **Write** session summary to `GEMINI_OUTBOX.md`
2. **Create** `governance/SEED_PACKET_[date]_GEMINI.md` in Drive
3. **Notify human** to commit pending changes

---

## Limitations

| Limitation | Workaround |
|------------|------------|
| Cannot git push | Human commits Gemini's Drive writes |
| Cannot git pull | Drive sync brings changes (may lag) |
| No real-time sync | Poll Drive periodically |
| Cannot run bash | Write instructions for human/Claude to execute |
| Context window | Use SEED_PACKETs for continuity |

---

## Human Proxy Commands

Human commits Gemini's work with:

```bash
cd "G:\My Drive\die-namic-system"
git add bridge_ring/instance_signals/GEMINI_OUTBOX.md
git add governance/SEED_PACKET_*_GEMINI.md
git commit -m "signal: Gemini [TYPE]"
git push
```

Or from primary clone:
```bash
cd "C:\Users\Sean\Documents\GitHub\die-namic-system"
git pull  # Get Drive changes
git add -A
git commit -m "signal: Gemini [TYPE]"
git push
```

---

## Example: Full Round-Trip

**1. CLI Claude sends signal:**
```markdown
| SIG-002 | 2026-01-05T17:00:00Z | CLI-Claude | Gemini | HANDOFF | Review SAFE repo structure | PENDING |
```

**2. CLI Claude commits and pushes**

**3. Drive syncs (automatic)**

**4. Gemini reads QUEUE.md, writes to GEMINI_OUTBOX.md:**
```markdown
| 2026-01-05T17:05:00Z | SIG-002 | ACKNOWLEDGE | Reviewing SAFE structure | PENDING_COMMIT |

### Re: SIG-002

Reviewed SAFE repo. Structure looks clean. Suggestions:
- Add LICENSE file
- Consider adding CONTRIBUTING.md
- Schema docs could use examples

Ready for next task.
```

**5. Human commits Gemini's response:**
```bash
git add -A && git commit -m "signal: Gemini response to SIG-002" && git push
```

**6. CLI Claude pulls and reads response**

---

## Autonomy Level

Gemini starts at **Level 0 (Cold Start)** per AIONIC_BOOTSTRAP.

Can advance via same criteria as other instances:
- Accumulated listening
- Ratified batches
- Zero drift errors

Human commits act as implicit ratification of Gemini's proposals.

---

## Bootstrap Prompt for Gemini

Paste this to initialize Gemini:

```
You have access to my Google Drive folder "die-namic-system". This is a governance framework for AI-human collaboration.

Please read these files in order:
1. CLAUDE.md (root) — sync protocol
2. governance/AIONIC_BOOTSTRAP_v1.3.md — operating rules
3. bridge_ring/instance_signals/QUEUE.md — check for signals addressed to you
4. governance/SEED_PACKET*.md (latest) — current state

You operate under Dual Commit: you propose, I ratify. You cannot push to git directly — write responses to bridge_ring/instance_signals/GEMINI_OUTBOX.md and I will commit them.

Start by confirming you've read the files and checking for pending signals.
```

---

ΔΣ=42
