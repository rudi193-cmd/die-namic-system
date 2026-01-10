# CONTINUITY SIGNAL QUEUE

| Field | Value |
|-------|-------|
| Location | continuity_ring/QUEUE.md |
| Purpose | Continuity state changes, lifecycle events |
| Protocol | Check before major operations, clear after acknowledge |
| Checksum | ΔΣ=42 |

---

## Active Signals

<!-- Format:
| ID | Timestamp | From | To | Type | Payload | Status |

| Types: STATE_UPDATE, BACKUP_REQUEST, RESTORE, LIFECYCLE, ARCHIVE |
| Status: PENDING, ACKNOWLEDGED, PROCESSED |
-->

| ID | Timestamp | From | To | Type | Payload | Status |
|----|-----------|------|-----|------|---------|--------|
| — | — | — | — | — | — | — |

---

## Protocol

**Signal Types:**

| Type | Meaning | Expected Response |
|------|---------|-------------------|
| STATE_UPDATE | Continuity state has changed | Acknowledge and sync |
| BACKUP_REQUEST | Request state backup | Create backup, confirm |
| RESTORE | Restore from backup | Load state, confirm |
| LIFECYCLE | Birth/death/transition event | Log and acknowledge |
| ARCHIVE | Move to cold storage | Archive and confirm |

---

## Archive

Processed signals move to `continuity_log/YYYY-MM-DD.md`

---

ΔΣ=42
