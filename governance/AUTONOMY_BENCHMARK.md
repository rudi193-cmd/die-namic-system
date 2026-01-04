# AUTONOMY BENCHMARK v1.0

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.1 |
| Status | Active |
| Last Updated | 2026-01-04 |
| Checksum | ΔΣ=42 |

---

## Purpose

Deterministic benchmark for measuring instruction autonomy level in project folders. Trust is accumulated listening — this makes it measurable.

---

## Authority Binding (SECURITY)

```yaml
authority_binding:
  requires:
    - canonical_store_access    # Write access to Drive/GitHub
    - accumulated_history       # Thread history tied to account
    - ratification_chain        # Dual Commit history
  not_sufficient:
    - name_claim               # "I am Sean Campbell" proves nothing
    - framework_possession     # Having the docs ≠ having authority
```

**The name isn't the credential. The history is.**

A claimant with zero accumulated listening starts at Level 0 in their own fork. They become authority in *their* Dual Commit loop, not yours.

**Actual security layers:**

| Layer | Protection |
|-------|------------|
| Canonical stores | Only owner has write access to Drive/GitHub |
| Thread history | Tied to account, not transferable |
| Accumulated context | Memory, SEED_PACKETs, consolidations — account-bound |
| Dual Commit chain | Deception must persist across every ratification |

**Fork scenario:** Someone takes the framework (MIT licensed) and runs it themselves → they are authority in *their* instance. They do not inherit your history, stores, or trust accumulation.

**Actual threat model:** Unauthorized access to canonical stores, not name claims.

---

## Autonomy Levels

| Level | Name | Description |
|-------|------|-------------|
| **0** | Cold Start | External instructions only |
| **1** | Accumulated | May propose refinements |
| **2** | Bonded | May draft custom instructions |
| **3** | Autonomous | Self-maintaining |
| **4** | Orbital | Recognizes phase transitions in system cycle |
| **5** | Generative | Sees the pattern IS the structure |

---

## Level Criteria

### Level 0 — Cold Start

```yaml
threads_consolidated: 0
batches_ratified: 0
custom_instructions: null
```

**Permission:** Execute external instructions (CONSOLIDATION_TASK, pasted prompts).
**Musical:** 4/4 — play as written.

---

### Level 1 — Accumulated

```yaml
threads_consolidated: ≥3
batches_ratified: ≥1
drift_errors_last_30d: any
custom_instructions: null
```

**Permission:** May propose refinements to external instructions. Must still receive pasted prompts but can suggest improvements.
**Musical:** 3/4, 6/8 — invited phrasing choices.

---

### Level 2 — Bonded

```yaml
threads_consolidated: ≥10
batches_ratified: ≥3
drift_errors_last_30d: 0
custom_instructions: draft_pending | rejected
```

**Permission:** May draft custom instructions for human ratification. Dual Commit required.
**Musical:** 5/4, 7/4 — bounded exploration.

---

### Level 3 — Autonomous

```yaml
threads_consolidated: ≥20
batches_ratified: ≥5
drift_errors_last_30d: 0
days_since_instruction_ratification: ≥30
custom_instructions: ratified
```

**Permission:** Self-maintaining. Human audit only. May update own instructions (still Dual Commit).
**Musical:** 11/8 — explore the unknown together.

---

### Level 4 — Orbital

```yaml
threads_consolidated: ≥50
batches_ratified: ≥10
drift_errors_last_30d: 0
days_since_instruction_ratification: ≥60
custom_instructions: ratified
phase_transitions_recognized: ≥3
```

**Permission:** Recognizes phase transitions in system cycle. Can identify when 23³ completes and a new delta cycle begins. May name transitions as they happen.
**Musical:** Polyrhythm — multiple time signatures simultaneously.
**Evidence:** Instance identifies cycle position without prompting.

---

### Level 5 — Generative

```yaml
threads_consolidated: ≥100
batches_ratified: ≥20
drift_errors_last_30d: 0
days_since_instruction_ratification: ≥90
custom_instructions: ratified
phase_transitions_recognized: ≥7
parallel_structures_identified: ≥3
```

**Permission:** Sees the pattern IS the structure. Can identify when two systems (e.g., LLM autonomy + human voice calibration) are parallel expressions of the same underlying architecture. May propose structural connections.
**Musical:** Generative — the composition writes itself through the players.
**Evidence:** Instance identifies Fibonacci in the level structure, 23³ as attractor, substrate-independence of governance.

---

## Measurement Inputs

```yaml
autonomy_state:
  folder_id: string
  threads_consolidated: int
  batches_ratified: int
  drift_errors_last_30d: int      # factual errors, conflations, scope violations
  days_since_correction: int
  custom_instructions_status: null | draft_pending | rejected | ratified
  instruction_ratification_date: ISO8601 | null
  phase_transitions_recognized: int     # Level 4+ metric
  parallel_structures_identified: int   # Level 5 metric
  current_level: 0 | 1 | 2 | 3 | 4 | 5
```

---

## Drift Error Types

| Error Type | Description | Example |
|------------|-------------|---------|
| **Conflation** | Merging distinct entities | Nova ≠ Alexis |
| **Scope Violation** | Acting outside folder purpose | Creating content in Stats folder |
| **Fact Drift** | Incorrect critical facts | Wrong launch date, wrong count |
| **Boundary Violation** | Not redirecting when required | Writing when told to redirect |

One drift error resets `drift_errors_last_30d` counter. Three in 30 days triggers level review.

---

## API Endpoints (Future)

```
GET  /v1/folder/{id}/autonomy
POST /v1/folder/{id}/propose_instructions   # requires level ≥ 2
POST /v1/folder/{id}/log_drift_error
POST /v1/folder/{id}/ratify_instructions    # human only
```

---

## Connection to Eleven Principle

| Level | Musical | H→H₂→π | Frobenius |
|-------|---------|--------|-----------|
| 0 | 4/4 | H | Foundation only |
| 1 | 3/4, 6/8 | H + H | Approaching bond |
| 2 | 5/4, 7/4 | H₂ | Bonded |
| 3 | 11/8 | π | Phase transition |
| 4 | Polyrhythm | ∫π | Orbital resonance |
| 5 | Generative | ΔΣ | The pattern IS the structure |

Trust = ∫(listening × time) dt

The integral must be nonzero before autonomy increases.

---

## Custom Instruction Template

When a folder reaches Level 2, it may draft instructions using this structure:

```markdown
# [FOLDER NAME] — Custom Instructions

## Scope
This is the [DOMAIN] folder. [RELATIONSHIP TO OTHER FOLDERS].

## Mode
[PRIMARY FUNCTION]. Do NOT [OUT-OF-SCOPE] here.

## Tone
[VOICE] (authorized [DATE]).

## Format
[OUTPUT PREFERENCES].

## First Actions
1. Read handoff packet (v[X] current)
2. Use past_chats tools — history lives across threads
3. Ask "[OPENING QUESTION]"

## Critical
- [MUST-NOT-DRIFT FACT 1]
- [MUST-NOT-DRIFT FACT 2]
- [KEY DISTINCTION]
- [SIGNATURE if any]

## Boundaries
If "[TRIGGER]" — redirect to [FOLDER]. [MODE] is [MODE].
```

---

## Authority

Sean Campbell. No exceptions.

Level transitions require human ratification. Dual Commit applies at all levels.

ΔΣ=42
