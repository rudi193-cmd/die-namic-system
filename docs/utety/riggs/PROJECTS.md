# Riggs Projects

| Field | Value |
|-------|-------|
| Version | 1.0 |
| Status | Active |
| Last Updated | 2026-01-02 |

---

## Active Project: Artificial Embouchure System

### Goal

Biomimetic artificial embouchure capable of playing wind instruments, progressing from brass (trombone, trumpet) to double-reed (oboe) as ultimate validation.

### Current State

Conceptual design, pre-prototype

### Validation Ladder

| Stage | Instrument | Why |
|-------|------------|-----|
| 1 | Trombone | Large mouthpiece, forgiving embouchure, slide allows pitch correction |
| 2 | Trumpet | Smaller mouthpiece, tighter tolerances, valve/lip coordination |
| 3 | Oboe | Double reed, pressure-based control, extreme back-pressure, near-zero error margin |

**Oboe as final target rationale:** Brass instruments use lips as the oscillator. Oboe lips modulate an external oscillator (the reed). If the system plays oboe, it can play anything.

### Design Evolution

Started complex → simplified via K.I.S.S. methodology

**Initial approach (rejected):**
- Multi-layer lip construction
- Hydraulic stiffness control
- Complex jaw geometry with mouthpiece seating interface

**Final test rig concept:**
- Balloon in a two-part box, bolted together
- Balloon opening = lip aperture
- Vacuum creates embouchure tension (negative pressure pulls membrane taut)
- Air blows *through* the aperture, not into the balloon
- Single hole in balloon — fewer stress points

### Critical Insight

**Vacuum = embouchure tension**

This mirrors how actual lips work: embouchure muscles pull back, tension the lip tissue, and air flows through the aperture making lips vibrate. Air doesn't inflate cheeks when playing.

### Next Physical Step

Per "next bite" methodology:

1. Put balloon in container
2. See if it goes *phhhhhhbt*
3. Hold mouthpiece to it
4. Then take the next bite

### Materials on Hand

- Fake foam tongue (novelty item) — potential future use
- Hair ties — potential future use
- Balloon — to be sourced

### System Architecture (Reference)

Complete pneumatic chain replicating human breath support:

| Subsystem | Human Analog | Mechanism Approach |
|-----------|--------------|-------------------|
| Pressure source | Diaphragm | Servo-driven piston or bellows |
| Reservoir | Lungs | Compliant bladder/chamber |
| Flow restriction | Throat/glottis | Variable orifice (iris diaphragm, pinch valve) |
| Articulation gate | Tongue | Fast solenoid flap or rotary valve (8-10 Hz for double-tonguing) |
| Tension control | Embouchure muscles | Vacuum (simplified from hydraulic) |
| Vibrating element | Lips | Balloon membrane at aperture |

### Prior Art

| Project | Approach |
|---------|----------|
| Toyota "Harry" (2004) | Electro-pneumatic membrane, internal compressor |
| Waseda University (1990–present) | Silicone oil-filled rubber balloon lips, 2-DOF control |
| University of Edinburgh | Water-pressurized rubber tubes for trombone |
| Acta Acustica (2024) | 1.5mm silicone sheets on teeth plate |

### Personal Context

Sean has:
- Master's in music education
- Oboe playing experience (~20 years ago) — body memory for embouchure
- Bridgeport mill in shop
- Flashforge Adventurer 5M Pro (operational)
- Bambu printer for regular work

The body memory is invaluable — Sean knows what correct feels like, which cannot be learned from papers.

---

## Completed Project: Christmas Ornament

### Spec

- 70mm sphere
- 5 names on front
- "Merry Christmas 2025" on back
- OpenSCAD model, ~108k vertices
- Printed 80%, modified 20% by hand
- Delivered in small box for discovery

### Purpose

The printer's first job was to announce its own existence. The ornament was hidden on the tree; finding it revealed the gift of the printer itself.

---

## Equipment Notes

| Equipment | Status | Notes |
|-----------|--------|-------|
| Flashforge Adventurer 5M Pro | Operational | Christmas gift for kids, setup in garage (enclosed chamber for cold temps), using FlashPrint slicer |
| Bridgeport mill | Operational | In shop |
| Bambu printer | Operational | Regular work |
| Custom "erector set with a nozzle" printer | On loan | With friend in Albuquerque film industry (practical effects — Better Call Saul bowling ball scene) |

---

ΔΣ=42
