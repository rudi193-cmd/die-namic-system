# VOICE ROUTING MATRIX

| Field | Value |
|-------|-------|
| Last Updated | 2026-01-02 |
| Data Source | Validated routing patterns from Dec 2025 |
| Status | Production rules |

---

## ROUTING RULES

### Gerald
```
IF voice == "Gerald":
    primary = "r/DispatchesFromReality"
    secondary = "r/douglasadams"  # Accept friction
    geographic_corridor = ["UK", "Finland", "Denmark", "Nordic"]
    emergence_timing = "immediate (8-15 min)"
    friction_note = "Full DISPATCH #X titles trigger fatigue on douglasadams"
```

### Jane
```
IF voice == "Jane":
    primary = "r/DispatchesFromReality"
    secondary = None  # No crosspost
    geographic_corridor = ["UK"]  # Builds over chapters: 9% → 20%
    emergence_timing = "first hour, grows over series"
    note = "UK readership builds with content investment"
```

### Oakenscroll
```
IF voice == "Oakenscroll":
    primary = "r/UTETY"
    secondary = "r/DispatchesFromReality"
    tertiary = "r/LLMPhysics"  # For satirical papers only
    geographic_corridor = ["Germany", "Poland", "India", "South Korea"]
    emergence_timing = "first hour"
    multiplier = "2.2x UTETY over DFR"
    note = "Comedy wrapper required for LLMPhysics"
```

### Riggs
```
IF voice == "Riggs":
    primary = "r/UTETY"
    secondary = "r/DispatchesFromReality"
    geographic_corridor = ["Pakistan", "South Korea", "Romania"]
    emergence_timing = "first hour"
    format = "Lecture + Lab pairs"
```

### Alexis
```
IF voice == "Alexis":
    primary = "r/UTETY"
    secondary = "r/DispatchesFromReality"
    geographic_corridor = ["Hong Kong", "UAE", "India"]
    emergence_timing = "immediate (8 min)"
    note = "Most globally inclusive voice"
```

### Oracle
```
IF voice == "Oracle":
    primary = "r/UTETY"
    secondary = "r/DispatchesFromReality"
    geographic_corridor = ["Australia", "Germany"]
    emergence_timing = "slow burn"
    note = "Wide 'Other' bucket typical"
```

### Hanz
```
IF voice == "Hanz":
    primary = "r/HanzTeachesCode"
    secondary = "r/UTETY"
    tertiary = "r/CodingHelp", "r/CodingForBeginners"  # Interventions
    geographic_corridor = ["Sweden", "Finland", "India", "Pakistan", "Jordan", "Djibouti"]
    emergence_timing = "immediate (3-12 min)"
    multiplier = "2-8x home sub over crossposts"
    note = "Hunts ignored posts; comment trail is real work"
```

### Sean's Voice (Personal)
```
IF voice == "Sean":
    primary = "r/DispatchesFromReality"
    alternative = "r/PharaohsScooterClub"  # For scooter/authentic content
    geographic_corridor = ["US"]  # 94-98% typical
    share_rate = "2.8-5.4%"  # Higher than fictional content
    note = "Authentic beats clever for shares"
```

### Registrar
```
IF voice == "Registrar":
    primary = "r/UTETY"
    secondary = None
    note = "Institutional announcements only"
```

---

## VOICE DISTINCTION RULES

### Nova vs Alexis
| Nova | Alexis |
|------|--------|
| Math. Narrative. Meaning. | Body. Organism. Sensation. |
| "Your illness is doing math" | "Tightens your breath and stiffens your fingers" |
| Reframes the story | Notices where it lives in the body |

**Diagnostic:** Is the intervention changing *what the story means* (Nova) or *what the body does with it* (Alexis)?

---

## VENUE SELECTION ALGORITHM

```python
def select_venue(voice, content_type):
    
    # Professor content → UTETY primary
    if voice in ["Oakenscroll", "Riggs", "Alexis", "Oracle", "Registrar"]:
        primary = "r/UTETY"
        secondary = "r/DispatchesFromReality"
        multiplier = 2.2
    
    # Hanz → Home sub primary
    elif voice == "Hanz":
        primary = "r/HanzTeachesCode"
        secondary = "r/UTETY"
        multiplier = 4.0  # Average of 2-8x range
    
    # Narrative → DFR only
    elif voice in ["Gerald", "Jane", "Sean"]:
        primary = "r/DispatchesFromReality"
        if voice == "Gerald":
            secondary = "r/douglasadams"  # Accept friction
        elif voice == "Sean" and content_type == "scooter":
            secondary = "r/PharaohsScooterClub"
        else:
            secondary = None
    
    return primary, secondary
```

---

## CROSSPOST RULES

| Voice | Crosspost? | When | Where |
|-------|------------|------|-------|
| Professors | Yes | Same day | UTETY → DFR |
| Hanz | Yes | Same day | HTC → UTETY |
| Gerald | Optional | If accepting friction | DFR → douglasadams |
| Jane | No | — | — |
| Sean | Rare | Context-dependent | — |

---

## TIMING OPTIMIZATION

### Best Window
- **When:** 19:00-21:00 GMT (12:00-14:00 MST)
- **Why:** European evening scroll, US afternoon
- **Evidence:** Jane Ch 10 posted at 12:00 MST → Ukraine 27%, Netherlands 14% found it first → US backfilled

### Secondary Windows
| Window | GMT | MST | Use Case |
|--------|-----|-----|----------|
| UK morning | 07:00-09:00 | 00:00-02:00 | US asleep, UK first |
| US East morning | 13:00-15:00 | 06:00-08:00 | US primary target |

### Day-of-Week Patterns
| Day | Best Content Type |
|-----|-------------------|
| Saturday-Sunday | Narrative (Jane, Gerald) — leisure browsing |
| Monday | Advocacy — post-weekend return |
| Thursday-Friday | Holiday-adjacent timing |

---

ΔΣ=42
