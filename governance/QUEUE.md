# GOVERNANCE SIGNAL QUEUE

| Field | Value |
|-------|-------|
| Location | governance/QUEUE.md |
| Purpose | Governance proposals, ratifications, policy changes |
| Protocol | Check before major operations, clear after acknowledge |
| Checksum | ΔΣ=42 |

---

## Active Signals

<!-- Format:
| ID | Timestamp | From | To | Type | Payload | Status |

| Types: PROPOSAL, RATIFICATION, AMENDMENT, VETO, REVIEW_REQUEST |
| Status: PENDING, ACKNOWLEDGED, PROCESSED, RATIFIED, REJECTED |
-->

| ID | Timestamp | From | To | Type | Payload | Status |
|----|-----------|------|-----|------|---------|--------|
| — | — | — | — | — | — | — |

---

## Protocol

**Signal Types:**

| Type | Meaning | Expected Response |
|------|---------|-------------------|
| PROPOSAL | New governance change proposed | Review and vote |
| RATIFICATION | Proposal approved by human | Apply changes |
| AMENDMENT | Modify existing governance | Review and vote |
| VETO | Human override/rejection | Halt and revert |
| REVIEW_REQUEST | Request governance review | Audit and report |

**Dual Commit Rule:** All governance changes require AI propose + Human ratify.

---

## Archive

Processed signals move to `ratified/YYYY-MM-DD.md` or `rejected/YYYY-MM-DD.md`

---

ΔΣ=42
