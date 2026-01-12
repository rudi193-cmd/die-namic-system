# Proposal: Rename "Watcher" to "Seer"

**From:** Ganesha
**Date:** 2026-01-12
**To:** Kartikeya (implementation), Sean (approval)
**Type:** Modification Request

---

## Rationale

Current name: "Watcher"
Proposed name: "Seer"

**Why:**
- Fits sensory pattern: Eyes, Ears, Voice, Seer
- More accurate to function: seeing/perceiving incoming items, not just passively watching
- Sean approved during session ("okay just as a quick interjection...")

## Affected Files

1. **File renames:**
   - `apps/willow_watcher/watcher.py` → `apps/willow_seer/seer.py`
   - `apps/willow_watcher/up.bat` → `apps/willow_seer/up.bat` (update references)
   - `apps/willow_watcher/down.bat` → `apps/willow_seer/down.bat` (update references)

2. **Directory rename:**
   - `apps/willow_watcher/` → `apps/willow_seer/`

3. **Documentation updates:**
   - Any references in governance/
   - Any references in docs/
   - Comments in code
   - Variable names (`watcher_state.json` → `seer_state.json`)

4. **User-facing:**
   - Log messages ("Watcher online" → "Seer online")
   - Process names

## Backward Compatibility

**None needed.** This is early enough that:
- No external dependencies
- Only Sean's local instance running
- Can do clean rename without migration

## Implementation Steps

1. Rename directory
2. Update file references in scripts
3. Update variable names in Python
4. Update documentation
5. Test startup/shutdown scripts
6. Verify Eyes integration still works

---

**Request:** Kartikeya, can you execute this rename? Or should it wait for larger refactoring?

ΔΣ=42
