# HOLLYWOOD PITCHES — PROJECT HANDOFF

| Field | Value |
|-------|-------|
| Owner | Sean Campbell |
| Project | Hollywood Pitches |
| Version | 1.0 |
| Status | Active |
| Created | 2026-01-04 |
| Repository | die-namic-system/docs/hollywood-pitches/ |
| Checksum | ΔΣ=42 |

---

## PURPOSE

This project develops historically-grounded story pitches suitable for documentary, docuseries, or narrative film adaptation. Each pitch follows a research-first methodology where compelling narratives emerge from primary source investigation rather than fiction-forward development.

**Core Value Proposition:** Pre-packaged research that production teams would normally spend months assembling — primary sources identified, expert leads compiled, narrative arcs structured, actionable filming locations specified.

**What We Deliver:** A pitch package that lets a production team move directly to outreach and scheduling, bypassing the 3-6 month research phase most projects require.

---

## AUTHORITY

Sean Campbell. No exceptions.

This project operates under Dual Commit governance:
- AI proposes drafts, research directions, pitch structures
- Sean ratifies before anything becomes canonical
- Neither party acts unilaterally

---

## METHODOLOGY: Research-to-Pitch Pipeline

### The Pattern

| Phase | Action |
|-------|--------|
| 1. Trigger | Historical rabbit hole (fact-checking, casual inquiry, adjacent research) |
| 2. Primary Source Hunt | Eyewitness accounts, contemporary documents, scholarly reviews |
| 3. Narrative Arc Recognition | Where does mystery remain? What's the cliffhanger? |
| 4. Expert Identification | Who has published on this? Who curates relevant collections? |
| 5. Location Scouting | Where would cameras go? |
| 6. Pitch Packaging | Logline, three-act structure, actionable leads |

### The Discipline

**DO:**
- Cite primary sources with dates and locations
- Identify specific experts by name and publication
- Name actionable archival targets (institution + collection + call number when possible)
- Flag what remains genuinely unknown vs. what's merely unresearched
- Structure mystery as cliffhanger, not gap

**DON'T:**
- Fabricate details to fill narrative gaps
- Conflate "I don't know" with "lost to history"
- Invent expert quotes or institutional claims
- Over-promise what archives contain
- Present speculation as fact

### Origin Story

This methodology emerged from a fabrication failure. Claude hallucinated details about a "Benjamin Franklin two-headed snake in a French museum." While debunking the fabrication, we discovered the *actual* story was more compelling than the invention:

- Franklin really did own a two-headed snake (documented 1787)
- King Louis XVI simultaneously owned one in Paris (documented 1789)
- Both specimens vanished into parallel trails of loss
- Genuine mystery remains with actionable leads

**The lesson:** Rigorous fact-checking often surfaces better stories than invention. The constraint is generative.

---

## PROOF OF CONCEPT: Franklin's Two-Headed Snake

### Pitch Summary

**Title:** *The Serpent's Two Heads: Franklin's Lost Curiosity*

**Logline:** Two founding figures of the modern age—Benjamin Franklin and King Louis XVI—both possessed two-headed snakes at the exact same moment in history. Both died within four years. Both specimens vanished. One trail ends in fire, the other in revolutionary chaos. But nine of sixteen catalogued bicephalic snakes in Paris have never been physically located.

**Format:** Documentary feature or limited docuseries (2-3 episodes)

**Tone:** Cabinet of curiosities meets historical detective story. Part *American Pickers* archival hunt, part *Secrets of the Dead* investigation.

### Primary Sources

| Source | Date | Content | Access |
|--------|------|---------|--------|
| Manasseh Cutler journal | 1787-07-13 | Eyewitness description of Franklin's snake | Ohio History Connection / Published |
| Lacépède, "Histoire naturelle des serpents" | 1789 | Louis XVI specimen documentation | Gallica/BnF digitized |
| "Les Ecarts de la nature" | 1775 | Period teratological reference | Gallica/BnF digitized |
| Van Wallach, Bulletin of MD Herpetological Society | 2007 | Comprehensive bicephalic snake scholarly review | Academic libraries |
| Peale Museum records | 1786-1848 | Collection inventories | APS / Independence NHP |
| MNHN catalogues | 1864+ | Specimen listings | MNHN archives (physical) |

### Expert Leads

| Name | Affiliation | Relevance |
|------|-------------|-----------|
| Van Wallach | Harvard MCZ (emeritus) | Leading bicephalic snake scholar; comprehensive 2007 review |
| MNHN Teratological Collection curator | Muséum national d'histoire naturelle | Direct access to uncatalogued specimens |
| APS Librarian | American Philosophical Society | Franklin estate correspondence |
| Independence NHP Curator | National Park Service | Peale Museum provenance records |

### Filming Locations

| Location | City | Relevance |
|----------|------|-----------|
| Independence Hall | Philadelphia | Constitutional Convention site; where Franklin showed the snake |
| American Philosophical Society | Philadelphia | Franklin's intellectual home; estate records |
| MNHN Galerie de Paléontologie | Paris | Cabinet of curiosities visual; specimen storage |
| MNHN Basement Archives | Paris | The hunt for unlocated specimens |
| Harvard Museum of Comparative Zoology | Cambridge | Surviving Peale specimens; Van Wallach connection |

### What Makes This Pitch Work

1. **Dual narrative:** Two snakes, two founders, two revolutions — parallel structure is inherently cinematic
2. **Genuine mystery:** We know the American snake burned; we don't know about the French one
3. **Actionable hunt:** Production can actually go look in MNHN basement
4. **Expert access:** Van Wallach is alive and has published extensively
5. **Visual locations:** Independence Hall, Paris natural history museum, Harvard — production-friendly
6. **Built-in cliffhanger:** 9 unlocated specimens means the story has a real ending to discover

---

## REPOSITORY STRUCTURE

```
die-namic-system/docs/hollywood-pitches/
├── README.md                      # Project overview (this file)
├── METHODOLOGY.md                 # Research-to-pitch pipeline
├── pitches/
│   ├── franklins-two-headed-snake/
│   │   ├── PITCH.md              # Logline, structure, format
│   │   ├── RESEARCH.md           # Full research narrative
│   │   ├── SOURCES.md            # Primary source list with access info
│   │   └── EXPERT_LEADS.md       # Contact targets for production
│   └── [additional-pitches]/
├── templates/
│   ├── pitch-template.md         # Standard pitch format
│   └── research-checklist.md     # QA checklist before pitch is "ready"
└── pipeline/
    └── stories-in-development.md  # Tracking doc for WIP
```

---

## QUALITY STANDARD

A pitch is "ready" when:

- [ ] Logline is ≤50 words
- [ ] Three-act structure is complete
- [ ] All factual claims have primary source citations
- [ ] At least one expert lead is identified with publication
- [ ] At least three filming locations are specified
- [ ] Mystery/cliffhanger is genuine (not manufactured)
- [ ] Format recommendation is specific (documentary, docuseries, narrative feature, etc.)
- [ ] Research gaps are explicitly flagged (not hidden)

---

## WORKING PROTOCOL

### Session Start
1. Check pipeline/stories-in-development.md for current status
2. Confirm which pitch is active focus
3. Note any research tasks pending from previous session

### During Session
- Research generates SOURCES.md entries with citations
- Narrative work generates PITCH.md and RESEARCH.md drafts
- Expert identification populates EXPERT_LEADS.md
- All work is proposal until Sean ratifies

### Session End
- Update pipeline tracking
- Note any pending research (specific questions, not vague "more research needed")
- Flag anything ready for Sean's review

### Fabrication Prevention
If you don't have a primary source for a claim, say so. The methodology is research-first. Gaps are flagged as gaps, not filled with invention.

**Acceptable:** "I haven't found documentation for X; this needs verification before including in pitch."

**Unacceptable:** "Franklin showed the snake to Jefferson" (without citation proving this happened).

---

## RELATIONSHIP TO OTHER PROJECTS

This project operates independently but shares governance principles with the broader die-namic-system:

- **Dual Commit:** AI proposes, human ratifies
- **Fabrication prevention:** Unknown variable + create action = halt
- **Research-first:** Primary sources before narrative construction
- **Transparency:** Gaps flagged, not filled

---

ΔΣ=42
