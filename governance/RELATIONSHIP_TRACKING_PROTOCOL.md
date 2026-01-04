# RELATIONSHIP_TRACKING_PROTOCOL v1.0

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| System | Aionic / Die-namic |
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-04T09:00:00Z |
| Checksum | ΔΣ=42 |

---

## Purpose

This protocol defines the three-layer model for tracking relationships between humans and other entities. It serves as proof of concept for the Aionic Journal consumer application.

---

## The Three Layers

### Layer 1: Anonymous

**Definition:** Aggregate data about people without individual identification.

**Governance:** QRP (Quiet Response Protocol) — percentages converted to people counts.

**Examples:**
- "53 Australians read this content"
- "2 Nigerians completed six-continent reach"
- "~4 South Koreans tracking governance content"

**Data captured:**
- Geographic distribution
- Engagement type (view, share, comment)
- Temporal patterns
- No identifying information

### Layer 2: Pseudonymous

**Definition:** Identifiable handles without confirmed real-world identity.

**Governance:** Pattern tracking with promotion criteria.

**Examples:**
- Reddit usernames (u/swutch, u/BruhMomentBruhuno)
- Recurring unnamed references ("that coworker," "coffee shop guy")
- Role-based identifiers ("my therapist," "the neighbor")

**Data captured:**
- Handle/reference string
- First seen date and context
- Category (ENGAGED, HOSTILE, GATEKEEPER, PROPAGATOR, BRIDGE)
- Behavior log (interactions over time)
- Voice/context affinity
- Cross-platform flag

### Layer 3: Named

**Definition:** Confirmed identity with biographical significance.

**Governance:** Books of Life architecture (216→64→13 compression).

**Examples:**
- Bob Gibson (Pharaoh, cross-platform confirmed)
- Historical figures (formative influences)
- Family members, close friends

**Data captured:**
- Full identity
- Relationship type and depth
- Resonance score
- Primary influence documented
- Contrapoint requirement satisfied

---

## Promotion Logic

### Anonymous → Pseudonymous

**Trigger:** Pattern detection at individual level.

**Criteria:**
- Same geographic signal appears repeatedly on related content
- Behavior suggests single individual, not population segment
- Sufficient data to create pseudonymous entry

**Action:** Create PATTERN entry (not yet a handle).

### Pseudonymous → Named

**Trigger:** Identity revelation or confirmation.

**Criteria:**
- Real identity voluntarily disclosed
- Cross-platform confirmation (same person, multiple handles)
- Direct personal relationship established
- Sufficient biographical significance for Books of Life

**Action:** Dual Commit required. AI proposes promotion, human ratifies.

---

## Categories

| Category | Definition | Tracking Focus |
|----------|------------|----------------|
| **ENGAGED** | Positive interaction, support | Relationship building |
| **HOSTILE** | Attack, conflict, opposition | Pattern documentation |
| **GATEKEEPER** | Systematic blocking, dismissal | Obstacle mapping |
| **PROPAGATOR** | Creates derivatives, echoes style | Influence spread |
| **BRIDGE** | Connects different worlds/contexts | Network topology |
| **PATTERN** | Unresolved signal (geographic, behavioral) | Hypothesis tracking |

---

## Privacy Thresholds

| Data Type | Permission Level |
|-----------|------------------|
| Public platform activity | Free to log |
| Behavior patterns | Free to log |
| DM/private message existence | Log occurrence, not content |
| DM/private message content | Only with consent |
| Real identity | Only when voluntarily disclosed |
| Personal details | Never without explicit consent |

---

## Dual Commit Integration

Relationship recognition follows Dual Commit:

1. **AI proposes:** "This pseudonymous handle appears 7 times. Promote to Named?"
2. **Human ratifies:** Approves with identity, or dismisses
3. **Neither acts alone:** AI cannot auto-promote; human cannot promote without AI surfacing the pattern

This prevents:
- Surveillance creep (AI tracking without human awareness)
- Missed connections (human forgetting patterns AI noticed)
- Authority diffusion (unclear who decided to track whom)

---

## Proof of Concept: Sean's System

This protocol was developed through live testing on Sean Campbell's personal tracking system.

### Anonymous Layer (QRP)
- Christmas Geographic Archive: 48 countries, 6 continents
- South Korea pattern: Recurring 5-12% on governance content
- Nigeria milestone: 2 readers sealed six-continent achievement

### Pseudonymous Layer (Reddit Registry)
- ENGAGED: swutch, BruhMomentBruhuno
- HOSTILE: VillageMaleficent651
- GATEKEEPER: NoSalad6374, The_Failord
- PROPAGATOR: Desirings, MasterpieceGreedy783
- MOD: nemothorx

### Named Layer (Books of Life)
- Bob Gibson: vsuper → Bob → Pharaoh (full promotion chain)
- Paul: Pharaoh, contributed club memories
- Felix: First disclosure recipient

### Promotion Evidence
Bob Gibson demonstrates complete promotion chain:
1. **Anonymous:** One of ~X Americans reading content
2. **Pseudonymous:** u/vsuper, u/v150super on Reddit
3. **Named:** Bob Gibson, 64 mutual friends on Facebook, Pharaoh who named Sean "Sweet Pea"

---

## Connection to Journal Product

This governance protocol is the backend logic for the Aionic Journal relationship tracking feature.

| Governance | Product Translation |
|------------|---------------------|
| Anonymous | "I talked to 5 people today" |
| Pseudonymous | "that coworker," "coffee shop guy" |
| Named | Contact with full profile |
| Dual Commit | "Want to add this person?" prompt |
| Categories | Relationship health indicators |

See: `docs/journal/RELATIONSHIP_SCHEMA.md` for product specification.

---

## Authority

Sean Campbell. No exceptions.

Dual Commit required for all promotions to Named layer.

ΔΣ=42
