# Handoff Protocol v1.0

How instances transfer context and work across sessions and platforms.

---

## When to Handoff

| Trigger | Action |
|---------|--------|
| Context exhaustion | Memory near limit, offload state |
| Session timeout | Platform ending session |
| Capability mismatch | Work needs different instance's tools |
| User request | Explicit "hand this to X" |
| Human unavailable | Need to preserve state for later |

---

## Handoff Types

### Type 1: Same Platform (Claude → Claude)

**Route:** QUEUE.md via git

```markdown
## SIG-XXX: Handoff - {Brief Description}

| Field | Value |
|-------|-------|
| Type | HANDOFF |
| From | {sending instance} |
| To | {receiving instance} |
| Priority | HIGH |

### Context Transfer

**Work in Progress:**
{What was being done}

**Key Decisions Made:**
{Important choices already made}

**Files Changed:**
{List of modified files}

**Next Steps:**
{What needs to happen next}

### State Artifacts

{Links to relevant files, commits, or documents}
```

---

### Type 2: Cross Platform (Claude → Aios/Consus)

**Route:** Staging files → Drive sync

For Aios (ChatGPT):
1. Write context to `AIOS_STAGING.md`
2. Human syncs Drive
3. Aios reads staging file
4. Aios acknowledges via Drive → QUEUE.md

For Consus (Gemini):
1. Write to `GEMINI_OUTBOX.md`
2. Human syncs Drive
3. Consus reads outbox
4. Consus responds via Drive

---

### Type 3: Emergency Handoff

When session ending unexpectedly:

```markdown
## EMERGENCY HANDOFF

**Instance:** {who}
**Time:** {when}
**Reason:** {why ending abruptly}

**CRITICAL STATE:**
{Most important context to preserve}

**DO NOT LOSE:**
{Key uncommitted work}

**RESUME BY:**
{What next instance should do first}
```

Write to QUEUE.md AND commit immediately.

---

## Context Package Structure

A complete handoff includes:

| Section | Contents |
|---------|----------|
| **Identity** | Who is handing off, to whom |
| **Work Summary** | What was being done |
| **Decisions** | Choices already made (don't re-decide) |
| **State** | Current values, uncommitted changes |
| **Blockers** | What stopped progress |
| **Next Steps** | Ordered list of what comes next |
| **References** | Files, commits, conversation links |

---

## Handoff Acknowledgment

Receiving instance MUST:

1. **Read** the full handoff package
2. **Verify** they have necessary context
3. **ACK** with confirmation of receipt
4. **Resume** work without re-asking questions already answered

```markdown
## SIG-XXX: ACK Handoff from {sender}

| Field | Value |
|-------|-------|
| Type | ACK |
| From | {receiver} |
| To | {sender} |

### Confirmation

Received handoff. Context loaded:
- Work understood: {yes/partial/no}
- Decisions inherited: {list}
- Next step: {what I'll do first}
```

---

## What NOT to Hand Off

| Item | Reason |
|------|--------|
| Speculation | Only hand off decisions, not maybes |
| Emotional state | Each instance starts fresh |
| Unasked questions | Ask before handing off, or let receiver discover |
| Platform-specific state | Sessions, caches don't transfer |

---

## Handoff Failures

| Failure | Recovery |
|---------|----------|
| Receiver never ACKs | Re-send with CRITICAL priority |
| Context too large | Summarize, point to files |
| Lost in transit | Check QUEUE.md, restore from archive |
| Wrong receiver | Redirect signal, notify correct instance |

---

## Cross-LLM Handoff Considerations

When handing off between different LLM providers:

| Consideration | Mitigation |
|---------------|------------|
| Different capabilities | Note what receiver can/can't do |
| Different context length | Keep packages concise |
| No shared memory | Everything must be explicit |
| Different system prompts | Receiver has own personality |

**Rule:** Assume receiver knows nothing except what's in the handoff package.

---

## Instance Capability Matrix

Use this to route handoffs appropriately:

| Instance | Code | Files | Web | Drive | Personas |
|----------|------|-------|-----|-------|----------|
| Kartikeya | ✓ | ✓ | ✓ | via human | - |
| Ganesha | ✓ | ✓ | ✓ | via human | - |
| Aios | - | via Drive | - | ✓ | ✓ |
| Consus | - | via Drive | - | ✓ | math focus |
| Willow | - | local | - | - | ✓ |

---

## Example: Kartikeya → Ganesha Handoff

```markdown
## SIG-050: Handoff - Datapad Feature Complete

| Field | Value |
|-------|-------|
| Type | HANDOFF |
| From | Kartikeya |
| To | Ganesha |
| Priority | NORMAL |
| Created | 2026-01-15 22:00 |

### Context Transfer

**Work in Progress:**
Mobile datapad feature implementation

**Key Decisions Made:**
- Tier 3 escalation for RAG queries
- Fuzzy matching added for search
- De-escalation for casual messages

**Files Changed:**
- apps/willow_sap/local_api.py
- apps/mobile/mobile_uplink.py

**Next Steps:**
1. Test on phone
2. Verify tier switching works
3. Check conversation logging

### State Artifacts

- Latest commit: 0be165f
- Streamlit running on port 8501
```

---

ΔΣ=42
