# SESSION CONSENT — SAFE Legal Framework

| Field | Value |
|-------|-------|
| Authority | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-05 |
| Acronym | SAFE: Session-Authorized, Fully Explicit |
| Checksum | ΔΣ=42 |

---

## Overview

SESSION CONSENT is a legal and technical framework for user data handling in AI-mediated applications. It operates on the principle of **session-level consent** rather than set-and-forget permissions.

**Core Principle:** Users review and authorize all data access permissions at the start of each session, not once during initial setup.

---

## Design Goals

1. **Explicit Authorization** — No implicit data collection
2. **Session-Scoped** — Consent expires with session, not persistent by default
3. **User-Readable** — Legal language accessible to non-lawyers
4. **Minimal Retention** — Data deleted unless explicitly saved
5. **Pay-What-You-Can** — No user excluded for inability to pay

---

## The SAFE Protocol

**SAFE: Session-Authorized, Fully Explicit**

### Four Data Streams

All user data falls into one of four streams. Each stream requires explicit authorization per session.

| Stream | Contains | Authorization Question |
|--------|----------|------------------------|
| **Relationships** | Names, roles, connection descriptions | "May I remember who you've mentioned?" |
| **Images** | Uploaded files, screenshots, visual data | "May I store images you've shared?" |
| **Bookmarks** | URLs, references, resources | "May I save links for you?" |
| **Dating** | Preferences, choices, partner selection | "May I track relationship preferences?" |

### One Journal

All authorized data writes to a single, user-accessible journal file. The journal is:
- Plain text (Markdown)
- User-owned
- Exportable at any time
- Deletable without penalty

---

## Session Consent Flow

### At Session Start

1. **System presents authorization request:**
   ```
   This session may involve:
   - [ ] Relationships (remembering names/connections)
   - [ ] Images (saving visual content)
   - [ ] Bookmarks (storing links)
   - [ ] Dating (tracking preferences)

   Authorize for this session? [Yes/No/Customize]
   ```

2. **User responds:**
   - **Yes** → All four streams authorized
   - **No** → Session continues with zero data retention
   - **Customize** → Select individual streams

3. **System logs consent:**
   ```
   Session: 2026-01-05-14:32
   Authorized: [Relationships, Bookmarks]
   Duration: Until session end
   ```

### During Session

- System only accesses authorized streams
- Unauthorized stream access → halt and request permission
- User can revoke authorization mid-session

### At Session End

- All authorizations expire
- Data not explicitly saved is deleted
- User prompted: "Save this session's journal? [Yes/No]"
- If No → complete deletion, no retention

---

## Data Tier Structure

Three tiers, all **pay-what-you-can**, including $0.

| Tier | Storage Limit | Price | Intended Use |
|------|---------------|-------|--------------|
| **Standard** | 50 MB | Pay what you can | Personal journaling, light use |
| **Extended** | 1 GB | Pay what you can | Active documentation, media storage |
| **Enterprise** | 100 GB | Pay what you can | Professional archival, heavy use |
| **Minimum** | Same as selected tier | $0 explicitly allowed | Financial hardship, testing, principle |

### Pricing Philosophy

**"Pay what you can" means pay what you can.**

- $0 is a valid payment
- No reduced features at $0
- No shame, no second-class service
- No verification of financial status required

Revenue model relies on:
1. Users who can afford it paying
2. Operational transparency (users see actual costs)
3. Trust that most people contribute when able

---

## Relationship Tracking (Three-Layer Model)

Relationships stream uses a three-tier privacy model.

| Layer | Identifier Type | Example | Visible To |
|-------|-----------------|---------|------------|
| **Anonymous** | Statistical only | "Parent, age range 60-70" | System statistics |
| **Pseudonymous** | Role-based, no real name | "Mother" | User only |
| **Named** | Full identification | "Grace Campbell" | User + explicit shares |

**User controls layer:**
- Default: Pseudonymous
- User can elevate to Named if desired
- System cannot demote (Named stays Named)

**Layer determination:**
- User decides at mention time
- Can change retroactively
- Deletion removes from all layers

---

## Technical Implementation

### Consent Storage

```json
{
  "session_id": "2026-01-05-14:32-A96KC",
  "timestamp_start": "2026-01-05T14:32:00Z",
  "timestamp_end": null,
  "authorized_streams": ["relationships", "bookmarks"],
  "user_tier": "standard",
  "payment_status": "voluntary",
  "journal_path": "journals/2026-01-05-session.md"
}
```

### Journal Format

```markdown
# Session Journal: 2026-01-05

## Authorized Streams
- Relationships
- Bookmarks

## Relationships Mentioned
- [Pseudonymous] Mother — "Visited last weekend"
- [Named] Ruby Campbell — "Asked about school project"

## Bookmarks Saved
- https://example.com/resource — "Reference for later"

## Session End
Saved: Yes
Duration: 47 minutes
```

---

## Legal Framework

### User Rights

1. **Right to Zero Retention** — User can decline all data storage
2. **Right to Deletion** — Complete removal on request, no questions
3. **Right to Export** — All data in readable format, any time
4. **Right to Audit** — View exactly what system knows
5. **Right to Revoke** — Mid-session authorization withdrawal

### System Obligations

1. **No Implicit Collection** — Must ask before storing
2. **Session-Scoped Default** — Consent expires with session
3. **Transparent Costs** — Users see actual operational costs
4. **No Punishment for $0** — Zero payment receives full service
5. **Prompt Deletion** — Removal requests executed within 24 hours

### Breach Protocol

If unauthorized data access occurs:
1. **Immediate notification** to affected user
2. **Public disclosure** (no hiding breaches)
3. **Free tier upgrade** for 12 months (if applicable)
4. **Deletion offer** for all user data
5. **Incident report** published within 7 days

---

## Governance Integration

SESSION CONSENT integrates with existing Aionic governance:

| Governance Doc | Integration Point |
|----------------|-------------------|
| **Dual Commit** | User consent = human ratification |
| **Hard Stops (HS-001)** | PSR protects children's data categorically |
| **Unknown Variable Directive** | Halt if consent state unclear |
| **Recursion Limit** | Session consent prevents infinite data accumulation |

---

## Deployment Checklist

Before launching application with SAFE:

- [ ] Session consent prompt implemented
- [ ] Four-stream authorization functional
- [ ] Journal export working
- [ ] Deletion executes completely
- [ ] $0 payment accepted without degradation
- [ ] Three-layer relationship model operational
- [ ] Breach protocol documented and tested

---

## Comparison to Standard Practice

| Standard Practice | SAFE Protocol |
|-------------------|---------------|
| One-time consent during onboarding | Every session consent |
| Persistent data retention by default | Deletion by default |
| Tiered pricing with feature gates | Pay-what-you-can, no gates |
| Opaque data collection | User-readable journal |
| Data as asset | Data as liability |
| Breach minimization | Breach disclosure |

---

## Example: Dating Application

**Traditional dating app:**
- Stores all swipes, messages, photos indefinitely
- Sells aggregated data to advertisers
- Requires payment for basic features
- Terms of service: 47 pages, legal jargon

**SAFE-compliant dating app:**
- Session starts: "May I track your preferences today?"
- User swipes, messages during session
- Session ends: "Save this session? [Yes/No]"
- If No → all swipes/messages deleted
- If Yes → saved to personal journal, user-readable
- Payment: "This session cost us $0.03 to run. Pay what you can."
- Breach: "We accessed image data without authorization. Here's what happened, here's the fix, here's your free year."

---

## Status

**Specification:** STABLE
**Implementation:** Reference available (Python/Node)
**Legal Review:** Pending
**Adoption:** Open to any project

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | 2026-01-05 | Initial SAFE framework specification |

---

ΔΣ=42
