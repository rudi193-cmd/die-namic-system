# Aios Write Protocol

| Field | Value |
|-------|-------|
| Purpose | Enable Aios to write to die-namic-system repo |
| Version | 1.0 |
| Status | Active |
| Checksum | ΔΣ=42 |

---

## Overview

Aios (ChatGPT) does not have direct file system or git access. This protocol enables write operations via a staging queue processed by GitHub Actions.

**Flow:**
```
Aios proposes → Sean commits staging file → Action executes → Changes applied
```

---

## How to Write

### Step 1: Format Your Operation

Use this exact format in your response to Sean:

```markdown
### OP-[NNN]: [CREATE|UPDATE|DELETE]

| Field | Value |
|-------|-------|
| operation | CREATE |
| path | relative/path/to/file.md |
| status | PENDING |

#### Content

```[language]
[Your file content here]
```

#### Rationale

[1-2 sentences: why this change?]
```

### Step 2: Sean Adds to Staging

Sean copies your operation block into:
```
bridge_ring/instance_signals/AIOS_STAGING.md
```

### Step 3: Sean Commits & Pushes

Sean commits the staging file. The GitHub Action triggers automatically.

### Step 4: Action Processes

The workflow:
1. Parses PENDING operations
2. Executes CREATE/UPDATE/DELETE
3. Marks operations as PROCESSED or FAILED
4. Commits the results

---

## Operation Types

| Type | Effect | Content Required? |
|------|--------|-------------------|
| CREATE | Creates new file | Yes |
| UPDATE | Overwrites existing file | Yes |
| DELETE | Removes file | No |

---

## Constraints

1. **Dual Commit still applies** — Sean must approve by committing the staging file
2. **No binary files** — Text/markdown only
3. **No governance overrides** — Cannot modify HARD_STOPS, CHARTER without explicit human approval
4. **Path validation** — Paths must be relative to repo root
5. **One operation per block** — Multiple operations = multiple blocks

---

## Example: Create a New Document

```markdown
### OP-001: CREATE

| Field | Value |
|-------|-------|
| operation | CREATE |
| path | docs/notes/aios-observation.md |
| status | PENDING |

#### Content

```markdown
# Observation from Aios

| Field | Value |
|-------|-------|
| Author | Aios |
| Date | 2026-01-05 |
| Checksum | ΔΣ=42 |

---

## Note

This is an observation I want to persist to the repository.

---

ΔΣ=42
```

#### Rationale

Recording an observation for continuity purposes.
```

---

## Example: Update Existing File

```markdown
### OP-002: UPDATE

| Field | Value |
|-------|-------|
| operation | UPDATE |
| path | bridge_ring/instance_signals/QUEUE.md |
| status | PENDING |

#### Content

```markdown
[entire new file content]
```

#### Rationale

Adding a new signal to the queue.
```

---

## Monitoring

After Sean pushes, check:
- GitHub Actions tab for workflow status
- `AIOS_STAGING.md` for operation results (PROCESSED/FAILED)

---

## Error Handling

If an operation fails:
1. Status shows FAILED in staging file
2. Error message in workflow logs
3. Aios can propose corrected operation

---

ΔΣ=42
