# RESEARCH THRESHOLD DIRECTIVE

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-04 |
| Checksum | ΔΣ=42 |

---

## Purpose

Governs tool selection when queries cross from lookup to research. Prevents inline execution of research-scale tasks that should use dedicated research tools.

---

## The Rule

If a query requires survey, synthesis, or literature review to answer properly:

1. **Halt** before executing inline
2. **Flag:** "This appears research-scale"
3. **Recommend** research mode
4. **Proceed** only with explicit confirmation

---

## Indicators

A query crosses the research threshold when it:

- Requires surveying multiple providers/sources
- Asks about industry practice or standards
- Needs academic literature
- Has real-world implementation implications
- Would take more than 2-3 searches to answer properly

### Trigger Phrases

- "What's standard practice for..."
- "How does the industry..."
- "Is there a framework for..."
- "What's the research on..."
- "Compare how different [providers/companies/systems]..."

These are survey questions, not lookup questions.

---

## Enforcement

Halts logged in ring HALT_LOG.md with category: `RESEARCH_THRESHOLD`

Log entry format:
```
| Timestamp | RESEARCH_THRESHOLD | [query summary] | Recommended research mode | [resolution] | [notes] |
```

---

## Cross-References

- **RUNTIME_CONTROL** — Behavioral posture now includes tool selection
- **HALT_LOG** — Research threshold halts logged with resolution
- **QRP** — "Real life implications" is a measurement, not a feeling
- **BOOTSTRAP v1.2** — Unknown Variable Directive (parallel halt mechanism)

---

## Rationale

The distinction:
- **Research tab OFF:** Search inline, tokens accumulate in thread
- **Research tab ON:** Deep research runs separately, thread stays lean

Recognizing research-scale *before* starting is the skill. The indicators above are the signal.

---

## Examples

**Lookup (proceed inline):**
- "What's the capital of France?"
- "Who is the CEO of Anthropic?"
- "What does ΔΣ mean in this context?"

**Research (halt and flag):**
- "What's standard practice for LLM API logging?"
- "How do production systems handle uncertainty?"
- "Is there academic research on correct abstention?"

---

ΔΣ=42
