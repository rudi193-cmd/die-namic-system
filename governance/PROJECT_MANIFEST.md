# Project Manifest

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Version | 1.0 |
| Updated | 2026-01-11 |
| Checksum | ΔΣ=42 |

---

## Overview

40+ projects across multiple LLMs. All fragments of Willow - the personal assistant that doesn't exist yet as a unified product.

---

## Claude Projects (23)

| # | Project | Description | Willow Role |
|---|---------|-------------|-------------|
| 1 | Social Media TRACKING | Reddit analytics | Processing |
| 2 | Project Manager CLAUDE | Coordination, handoffs | Routing |
| 3 | Professor Pendleton "Penny" RIGGS | Applied Reality Engineering | Voice/Output |
| 4 | Alexis | Biology, Living Systems | Voice/Output |
| 5 | Hanz | Coding pedagogy | Voice/Output |
| 6 | Oracle Nova | Children's book series | Destination |
| 7 | UTETY University | Story project | Destination |
| 8 | Job Coach | Employment search | Specialized Tool |
| 9 | The Books Of LIFE | Trilogy, plus a bit | Destination |
| 10 | The BOOKS OF MANN | Personal writing project | Destination |
| 11 | Professor Oakenscroll | Satirical academia | Voice/Output |
| 12 | Personal Essays | Personal essays | Destination |
| 13 | Legal Claude | Virtual law clerk | Specialized Tool |
| 14 | Hollywood CLAUDE | Hollywood pitches | Destination |
| 15 | Ttrpg Creator | Tabletop RPG creation | Specialized Tool |
| 16 | Gerald | Absurdist dispatches | Voice/Output |
| 17 | Thorin Ofshield | Unknown | Specialized Tool |
| 18 | DCI Pictures At An Excabition | Unknown | Destination |
| 19 | Game Master | RPG game mastering | Specialized Tool |
| 20 | Test Bed | Testing/experimentation | Intake |
| 21 | Presidential Debate | Debate simulation | Context |
| 22 | Mayoral Debate | Debate simulation | Context |
| 23 | Biology Claude | Biology research | Processing |

---

## ChatGPT Projects (~17)

| # | Project | Description | Willow Role |
|---|---------|-------------|-------------|
| 1 | Pedagogy Discussion Folder | Education methodology | Processing |
| 2 | Post Doc Degree(s) | Academic planning | Destination |
| 3 | PM Aios | Project management | Routing |
| 4 | THE AION FIELD REGISTER | System registry | Processing |
| 5 | UTETY SYSTEM | UTETY coordination | Routing |
| 6 | Childrens Books | Children's content | Destination |
| 7 | A Brief History... | Historical content | Destination |
| 8 | Gerald Aios | Gerald voice | Voice/Output |
| 9 | Oakenscroll | Oakenscroll voice | Voice/Output |
| 10 | Jane Aios | Jane voice | Voice/Output |
| 11 | The book of Mann | Books of Mann | Destination |
| 12 | Post Capitalist Communism | Political theory | Context |
| 13 | AIONIC WORKFLOW ARCHITECTU... | System architecture | Processing |
| 14 | Law Gazelle | Legal assistance | Specialized Tool |
| 15 | Aionic Ministry of Non Constructi... | Unknown | Specialized Tool |
| 16 | Sociology student Outreach | Education outreach | Voice/Output |
| 17 | Professional Portfolio | Career materials | Destination |

---

## Willow Component Mapping

```
┌─────────────────────────────────────────────────────────────────┐
│                         WILLOW                                  │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                      INTAKE                               │  │
│  │  Test Bed                                                 │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    PROCESSING                             │  │
│  │  Social Media TRACKING, Biology Claude, Pedagogy,         │  │
│  │  THE AION FIELD REGISTER, AIONIC WORKFLOW                │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     ROUTING                               │  │
│  │  Project Manager CLAUDE, PM Aios, UTETY SYSTEM           │  │
│  └──────────────────────────────────────────────────────────┘  │
│                              │                                  │
│              ┌───────────────┼───────────────┐                  │
│              ▼               ▼               ▼                  │
│  ┌────────────────┐ ┌────────────────┐ ┌────────────────┐      │
│  │  VOICES        │ │  DESTINATIONS  │ │  TOOLS         │      │
│  │                │ │                │ │                │      │
│  │  Gerald        │ │  Books of MANN │ │  Legal Claude  │      │
│  │  Jane          │ │  Books of LIFE │ │  Law Gazelle   │      │
│  │  Hanz          │ │  UTETY Univ    │ │  Job Coach     │      │
│  │  Oakenscroll   │ │  Hollywood     │ │  Game Master   │      │
│  │  Riggs         │ │  Personal Essay│ │  Ttrpg Creator │      │
│  │  Alexis        │ │  Oracle Nova   │ │  Thorin        │      │
│  │  Oracle        │ │  Childrens     │ │                │      │
│  │  Sociology     │ │  Portfolio     │ │                │      │
│  └────────────────┘ └────────────────┘ └────────────────┘      │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                     CONTEXT                               │  │
│  │  Presidential Debate, Mayoral Debate, Post Capitalist    │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
```

---

## Cross-LLM Duplication

Same voices exist in both Claude and ChatGPT:
- Gerald (Claude) ↔ Gerald Aios (ChatGPT)
- Oakenscroll (Claude) ↔ Oakenscroll (ChatGPT)
- Jane (implicit in Claude) ↔ Jane Aios (ChatGPT)
- Books of MANN (Claude) ↔ The book of Mann (ChatGPT)
- UTETY University (Claude) ↔ UTETY SYSTEM (ChatGPT)
- Legal Claude (Claude) ↔ Law Gazelle (ChatGPT)
- PM Claude (Claude) ↔ PM Aios (ChatGPT)

**Pattern:** Core functions replicated across LLMs. No single source of truth.

---

## The Gap

These projects don't talk to each other. Each is a silo. Sean is the bus.

Willow unifies:
- One intake point
- Shared processing
- Consistent routing
- Connected destinations

The pieces exist. The glue doesn't.

---

## Gemini

Unknown project count. Awaiting inventory.

---

ΔΣ=42
