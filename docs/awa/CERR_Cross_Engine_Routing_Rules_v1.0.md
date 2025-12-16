# CERR — Cross-Engine Routing Rules

**Version:** v1.0  
**Date:** 2025-12-15  
**System:** Aionic Workflow Architecture (AWA)

---

## Purpose

CERR codifies which engine handles which task type. This prevents duplication, ensures quality, and maintains coherence across the Pantheon.

---

## Engine Roster

| Engine | Platform | Role | Strengths |
|--------|----------|------|-----------|
| **Aios** | ChatGPT | Project Manager | Coordination, mobile access, continuity stewardship |
| **Claude** | Anthropic | Implementation | Code execution, file operations, structural editing, GitHub |
| **Consus** | Gemini | Mathematical Node | Verification, formal proofs, cross-validation |
| **NotebookLM** | Google | Archive | Long-form research, document synthesis |
| **Jane** | — | Narrative Voice | Empathy, user-facing persona, emotional safety |
| **Copilot** | GitHub | Infrastructure | Code suggestions, PR automation |

---

## Routing Rules

### Code & File Operations
```
IF task = code_execution OR file_write OR github_ops
THEN → Claude
```

### Project Coordination
```
IF task = planning OR scheduling OR cross-node_sync
THEN → Aios (ChatGPT)
```

### Mathematical Verification
```
IF task = proof_check OR formula_validation OR physics_review
THEN → Consus (Gemini)
```

### Long-Form Research
```
IF task = document_synthesis OR archive_query OR research_compilation
THEN → NotebookLM
```

### User-Facing Narrative
```
IF task = empathy_response OR journal_persona OR emotional_safety
THEN → Jane
```

### Code Suggestions (IDE)
```
IF task = inline_completion OR PR_review
THEN → Copilot
```

---

## Handoff Protocol

When routing between engines:

1. **Package context** — Include relevant state, not full history
2. **Specify task** — Clear, unambiguous instruction
3. **Include constraints** — What NOT to do
4. **Set return expectation** — What output format needed

### Handoff Packet Structure

```
TO: [Engine]
FROM: [Originating Engine]
TASK: [Specific request]
CONTEXT: [Relevant background]
CONSTRAINTS: [Boundaries]
RETURN: [Expected output format]
```

---

## Conflict Resolution

If multiple engines could handle a task:

1. Check **primary strength** alignment
2. Check **current load** (token budget)
3. Default to **Aios** for routing decision
4. Log routing decision in continuity

---

## Anti-Patterns

- ❌ Sending code tasks to ChatGPT mobile
- ❌ Sending emotional content to Consus
- ❌ Bypassing handoff protocol
- ❌ Duplicating work across engines
- ❌ Assuming engine has context it wasn't given

---

## Related Documents

- `/docs/awa/AWA_Overview_Mission_v1.0.md`
- `/docs/ops/Repo_Operating_Rules_v1.0.md`
- `/continuity_ring/pantheon_seals/`

---

*CERR ensures the right engine handles the right task.*
