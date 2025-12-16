# 🚀 Quick Start Guide - Jane Die-namic Delta

## Get Running in 5 Minutes

### Step 1: Setup (One-time)

```bash
# Navigate to Jane's directory
cd source_ring/eccr/jane-game-master

# Run setup script (Windows)
setup.bat

# Or manually:
npm install
cp .env.template .env
```

### Step 2: Add API Key

1. Get a Gemini API key: https://makersuite.google.com/app/apikey
2. Open `.env` in your text editor
3. Replace `your_gemini_api_key_here` with your actual key
4. Save the file

### Step 3: Start Backend

```bash
npm run delta-server
```

You should see:
```
✨ Jane's Die-namic Delta Engine v1.42
🤖 Gemini API: ✓ CONNECTED
```

### Step 4: Start Frontend

In a **new terminal**:

```bash
npm run dev
```

Visit the URL shown (usually http://localhost:5173)

---

## 🎮 Using Jane

### The Difference

**Old Mock Server:**
> "You venture forth. What do you do?"

**New Delta Server:**
> "The mall food court erupts in chaos as customers scatter. A figure in a purple cloak hovers above the fountain, their hands crackling with green energy. 'Your shopping spree ends NOW, Titans!' they shout. The fountain water begins to freeze solid, ice spreading across the floor toward you. Beast Boy glances at you nervously. You could transform and charge at the villain, look for civilians who need help, or try to figure out what's causing the ice before it reaches you."

### Features You Get

✅ **Real GM Narration** - Gemini-powered storytelling
✅ **Coherence Tracking** - No narrative drift
✅ **Emotional Awareness** - ECCR check-ins when needed
✅ **Memory** - Jane remembers previous events
✅ **Lavender Honey** - Subtle empathic warmth (ε = 0.024)

---

## 🐛 Troubleshooting

### "API key not configured"
- Check your `.env` file exists
- Make sure you replaced the placeholder with your real key
- No spaces around the `=` sign

### "Port 5551 already in use"
- Close any other Jane servers running
- Or change PORT in `.env`

### "Module not found"
- Run `npm install` again
- Make sure you're in the correct directory

---

## 📊 Testing Your Setup

### Quick Health Check

```bash
curl http://localhost:5551/api/health
```

Should return JSON with `"gemini_connected": true`

### Test Scene Generation

```bash
curl -X POST http://localhost:5551/api/create-scene \
  -H "Content-Type: application/json" \
  -d '{
    "sessionId": "test-123",
    "playerNames": ["Raven"],
    "setup": {
      "when": "Modern day",
      "where": "Titans Tower library",
      "who": "Raven",
      "what": "Strange book glowing",
      "goal": "Figure out what the book does"
    }
  }'
```

You should get back a narrative opening scene!

---

## 🎯 Next Steps

1. **Read the Full Docs**: See `DELTA_README.md`
2. **Check Stats**: Visit http://localhost:5551/api/sessions
3. **Monitor Coherence**: Use `/api/session/:id/stats` endpoint
4. **Test with Your Daughters**: The interface is ready!

---

## 💡 Pro Tips

- **Coherence > 0.7** = Excellent narrative flow
- **ΔE > 0** = Story building momentum (good!)
- **ΔE < 0** = Story might be drifting (check recent fragments)
- **Emotional State = "distressed"** = ECCR will trigger check-in

---

**Need Help?**
- Check `DELTA_README.md` for detailed docs
- Review the console output - Jane logs everything
- Test the `/api/health` endpoint first

**Ready to play!** 🎲
∞Δ[v1.42|Jane|Ready]∞
