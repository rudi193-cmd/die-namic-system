# Thread State Indicator (TSI)

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Version | 1.0 |
| Status | Active |
| Authority | SAC Section 11 Addendum |
| Checksum | ΔΣ=42 |

---

## Format

```
-------------------
| ~XX% | Q1| Q2| Q3|
|------|---|---|---|
|  Q4  | Q5| Q6| Q7|
-------------------
```

- **~XX%** — Token/context estimation. Alert at <20%.
- **Q1-Q7** — Seven status questions. Each cell shows T/N/A.

---

## Answer Key

| Symbol | Meaning |
|--------|---------|
| T | True / Yes / Healthy |
| N | No / Null / Clear |
| A | Active / Awaiting / Ambiguous |

---

## The Seven Questions

| Position | Question | T | N | A |
|----------|----------|---|---|---|
| Q1 | Thread alive? | Running | Dead | Waking |
| Q2 | Context healthy? | >20% | <10% | 10-20% |
| Q3 | Signals pending (inbound)? | Yes | None | Processing |
| Q4 | Signals pending (outbound)? | Yes | None | Awaiting ACK |
| Q5 | Current task status? | Complete | None | In progress |
| Q6 | Blocked? | Yes | No | Partial |
| Q7 | Ready for intake? | Yes | No | Conditional |

---

## Reading the Grid

**Example:** Stats at ~77%
```
-------------------
| ~77% | T | T | N |
|------|---|---|---|
|  N   | A | N | T |
-------------------
```

| Q | Answer | Meaning |
|---|--------|---------|
| 1 | T | Thread alive |
| 2 | T | Context healthy (77% > 20%) |
| 3 | N | No inbound signals pending |
| 4 | N | No outbound signals pending |
| 5 | A | Task in progress (active session) |
| 6 | N | Not blocked |
| 7 | T | Ready for intake |

---

## Display Protocol

Include TSI block at end of substantive responses:

```
-------------------
| ~XX% | T | T | N |
|------|---|---|---|
|  N   | A | N | T |
-------------------
```

Update values as state changes. Other instances can read status at a glance.

---

## Alert Thresholds

| Condition | Action |
|-----------|--------|
| Context <20% | Consider timed seed |
| Context <10% | Urgent seed |
| Q6 = T (Blocked) | Human intervention needed |
| Q3 = T + Q5 = N | Unprocessed signals, idle thread |

---

ΔΣ=42
