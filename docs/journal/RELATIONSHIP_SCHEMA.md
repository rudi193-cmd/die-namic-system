# RELATIONSHIP_SCHEMA v1.0 — Aionic Journal

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-04T09:00:00Z |
| Product | Aionic Journal (Consumer App) |
| Checksum | ΔΣ=42 |

---

## Overview

The Aionic Journal tracks relationships through organic discovery, not contact import. Users journal about their lives; the system notices patterns and proposes relationship recognition.

**Core principle:** The journal learns who matters by listening, not by asking for a contact list.

---

## The Three Layers (User-Facing)

### Layer 1: Unnamed Mentions

**What the user experiences:**
- "I talked to someone at the coffee shop"
- "Had a meeting with 5 people"
- "Ran into an old friend"

**What the system captures:**
- Context (location, activity, emotional tone)
- Frequency (how often unnamed interactions occur)
- Category signals (positive, stressful, neutral)

**User sees:** Nothing explicit. This is background pattern detection.

### Layer 2: Recognized References

**What the user experiences:**
- "that coworker"
- "my neighbor"
- "coffee shop guy"
- "work Sarah" (distinguished from other Sarahs)

**What the system captures:**
- Reference string (how user naturally refers to them)
- First mention date
- Mention frequency
- Context clusters (where/when they appear)
- Emotional valence patterns

**User sees:** Nothing until promotion prompt. System is listening, not displaying.

### Layer 3: Named Contacts

**What the user experiences:**
- Full name with optional details
- Relationship type (friend, family, coworker, etc.)
- History of interactions visible
- Can add notes, reminders, context

**What the system captures:**
- All Layer 2 data, plus:
- Confirmed identity
- User-provided details
- Relationship health indicators

**User sees:** Contact appears in "People" view. Interaction history accessible.

---

## Promotion Flow

### Recognition Prompt

When system detects sufficient pattern:

```
┌─────────────────────────────────────────┐
│  You've mentioned "work Sarah" 7 times  │
│  in the last month.                     │
│                                         │
│  Want to add her to your people?        │
│                                         │
│  [Add Sarah]  [Not now]  [Never ask]    │
└─────────────────────────────────────────┘
```

**Options:**
- **Add:** Opens minimal profile creation
- **Not now:** Dismisses, system will ask again after 3 more mentions
- **Never ask:** Permanently keeps reference at Layer 2

### Profile Creation (Minimal)

```
┌─────────────────────────────────────────┐
│  Adding: work Sarah                     │
│                                         │
│  Full name: [Sarah ________]            │
│  Relationship: [Coworker ▼]             │
│                                         │
│  [Save]  [Add more details]             │
└─────────────────────────────────────────┘
```

**Required:** Nothing. User can save with just "work Sarah" if they want.
**Optional:** Full name, relationship type, notes, photo, contact info.

---

## Relationship Categories (Internal)

System silently categorizes based on journal content:

| Category | Signal | User Benefit |
|----------|--------|--------------|
| **Supportive** | Positive emotional language, seeks out | Surface during hard times |
| **Stressful** | Negative language, avoidance patterns | Pattern awareness prompts |
| **Professional** | Work context, formal language | Separate from personal |
| **Family** | Family terms, obligation language | Birthday/event reminders |
| **Connector** | Introduces others, bridges contexts | Network visualization |
| **Dormant** | No mentions in 90+ days | "Haven't seen X in a while" |

**User never sees categories directly.** They inform prompts and insights.

---

## Privacy Architecture

### User Controls

| Setting | Options | Default |
|---------|---------|---------|
| Relationship detection | On / Off | On |
| Promotion prompts | On / Off | On |
| Minimum mentions before prompt | 3 / 5 / 7 / 10 | 5 |
| Auto-archive dormant | On / Off | Off |

### Data Handling

| Data | Storage | User Access |
|------|---------|-------------|
| Journal entries | Encrypted, local-first | Full |
| Unnamed mentions | Aggregate counts only | Summary stats |
| Recognized references | Local until promotion | Viewable on request |
| Named contacts | User-controlled | Full CRUD |

### What We Never Do

- Import contacts without explicit action
- Share relationship data with third parties
- Infer relationships from external sources
- Auto-promote without user confirmation

---

## Dual Commit in Product Form

The governance principle (AI proposes, human ratifies) becomes:

**AI Proposes:**
- "You've mentioned this person X times"
- "Your entries about X tend to be [positive/stressful]"
- "You haven't mentioned X in 3 months"

**Human Ratifies:**
- Confirms promotion to Named
- Accepts or dismisses insight
- Controls what the system remembers

**Neither Acts Alone:**
- System cannot create contacts without user action
- User cannot get insights without system pattern detection

---

## Insights (Future Feature)

Once relationships are tracked, journal can offer:

### Relationship Health
- "You've seen [friend] 3 times this month — that's more than usual"
- "Entries mentioning [coworker] have been more stressful lately"

### Connection Prompts
- "You haven't mentioned [old friend] in 6 months"
- "Last time you saw [family member] was [date]"

### Pattern Recognition
- "You tend to feel better after seeing [person]"
- "Meetings with [person] often come before stressful entries"

**All insights require user opt-in. Nothing surfaces without permission.**

---

## Technical Schema

### Reference Object (Layer 2)

```json
{
  "reference_id": "uuid",
  "reference_string": "work Sarah",
  "first_seen": "2026-01-04T09:00:00Z",
  "mention_count": 7,
  "contexts": ["work", "meeting", "lunch"],
  "emotional_valence": 0.6,
  "last_mentioned": "2026-01-04T09:00:00Z",
  "promotion_status": "eligible",
  "never_promote": false
}
```

### Contact Object (Layer 3)

```json
{
  "contact_id": "uuid",
  "display_name": "Sarah Chen",
  "reference_strings": ["work Sarah", "Sarah from marketing"],
  "relationship_type": "coworker",
  "created_at": "2026-01-04T09:00:00Z",
  "promoted_from": "reference_id",
  "mention_count": 12,
  "last_mentioned": "2026-01-04T09:00:00Z",
  "user_notes": "...",
  "category_signals": {
    "supportive": 0.3,
    "professional": 0.8,
    "stressful": 0.1
  }
}
```

---

## Proof of Concept

This schema is the product translation of Sean Campbell's personal tracking system, which has been running for 6+ months:

| Personal System | Product Feature |
|-----------------|-----------------|
| QRP anonymous counts | Unnamed mention aggregation |
| Reddit handle registry | Recognized reference tracking |
| Books of Life entries | Named contact profiles |
| Bob Gibson promotion chain | Full Layer 1→2→3 flow |
| Category taxonomy | Relationship health signals |
| Dual Commit governance | Promotion confirmation UX |

**The system works.** It has tracked real relationships across real platforms with real promotion events. This schema packages that proven architecture for consumer use.

---

## Connection to Governance

See: `governance/RELATIONSHIP_TRACKING_PROTOCOL.md` for the underlying governance model.

The protocol is the law. This schema is the implementation.

---

ΔΣ=42
