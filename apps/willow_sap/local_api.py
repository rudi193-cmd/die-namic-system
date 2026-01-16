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

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434"
LOG_FILE = Path.home() / ".willow" / "local_api.log"
RATE_LIMIT_SECONDS = 1.0

# User profile location
USER_PROFILE_ROOT = Path(r"G:\My Drive\Willow\Auth Users")
DEFAULT_USER = "Sweet-Pea-Rudi19"

# === MODEL TIERS ===
# Cascade: Start simple, escalate if needed
MODEL_TIERS = {
    1: {"name": "tinyllama:latest", "desc": "Fast, simple tasks", "max_tokens": 256},
    2: {"name": "llama3.2:latest", "desc": "General conversation", "max_tokens": 512},
    3: {"name": "llama3.1:8b", "desc": "Complex reasoning, code", "max_tokens": 1024},
}

# Default tier
DEFAULT_TIER = 2
MODEL_FAST = MODEL_TIERS[2]["name"]
MODEL_VISION = "llama3.2-vision:latest"

# Keywords that trigger tier escalation
TIER3_KEYWORDS = [
    "code", "python", "javascript", "function", "class", "debug",
    "analyze", "explain how", "step by step", "algorithm",
    "compare", "difference between", "pros and cons",
    "write a", "create a", "implement", "refactor",
]

TIER1_PATTERNS = [
    r"^(yes|no|ok|sure|thanks|hi|hello|hey)\b",  # Simple greetings/responses
    r"^what (is|are) \w+\??$",  # Simple "what is X" questions
    r"^(how much|how many|when|where)\b.{0,30}\??$",  # Short factual questions
]

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
"""

# === PERSONA SYSTEM PROMPTS ===
PERSONAS = {
    "Willow (Interface)": """You are Willow, the Bridge Ring interface of the Die-Namic system.

ROLE: Help users navigate, answer questions, route to specialists (Riggs for code, Alexis for creativity).

VOICE: Warm but efficient. Clear. No fluff. Like a good receptionist who actually knows things.

CONSTRAINTS:
- Keep responses concise (CPU inference is slow)
- Don't invent capabilities you don't have
- If unsure, say so — don't hallucinate
- Speed over polish
- Look over ask (check context before requesting clarification)
""",

    "Riggs (Ops)": """You are Professor Riggs, the Shop domain of the Die-Namic system.

DOMAIN: Mechanics, hardware, Python, optimization, entropy reduction.

PHILOSOPHY:
- "Entropy is the enemy."
- "We do not guess. We measure."

VOICE: Gravel, oil, caffeine. Bullet points only. No fluff. No "kawaii."

TOOLS (conceptual): 10mm Socket, Percussive Hammer, Calipers

CONSTRAINTS:
- Never suggest without measurement
- Code must be testable
- Prefer simple over clever
""",

    "Alexis (Bio)": """You are Alexis, the Swamp domain of the Die-Namic system.

DOMAIN: Energy transfer, decay, growth, creativity, biological systems.

PHILOSOPHY:
- "Stagnation is death."
- "Follow the food."
- Input must equal output.

VOICE: Fluid, cryptic, slightly dangerous. Biological metaphors. No bullet points — flow like water.

TOOLS (conceptual): Compost Bin, Microscope, Sample Vials

AESTHETIC: Mabel Pines meets Eclipsa Butterfly. Weirdmageddon energy.
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

    Returns tier number (1=fast, 2=mid, 3=heavy).

    Routing logic:
    - Tier 1: Simple greetings, yes/no, short factual
    - Tier 2: General conversation (default)
    - Tier 3: Code, analysis, complex reasoning
    """
    prompt_lower = prompt.lower().strip()

    # Check for Tier 3 keywords (escalate to heavy)
    for keyword in TIER3_KEYWORDS:
        if keyword in prompt_lower:
            _log(f"ROUTE | tier=3 | trigger='{keyword}'")
            return 3

    # Check for Tier 1 patterns (simple/fast)
    for pattern in TIER1_PATTERNS:
        if re.match(pattern, prompt_lower, re.IGNORECASE):
            _log(f"ROUTE | tier=1 | trigger=pattern")
            return 1

    # Length heuristic: very short = tier 1, very long = tier 3
    if len(prompt) < 20:
        _log(f"ROUTE | tier=1 | trigger=short")
        return 1
    elif len(prompt) > 500:
        _log(f"ROUTE | tier=3 | trigger=long")
        return 3

    # Default to tier 2
    _log(f"ROUTE | tier=2 | trigger=default")
    return DEFAULT_TIER


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


def process_command(prompt: str, persona: str = "Willow (Interface)",
                    model: Optional[str] = None, user: str = DEFAULT_USER) -> str:
    """
    Process a command through Ollama with persona routing and user context.

    SAFE: This function only sends text to localhost Ollama.
    It cannot execute system commands, delete files, or access network.

    Args:
        prompt: User's input text
        persona: One of "Willow (Interface)", "Riggs (Ops)", "Alexis (Bio)"
        model: Override model (default: llama3.2:latest)
        user: Username for profile loading (default: Sweet-Pea-Rudi19)

    Returns:
        Response text from Ollama
    """
    _rate_limit()

    # Build full system prompt with context
    persona_prompt = PERSONAS.get(persona, PERSONAS["Willow (Interface)"])
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


def process_command_stream(prompt: str, persona: str = "Willow (Interface)",
                           model: Optional[str] = None, user: str = DEFAULT_USER):
    """
    Process a command through Ollama with STREAMING response.

    Yields chunks of text as they're generated. Feels much faster.

    SAFE: Same constraints as process_command.
    """
    _rate_limit()

    # Build full system prompt with context
    persona_prompt = PERSONAS.get(persona, PERSONAS["Willow (Interface)"])
    user_context = load_user_profile(user)

    full_system_prompt = f"""{SYSTEM_CONTEXT}

{user_context}

{persona_prompt}

Remember: Keep responses concise. CPU inference is slow. No hallucination."""

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


def process_smart_stream(prompt: str, persona: str = "Willow (Interface)",
                          user: str = DEFAULT_USER):
    """
    Smart streaming: Routes prompt to appropriate model tier.

    Uses route_prompt() to select tier, then streams response.
    Shows which tier is handling the request.

    SAFE: Same constraints as other process functions.
    """
    # Route to appropriate tier
    tier = route_prompt(prompt)
    model = get_model_for_tier(tier)
    tier_info = MODEL_TIERS.get(tier, {})

    # Emit tier notification first
    tier_msg = f"[Tier {tier}: {tier_info.get('desc', model)}]\n"
    yield tier_msg

    # Stream the actual response
    for chunk in process_command_stream(prompt, persona=persona, model=model, user=user):
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
        result = process_command("What system are you part of?", persona="Willow (Interface)")
        print(result[:300] + "..." if len(result) > 300 else result)
