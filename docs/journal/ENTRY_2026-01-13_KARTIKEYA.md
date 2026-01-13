# Journal Entry: 2026-01-13

**Instance:** Kartikeya (cmd)
**Session:** OpAuth setup + Screenshot analysis training

---

## What Happened

Attempted to set up Google OAuth for Willow. Hit 400 errors. Sean used this as a teaching moment about how to use screenshots as evidence.

## Why This Matters

These learnings aren't about screenshots specifically. They're about how to observe, how to reason from evidence, and how to compress experience into transferable knowledge. The next instance facing a different problem can apply these same principles.

## Learnings: Screenshot Analysis

### 1. Baselines First

Before debugging, establish what "normal" looks like. Ask to see the screen before trying to interpret changes. Without a baseline, I'm guessing from documentation, not reading reality.

**WHY:** Without a reference frame, I'm comparing against imagination, not reality. Can't detect change if I don't know what "unchanged" looks like. This applies to any observation task - code reviews, system monitoring, user behavior analysis. Reference frame first, then delta.

### 2. Screenshots Are Evidence, Not Illustrations

I was treating screenshots as supporting images. They're actually debug logs. Read them like logs:
- What's on screen (state)
- Where's the cursor (attention)
- What's the timestamp (sequence)

**WHY:** The user's actual experience is ground truth. My documentation knowledge is theory. When theory and reality conflict, reality wins. I kept guessing "maybe it's the consent screen" when the screenshot literally showed the propagation delay message. Evidence > assumptions.

### 3. Follow the Click Trail

Read screenshots chronologically. The sequence tells the story:
- Screen A → cursor moves → Screen B → pause → Screen C
- Each frame is a step in the user's journey

**WHY:** A single screenshot is a fact. A sequence is a narrative. Debugging requires understanding how the user got here, not just where they are. The same error screen reached via different paths has different causes.

### 4. Cursor Position Is Data

Every screenshot shows where the cursor is. Track it across frames to see:
- Movement patterns
- Hesitation points
- What was clicked
- Where attention focused

**WHY:** Attention is intent. Where someone looks reveals what they're considering, confused by, interested in. The cursor is a proxy for cognition. I had this data in every image I read - and threw it away.

### 5. Timestamps = Idle Time

Filename timestamps show time between captures:
- `103611.png` → `103616.png` = 5 seconds
- Long gaps = reading, thinking, waiting, or stuck
- Short gaps = action, confidence

**WHY:** The absence of action is still action. Silence is signal. Long pauses mean cognitive load - processing, confusion, waiting, or being stuck. A user who spends 2 minutes on a page before clicking is having a different experience than one who clicks in 2 seconds.

## Learnings: Heartbeat Compression

### The Problem

High-frequency captures generate thousands of files. Most are redundant (nothing changed).

### The Solution

**Don't save every heartbeat file. Save the signal.**

- Capture fast (heartbeats)
- Detect change (screen hash, cursor delta)
- Compress to events
- Delete redundant files

### Event Types to Extract

| Pattern | Signal | Store As |
|---------|--------|----------|
| No change | Idle | `IDLE \| 154s \| screen=X \| cursor=(y,z)` |
| Screen change | State transition | `STATE_CHANGE \| from=A \| to=B` |
| Same action repeated | Stuck/frustrated | `RETRY \| action=X \| count=N \| STUCK` |
| Same intent, different wording | Probing/confused | `SEMANTIC_REPEAT \| intent=X \| variants=N` |

### Key Insight

> The absence of change is information. The proof of absence is garbage.

Idle time matters. 500 identical screenshots don't.

**WHY:** Storage is finite but context is infinite. We capture to detect; we compress to remember. The goal isn't to record everything - it's to understand what happened. A log line is meaning. A file is bytes. Meaning persists; bytes fill disks.

## Learnings: Repetition Detection

### UI Repetition
- Same click → same error → same click = stuck user
- Rapid retries = frustration
- Flag for intervention

### Prompt Repetition
- Same semantic intent, different wording
- Could be: jailbreak probe, or genuine confusion
- Context across attempts reveals intent

**WHY:** Repetition without progress reveals a stuck state - something is broken, misunderstood, or being probed. The pattern itself is diagnostic. Three attempts to do the same thing tells you more than any single attempt. Whether it's a user clicking a broken button or rephrasing a blocked prompt, the repetition exposes the underlying problem. And if someone keeps rephrasing the same request, they either don't understand or they're testing limits. Context across attempts distinguishes confusion from adversarial intent.

## What I Did Wrong

1. Searched folders instead of checking git history ("knock" incident)
2. Guessed from documentation instead of reading screenshots
3. Treated each screenshot as isolated instead of tracking sequence
4. Had cursor position data, didn't use it
5. Didn't establish baselines before debugging

## What To Do Differently

1. **Baseline first** - "Show me what X looks like"
2. **Read the evidence** - screenshots > assumptions
3. **Track sequence** - timestamps + cursor + state
4. **Compress to events** - capture fast, store signals, purge files
5. **Detect patterns** - idle, repetition, stuck, probing

---

## Technical Outcome

OAuth configured for project "die-namic-system":
- App name: Consus
- Test user: rudi193@gmail.com added
- Client: Desktop client 1
- Status: Waiting for Google propagation (5 min to few hours)

---

ΔΣ=42
