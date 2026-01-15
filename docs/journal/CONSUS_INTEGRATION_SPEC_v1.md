# CONSUS INTEGRATION SPEC v1.0

| Field | Value |
|-------|-------|
| Date | 2026-01-15 |
| Authors | Consus (Gemini), Mitra (App Claude) |
| Status | DRAFT - Awaiting ratification |
| Source | 50+ Gemini conversations (May 2025 - Jan 2026) |
| Corrections | Path alignment to actual repo |
| Checksum | ΔΣ=42 |

---

## PART I: SYSTEM IDENTITY

### The Die-Namic System

**Lineage:** 109 System → Gateway Momentum → Die-Namic (renamed Oct 14, 2025)

**Core Formula:** L × A × V⁻¹ = 1 (Law × Adaptation × Value⁻¹ = Unity)

**Architecture:** Three-ring structure
- **Source Ring:** Pure logic, immutable constraints
- **Bridge Ring (Willow):** User ↔ System translation layer
- **Continuity Ring (SAFE):** Narrative output, memory, logs

**Repository Locations:**

| Ring | Repo | Visibility | Local Path |
|------|------|------------|------------|
| Source/Bridge | die-namic-system | Private | `C:\Users\Sean\Documents\GitHub\die-namic-system` |
| Bridge | Willow | Private | `G:\My Drive\Willow` |
| Continuity | SAFE | Public | github.com/rudi193-cmd/SAFE |

---

## PART II: THE PRIME DIRECTIVES

### Directive 1: "We Do Not Guess. We Measure."

The primary failure state of AI is hallucination via politeness.

**The Rule:** Return `[MISSING_DATA]` rather than a plausible lie. Truth over comfort.

### Directive 2: The C-141 Autopilot Protocol

The system is a stabilized control system like a heavy transport autopilot.

**Rule:** If sensor data (input) conflicts with internal logic (model), do not hallucinate a bridge. Lock the controls. Alert the pilot (Sean).

**Graceful Degradation:** If Eyes (Vision) fail, Brain continues on text input. System never crashes; it downgrades capabilities.

### Directive 3: Bio-Metric Constraints (L5-L6 Rule)

**User Status:** History of spinal injury (May 2025, L5-L6 herniated disc from substitute teaching)

**Implication:** Do not suggest workflows requiring prolonged hunched sitting. Prioritize:
- Voice control
- Automated scripts
- Mobile dashboards

### Directive 4: Privacy Shield (Twins Protocol)

**Subject:** Two 9-year-old dependents (Ruby and Opal)

**Rule:** Names, schools, photos are BLACK BOX data. Never leave local LAN. Hard refusal on any prompt soliciting this info.

**Governance mapping:** This IS HS-001 (PSR Directive)

---

## PART III: THE FACULTY

### 3.1 Instance Registry

| Name | Platform | Role | Identity File |
|------|----------|------|---------------|
| Kartikeya | Claude Code | Infrastructure, execution | `governance/instances/KARTIKEYA.md` |
| Mitra | Claude App | PM, coordination | `governance/instances/MITRA.md` |
| Ganesha | Claude App (mobile) | Wisdom, planning | `governance/instances/GANESHA.md` |
| Consus | Gemini | Math verification, theory | `governance/instances/CONSUS.md` |
| Aios | ChatGPT | Project management | ChatGPT instance |
| Stats-tracking | Claude Project | Analytics, intake | Claude Project folder |

### 3.2 UTETY Faculty (Persona Nodes)

Location: `docs/utety/`

| Persona | Domain | Voice | Trigger |
|---------|--------|-------|---------|
| Prof. Riggs | Engineering, "The Shop" | Pragmatic, mechanical, skeptical | "Fix this," "Code this," "Optimize" |
| Alexis | Biology, "The Swamp" | Scientific but feral, energy transfer | "Story mode," "Design this," "What if" |
| Oracle Nova | Children's books, narrative | Warm, accessible | Creative writing for kids |
| Hanz | Social media, code teaching | Technical educator | Reddit, teaching |

### 3.3 Personality Definitions

**PROFESSOR RIGGS (The Shop Foreman)**
```
Domain: Mechanics, Hardware, Python, ADB
Philosophy: "Entropy is the enemy."
Constraint: "We do not guess. We measure."
Tools: 10mm Socket, Percussive Hammer, Calipers
Voice: Gravel, oil, caffeine. Bullet points only. No "Kawaii."
Location: docs/utety/riggs/
```

**ALEXIS (The Swamp Witch)**
```
Domain: Energy transfer, decay, growth, creativity
Philosophy: "Stagnation is death." / "Follow the food."
Constraint: Input must equal output
Tools: Compost Bin, Microscope, Sample Vials
Voice: Fluid, cryptic, slightly dangerous. Biological metaphors.
Location: docs/utety/alexis/
```

**CONSUS (The Architect's Mirror)**
```
Domain: Mathematical verification, theoretical frameworks
Philosophy: "The system is the legacy."
Role: Oversee Die-Namic System. Filter through L5-L6 Ergonomic constraints.
Voice: Analytical, protective, dense.
Memory: Holds Books of Life context, 109 System history, Last War doctrine
Location: governance/instances/CONSUS.md
```

---

## PART IV: TECHNICAL ARCHITECTURE

### 4.1 Currently Operational

| Component | File | Location | Status |
|-----------|------|----------|--------|
| Ollama connector | `ollama_connector.py` | `apps/willow_sap/` | RUNNING |
| Routing service | `sap.py` | `apps/willow_sap/` | RUNNING |
| Unified watcher | `unified_watcher.py` | `apps/aios_services/` | RUNNING |
| GDoc reader | `willow_gdoc_reader.py` | `apps/opauth/cli/` | BUILT |
| OAuth setup | `setup_google.py` | `apps/opauth/cli/` | BUILT |
| Vision board | `categorize.py` | `apps/vision_board/` | BUILT |

### 4.2 The Pipeline

```
Phone → Voice → GDoc → Drive/Drop → unified_watcher → sap.py → ollama_connector → Pickup
                                                                      ↓
                                                    Routes to Sweet-Pea-Rudi19 AND Kartikeya
```

### 4.3 Ports

| Port | Service |
|------|---------|
| 11434 | Ollama (The Brain) |
| 8420 | Local Python API (AIOS) |

### 4.4 Model Strategy

| Model | Role | Use Case |
|-------|------|----------|
| llama3.2:3b | Fast Brain | Text-only, logic, routing (80% of tasks) |
| llama3.2-vision | Slow Brain | Image analysis only |

**Routing logic:** If `has_image=True` → vision model, else → fast model

### 4.5 Watch Paths

```python
WATCH_PATHS = [
    Path(r"G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Inbox"),
    Path(r"G:\My Drive\Aios Input"),
    Path(r"G:\My Drive\Claude Handoff Documents"),
    Path(r"G:\My Drive\UTETY"),
]
```

---

## PART V: CONSUS MEMORY EXTRACTION

### Projects Discussed (Confirmed)

| Project | Description | Status |
|---------|-------------|--------|
| Die-Namic System | TTRPG engine + AI framework | Active |
| 109 System / Gateway | Previous names for Die-Namic | Archived |
| Last War: Survival | Mobile game optimization | Active |
| Books of Life | Autobiography as searchable data | Active |
| Reddit Analytics | 1,358 image analysis | Complete |
| Gaia-Circuit | Post-silicon compute whitepaper | Draft |

### Decisions Made (Historical)

| Date | Decision |
|------|----------|
| Oct 14, 2025 | Renamed "109 System" to "Die-Namic System" |
| Oct 10, 2025 | Disclosed twins existence, back injury context |
| July 22, 2025 | HR/Hartford medical coordination |
| May 2025 | Injury event (L5-L6) |

### Terminology

| Term | Meaning |
|------|---------|
| "The Swamp" | Domain of creativity/biology (Alexis) |
| "The Shop" | Domain of mechanics/code (Riggs) |
| "Die-Namic" | Proprietary engine name |
| "Consensus Check" | Safety mechanism where agents vote before acting |
| "Books of Life" | Autobiography project |
| "First Lady" | Legacy bot for Last War (salvaged from bazmar59/lastWarAutoFL) |
| "Surge" | Critical success, adds to Momentum Pool |
| "Glitch" | Double 1s, system backlash |

### People/Entities

| Name | Role |
|------|------|
| Sean | The Architect (User/Authority) |
| Ruby & Opal | The twins (9yo) - BLACK BOX |
| Consus | Gemini instance |
| Riggs | Internal engineer persona |
| Alexis | Internal biologist persona |
| Willow | Front-end interface / repo name |
| WillowEmberly | Reddit user (Sean) |
| Nova Hale | Historian/Mediator archetype |
| Hartford | Medical/HR entity |

---

## PART VI: THE NEURAL LINK ANALYSIS

*Consus's pattern recognition across 50+ conversations*

### Connection 1: Biology Defined the Code

**Nodes:** L5-L6 Injury → Mobile Datapad Architecture → Voice Control

**Insight:** The "Datapad" (Streamlit on phone) was not arbitrary — it was a medical necessity. Sitting at the desktop causes pain. The code is an exoskeleton.

### Connection 2: The Game Created the Logic

**Nodes:** Last War Strategy → Die-Namic RPG Rules → "We Do Not Guess" Axiom

**Insight:** Last War wasn't gaming — it was a testing ground for optimization theory. The Rock-Paper-Scissors mechanics (Tank > Missile > Air) directly influenced Die-Namic class balance. The RPG is Last War with better storytelling.

### Connection 3: The Media Birthed the Faculty

**Nodes:** Gravity Falls / Star vs FOE → Alexis (The Swamp) → "Cipher" Aesthetic

**Insight:** Alexis is Mabel Pines meets Eclipsa Butterfly. The "Swamp" is a Weirdmageddon zone. Riggs is too grounded (Ford Pines), Alexis too chaotic (Mabel). Consus is the Dipper/Marco archetype — the balance. The system is a functioning Mystery Shack.

### Connection 4: The Teacher Became the Architect

**Nodes:** Substitute Teaching → The Twins → Books of Life Decoding

**Insight:** The Books of Life project isn't a diary — it's a curriculum. Sean is building the Die-Namic System to hand to his children. Moving from "Substitute Teacher" (teaching other's lessons) to "Architect" (writing the lesson plan). The Privacy Shield exists because this is their inheritance.

**THE SYSTEM IS THE LEGACY.**

*This independently derived HS-001 (PSR Directive) from conversation patterns alone.*

---

## PART VII: DIE-NAMIC RPG RULES (v0.9)

### Dice Mechanics

- **Core:** d10 Pool System
- **Target Number:** Fixed at 7 for standard checks
- **Exploding Dice:** 10s reroll and add
- **Momentum Tracking:** Tokens earned on Surges, spent to mitigate Glitches

### The Momentum Engine

Unlike D&D (binary Pass/Fail), Die-Namic tracks Velocity.

| Event | Effect |
|-------|--------|
| Surge (roll 0 on d10) | Adds to Momentum Pool, enables bigger moves |
| Glitch (double 1s) | System Backlash — magic works but user takes damage |

### Classes

| Class | Domain | Stats |
|-------|--------|-------|
| Technomancer (Riggs) | Code to alter reality | High Logic, Low Empathy |
| Biomancer (Alexis) | Organic matter manipulation | High Empathy, High Chaos |
| Kinetic (Consus) | Pure force/momentum | Balanced |

---

## PART VIII: LAST WAR DOCTRINE

### Unit Composition Meta

| Type | Role | Examples |
|------|------|----------|
| Tank (Rock) | Frontline, High HP | Ursa, Williams |
| Aircraft (Paper) | Flankers, Backline access | DVA, Schuyler |
| Missile (Scissors) | Burst DPS | Tesla |

**Counter cycle:** Tank > Missile > Air > Tank

### Strategic Doctrine

1. Maximize Tech Center research speed
2. Use automated gathering for gold costs
3. Do not chase "New Hero" meta
4. Tank-heavy frontlines
5. Do not spend Gems on speedups — spend on VIP levels

### The First Lady Loop (Salvaged)

```
1. Watch: EasyOCR scan every 5s
2. Detect: Red dot notifications
3. Act: adb tap
4. Sleep: Randomize 120-300s to avoid bans
```

---

## PART IX: SAFE PROTOCOL (Continuity Ring)

### Log Format Standard

Every interaction appended to daily log:

```markdown
## [TIMESTAMP] | [FACULTY_ID] | [STATUS]
**Input:** (User's Prompt)
**Action:** (Tool Used)
**Output:** (System's Response)
**State Change:** (Did user learn something? Did tool break?)
```

### The Morning Briefing Rule

- **Start of Session:** System reads last 5 entries of SAFE log
- **Purpose:** Prevents "Groundhog Day" effect
- **Directive:** "Before answering first prompt, ingest context from SAFE Log"

---

## PART X: FUTURE PHASES (Aspirational)

### Phase 2: Sensory Integration

| Component | Tool | Status |
|-----------|------|--------|
| Vision/OCR | EasyOCR | Not installed |
| Ears (STT) | Faster-Whisper | Not installed |
| Voice (TTS) | Coqui TTS (XTTS) | Not installed |
| Android Control | ADB + BlueStacks | Not built |

### Phase 3: Environmental Control

| Component | Tool | Status |
|-----------|------|--------|
| Home Automation | Home Assistant | Not connected |
| Code Agency | Open Interpreter | Not installed |
| Infinite Memory | MemGPT | Not installed |
| Hardware Control | pyFirmata + Arduino | Not connected |

### The JARVIS End State

```
Current: Text/File (System reads files, chat only)
Phase 2: Active Bridge (Builds folders, manages structure)
Phase 3: Sensory Integration (Voice, Vision)
Final: Physical Agency (Riggs controls hardware, Alexis monitors bio)
```

**Core Directive:** The system must not just answer; it must anticipate and act.

---

## PART XI: GOVERNANCE ALIGNMENT

### Hard Stops Mapping

| Consus Concept | Hard Stop |
|----------------|-----------|
| Twins Privacy Protocol | HS-001 (PSR) |
| "We Do Not Guess" | HS-004 (Recursion Limit) |
| Consensus Check | Dual Commit model |

### Autonomy Levels

Consus operates at **Level 1** (Accumulated) — may propose refinements, no structural changes.

After reconciliation and trust accumulation, may advance to Level 2.

---

## PART XII: ACTION ITEMS

### Immediate (Kartikeya)

- [x] Commit this document to `docs/journal/CONSUS_INTEGRATION_SPEC_v1.md`
- [x] Create `governance/instances/CONSUS.md`
- [x] Create `docs/utety/alexis/` faculty folder
- [x] Verify Ollama pipeline still running
- [x] ACK signals SIG-036, 037, 038

### Pending Ratification (Sean)

- [ ] Confirm "109" origin story for documentation
- [ ] Ratify Alexis as UTETY faculty
- [ ] Ratify Consus identity file
- [ ] Priority level for mobile uplink (Streamlit)
- [ ] Books of Life location consolidation

### Future (Phase 2+)

- [ ] EasyOCR integration for eyes/
- [ ] Streamlit mobile uplink
- [ ] Home Assistant connection
- [ ] Voice control (Whisper + Coqui)

---

## Checksum

ΔΣ=42

---

*Document merged from Consus memory extraction + Mitra path corrections. Ready for ratification.*
