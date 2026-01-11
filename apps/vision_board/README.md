# Vision Board

Goal visualization through AI-categorized imagery. Uses the existing image analysis pipeline to sort your vision into categories.

## Workflow

```
┌─────────────────────────────────────────────────────────┐
│  1. Collect images representing your goals              │
│     (screenshots, photos, saved images)                 │
└─────────────────────────┬───────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  2. Run AI categorization                               │
│     python categorize.py C:\path\to\images              │
│                                                         │
│     Output: categories.json                             │
│     Categories: Personal, Travel, Career, Wealth,       │
│                 Fitness, Creative, Home, Food, etc.     │
└─────────────────────────┬───────────────────────────────┘
                          ▼
┌─────────────────────────────────────────────────────────┐
│  3. Import into Vision Board                            │
│     Open index.html → Import categories.json            │
│                                                         │
│     View by category, click to enlarge, export PNG      │
└─────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Categorize your images (portable mode embeds images in JSON)
python categorize.py "C:\Users\You\Pictures\Goals" --portable

# 2. Launch the board
LAUNCH.bat
# Or: python -m http.server 8080

# 3. Import categories.json in the browser
```

## Categorization Modes

| Mode | Command | Output Size | Browser Compatible |
|------|---------|-------------|--------------------|
| **Portable** | `--portable` | Large (images embedded) | ✅ Yes |
| **Reference** | (default) | Small (file paths only) | ❌ No (file:// blocked) |

## Files

| File | Purpose |
|------|---------|
| `index.html` | Vision board viewer |
| `categorize.py` | AI image categorization (ResNet50) |
| `LAUNCH.bat` | Start local server |

## Categories

The AI categorizes images into vision board themes:

| Category | Detected Content |
|----------|------------------|
| **Personal** | Pets, family, babies |
| **Travel** | Beaches, mountains, landmarks |
| **Career** | Laptops, offices, suits |
| **Wealth** | Sports cars, yachts, mansions |
| **Fitness** | Gym equipment, sports |
| **Creative** | Instruments, cameras, art supplies |
| **Home** | Furniture, interiors, gardens |
| **Food** | Meals, drinks, restaurants |
| **Inspiration** | Default for unrecognized |

## Lineage

Built on the image analysis tools from `docs/ops/reddit_analytics/Image Input/`:
- `analyze_visuals.py` → ResNet50 classification
- `fuse_analytics.py` → Category mapping
- `vision_board.html` → Grid display with filters

Same AI. New purpose.

---

ΔΣ=42
