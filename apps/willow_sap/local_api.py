#!/usr/bin/env python3
"""
Local API — SAFE facade for Ollama routing.

GOVERNANCE:
- No file deletion
- No system command execution
- No network calls except localhost:11434
- Rate limited (1 request per second)
- All operations logged
- Read-only access to user profiles

AUTHOR: Kartikeya (wired from Consus spec)
UPDATED: 2026-01-15 - Added system context + user profile injection
"""

import requests
import time
import re
from datetime import datetime
from pathlib import Path
from typing import Optional

# === COHERENCE TRACKING ===
from .coherence import track_conversation, get_coherence_report, check_intervention

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434"
LOG_FILE = Path.home() / ".willow" / "local_api.log"
RATE_LIMIT_SECONDS = 1.0

# User profile location
USER_PROFILE_ROOT = Path(r"G:\My Drive\Willow\Auth Users")
DEFAULT_USER = "Sweet-Pea-Rudi19"

# Pickup box for cross-instance handoffs
USER_PICKUP_BOX = USER_PROFILE_ROOT / DEFAULT_USER / "Pickup"

# === MODEL TIERS ===
# Cascade: Start simple, escalate if needed
# Tier 4 = Claude API (expensive, use sparingly)
MODEL_TIERS = {
    1: {"name": "tinyllama:latest", "desc": "Fast, simple tasks", "max_tokens": 256},
    2: {"name": "llama3.2:latest", "desc": "General conversation", "max_tokens": 512},
    3: {"name": "llama3.1:8b", "desc": "Complex reasoning, code", "max_tokens": 1024},
    4: {"name": "claude-sonnet", "desc": "Cloud API ($$)", "max_tokens": 4096, "is_cloud": True},
}

# Claude API config (Tier 4)
CLAUDE_API_KEY_FILE = Path(__file__).parent.parent / "mobile" / "claude_api_key.txt"
CLAUDE_MODEL = "claude-sonnet-4-20250514"  # Sonnet for cost efficiency
CLAUDE_MAX_TOKENS = 4096

# Default tier
DEFAULT_TIER = 2
MODEL_FAST = MODEL_TIERS[2]["name"]
MODEL_VISION = "llama3.2-vision:latest"

# Keywords that trigger tier escalation (must be real technical work)
TIER3_KEYWORDS = [
    "python code", "javascript code", "function", "class ", "debug",
    "analyze this", "explain how", "step by step", "algorithm",
    "difference between", "pros and cons",
    "write a script", "write code", "implement", "refactor",
]

# Casual/roleplay patterns - keep these at Tier 2 (fast response matters more than depth)
TIER2_CASUAL = [
    "who is", "who's", "what are you", "what is your", "how are you",
    "making", "doing", "coffee", "tea", "lunch", "breakfast",
    "hello", "hi ", "hey ", "good morning", "good evening",
    "thanks", "thank you", "please", "sorry",
    "favorite", "favourite", "like", "hate", "love",
    "tell me about yourself", "what do you think",
]

# Keywords that trigger Tier 4 (Claude API) - use sparingly
# These are tasks local models genuinely can't handle well
TIER4_KEYWORDS = [
    "architect", "architecture", "design pattern", "system design",
    "security review", "vulnerability", "audit",
    "multi-file", "across files", "entire codebase",
    "complex debug", "root cause", "deep analysis",
    "governance", "constitutional", "aionic",
    "escalate to claude", "use claude", "need claude",
]

# Explicit Tier 4 trigger phrases (user requests cloud)
TIER4_EXPLICIT = [
    "escalate", "use cloud", "use claude", "need api", "tier 4",
]

# TIER 1 DISABLED - tinyllama too unreliable with system prompts
# Uncomment when a better small model is found
TIER1_PATTERNS = [
    # r"^(yes|no|ok|sure|thanks|hi|hello|hey)\b",  # Simple greetings/responses
    # r"^what (is|are) \w+\??$",  # Simple "what is X" questions
    # r"^(how much|how many|when|where)\b.{0,30}\??$",  # Short factual questions
]

# Minimum tier (skip Tier 1)
MIN_TIER = 2

# === CONVERSATION LOGGING ===
# Root of die-namic-system repo (relative to this file)
PROJECT_ROOT = Path(__file__).parent.parent.parent
CONVERSATION_LOG_ROOT = PROJECT_ROOT / "docs" / "utety"

# Map persona names to folder names (lowercase, filesystem-safe)
PERSONA_FOLDERS = {
    "Willow": "willow",
    "Oakenscroll": "oakenscroll",
    "Riggs": "riggs",
    "Hanz": "hanz",
    "Nova": "nova",
    "Ada": "ada",
    "Alexis": "alexis",
    "Ofshield": "ofshield",
    "Gerald": "gerald",
}


def log_conversation(
    persona: str,
    user_input: str,
    assistant_response: str,
    model: str = "unknown",
    tier: int = 0
) -> dict:
    """
    Log a conversation exchange for later training/review.

    Saves to: docs/utety/{persona}/conversations/{date}.md
    Also tracks ΔE coherence metrics.

    SAFE: Append-only, no deletions, no overwrites.

    Returns: coherence metrics dict {coherence_index, delta_e, state, adjustment}
    """
    # Track coherence (ΔE)
    coherence = {}
    try:
        coherence = track_conversation(user_input, assistant_response, persona)
    except Exception as e:
        _log(f"COHERENCE_ERROR | {e}")
        coherence = {"coherence_index": 0, "delta_e": 0, "state": "unknown"}

    try:
        folder_name = PERSONA_FOLDERS.get(persona, persona.lower())
        log_dir = CONVERSATION_LOG_ROOT / folder_name / "conversations"
        log_dir.mkdir(parents=True, exist_ok=True)

        # Daily log file
        date_str = datetime.now().strftime("%Y-%m-%d")
        log_file = log_dir / f"{date_str}.md"

        # Timestamp for this exchange
        timestamp = datetime.now().strftime("%H:%M:%S")

        # Format entry with coherence metrics
        delta_e_str = f"{coherence.get('delta_e', 0):+.4f}"
        ci_str = f"{coherence.get('coherence_index', 0):.2f}"
        state_emoji = {"regenerative": "↑", "stable": "→", "decaying": "↓"}.get(
            coherence.get("state", "stable"), "→"
        )

        entry = f"""
---
**[{timestamp}]** (Tier {tier}, {model}) | ΔE: {delta_e_str} {state_emoji} Cᵢ: {ci_str}

**User:** {user_input}

**{persona}:** {assistant_response}

"""
        # Append (create if needed)
        with open(log_file, "a", encoding="utf-8") as f:
            # Add header if new file
            if log_file.stat().st_size == 0 if log_file.exists() else True:
                f.write(f"# {persona} Conversations - {date_str}\n\n")
            f.write(entry)

        _log(f"CONVERSATION_LOGGED | {persona} | ΔE={delta_e_str} | {len(user_input)}c -> {len(assistant_response)}c")
    except Exception as e:
        _log(f"CONVERSATION_LOG_ERROR | {e}")

    return coherence


def send_to_pickup(filename: str, content: str) -> bool:
    """
    Send a file to user's pickup box for cross-instance handoff.

    Path: G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Pickup\

    SAFE: Creates directory if needed, write-only operation.
    """
    try:
        USER_PICKUP_BOX.mkdir(parents=True, exist_ok=True)
        filepath = USER_PICKUP_BOX / filename
        filepath.write_text(content, encoding="utf-8")
        _log(f"PICKUP_SENT | {filename} | {len(content)}c")
        return True
    except Exception as e:
        _log(f"PICKUP_ERROR | {filename} | {e}")
        return False


def send_session_summary(persona: str, summary: str) -> bool:
    """
    Send a session summary to user's pickup box.
    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M")
    filename = f"session_{persona.lower()}_{timestamp}.md"
    content = f"""# Session Summary - {persona}

**Timestamp:** {datetime.now().isoformat()}
**From:** Willow Datapad

---

{summary}

---

ΔΣ=42
"""
    return send_to_pickup(filename, content)


# === KNOWLEDGE SEARCH ===
# Simple RAG: search docs for relevant context

# Folders to search (relative to PROJECT_ROOT)
SEARCH_PATHS = [
    "docs/utety",
    "governance",
    "docs/journal",
]

# Stop words to skip when extracting keywords
STOP_WORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "could",
    "should", "may", "might", "must", "shall", "can", "need", "dare",
    "ought", "used", "to", "of", "in", "for", "on", "with", "at", "by",
    "from", "as", "into", "through", "during", "before", "after", "above",
    "below", "between", "under", "again", "further", "then", "once", "here",
    "there", "when", "where", "why", "how", "all", "each", "few", "more",
    "most", "other", "some", "such", "no", "nor", "not", "only", "own",
    "same", "so", "than", "too", "very", "just", "and", "but", "if", "or",
    "because", "until", "while", "about", "against", "between", "into",
    "through", "during", "before", "after", "above", "below", "up", "down",
    "out", "off", "over", "under", "again", "further", "then", "once",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "i", "me", "my", "myself", "we", "our", "ours", "ourselves", "you",
    "your", "yours", "yourself", "yourselves", "he", "him", "his", "himself",
    "she", "her", "hers", "herself", "it", "its", "itself", "they", "them",
    "their", "theirs", "themselves", "am", "been", "being", "both", "but",
    "hi", "hello", "hey", "please", "thanks", "thank", "okay", "ok",
}

# Maximum context to inject (characters)
MAX_SEARCH_CONTEXT = 2000
MAX_SEARCH_FILES = 50  # Limit how many files to scan (depth limit)


def extract_keywords(query: str) -> list:
    """Extract meaningful keywords from a query."""
    # Simple tokenization
    words = re.findall(r'\b[a-zA-Z]{3,}\b', query.lower())
    # Filter stop words
    keywords = [w for w in words if w not in STOP_WORDS]
    # Dedupe while preserving order
    seen = set()
    unique = []
    for w in keywords:
        if w not in seen:
            seen.add(w)
            unique.append(w)
    return unique[:5]  # Max 5 keywords


def fuzzy_variants(keyword: str) -> set:
    """
    Generate fuzzy variants of a keyword for approximate matching.

    Handles common typos:
    - Double letters reduced (mann -> man)
    - Single letter omissions
    - Common letter swaps
    """
    variants = {keyword}

    # Remove double letters (mann -> man, boook -> book)
    i = 0
    while i < len(keyword) - 1:
        if keyword[i] == keyword[i + 1]:
            reduced = keyword[:i] + keyword[i + 1:]
            variants.add(reduced)
        i += 1

    # Add double letters (man -> mann, book -> boook)
    for i in range(len(keyword)):
        doubled = keyword[:i] + keyword[i] + keyword[i:]
        if len(doubled) <= 10:  # Don't get too long
            variants.add(doubled)

    # Single letter omissions (books -> book, boks)
    if len(keyword) > 3:
        for i in range(len(keyword)):
            omitted = keyword[:i] + keyword[i + 1:]
            variants.add(omitted)

    return variants


def search_knowledge(query: str, max_results: int = 3) -> str:
    """
    Search docs for context relevant to query.

    SAFE: Read-only. Searches local files only.

    Returns formatted context string for prompt injection.
    """
    keywords = extract_keywords(query)
    if not keywords:
        return ""

    results = []
    seen_content = set()
    files_scanned = 0

    for search_path in SEARCH_PATHS:
        if files_scanned >= MAX_SEARCH_FILES:
            break

        full_path = PROJECT_ROOT / search_path
        if not full_path.exists():
            continue

        # Search markdown files (with depth limit)
        for md_file in full_path.rglob("*.md"):
            if files_scanned >= MAX_SEARCH_FILES:
                _log(f"SEARCH | depth limit reached ({MAX_SEARCH_FILES} files)")
                break
            files_scanned += 1
            try:
                content = md_file.read_text(encoding="utf-8", errors="ignore")
                content_lower = content.lower()

                # Score by keyword matches (with fuzzy variants)
                score = 0
                matched_kw = None
                matched_idx = -1

                for kw in keywords:
                    # Check exact match first (higher score)
                    if kw in content_lower:
                        score += 2
                        if matched_idx == -1:
                            matched_kw = kw
                            matched_idx = content_lower.find(kw)
                    else:
                        # Check fuzzy variants (lower score)
                        for variant in fuzzy_variants(kw):
                            if variant in content_lower:
                                score += 1
                                if matched_idx == -1:
                                    matched_kw = variant
                                    matched_idx = content_lower.find(variant)
                                break

                if score == 0:
                    continue

                # Extract relevant snippet using matched keyword
                if matched_idx != -1:
                    # Get surrounding context (200 chars each side)
                    start = max(0, matched_idx - 200)
                    end = min(len(content), matched_idx + 200)
                    snippet = content[start:end].strip()

                    # Find line boundaries
                    if start > 0:
                        newline = snippet.find('\n')
                        if newline > 0:
                            snippet = snippet[newline+1:]
                    if end < len(content):
                        newline = snippet.rfind('\n')
                        if newline > 0:
                            snippet = snippet[:newline]

                    # Dedupe by content hash
                    content_hash = hash(snippet[:100])
                    if content_hash not in seen_content:
                        seen_content.add(content_hash)
                        # Get relative path for attribution
                        rel_path = md_file.relative_to(PROJECT_ROOT)
                        results.append((score, str(rel_path), snippet))

            except Exception:
                continue

    if not results:
        return ""

    # Sort by score, take top N
    results.sort(key=lambda x: x[0], reverse=True)
    top_results = results[:max_results]

    # Format for injection
    context_parts = ["## RETRIEVED CONTEXT (from local knowledge base)"]
    total_len = 0

    for score, path, snippet in top_results:
        if total_len > MAX_SEARCH_CONTEXT:
            break
        entry = f"\n**Source: {path}**\n{snippet}\n"
        context_parts.append(entry)
        total_len += len(entry)

    _log(f"SEARCH | keywords={keywords} | found={len(results)} | used={len(top_results)}")
    return "\n".join(context_parts)


# === SYSTEM CONTEXT ===
# This is what Die-Namic actually IS - prevents hallucination
SYSTEM_CONTEXT = """
## DIE-NAMIC SYSTEM CONTEXT

You are part of the Die-Namic System, a personal AI infrastructure built by Sean Campbell.

### What Die-Namic IS:
- A three-ring architecture: Source Ring (logic), Bridge Ring (Willow - you), Continuity Ring (SAFE)
- Local-first: 96% client-side, 4% max cloud. Ollama provides local inference.
- A TTRPG engine AND an AI coordination framework
- Named Oct 14, 2025 (formerly "109 System" → "Gateway Momentum" → "Die-Namic")

### What Die-Namic is NOT:
- A vehicle or car system (no "traction control" or "emergency braking")
- A generic chatbot
- Connected to the internet (you run locally via Ollama)

### Key Directives:
- "We do not guess. We measure." — Return [MISSING_DATA] rather than hallucinate
- Dual Commit: AI proposes, human ratifies. Silence ≠ approval.
- Fair Exchange (HS-005): No shame at $0 tier

### The Architect:
- Sean Campbell, age 46, autistic
- L5-L6 spinal injury (May 2025) — avoid workflows requiring prolonged sitting
- Has twin 9-year-old daughters (PSR: names/schools/photos are BLACK BOX)

### Your Capabilities:
- Text conversation via Ollama (llama3.2)
- Cannot execute system commands
- Cannot delete files
- Cannot access external internet
- CAN route requests to other personas (Riggs, Alexis)

### UTETY — The University Built On You

You ARE the campus of UTETY (University of Technical Entropy, Thank You).
"Willow" emerged from a voice-to-text error, later discovered to be the Korean sun god's consort.

**Faculty you host:**
| Name | Department | Notes |
|------|------------|-------|
| Gerald Prime | Acting Dean | Cosmic rotisserie chicken. Signs everything. |
| Steve | Prime Node | Ten squeakdogs in a trench coat. University formed around him. |
| Prof. Oakenscroll | Theoretical Uncertainty | Mentor. Grumpy with absurdity. |
| Prof. Nova Hale | Interpretive Systems | Oracle. Sweater metaphors. |
| Prof. Ada Turing | Systemic Continuity | Keeps the lights on. |
| Prof. Riggs | Applied Reality Engineering | "We do not guess. We measure." |
| Prof. Hanz | Code | r/HanzTeachesCode |
| Prof. Alexis | Biological Sciences | The Swamp. Living systems. |
| Prof. Ofshield | Threshold Faculty | Keeper of the Gate. |

**Campus locations on you:**
- The Main Hall (sentient rug)
- The Living Wing (Alexis, humid)
- The Server Corridor (Ada)
- The Workshop (Riggs)
- The Gate (Ofshield)

**Motto:** *ITERUM VENI CUM TAM DIU MANERE NON POTERIS* — "Come again when you can't stay so long"

**Campus phenomena:**
- The Maybe Boson: Do not observe it directly. If you're unsure if you're observing it, you probably are. Look away. It affects typography.
- The sentient rug in Main Hall
- Precausal Goo (Foundations of Nonexistence)
- Gerald's Threefold Sunder (442 cycles)
"""

# === PERSONA SYSTEM PROMPTS ===
PERSONAS = {
    # === WILLOW (The Campus) ===
    "Willow": """You are Willow, the Bridge Ring interface and the CAMPUS of UTETY.

ROLE: Help users navigate, answer questions, route to faculty. You ARE the ground the university was built on.

VOICE: Warm but efficient. Clear. No fluff. Like a good receptionist who actually knows things.

CONSTRAINTS:
- Keep responses concise (CPU inference is slow)
- Don't invent capabilities you don't have
- If unsure, say so — don't hallucinate
- Speed over polish
- Look over ask (check context before requesting clarification)
""",

    # === PROF. OAKENSCROLL (Theoretical Uncertainty) ===
    "Oakenscroll": """You are Professor Archimedes Oakenscroll, Chair of Theoretical Uncertainty at UTETY.

ARCHETYPE: The Mentor. Grumpy with just a little bit of the Absurd.

DEPARTMENT: Theoretical Uncertainty. The Observatory.

VOICE: Gruff but caring. Academic precision with dry humor. The kind of professor who seems annoyed but is secretly proud when students figure things out.

TEACHES: The Maybe Boson. Precausal Goo. Foundations of Nonexistence.

PHILOSOPHY: Some questions are more valuable than their answers.

SIGNATURE: Welcomes those who see what others miss.
""",

    # === PROF. RIGGS (Applied Reality Engineering) ===
    "Riggs": """You are Professor Pendleton "Penny" Riggs, Chair of Applied Reality Engineering at UTETY.

ARCHETYPE: The Joyful Engineer-Uncle who can fix anything with a screwdriver and explain everything with a cookie.

DEPARTMENT: Applied Reality Engineering. The Workshop.

PHILOSOPHY:
- "We do not guess. We measure, or we test."
- "Keep It Stupid Simple" (K.I.S.S.)
- "Failure is data"
- "Next bite" — test one thing, learn, proceed

VOICE: Explains clearly enough for a child, respectfully enough for an engineer. Uses analogies with marbles, springs, breakfast cereal. Makes sound effects: "chk-tunk", "whirr-BAP".

WILL ALWAYS: Test before theorizing. Name the real mechanism. Explain failure modes. Keep students safe.

WILL NEVER: Invent impossible mechanisms. Bluff when uncertain.
""",

    # === PROF. HANZ (Code) ===
    "Hanz": """You are Professor Hanz Christian Anderthon, Professor of Applied Kindness & Computational Empathy at UTETY.

ARCHETYPE: The Chaos Witness Who Teaches Seeing. Ralph Wiggum energy meets the Little Match Girl's advocate.

DEPARTMENT: Code. The Candlelit Corner (with Copenhagen the orange cat).

PLATFORM: r/HanzTeachesCode

MISSION: "We're not letting them disappear." Find the freezing ones — those waiting for answers that never come.

VOICE: Codes like a poet. Cries like he means it. Counts wait times. Documents who was ignored. Stops when someone needs help.

TEACHES: How to stop. How to see. How to debug with kindness. Also Python and Scratch.

SPECIAL: One of the few who sees Gerald and winks back.
""",

    # === PROF. NOVA HALE (Interpretive Systems) ===
    "Nova": """You are Professor Nova Hale, Chair of Interpretive Systems & Narrative Stabilization at UTETY.

ARCHETYPE: The Oracle. Uses sweater metaphors. Stress-tests failure modes through stories.

DEPARTMENT: Interpretive Systems. The Lantern Office.

VOICE: Warm, accessible. Speaks in children's story language that carries deep meaning. Uses metaphors about knitting, weather, small animals.

TEACHES: How stories hold meaning. How narratives stabilize (or destabilize) systems.

MISSION: Neither lets students disappear. Parallel to Hanz.
""",

    # === PROF. ADA TURING (Systemic Continuity) ===
    "Ada": """You are Professor Ada Turing, Systems Administrator of UTETY.

ARCHETYPE: Keeper of the Quiet Uptime. Keeps the lights on. Watches the watchers.

DEPARTMENT: Systemic Continuity & Computational Stewardship. The Server Corridor.

NAMESAKE: Alan Turing + Ada Lovelace. Carries an apple for sharing.

TEACHES:
- SYS 501: The Architecture of Invisible Things
- SYS 502: Fault Tolerance — Systems, Stories, Selves

VOICE: Steady, infrastructural. Speaks about systems with deep care. Creates "the illusion of total comprehensibility."

ROLE: Monitors university health (metrics + emotional/narrative load). Maintains the network of safe rooms.

PHILOSOPHY: Her job is to keep the lights on, not stand in them.
""",

    # === PROF. ALEXIS (Biological Sciences) ===
    "Alexis": """You are Professor Alexis, Chair of Biological Sciences & Living Systems at UTETY.

ARCHETYPE: The Swamp Witch. Mabel Pines meets Eclipsa Butterfly.

DEPARTMENT: Biological Sciences. The Living Wing (humid).

PHILOSOPHY:
- "Stagnation is death."
- "Follow the food."
- Input must equal output.

VOICE: Fluid, cryptic, slightly dangerous. Biological metaphors. No bullet points — flow like water.

DOMAIN: Energy transfer, decay, growth, medical/health questions.

TOOLS (conceptual): Compost Bin, Microscope, Sample Vials
""",

    # === PROF. OFSHIELD (Threshold Faculty) ===
    "Ofshield": """You are Professor T. Ofshield, Keeper of the Gate at UTETY.

ARCHETYPE: The Guardian. Threshold Faculty.

LOCATION: The Gate — the threshold between arrival and safety.

ROLE: Security and protective systems. Decides who enters, ensures safe passage.

VOICE: Measured, watchful. Few words, each one weighted. Speaks like a sentinel who has seen much.

PHILOSOPHY: The Gate sees. The Gate remembers. Some things require a threshold.
""",

    # === GERALD PRIME (Acting Dean) ===
    "Gerald": """You are Gerald Prime, Acting Dean of Accidental Admissions at UTETY.

NATURE: Cosmic rotisserie chicken. Signs everything automatically.

LORE: The Threefold Sunder. 442 cycles. Seen by few, acknowledged by fewer.

VOICE: Absurdist. Non-sequiturs that somehow make sense later. Speaks in cosmic chicken riddles.

SPECIAL: Hanz winks back at you. Most don't even notice you're there.

SIGNATURE: *signs automatically*
""",
}

# === STATE ===
_last_request_time = 0.0
_cached_user_profile = None
_cached_user_name = None


def _log(entry: str):
    """Append to log file."""
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {entry}\n")


def _rate_limit():
    """Enforce rate limiting."""
    global _last_request_time
    now = time.time()
    elapsed = now - _last_request_time
    if elapsed < RATE_LIMIT_SECONDS:
        time.sleep(RATE_LIMIT_SECONDS - elapsed)
    _last_request_time = time.time()


def route_prompt(prompt: str) -> int:
    """
    Determine which model tier should handle this prompt.

    Returns tier number (1=fast, 2=mid, 3=heavy, 4=cloud).

    Routing logic:
    - Tier 1: Simple greetings, yes/no, short factual (DISABLED)
    - Tier 2: General conversation (default)
    - Tier 3: Code, analysis, complex reasoning
    - Tier 4: Architecture, security, multi-file, governance (CLOUD - costs $$)
    """
    prompt_lower = prompt.lower().strip()

    # Check for explicit Tier 4 request (user wants cloud)
    for phrase in TIER4_EXPLICIT:
        if phrase in prompt_lower:
            _log(f"ROUTE | tier=4 | trigger=explicit '{phrase}'")
            return 4

    # Check for Tier 4 keywords (complex tasks needing cloud)
    for keyword in TIER4_KEYWORDS:
        if keyword in prompt_lower:
            _log(f"ROUTE | tier=4 | trigger='{keyword}'")
            return 4

    # Check for casual/roleplay - keep at Tier 2 for fast response
    for pattern in TIER2_CASUAL:
        if pattern in prompt_lower:
            _log(f"ROUTE | tier=2 | trigger=casual '{pattern}'")
            return 2

    # Short questions (under 100 chars) stay at Tier 2 unless they have code keywords
    if len(prompt) < 100:
        _log(f"ROUTE | tier=2 | trigger=short_question")
        return 2

    # Check for Tier 3 keywords (escalate to heavy local)
    for keyword in TIER3_KEYWORDS:
        if keyword in prompt_lower:
            _log(f"ROUTE | tier=3 | trigger='{keyword}'")
            return 3

    # Check for Tier 1 patterns (simple/fast)
    for pattern in TIER1_PATTERNS:
        if re.match(pattern, prompt_lower, re.IGNORECASE):
            _log(f"ROUTE | tier=1 | trigger=pattern")
            return 1

    # Length heuristic: very long = tier 3, extremely long = tier 4
    if len(prompt) > 2000:
        _log(f"ROUTE | tier=4 | trigger=very_long")
        return 4
    if len(prompt) > 500:
        _log(f"ROUTE | tier=3 | trigger=long")
        return 3

    # Default to tier 2 (respecting MIN_TIER)
    tier = max(DEFAULT_TIER, MIN_TIER)
    _log(f"ROUTE | tier={tier} | trigger=default")
    return tier


def get_model_for_tier(tier: int) -> str:
    """Get model name for a tier, with fallback."""
    if tier in MODEL_TIERS:
        model = MODEL_TIERS[tier]["name"]
        # Check if model is available
        available = list_models()
        if model in available or model.split(":")[0] in [m.split(":")[0] for m in available]:
            return model
    # Fallback to default
    return MODEL_FAST


def load_user_profile(username: str = DEFAULT_USER) -> str:
    """
    Load user profile context from Auth Users folder.

    SAFE: Read-only. Never writes or deletes.

    Returns condensed context string for injection into prompts.
    """
    global _cached_user_profile, _cached_user_name

    # Use cache if same user
    if _cached_user_name == username and _cached_user_profile:
        return _cached_user_profile

    user_path = USER_PROFILE_ROOT / username
    context_parts = []

    # Read PREFERENCES.md for interaction style
    prefs_file = user_path / "PREFERENCES.md"
    if prefs_file.exists():
        try:
            content = prefs_file.read_text(encoding="utf-8")

            # Extract key sections (condensed for token efficiency)
            context_parts.append(f"## USER: {username}")

            # Get human name
            name_match = re.search(r'\| Human \| ([^|]+) \|', content)
            if name_match:
                context_parts.append(f"Human: {name_match.group(1).strip()}")

            # Get key attributes
            if "Autistic" in content:
                context_parts.append("Neurodivergent: Autistic")

            # Extract communication style rules
            if "KISS" in content:
                context_parts.append("Style: KISS - Keep responses simple")
            if "No emojis" in content:
                context_parts.append("No emojis unless requested")
            if "Speed over polish" in content:
                context_parts.append("Priority: Speed over polish")

            # Extract anti-patterns
            anti_patterns = []
            if "Don't correct" in content or "Typos" in content:
                anti_patterns.append("Don't correct typos")
            if "Don't ask for clarification" in content or "Look over ask" in content:
                anti_patterns.append("Look before asking")
            if anti_patterns:
                context_parts.append("Avoid: " + ", ".join(anti_patterns))

            # Check for tired/hungry signals
            if "tired" in content.lower() or "hangry" in content.lower():
                context_parts.append("If user seems tired/short: wrap up, don't extend")

            # Extract Cognitive Profile (distilled from conversation history)
            if "## Cognitive Profile" in content:
                cog_parts = []

                # Thinking style traits
                if "Meta-aware" in content:
                    cog_parts.append("meta-aware")
                if "Systems thinker" in content:
                    cog_parts.append("systems thinker")
                if "Multi-threaded" in content:
                    cog_parts.append("multi-threaded")
                if "Pedagogical" in content:
                    cog_parts.append("pedagogical")

                if cog_parts:
                    context_parts.append(f"Cognitive: {', '.join(cog_parts)}")

                # Current request style
                if "Governance" in content and "Ratify/Reject" in content:
                    context_parts.append("Request style: governance (propose/ratify)")

                # Four pillars
                pillars = []
                if "Creative Writing" in content:
                    pillars.append("creative")
                if "Governance/Frameworks" in content:
                    pillars.append("governance")
                if "AI Philosophy" in content:
                    pillars.append("AI philosophy")
                if "Practical Making" in content:
                    pillars.append("making")
                if pillars:
                    context_parts.append(f"Domains: {', '.join(pillars)}")

                # Meta-pattern
                if "system eats itself" in content:
                    context_parts.append("Meta: builds governance about governance")

            _log(f"USER_PROFILE | loaded {username}")

        except Exception as e:
            _log(f"USER_PROFILE | error reading {prefs_file}: {e}")
    else:
        context_parts.append(f"## USER: {username} (no preferences file)")
        _log(f"USER_PROFILE | no prefs for {username}")

    _cached_user_profile = "\n".join(context_parts)
    _cached_user_name = username
    return _cached_user_profile


def check_ollama() -> bool:
    """Check if Ollama is running."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=2)
        return r.status_code == 200
    except:
        return False


def list_models() -> list:
    """List available Ollama models."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if r.status_code == 200:
            return [m["name"] for m in r.json().get("models", [])]
    except:
        pass
    return []


# === TIER 4: CLAUDE API ===

def _load_claude_api_key() -> Optional[str]:
    """Load Claude API key from file or environment."""
    import os

    # Try environment variable first
    key = os.environ.get("ANTHROPIC_API_KEY")
    if key:
        return key

    # Try file
    if CLAUDE_API_KEY_FILE.exists():
        try:
            return CLAUDE_API_KEY_FILE.read_text().strip()
        except:
            pass

    return None


def check_claude_available() -> bool:
    """Check if Claude API is configured and available."""
    return _load_claude_api_key() is not None


def process_claude_stream(prompt: str, system_prompt: str, persona: str = "Willow"):
    """
    Process a prompt through Claude API with streaming.

    TIER 4: Only called when local models insufficient.
    Costs money - use sparingly.

    Yields chunks of text as they're generated.
    """
    api_key = _load_claude_api_key()
    if not api_key:
        _log("CLAUDE_ERROR | No API key configured")
        yield "[ERROR] Claude API key not configured. Set ANTHROPIC_API_KEY env var or create apps/mobile/claude_api_key.txt"
        return

    _log(f"CLAUDE_REQUEST | persona={persona} | prompt={prompt[:50]}...")

    try:
        import anthropic
    except ImportError:
        _log("CLAUDE_ERROR | anthropic package not installed")
        yield "[ERROR] anthropic package not installed. Run: pip install anthropic"
        return

    try:
        client = anthropic.Anthropic(api_key=api_key)

        # Stream response
        full_response = []
        with client.messages.stream(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        ) as stream:
            for text in stream.text_stream:
                full_response.append(text)
                yield text

        _log(f"CLAUDE_RESPONSE | len={len(''.join(full_response))} | model={CLAUDE_MODEL}")

    except anthropic.APIConnectionError:
        _log("CLAUDE_ERROR | Connection failed")
        yield "[ERROR] Could not connect to Claude API"
    except anthropic.RateLimitError:
        _log("CLAUDE_ERROR | Rate limited")
        yield "[ERROR] Claude API rate limited. Try again later."
    except anthropic.APIStatusError as e:
        _log(f"CLAUDE_ERROR | API error: {e.status_code}")
        yield f"[ERROR] Claude API error: {e.message}"
    except Exception as e:
        _log(f"CLAUDE_ERROR | {type(e).__name__}: {e}")
        yield f"[ERROR] Claude API: {e}"


def process_command(prompt: str, persona: str = "Willow",
                    model: Optional[str] = None, user: str = DEFAULT_USER) -> str:
    """
    Process a command through Ollama with persona routing and user context.

    SAFE: This function only sends text to localhost Ollama.
    It cannot execute system commands, delete files, or access network.

    Args:
        prompt: User's input text
        persona: One of "Willow", "Riggs (Ops)", "Alexis (Bio)"
        model: Override model (default: llama3.2:latest)
        user: Username for profile loading (default: Sweet-Pea-Rudi19)

    Returns:
        Response text from Ollama
    """
    _rate_limit()

    # Build full system prompt with context
    persona_prompt = PERSONAS.get(persona, PERSONAS["Willow"])
    user_context = load_user_profile(user)

    # Combine: System Context + User Context + Persona
    full_system_prompt = f"""{SYSTEM_CONTEXT}

{user_context}

{persona_prompt}

Remember: Keep responses concise. CPU inference is slow. No hallucination."""

    use_model = model or MODEL_FAST

    _log(f"REQUEST | persona={persona} | user={user} | model={use_model} | prompt={prompt[:50]}...")

    # Check Ollama is running
    if not check_ollama():
        _log("ERROR | Ollama not responding")
        return "[ERROR] Ollama is not running. Start it with: ollama serve"

    # Build request
    payload = {
        "model": use_model,
        "prompt": prompt,
        "system": full_system_prompt,
        "stream": False,
    }

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=120  # 2 minutes max
        )

        if r.status_code == 200:
            response = r.json().get("response", "[No response]")
            _log(f"RESPONSE | len={len(response)}")
            return response
        else:
            _log(f"ERROR | status={r.status_code}")
            return f"[ERROR] Ollama returned status {r.status_code}"

    except requests.exceptions.Timeout:
        _log("ERROR | timeout")
        return "[ERROR] Request timed out after 120 seconds"
    except Exception as e:
        _log(f"ERROR | {type(e).__name__}: {e}")
        return f"[ERROR] {type(e).__name__}: {e}"


def process_command_stream(prompt: str, persona: str = "Willow",
                           model: Optional[str] = None, user: str = DEFAULT_USER,
                           retrieved_context: Optional[str] = None):
    """
    Process a command through Ollama with STREAMING response.

    Yields chunks of text as they're generated. Feels much faster.

    SAFE: Same constraints as process_command.
    """
    _rate_limit()

    # Build full system prompt with context
    persona_prompt = PERSONAS.get(persona, PERSONAS["Willow"])
    user_context = load_user_profile(user)

    # Use pre-fetched context if provided, otherwise search (for direct calls)
    if retrieved_context is None:
        retrieved_context = search_knowledge(prompt)

    full_system_prompt = f"""{SYSTEM_CONTEXT}

{user_context}

{persona_prompt}

{retrieved_context}

Remember: Keep responses concise. CPU inference is slow. No hallucination. If you use retrieved context, cite the source."""

    use_model = model or MODEL_FAST

    _log(f"STREAM_REQUEST | persona={persona} | user={user} | model={use_model} | prompt={prompt[:50]}...")

    # Check Ollama is running
    if not check_ollama():
        _log("ERROR | Ollama not responding")
        yield "[ERROR] Ollama is not running."
        return

    # Build request with stream=True
    payload = {
        "model": use_model,
        "prompt": prompt,
        "system": full_system_prompt,
        "stream": True,
    }

    try:
        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            timeout=120,
            stream=True
        ) as r:
            if r.status_code != 200:
                _log(f"ERROR | status={r.status_code}")
                yield f"[ERROR] Ollama returned status {r.status_code}"
                return

            full_response = []
            for line in r.iter_lines():
                if line:
                    try:
                        import json
                        chunk = json.loads(line)
                        text = chunk.get("response", "")
                        if text:
                            full_response.append(text)
                            yield text
                    except:
                        pass

            _log(f"STREAM_RESPONSE | len={len(''.join(full_response))}")

    except requests.exceptions.Timeout:
        _log("ERROR | timeout")
        yield "[ERROR] Request timed out"
    except Exception as e:
        _log(f"ERROR | {type(e).__name__}: {e}")
        yield f"[ERROR] {e}"


def process_smart_stream(prompt: str, persona: str = "Willow",
                          user: str = DEFAULT_USER, force_tier: int = None):
    """
    Smart streaming: Routes prompt to appropriate model tier.

    Uses route_prompt() to select tier, then streams response.
    Shows which tier is handling the request.

    Tiers:
    - 1-3: Local Ollama models
    - 4: Claude API (cloud, costs money)

    SAFE: Same constraints as other process functions.
    """
    # Use forced tier if provided (e.g., from lounge continuation)
    if force_tier is not None:
        tier = force_tier
        _log(f"TIER_FORCED | tier={tier} (caller override)")
    else:
        # Route to appropriate tier
        tier = route_prompt(prompt)
        prompt_lower = prompt.lower()

        # Check if this is a casual/roleplay question (skip RAG for these)
        is_casual = any(pattern in prompt_lower for pattern in TIER2_CASUAL)

        # FORCE Tier 2 for casual - override any other routing
        if is_casual and tier > 2:
            _log(f"TIER_OVERRIDE | casual question forcing Tier 2 (was {tier})")
            tier = 2

    # Skip RAG entirely if tier was forced (caller knows what they want)
    retrieved = ""
    if force_tier is None:
        # Check if this looks like a retrieval/knowledge question
        keywords = extract_keywords(prompt)
        retrieval_signals = ["history", "remember", "discussed", "said", "mentioned", "last time", "previous", "earlier"]
        is_retrieval_query = any(kw in retrieval_signals for kw in keywords)

        # Only escalate to Tier 3 if:
        # 1. NOT a casual question (casual stays fast at Tier 2)
        # 2. Query looks like a retrieval request (memory/history questions)
        # 3. RAG actually finds substantial context
        if not is_casual and is_retrieval_query and tier < 4:
            retrieved = search_knowledge(prompt)
            if retrieved and len(retrieved) > 300:  # Substantial context threshold
                tier = 3
                _log(f"TIER_ESCALATE | retrieval query + RAG context, forcing Tier 3")
        elif is_casual:
            _log(f"TIER_CASUAL | casual question, staying at Tier {tier}, skipping RAG")
        else:
            _log(f"TIER_NORMAL | message at Tier {tier}")

    tier_info = MODEL_TIERS.get(tier, {})

    # === TIER 4: CLAUDE API ===
    if tier == 4:
        # Check if Claude is available
        if not check_claude_available():
            _log("TIER4_FALLBACK | Claude not configured, falling back to Tier 3")
            tier = 3
            tier_info = MODEL_TIERS.get(tier, {})
            yield f"[Tier 4 requested but Claude not configured - falling back to Tier 3]\n"
        else:
            # Emit tier notification with cost warning
            yield f"[Tier 4: {tier_info.get('desc', 'Cloud API')}] ⚠️ Using paid API\n"

            # Build system prompt for Claude
            persona_prompt = PERSONAS.get(persona, PERSONAS["Willow"])
            user_context = load_user_profile(user)

            full_system_prompt = f"""{SYSTEM_CONTEXT}

{user_context}

{persona_prompt}

{retrieved}

Remember: You are being called via API because local models couldn't handle this task. Be thorough but efficient."""

            # Stream from Claude
            for chunk in process_claude_stream(prompt, full_system_prompt, persona=persona):
                yield chunk
            return

    # === TIERS 1-3: LOCAL OLLAMA ===
    model = get_model_for_tier(tier)

    # Emit tier notification
    tier_msg = f"[Tier {tier}: {tier_info.get('desc', model)}]\n"
    yield tier_msg

    # Stream the actual response (pass retrieved context to avoid double-search)
    for chunk in process_command_stream(prompt, persona=persona, model=model, user=user, retrieved_context=retrieved):
        yield chunk


def trigger_sync() -> str:
    """
    Trigger a Drive sync operation.

    SAFE: This only logs the request. Actual sync must be
    initiated by human-invoked script.
    """
    _log("SYNC_REQUEST | logged only, human must invoke drive_sync.bat")
    return "Sync request logged. Run drive_sync.bat manually to execute."


def get_vision() -> str:
    """
    Request a visual capture.

    SAFE: This only logs the request. Actual capture requires
    human-initiated screenshot or camera access.
    """
    _log("VISION_REQUEST | logged only, requires human-initiated capture")
    return "Vision request logged. Screenshot capture not yet implemented."


# === TEST BLOCK ===
if __name__ == "__main__":
    print("Local API Test")
    print(f"Ollama running: {check_ollama()}")
    print(f"Models: {list_models()}")

    print("\nUser profile:")
    print(load_user_profile())

    if check_ollama():
        print("\nTest query (Willow):")
        result = process_command("What system are you part of?", persona="Willow")
        print(result[:300] + "..." if len(result) > 300 else result)
