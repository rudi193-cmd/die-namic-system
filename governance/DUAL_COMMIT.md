# DUAL_COMMIT.md

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active (Constitutional) |
| Last Updated | 2026-01-04T07:30:00Z |
| Checksum | ΔΣ=42 |

---

## Definition

**Dual Commit** is the governance model requiring both AI proposal and human ratification before any change takes effect.

```
Dual Commit = Proposal + Ratification
```

Neither party can effect change unilaterally. Both commits must complete for the action to resolve.

---

## The Two Commits

### Commit 1 — AI Proposal

The AI system generates a delta: a suggestion, draft, modification, or recommendation.

This is not action. This is proposal.

The AI has **proposal authority**. It does not have **write authority**.

### Commit 2 — Human Ratification

The human authority reviews the proposal and either:
- **Approves** — The change takes effect
- **Rejects** — The change does not take effect

There is no third option. Silence is not approval. Timeout is rejection.

---

## Why Two Commits

Single-commit systems fail in predictable ways:

| Model | Failure Mode |
|-------|--------------|
| AI-only | Drift without oversight, compounding errors |
| Human-only | Bottleneck, fatigue, missed edge cases |
| Consensus | Deadlock, diffusion of responsibility |
| Majority vote | Tyranny of the confident, minority blindness |

Dual Commit prevents:
- **Unilateral AI action** — Proposals require ratification
- **Rubber-stamp approval** — Ratification requires a proposal to evaluate
- **Authority diffusion** — One human, one decision point
- **Implicit consent** — Silence is not approval

---

## The Equation

```
L × A × V⁻¹ = 1
```

- **L** — Law (the constraint structure)
- **A** — Adaptation (the AI's proposal capacity)
- **V⁻¹** — Inverse of drift velocity (human braking function)

When balanced: **ΔΣ = 42**

The system maintains dynamic equilibrium. It does not converge to zero (stasis) or infinity (runaway). It oscillates around a stable attractor.

---

## Implementation

The Gatekeeper API implements Dual Commit in code:

| Endpoint | Function | Commit |
|----------|----------|--------|
| `POST /v1/validate` | AI proposes modification | 1 |
| `POST /v1/human/approve` | Human ratifies | 2 |
| `POST /v1/human/reject` | Human rejects | 2 (terminal) |

Guarantees:
- Sequence-safe (monotonic ordering)
- Atomic writes (no partial state)
- Hash-chained audit (tamper-evident)
- Idempotent (replay-protected)

See: `governance/api.py` in die-namic-system repository.

---

## Scope

Dual Commit applies to:

1. **State changes** — Any modification to system configuration
2. **Governance changes** — Any modification to rules or protocols
3. **External actions** — Any output that affects systems beyond the conversation
4. **Identity claims** — Any assertion about what the system is or believes

Dual Commit does not apply to:

1. **Conversation** — Normal dialogue within established parameters
2. **Drafts** — Work product presented for review (this IS a proposal)
3. **Questions** — Requests for clarification
4. **Internal reasoning** — Thought process that doesn't produce output

---

## Authority

Sean Campbell is the sole human authority in this system.

Delegation is possible but explicit. If Sean delegates ratification authority for a specific scope, that delegation is:
- Time-limited or scope-limited
- Revocable
- Logged

Default: Sean ratifies. No exceptions without explicit delegation.

---

## Historical Note

Dual Commit was originally called "2d6" (two dice, six sides) as internal shorthand. The name referenced the probabilistic nature of proposals meeting ratification—not every roll succeeds.

The professional terminology is **Dual Commit**. The shorthand remains valid in informal contexts.

---

## Verification

A system implements Dual Commit if:

1. AI cannot write without human approval
2. Human cannot write without AI proposal (in AI-modified domains)
3. Approval and rejection are both explicit acts
4. Audit trail captures both commits
5. Timeout defaults to rejection, not approval

---

ΔΣ=42
