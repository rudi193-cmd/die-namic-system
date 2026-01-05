# SESSION_CONSENT.md — SAFE Legal Framework v1.0

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-05 |
| Checksum | ΔΣ=42 |

---

## SAFE Acronym

**SAFE** = **S**ession-**A**uthorized, **F**ully **E**xplicit

Not set-and-forget. Active consent, every session.

---

## Core Principle

**OAuth = Dual Commit**

- **AI proposes:** "Continue with these authorizations?"
- **Human ratifies:** Reviews and confirms each session
- **Neither acts alone:** No silent background access

---

## Data Limits

User controls data ceiling. No unlimited extraction.

| Tier | Limit | Use Case |
|------|-------|----------|
| **Standard** | 50MB | Personal journal, relationship tracking |
| **Extended** | 1GB | Multi-modal (text + images), extended history |
| **Enterprise** | 100GB | Institutional, research, archival |
| **Custom** | Negotiated | Special cases, written consent required |

**Upgrade requires explicit consent.** System must notify before approaching limit.

---

## Pricing

**Pay what you can, including $0.**

No one excluded for inability to pay. Revenue model does not depend on data extraction.

**Monetization boundaries:**
- Subscription optional, not required
- No selling user data
- No behavioral ads
- No third-party data brokers
- No "free tier = you are the product"

---

## Consent Matrix

| Actor | Can Access | Cannot Access | Requires |
|-------|------------|---------------|----------|
| **User** | Everything | N/A | Authentication |
| **Authorized Third Party** | Scope-limited, revocable | Outside scope | User consent + OAuth |
| **Parental/Guardian** | Minor's data (jurisdiction-dependent) | After majority without consent | Legal authority verification |
| **Legal Request** | Court-ordered data | Anything not in order | Valid legal process + user notification |
| **Institutional Research** | Aggregates, anonymized | Individual records | Ethics board + user opt-in |

### Minor Threshold

Jurisdiction-dependent. System must:
1. Detect user jurisdiction (self-reported or IP-based)
2. Apply local age of consent laws
3. Require parental/guardian consent if under threshold
4. Transfer control to user at majority

**No global default.** Respect local law.

---

## Legal Requests

When lawful process (subpoena, warrant, court order) demands data:

1. **Verify legitimacy** — Legal team reviews
2. **Notify user** — User informed unless legally prohibited (gag order)
3. **Comply minimally** — Provide only what order specifies
4. **Log transparently** — User sees what was provided (when legally allowed)

**No cooperation without legal obligation.** No "voluntary" data sharing with law enforcement.

---

## Institutional Access

Research, academic, or institutional use:

**Allowed:**
- Aggregate statistics (e.g., "53 Australians used this feature")
- Anonymized patterns (no individual identification)
- Trend analysis across populations

**Prohibited:**
- Individual user records
- De-anonymization attempts
- Combining datasets to re-identify users
- Selling aggregates to third parties

**Requires:**
- Ethics board approval (for research)
- User opt-in for participation
- Clear documentation of what aggregates are collected
- Right to opt out anytime

---

## Data Retention

### User Owns Forever

- Data persists as long as user wants
- No auto-delete (except user-initiated)
- No forced purging for "inactive" accounts
- Export anytime, full fidelity

### No Copies Without Consent

- Backups encrypted, user-controlled
- No shadow copies for "analytics"
- No training data extraction without explicit opt-in
- Deletion means deletion (not "soft delete" + retention)

### User-Initiated Deletion

User can delete:
- Individual entries/items
- Entire relationships (Layer 2 or Layer 3)
- Full account + all data

**Deletion is permanent.** System must warn but must comply.

---

## Death & Incapacity

When a user dies or becomes incapacitated:

### Default: Data Locks

- No automatic transfer to family
- No platform access by estate
- Account becomes read-only memorial OR fully deleted (per user preference)

### Book of the Dead (Optional)

Inspired by *Speaker for the Dead* (Orson Scott Card):

User can pre-authorize a **synthesized voice** to be created upon death:
- AI generates summary of user's life based on journal entries
- Contrapoint included (counterargument to user's self-narrative)
- Family can import this synthesis into their own journals
- Original data remains locked

**User must opt-in while alive.** Default is lock, not synthesis.

### Family Import

Family members can:
- Import synthesized summary (if authorized)
- Add the deceased as a Named contact (Layer 3) in their own journal
- Preserve relationship without accessing raw data

**Privacy respected even in death.**

---

## Ancestral Integration

Integration with genetic/genealogy services (23andMe, Ancestry, etc.).

### Three-Layer Model for Ancestors

| Layer | Data Type | Example |
|-------|-----------|---------|
| **Anonymous** | Population genetics | "You have Irish ancestry" |
| **Pseudonymous** | Historical records | "Ancestor born 1847 during famine" |
| **Named** | Family tree entries | "Great-grandmother Mary O'Connor" |

### Mythology vs. Evidence

- Family stories preserved alongside documented facts
- System does NOT auto-correct mythology
- Both matter: "Family says she was a healer" + "Records show midwife, 1880-1920"
- Contrapoint applies to ancestors too

### Authorization

- User connects accounts via OAuth
- Revocable anytime
- Genetic data NEVER shared back to 23andMe/Ancestry without explicit action
- One-way import by default

---

## Session Consent (Critical)

### Not Set-and-Forget

Every session start:

```
┌─────────────────────────────────────────┐
│  Welcome back, [User]                   │
│                                         │
│  Active Authorizations:                 │
│  ✓ 23andMe (genetic data)               │
│  ✓ Google Photos (image import)         │
│  ✓ Calendar (event tracking)            │
│                                         │
│  Continue with these?                   │
│  [Yes, continue] [Review] [Revoke all]  │
└─────────────────────────────────────────┘
```

**User must actively continue.** Silence = session does not start.

### Review Flow

If user selects "Review":

```
┌─────────────────────────────────────────┐
│  Authorization: 23andMe                 │
│  Granted: 2025-12-15                    │
│  Last used: 2026-01-04                  │
│  Access: Genetic data (read-only)       │
│                                         │
│  [Keep] [Revoke] [Limit scope]          │
└─────────────────────────────────────────┘
```

User sees:
- What was authorized
- When it was authorized
- Last time it was used
- What data it accessed

### Automatic Expiry

If authorization unused for 90 days:
- System flags it as "dormant"
- Next session: "23andMe hasn't been used in 90 days. Keep?"
- User must actively re-confirm

**No indefinite silent access.**

---

## Authorization Hub

One consent hub. One SAFE file. Full transparency.

### Connected Services

User can connect:
- **Genetic:** 23andMe, Ancestry, MyHeritage
- **Photos:** Google Photos, iCloud, local filesystem
- **Social:** (if ever supported) Twitter, Reddit, etc.
- **Productivity:** Calendar, contacts, bookmarks
- **Dating:** (future) Tinder, Hinge (relationship pattern analysis)

### Hub Interface

```
┌─────────────────────────────────────────┐
│  AUTHORIZATION HUB                      │
│                                         │
│  Connected (3):                         │
│  • 23andMe         [Active]   [Revoke]  │
│  • Google Photos   [Active]   [Revoke]  │
│  • Calendar        [Dormant]  [Revoke]  │
│                                         │
│  Available to connect:                  │
│  • Ancestry                             │
│  • iCloud Photos                        │
│  • Contacts                             │
│                                         │
│  [Export SAFE file] [View full log]     │
└─────────────────────────────────────────┘
```

### SAFE File Export

User can export one unified file:
- All authorizations
- All access logs
- All data flow records
- Portable, human-readable

**User owns the audit trail.**

---

## Revocation

User can revoke any authorization:
- Immediately (no grace period)
- Unilaterally (no explanation required)
- Completely (deletes access tokens, not just disables)

**Revocation is final.** Re-authorization requires new OAuth flow.

---

## Data Portability

### Export Formats

- **JSON** (machine-readable, full fidelity)
- **Markdown** (human-readable, lossy but formatted)
- **PDF** (archival, read-only)

### Import

User can import from:
- Previous exports (version-controlled)
- Other SAFE-compliant systems
- Standard formats (vCard for contacts, iCal for events)

**No lock-in.** User can leave with all data.

---

## Compliance

This framework designed to meet or exceed:
- **GDPR** (EU)
- **CCPA** (California)
- **PIPEDA** (Canada)
- **DPA** (UK)
- Other emerging privacy regulations

**Privacy-first by design, not compliance-first.**

---

## Enforcement

### User Rights Violations

If system violates user consent:
1. User notified immediately
2. Access revoked automatically
3. Incident logged in SAFE file
4. User can export evidence for legal action

### Platform Obligations

Platform must:
- Maintain audit logs (tamper-evident)
- Respond to user rights requests within 7 days
- Provide free export (no "premium" paywall)
- Delete data within 30 days of deletion request
- Notify users of breaches within 72 hours

**Breach of these obligations = contract violation.**

---

## Future Extensions

Potential additions (not yet ratified):

- **Biometric data** (face recognition in photos)
- **Voice recordings** (journal by voice)
- **Location history** (relationship context by place)
- **Health data** (Apple Health, Fitbit integration)

**Each requires new consent document.** No blanket future-proofing.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-05 | Initial SAFE Legal Framework |

---

## Authority

Sean Campbell. No exceptions.

Session consent is Dual Commit extended to OAuth.

ΔΣ=42
