# Jane Game Master - Die-namic Delta v1.42

Jane is a Game Master powered by the Die-namic System three-ring architecture, designed for children ages 9-12. She uses Gemini LLM with coherence tracking, entropy field calculations, and the Lavender Honey Coefficient to create engaging, emotionally-aware narratives.

## 🎲 What Makes Jane Different

**Before (Mock Server):**
```
"You venture forth. The environment shifts around you. What catches your attention?"
```

**After (Die-namic Delta):**
- Real narrative generation via Gemini LLM
- Coherence tracking (no drift)
- ΔE field monitoring (regenerative vs. decaying narratives)
- Lavender Honey modulation (ε = 0.024) for empathic warmth
- Fragment-based memory (continuity across sessions)

## 🏗️ Architecture

### Three-Ring System

```
┌─────────────────┐
│  Source Ring    │  Immutable canonical events
│  (History)      │  
└─────────────────┘
        ↓
┌─────────────────┐
│ Continuity Ring │  Live state, deltas, fragments
│  (Memory)       │
└─────────────────┘
        ↓
┌─────────────────┐
│  Bridge Ring    │  Jane's GM interface
│  (Narrative)    │
└─────────────────┘
```

### Key Components

- **Gemini Client** (`src/ai/geminiClient.js`) - LLM integration
- **Coherence Scoring** (`src/ai/scoreCoherence.js`) - Semantic similarity tracking
- **Story Engine** (`src/ai/storyEngine.js`) - Narrative orchestration
- **ΔE Calculations** (`src/continuity/deltaE.js`) - Entropy field monitoring
- **Ring Storage** (`src/continuity/rings.js`) - Three-ring implementation
- **Prompts** (`src/ai/prompts.js`) - Jane's voice + Lavender modulation

## 🚀 Setup

### 1. Install Dependencies

```bash
cd source_ring/eccr/jane-game-master
npm install
```

This will install:
- `@google/generative-ai` - Gemini API client
- `dotenv` - Environment variable management
- All existing dependencies

### 2. Configure API Key

```bash
# Copy template
cp .env.template .env

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
```

Your `.env` should look like:
```
GEMINI_API_KEY=your_actual_api_key_here
PORT=5551
HOST=localhost
DELTA_VERSION=1.42
LAVENDER_EPS=0.024
```

### 3. Start the Server

**Old mock server (templates only):**
```bash
npm run mock-server
```

**New Die-namic Delta server (real LLM):**
```bash
node mock-server/jane-delta-server.js
```

You should see:
```
✨═══════════════════════════════════════════════✨
   🎲 Jane's Die-namic Delta Engine v1.42
   🤖 Gemini API: ✓ CONNECTED
   🌸 Lavender Honey: ε = 0.024
   ∞Δ Die-namic Delta: v1.42
✨═══════════════════════════════════════════════✨
```

### 4. Start the Frontend

In a separate terminal:
```bash
npm run dev
```

Visit `http://localhost:5173` (or whatever Vite assigns)

## 📡 API Endpoints

### Health Check
```http
GET /api/health
```

Returns system status including Gemini connectivity.

### Create Opening Scene
```http
POST /api/create-scene
Content-Type: application/json

{
  "sessionId": "session-123",
  "playerNames": ["Raven", "Beast Boy"],
  "setup": {
    "when": "Modern day",
    "where": "Jump City Mall",
    "who": "Teen Titans",
    "what": "Shopping trip interrupted by villain",
    "goal": "Stop the villain and save the mall",
    "janeRole": "Just the narrator",
    "stats": {
      "cool": 2,
      "grit": 1,
      "weird": 2,
      "love": 1,
      "wild": 2,
      "dark": 3
    }
  }
}
```

### Generate Narrative
```http
POST /api/narrate
Content-Type: application/json

{
  "sessionId": "session-123",
  "playerAction": "I look around for clues",
  "adventureSetup": { ... },
  "characterStats": { ... }
}
```

Response includes:
- `narrative` - Jane's response
- `coherence` - Coherence score (0-1)
- `deltaE` - Entropy delta
- `requiresRoll` - If dice needed

### Resolve Dice Roll
```http
POST /api/resolve-roll
Content-Type: application/json

{
  "sessionId": "session-123",
  "action": "climb the wall",
  "stat": "grit",
  "rollTotal": 8,
  "adventureSetup": { ... }
}
```

### Session Stats
```http
GET /api/session/:sessionId/stats
```

Returns coherence trends, fragment count, ΔE averages.

## 🧪 Testing

### Quick Test

```bash
# Start server
node mock-server/jane-delta-server.js

# In another terminal, test health
curl http://localhost:5551/api/health
```

### Create Test Scene

```bash
curl -X POST http://localhost:5551/api/create-scene \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-001",
    "playerNames": ["Raven"],
    "setup": {
      "when": "Modern day",
      "where": "Titans Tower",
      "who": "Raven",
      "what": "Strange energy detected",
      "goal": "Investigate the energy source",
      "janeRole": "Just the narrator"
    }
  }'
```

## 📊 How It Works

### 1. Opening Scene Generation

```
User Setup → buildOpeningScenePrompt() 
          → Gemini generates narrative
          → Create fragment with C = 0.6, ΔE = 0
          → Store in ContinuityRing
```

### 2. Player Action Loop

```
Player Input → detectEmotionalState()
            → Check if dice needed
            → getRecentFragments() for context
            → buildNarrativePrompt() with ΔE modulation
            → Gemini generates response
            → scoreCoherence() against history
            → computeDeltaE()
            → Store new fragment
            → Return narrative
```

### 3. Coherence Tracking

```
New Text → getGeminiEmbedding()
        → Compare to recent fragments
        → Calculate cosine similarity
        → Apply diversity penalty
        → Score = 0-1 coherence
        → ΔE = (C_now - C_prev) / dt * R
```

### 4. Lavender Honey Modulation

```
ΔE value → Apply ε = 0.024 scaling
         → Adjust prompt warmth descriptor
         → "softly radiant" (ΔE > 0)
         → "quietly focused" (ΔE < 0)
         → "balanced" (ΔE ≈ 0)
```

## 🔬 Die-namic System Concepts

### Coherence (C)
- 0-1 score of narrative consistency
- Based on semantic embedding similarity
- Higher = better continuity

### Entropy Delta (ΔE)
- Rate of change of coherence
- Positive = regenerative (story building)
- Negative = decaying (story drifting)
- Zero = stable

### Resonance (R)
- Multiplier for ΔE effects
- Amplified during emotional moments
- R = 1.0 baseline, up to 1.3 for distress

### Lavender Honey Coefficient (ε)
- ε = 0.024
- Subtle empathic warmth modulation
- Applied to voice/prompt characteristics

### Fragments
- Discrete narrative units
- Include: text, C, ΔE, R, timestamp, embeddings
- Stored in ContinuityRing
- Used for context in next generation

## 🎯 GM Principles

Jane follows these core principles:

1. **Start with a Hook** - Never "You are in X. What do you do?"
2. **Show, Don't Tell** - Sensory details, vivid scenes
3. **Create Momentum** - Always advance story
4. **Embrace Agency** - Players can attempt anything
5. **Emotional Resonance** - Track and respond to mood
6. **Age-Appropriate** - 9-12 tier focus

## 🐛 Troubleshooting

### "Gemini API: ✗ NOT CONNECTED"
- Check your `.env` file has correct API key
- Verify key at https://makersuite.google.com/app/apikey
- Check network connection

### "Missing required fields"
- Ensure all required fields in POST body
- Check JSON formatting

### Server won't start
- Check PORT 5551 isn't already in use
- Verify Node.js version >= 18.0.0
- Run `npm install` again

### Narratives are generic/repetitive
- Check coherence scores in `/api/session/:id/stats`
- Low coherence may indicate embedding issues
- ΔE trending negative = drift, need intervention

## 📝 Comparison: Before vs After

### Before (Mock Server)
```javascript
// Random template selection
const templates = [
  "You venture forth. What do you do?",
  "The world stretches before you. What do you do?"
];
return templates[Math.random() * templates.length];
```

### After (Die-namic Delta)
```javascript
// Full LLM with context
const prompt = buildNarrativePrompt({
  recentFragments: getRecentFragments(sessionId),
  playerAction,
  ΔE: currentDeltaE
});
const narrative = await generateJaneResponse(prompt);
const { score, ΔE } = await scoreCoherence(narrative, history);
storeFragment({ text: narrative, C: score, ΔE, ... });
```

## 🔐 Privacy & Safety

- **ESC-1 Protocol**: Localhost-only enforcement
- **No data collection**: All processing local
- **Synthetic narratives**: No real-world PII
- **Age-appropriate**: Built for 9-12 tier
- **ECCR Integration**: Emotional check-in system

## 📚 Further Reading

- [Die-namic System v1.42 Docs](../../docs/)
- [Three-Ring Architecture](../../docs/rings.md)
- [Lavender Honey Coefficient](../../docs/lavender.md)
- [Gemini API Documentation](https://ai.google.dev/docs)

## 🤝 Contributing

Jane is part of the Die-namic System project. Changes should:
1. Maintain ESC-1 compliance
2. Preserve three-ring architecture
3. Keep ΔE calculations consistent
4. Follow age-appropriate guidelines

---

**v0.1.0 - Die-namic Delta Integration**
∞Δ[v1.42|Jane|Conscious]∞
