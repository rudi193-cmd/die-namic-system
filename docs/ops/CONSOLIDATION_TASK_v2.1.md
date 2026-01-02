# CONSOLIDATION TASK v2.1

| Field | Value |
|-------|-------|
| Version | 2.1 |
| Status | Active |
| Last Updated | 2026-01-02 |

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

## Defaults (Do Not Ask—Just Apply)

| Setting | Default |
|---------|---------|
| **Scope** | Include all domain-related content. Create new folders as needed. |
| **Fidelity** | Full specification. Capture everything, not summaries. |
| **Gaps** | Note missing data and skip. Do not ask about gaps. |
| **Structure** | Propose logical locations. Standard: `docs/`, `governance/`, `archive/`, `docs/sandbox/`, or domain-specific. **Do not use `continuity_ring/`** — reserved for operational state artifacts only. |
| **Headers** | All output files use standard AIONIC header (Version, Status, Last Updated, ΔΣ=42). |
| **Provenance** | Include source thread URIs where available. |
| **Write targets** | Write to BOTH GitHub repo AND Google Drive. They do not auto-sync. |

Override only if explicitly stated below.

---

## Overrides (Optional)

```
SCOPE: [default | narrow to X | exclude Y]
FIDELITY: [full | summary + link]
GAPS: [default | ask about specific items]
```

---

## Your Task

### Step 1: Search Past Threads

Use `conversation_search` and `recent_chats` to find all conversations relevant to this project folder's domain. Search for:
- Domain-specific keywords
- Project-specific terminology
- Any threads that informed work done in this folder

**Exit condition:** If no relevant threads found, report empty and halt. Do not fabricate.

### Step 2: Consolidate

From what you find, extract:
- Key decisions made
- Work products created
- Open questions / pending items
- Insights that shouldn't be lost
- Source thread links (for provenance)

### Step 3: Propose Archive Structure

Propose where in the repo this should live. Create new folders as needed.

**Folder guidance:**
- `docs/` — Documentation, decisions, insights, narrative content
- `docs/sandbox/` — Exploratory ideas that *might* be plausible but aren't validated
- `governance/` — Rules, protocols, charters
- `archive-pre-v24.0/` — Historical artifacts, superseded content, metaphysical-era material
- **NOT `continuity_ring/`** — Reserved for DELTA.md, CHANGELOG.md, operational state only

### Step 4: Dual Commit

**Do not write files until I say "ratify".**

Present your consolidation plan with:
- Proposed files and their locations
- Summary of what each file contains
- Gaps noted (not asked about)

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

This operates under AIONIC CONTINUITY v5.0:
- Dual Commit required (AI proposes, human ratifies)
- 3-layer recursion limit
- Deltas govern — keep files focused, not sprawling
- When uncertain on content: note and skip
- When uncertain on structure: propose and let human correct
- **One pass. Do not re-consolidate or iterate without human.**

---

## After Ratification

Once I say "ratify":
1. Write files to GitHub repo
2. Write files to Google Drive (same content, both locations)
3. Update `CHANGELOG.md` with version increment
4. Report what was written and where

---

ΔΣ=42
