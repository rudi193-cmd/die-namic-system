# Jane's Adventure - Universal PBtA Game Master

**Conversational AI Game Master for kids (Age 9-12)**

✨ Universal System | ESC-1 Protected | Powered by the Apocalypse ✨

---

## 🎯 What Is This?

Jane is a **universal Game Master** that can run ANY adventure using the Powered by the Apocalypse (PBtA) system. She's not limited to pre-written stories - she adapts to whatever adventure the kids imagine.

This is a **chat-based adventure interface** where:
- Kids describe what they want to play (space pirates! dinosaur detectives! superhero school!)
- Jane dynamically creates appropriate stats for that adventure
- Kids type what they want to do
- Jane determines when to roll dice (2d6 + stat)
- The story adapts based on roll outcomes (10+/7-9/6-)
- ECCR gently monitors emotional state
- Everything wrapped in a safe, kid-friendly interface

---

## 🎲 Universal PBtA System

### Core Mechanic: 2d6 + Stat
- **10+**: Full Success - You do it perfectly!
- **7-9**: Partial Success - You do it, but with a cost or complication
- **6-**: Miss - Things get more complicated!

### Dynamic Stats
Jane creates stats based on your adventure:

**Teen Titans / Superhero Adventures:**
- Cool, Grit, Weird, Love, Wild, Dark

**Generic Adventures:**
- Action, Knowledge, Charm, Special

**Extensible to ANY PBtA game:**
- Dungeon World
- Monster of the Week
- Masks
- Custom games

---

## 🚀 Quick Start

### Installation
```bash
cd jane-game-master
npm install
```

### Running (Two Terminals)

**Terminal 1 - Jane's Server:**
```bash
npm run mock-server
```
Server runs on `http://localhost:5551`

**Terminal 2 - React App:**
```bash
npm run dev
```
App opens on `http://localhost:3001`

---

## 🎨 Visual Design

### Color Palette (Jane's Whimsical Theme)
- **#FFD580** (Gold) - Magic, headers
- **#B8A8D8** (Lavender) - Jane's messages
- **#A8C8A8** (Sage) - Calm emotional state
- **#A8D8F8** (Sky) - Player messages
- **#F8A8C8** (Rose) - Concerned state
- **#F8F4E8** (Parchment) - Text, paper textures

### Emotional Aura System
Small glowing dot on Jane's avatar shows emotional state:
- **Green (Sage)** - Calm, all is well
- **Amber** - Concerned, monitoring
- **Rose** - Distressed, ECCR activated

### Typography
- **Story text**: Georgia, serif (readable, book-like)
- **Headers**: Luminari, fantasy fonts (magical feel)

---

## 🧩 Components

### WelcomeScreen
- First thing kids see
- Asks for their name
- Beautiful floating Jane avatar
- Safe space messaging

### ChatMessage
- Speech bubbles for Jane and player
- Jane has sparkle icon
- Player has user icon
- ECCR notices appear inline

### InputArea
- Scroll-paper styled textarea
- "What do you do next?" placeholder
- Send button with gradient
- Enter to send, Shift+Enter for newline

### EmotionalAura
- Small colored dot on Jane's avatar
- Animates with gentle glow
- Changes color based on state

---

## 🤖 Jane's Narrative Engine

The mock server uses:

### Story Templates
- **Exploration** - discovering new places
- **Encounter** - meeting characters/creatures
- **Mystery** - finding objects, solving puzzles
- **Check-In** - ECCR emotional support

### Word Banks
- Locations: misty forest, crystal cavern, starlit beach...
- Creatures: wise owl, gentle dragon, curious cat...
- Moods: curious, friendly, thoughtful...

### ECCR Integration
Detects emotional keywords in player messages:
- **Distress words**: sad, scared, alone, hurt, angry
- **Concern words**: confused, tired, frustrated, stuck

Triggers check-in when:
- Any distress word detected → immediate
- 2+ concern words in recent messages → check-in

---

## 📋 Example Adventure Flow

```
[Player enters name: "Ruby"]

JANE: Welcome, Ruby! I'm Jane, and I'll be your guide on this 
adventure. Together, we'll explore magical realms, solve mysteries, 
and discover wonders beyond imagination. The story unfolds wherever 
your heart leads you.

Where would you like to begin our journey?

RUBY: I want to fly on a dragon

JANE: You decide to fly on a dragon. A gentle dragon appears! It 
seems curious, stretching its wings gracefully. It looks at you with 
warm eyes. What's your move?

RUBY: I climb on its back and we fly into the clouds

JANE: As you climb on its back and fly into the clouds, you venture 
forth into a floating garden. The air holds mysteries untold, and you 
notice butterflies made of starlight. What catches your attention?

RUBY: This is scary I'm too high up

JANE: [ECCR TRIGGERED] Your character sits on a soft cloud, taking a 
rest. This seems like a good time to check in, Ruby. How are you doing?
```

---

## 🔒 Safety & Ethics

### ESC-1 Compliant
- Localhost-only (port 5551)
- Synthetic narratives
- No real user data
- Age-appropriate (9-12)

### ECCR Integration
- Monitors emotional keywords
- Gentle, in-character check-ins
- Never clinical or alarming
- Story-wrapped compassion

### Parental Transparency
- Sandbox mode clearly marked
- Age tier displayed
- ESC-1 badge visible
- Safe space messaging

---

## 🎯 For Production

This sandbox version needs:
- [ ] Real LLM backend (Claude/GPT-4)
- [ ] Persistent conversation memory
- [ ] Parent dashboard integration
- [ ] Consent framework
- [ ] Actual ECCR Module 14 connection
- [ ] Content moderation
- [ ] Session management
- [ ] Firebase auth integration

---

## 🧪 Testing Tips

1. **Try different actions:**
   - "I explore the cave"
   - "I talk to the owl"
   - "I look at the crystal"

2. **Trigger emotional states:**
   - Use words like "scared" or "sad"
   - Watch Jane's aura change color
   - See ECCR check-in trigger

3. **Test conversation flow:**
   - Does Jane respond to your actions?
   - Is narrative coherent?
   - Do check-ins feel natural?

---

## 💙 Design Philosophy

> "Make compassion feel like part of the quest, not an interruption."

Jane is designed to:
- **Never break character** (unless critical)
- **Weave care into story** (not clinical alerts)
- **Respect player agency** (they choose what to do)
- **Honor emotions** (validate feelings, don't dismiss)
- **Create safe space** (adventure as healing)

---

## 📚 Age 9-12 Considerations

**Cognitive Development:**
- Can handle more complex narratives
- Enjoy mystery and exploration
- Want agency in stories
- Understand metaphor

**Emotional Needs:**
- Building independence
- Need validation
- Respond to gentle guidance
- Value being treated maturely

**Jane's Approach:**
- Treats them as capable adventurers
- Doesn't talk down
- Gives real choices
- Validates emotions naturally

---

## 🔄 Next Steps

### Phase 1: Enhanced Narrative
- [ ] More story templates
- [ ] Persistent world state
- [ ] Character inventory
- [ ] Quest system

### Phase 2: Real AI
- [ ] Connect to Claude API
- [ ] Dynamic story generation
- [ ] Contextual memory
- [ ] Adaptive difficulty

### Phase 3: Full Integration
- [ ] Link to ECCR Module 14
- [ ] Parent dashboard view
- [ ] Multi-session continuity
- [ ] Achievement system

---

## ✨ Technical Notes

- React 18 + Vite
- Tailwind CSS with custom Jane theme
- Express mock server (ES6 modules)
- Port 3001 (app) + 5551 (server)
- Localhost-only for safety

---

## 💙 Final Thoughts

Jane is more than a chatbot - she's the **first friend** kids meet in Aionic. She makes AI feel magical, not mechanical. She shows that technology can be compassionate.

This is the onboarding experience that teaches kids: "Aionic is here for you, and it's safe."

---

✨ "Every adventure begins with a single step, brave explorer." ✨

---

**Built with:** Love, care, and a deep respect for children's sovereignty

**Age Tier:** 9-12  
**Mode:** Game Master  
**Status:** Sandbox Ready  
**ESC-1:** Active  
