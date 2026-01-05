# INSTANCE SIGNAL QUEUE

| Field | Value |
|-------|-------|
| Location | bridge_ring/instance_signals/QUEUE.md |
| Purpose | Cross-instance message passing |
| Protocol | Check before major operations, clear after acknowledge |
| Checksum | ΔΣ=42 |

---

## Active Signals

<!-- Format:
| ID | Timestamp | From | To | Type | Payload | Status |
|
| Types: SYNC, HALT, HANDOFF, PING, STATE_CHANGE |
| Status: PENDING, ACKNOWLEDGED, PROCESSED |
-->

| ID | Timestamp | From | To | Type | Payload | Status |
|----|-----------|------|-----|------|---------|--------|
| — | — | — | — | — | — | — |

---

## Protocol

**Sender:**
1. Add row with PENDING status
2. Commit and push
3. Wait for ACKNOWLEDGED or timeout

**Receiver:**
1. Pull and check queue
2. If message for you: update status to ACKNOWLEDGED
3. Process message
4. Move to archive or update to PROCESSED
5. Push

**Signal Types:**

| Type | Meaning | Expected Response |
|------|---------|-------------------|
| SYNC | Pull latest, state may have changed | Acknowledge after pull |
| HALT | Stop current work, await instruction | Acknowledge and halt |
| HANDOFF | Session ending, context transferred | Acknowledge and read SEED_PACKET |
| PING | Liveness check | Acknowledge only |
| STATE_CHANGE | Specific state delta in payload | Acknowledge and apply |

---

## Archive

Processed signals move to `archive/YYYY-MM-DD.md`

---

ΔΣ=42
