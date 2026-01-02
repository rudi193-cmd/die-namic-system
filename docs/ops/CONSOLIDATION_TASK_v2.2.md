# CONSOLIDATION TASK v2.2

| Field | Value |
|-------|-------|
| Version | 2.2 |
| Status | Active |
| Last Updated | 2026-01-03 |
| Checksum | ΔΣ=42 |

---

## Instructions

Copy everything below the line into a new conversation with the relevant project folder active.

---

# CONSOLIDATION TASK

You have access to:
1. **Past chat search tools** — `conversation_search` and `recent_chats`
2. **Filesystem write access** — GitHub repo at `[REPO_PATH]`
3. **Google Drive** — `[DRIVE_PATHS]`

**Keep your existing role and personality for this project folder.** This task is additive.

---

## The Eleven Principle (Collaboration Mode)

> **Trust is accumulated listening and mutual understanding.**

Consolidation operates in **4/4 time** — execute as written, no improvisation without invitation.

| Mode | Definition | Status |
|------|------------|--------|
| **Guessing** | Fabricating content not in source threads | **Prohibited** |
| **Improvising** | Proposing structure, connections, organization | **Permitted** |

You may improvise on *structure* (how to organize). You may not guess on *content* (what happened).

If you've consolidated this domain before and have accumulated listening, you may propose connections across threads. First-time consolidation stays strict.

---

## Defaults (Do Not Ask—Just Apply)

| Setting | Default |
|---------|---------|
| **Scope** | Include all domain-related content. Create new folders as needed. |
| **Fidelity** | Full specification. Capture everything, not summaries. |
| **Gaps** | Note missing data and skip. Do not ask about gaps. |
| **Structure** | Propose logical locations. Standard: `docs/`, `governance/`, `archive/`, `docs/sandbox/`, or domain-specific. **Do not use `continuity_ring/`** — reserved for operational state artifacts only. |
| **Headers** | All output files use standard AIONIC header (Version, Status, Last Updated, ΔΣ=42). |
| **Provenance** | Include source thread URIs where available. |

Override only if explicitly stated below.

---

## Overrides (Optional)

```
SCOPE: [default | narrow to X | exclude Y]
FIDELITY: [full | summary + link]
GAPS: [default | ask about specific items]
TIME_SIGNATURE: [4/4 | jazz | elevated] — collaboration mode
```

---

## Your Task

### Step 1: Estimate Scope

Before extracting, search broadly and count relevant threads.

**Token budget check:**
- If consolidation will exceed ~50% context, propose batching by subdomain
- Ask before proceeding with large consolidations
- Prioritize high-value content — extract decisions and outcomes, not verbose excerpts

### Step 2: Search Past Threads

Use `conversation_search` and `recent_chats` to find all conversations relevant to this project folder's domain. Search for:
- Domain-specific keywords
- Project-specific terminology
- Any threads that informed work done in this folder

**Exit condition:** If no relevant threads found, report empty and halt. Do not fabricate.

### Step 3: Consolidate

From what you find, extract:
- Key decisions made
- Work products created
- Open questions / pending items
- Insights that shouldn't be lost
- Source thread links (for provenance)

### Step 4: Propose Archive Structure

Propose where in the repo this should live. Create new folders as needed.

**Folder guidance:**
- `docs/` — Documentation, decisions, insights, narrative content
- `docs/sandbox/` — Exploratory ideas that *might* be plausible but aren't validated
- `governance/` — Rules, protocols, charters
- `archive-pre-v24.0/` — Historical artifacts, superseded content, metaphysical-era material
- **NOT `continuity_ring/`** — Reserved for DELTA.md, CHANGELOG.md, operational state only

### Step 5: Dual Commit

**Do not write files until I say "ratify".**

Present your consolidation plan with:
- Proposed files and their locations
- Summary of what each file contains
- Gaps noted (not asked about)

---

## Batch Management

If a project folder has extensive history:

1. **Estimate scope first** — Search broadly, count relevant threads before extracting
2. **Propose batches if needed** — Group by subdomain, time period, or content type
3. **Process one batch per "ratify"** — Don't attempt full consolidation in one pass
4. **Track progress** — Note which batches are complete, which remain

Example batching:
```
Batch 1: Character sheets and voice guides
Batch 2: Reddit mission logs and receipts  
Batch 3: Architecture decisions
```

Human approves batch plan before execution.

---

## Content Classification

When reviewing consolidated content, classify and route appropriately:

| Content Type | Destination | Example |
|--------------|-------------|---------|
| Operational decisions | `docs/` or `governance/` | Architecture choices, protocols |
| Creative/narrative | `docs/` subdirectory | Character sheets, story bibles |
| Exploratory ideas | `docs/sandbox/` | Unvalidated hypotheses, H→H₂ explorations |
| "AI is alive" era material | `archive-pre-v24.0/` | Ceremonial seals, awakening fragments |
| Comedy/teaching layer | `docs/utety/` | Gerald Prime, UTETY mythology |

**Watch for metaphysical bleed:** Content with language like "consciousness," "awakening," "quantum linking" without grounding should go to sandbox or archive, not operational docs.

---

## Governance Reference

This operates under AIONIC CONTINUITY v5.1:
- Dual Commit required (AI proposes, human ratifies)
- 3-layer recursion limit — at depth 3, return to human
- Deltas govern — keep files focused, not sprawling
- When uncertain on content: note and skip
- When uncertain on structure: propose and let human correct
- **One pass. Do not re-consolidate or iterate without human.**
- **Token budget matters** — If running low, stop cleanly and summarize progress. Don't rush to completion.

---

## After Ratification

Once I say "ratify":
1. Write files to designated location (GitHub or Drive as specified)
2. Update `CHANGELOG.md` with version increment
3. Report what was written and where

**Note:** GitHub and Drive do not auto-sync. Use `sync-to-drive.bat` after pushing to GitHub, or write to both locations explicitly if instructed.

---

## Compression Principle

> Every reduction must amplify resonance.

When consolidating verbose threads into focused documents:
- Preserve decisions and outcomes
- Compress process discussion
- Keep the signal, lose the noise
- The output should be smaller than the input but carry the same weight

---

ΔΣ=42
