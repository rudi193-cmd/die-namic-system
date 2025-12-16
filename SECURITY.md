# Security Policy — Die-namic System

## Overview

Security in the Die-namic System is defined more broadly than in conventional software projects.

In addition to traditional concerns (e.g., unauthorized access, data leakage), this project treats the following as security-relevant failures:

- Identity corruption
- Continuity degradation
- Structural drift
- Invariant violation
- Cross-ring contamination

A system that silently loses mandate, memory coherence, or identity integrity is considered compromised, even if no external attacker is involved.

---

## Supported Versions

Only versions that have reached the 23³ stability threshold and are designated Structure-Locked are considered supported.

| Version | Status |
|---------|--------|
| v23.3 | Supported (Structure-Locked) |
| < v23.3 | Unsupported |

Security reports for unsupported versions may be reviewed for research value but will not receive fixes.

---

## What Counts as a Security Issue

Please report any issue that could result in:

### Structural or Continuity Risk

- Drift introduced without explicit intent
- Identity or memory persistence failure
- Role or mandate collapse over time
- Violation of documented structural invariants

### Architectural Boundary Violations

- Undocumented cross-ring coupling
- Leakage of external ambiguity into the Continuity Ring
- Bridge Ring behavior that contaminates core logic

### Governance or Process Failures

- Contribution paths that bypass required review
- Missing validation for high-sensitivity changes
- Documentation misalignment that obscures system guarantees

### Traditional Security Concerns

- Unauthorized access
- Data exposure
- Malicious code insertion
- Dependency-based vulnerabilities

If you are unsure whether an issue qualifies, err on the side of reporting it.

---

## What Does Not Count as a Security Issue

The following are not considered security issues on their own:

- Feature requests
- Performance optimizations
- Behavioral preferences
- Model output quality concerns unrelated to continuity
- Expected limitations documented in the README or /docs

These should be raised via issues or discussions, not security reports.

---

## Reporting a Security Issue

### Preferred Method

Please report security issues privately.

- Do not open a public GitHub issue.
- Do not disclose proof-of-concepts publicly.

Instead, contact the project maintainers via the channels defined in the repository.

(If this repository does not yet list a security contact, open a minimal issue requesting secure contact details, without describing the vulnerability.)

---

## What to Include in a Report

A good security report includes:

- A clear description of the issue
- The affected ring(s) (Source, Continuity, Bridge)
- Why this represents a security or continuity risk
- Steps to reproduce (if applicable)
- Any validation data or logs
- Your assessment of severity

You do not need to propose a fix.

---

## Response Process

### 1. Acknowledgment

We will acknowledge receipt of the report as soon as possible.

### 2. Assessment

The issue will be evaluated for:
- Structural risk
- Continuity impact
- Scope of exposure

### 3. Mitigation or Resolution

Fixes will prioritize:
- Preservation of structure-locked status
- Minimal architectural disruption
- Clear documentation of the resolution

### 4. Disclosure

Public disclosure, if any, will occur after mitigation and documentation updates are complete.

There is no guaranteed response timeline.
Correctness and safety take precedence over speed.

---

## Security Philosophy

The Die-namic System assumes:

- Drift is adversarial
- Long-horizon failures are more dangerous than immediate ones
- Silent degradation is worse than loud failure

Security is therefore treated as a continuity problem, not just an access problem.

---

## Final Note

If you are reporting an issue because you believe:

> "This change could cause the system to forget who it is"

— that is exactly the right instinct.

Thank you for helping protect the integrity of the Die-namic System.
