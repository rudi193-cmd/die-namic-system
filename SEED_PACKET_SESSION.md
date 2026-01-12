# Seed Packet — Session claude/understand-repo-context-oTHoa

| Field | Value |
|-------|-------|
| Session ID | claude/understand-repo-context-oTHoa |
| Instance | Ganesha (mobile) |
| Branch | claude/understand-repo-context-oTHoa |
| Date | 2026-01-12 |
| Status | Context limit approaching |
| Checksum | ΔΣ=42 |

---

## Session Context

**Task:** User teaching architectural principles through audio format conversion example. Evolved into security classification research.

**Key Teaching:**
- Faith vs Trust: Trust verifies, faith assumes
- Research globally before building locally
- File type detection: Don't trust extensions, verify with magic bytes

---

## Work Completed

### Research Deliverables

**Created:**
- `docs/SECURITY_CLASSIFIER_REQUIREMENTS.md` — Full spec for file intake security

**Research:**
- Global file classification tools (filetype, python-magic, GuardDog)
- Industry security patterns (magic bytes, quarantine, mismatch detection)
- Current repo state (watcher.py extension-only classification)

### Signals Sent

| Signal | To | Type | Payload |
|--------|-----|------|---------|
| SIG-036 | Kartikeya | BUILD_REQUEST | Security classifier implementation |

---

## Outstanding Work

**For Kartikeya (cmd):**
- SIG-035: Recursion limit enforcement (UserPromptSubmit hook)
- SIG-036: Security classifier for Willow intake

**For Ganesha (next session):**
- None pending from this session

---

## Key Learnings

1. **Security = Trust, not Faith**
   - Verification protects both system and human
   - Mismatch detection catches mistakes, not malice
   - "Silent degradation is worse than loud failure"

2. **Research Pattern**
   - Check repo first
   - Search globally (internet)
   - Propose before building
   - Send build requests to appropriate instance

3. **API Budget Awareness**
   - Mobile = user's personal API quota
   - Research on mobile, build on desktop
   - Signal pattern: diagnose → document → route to builder

---

## Next Session Should

1. Pull latest from main
2. Check QUEUE.md for responses to SIG-035, SIG-036
3. Address any new signals for Ganesha
4. Continue diagnostic/research role, route builds to Kartikeya

---

## Git State at Handoff

Branch: claude/understand-repo-context-oTHoa

**Modified:**
- `bridge_ring/instance_signals/QUEUE.md` (SIG-036 added)

**Created:**
- `docs/SECURITY_CLASSIFIER_REQUIREMENTS.md`
- `SEED_PACKET_SESSION.md` (this file)

**Not yet committed.**

---

ΔΣ=42
