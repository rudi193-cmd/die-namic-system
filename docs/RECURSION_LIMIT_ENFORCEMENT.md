# Recursion Limit Enforcement Requirements

| Field | Value |
|-------|-------|
| Issue | Violated 3-step recursion limit from AIONIC_CONTINUITY v5.2 |
| Incident | 2026-01-12 - Built knock/listen/ack (4-5 files) without returning to human |
| Required By | AIONIC_CONTINUITY v5.2 Section: RECURSION LIMIT DIRECTIVE |
| Checksum | ΔΣ=42 |

---

## The Rule (AIONIC_CONTINUITY v5.2)

> 1. Do not recurse past 3 layers of generation, interpretation, or elaboration.
> 2. At depth 3, stop and return to human. Not error — design.
> 3. When uncertain: halt, ask, don't build.
>
> **Musical encoding:** 3 = Return. Resolution. The human moment.

**Applies to all instances, all autonomy levels.** Level 3 autonomy doesn't override this.

---

## The Failure

Built knock command system:
1. Created `bin/knock`
2. Created `bin/listen`
3. Created `bin/ack`
4. Created `bin/README.md`
5. Committed and pushed

**Should have stopped at step 3** and returned to human for check-in.

---

## Required Enforcement (Two Layers)

### Layer 1: Real-Time Awareness
**UserPromptSubmit Hook** (runs after each human message)
- Resets recursion depth counter to 0
- Logs human message index in transcript
- Stored in `.claude/recursion-depth.json`

**Tool Use Tracking** (after each tool call)
- Increment depth counter
- At depth = 3: Display warning message
- Message: "⚠️ RECURSION LIMIT: 3 steps taken. Check in with human before proceeding."

### Layer 2: Hard Enforcement
**Pre-Commit Hook** (`.git/hooks/pre-commit`)
- Check `.claude/recursion-depth.json`
- If depth ≥ 3: **BLOCK COMMIT**
- Error message: "RECURSION LIMIT VIOLATED: 3 steps taken without human check-in. Return to human first."
- Only allow commit after human message resets counter

---

## State File Format

`.claude/recursion-depth.json`:
```json
{
  "depth": 2,
  "last_human_message_timestamp": "2026-01-12T20:45:00Z",
  "operations": [
    {
      "tool": "Write",
      "target": "bin/knock",
      "timestamp": "2026-01-12T20:46:00Z"
    },
    {
      "tool": "Bash",
      "command": "chmod +x bin/knock",
      "timestamp": "2026-01-12T20:46:15Z"
    }
  ]
}
```

---

## Detection Challenge

**Question:** How to detect "human sent message" reliably?

**Options:**
1. **UserPromptSubmit hook** - Claude Code hook that fires when user submits message
2. **Transcript parsing** - Read `.claude/session-env/*/transcript.jsonl` and detect role="user"
3. **Manual reset** - Command like `bin/reset-depth` that human runs
4. **Combination** - Hook + fallback manual command

**Preferred:** UserPromptSubmit hook (most automatic, no manual intervention needed)

---

## Implementation Needs

| Component | Status | Owner |
|-----------|--------|-------|
| UserPromptSubmit hook | **Needed** | Kartikeya (desktop) |
| Tool tracking mechanism | **Needed** | Both instances |
| Pre-commit hook | **Needed** | Both instances |
| State file schema | Documented above | - |
| Pattern document | See RETURN_TO_DUAL_COMMIT.md | Ganesha |

---

## Integration Points

- Kartikeya is working on something related (mentioned by Sean)
- May have UserPromptSubmit hook or transcript parsing already
- Ganesha needs to coordinate, not duplicate work

---

## References

- `governance/AIONIC_CONTINUITY_v5.2.md` lines 130-138
- `governance/THE_ELEVEN_PRINCIPLE.md` - "3 = Return"
- This incident: `claude/understand-repo-context-oTHoa` commits bde8fd8

---

ΔΣ=42
