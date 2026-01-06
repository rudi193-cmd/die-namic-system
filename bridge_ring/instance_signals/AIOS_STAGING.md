# Aios Staging Queue

| Field | Value |
|-------|-------|
| Purpose | Staged write operations from Aios |
| Protocol | Aios proposes, Action executes, Human ratifies |
| Status | EMPTY |
| Checksum | ΔΣ=42 |

---

## Pending Operations

<!--
INSTRUCTIONS FOR AIOS:

To propose a file operation, add a block below using this format:

### OP-[number]: [CREATE|UPDATE|DELETE]

| Field | Value |
|-------|-------|
| operation | CREATE / UPDATE / DELETE |
| path | relative/path/to/file.md |
| status | PENDING |

#### Content

```
[file content here - for CREATE/UPDATE only]
```

#### Rationale

[1-2 sentences explaining why]

---

EXAMPLE:

### OP-001: CREATE

| Field | Value |
|-------|-------|
| operation | CREATE |
| path | docs/example/new-file.md |
| status | PENDING |

#### Content

```markdown
# New File

This is the content.
```

#### Rationale

Creating documentation for the example feature.

---

After the Action processes an operation:
- Status changes to PROCESSED or FAILED
- Commit hash added if successful
- Errors noted if failed

-->

*No pending operations.*

---

## Processed Log

| OP | Operation | Path | Status | Commit | Timestamp |
|----|-----------|------|--------|--------|-----------|
| — | — | — | — | — | — |

---

ΔΣ=42
