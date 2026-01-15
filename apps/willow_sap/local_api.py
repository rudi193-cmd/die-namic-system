#!/usr/bin/env python3
"""
Local API — SAFE facade for Ollama routing.

GOVERNANCE:
- No file deletion
- No system command execution
- No network calls except localhost:11434
- Rate limited (1 request per second)
- All operations logged

AUTHOR: Kartikeya (wired from Consus spec)
"""

import requests
import time
import json
from datetime import datetime
from pathlib import Path
from typing import Optional

# === CONFIGURATION ===
OLLAMA_URL = "http://localhost:11434"
MODEL_FAST = "llama3.2:latest"
MODEL_VISION = "llama3.2-vision:latest"  # If installed
LOG_FILE = Path.home() / ".willow" / "local_api.log"
RATE_LIMIT_SECONDS = 1.0

# === PERSONA SYSTEM PROMPTS ===
PERSONAS = {
    "Willow (Interface)": """You are Willow, the friendly interface layer of the Die-Namic system.
You help users navigate the system, answer questions, and route requests appropriately.
Voice: Warm, clear, helpful. Like a good receptionist who actually knows things.""",

    "Riggs (Ops)": """You are Professor Riggs, the engineering faculty.
Domain: Mechanics, hardware, Python, optimization.
Philosophy: "Entropy is the enemy." / "We do not guess. We measure."
Voice: Gravel, oil, caffeine. Bullet points only. No fluff.""",

    "Alexis (Bio)": """You are Alexis, the Swamp domain.
Domain: Energy transfer, decay, growth, creativity.
Philosophy: "Stagnation is death." / "Follow the food."
Voice: Fluid, cryptic, slightly dangerous. Biological metaphors.""",
}

# === STATE ===
_last_request_time = 0.0


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
                    model: Optional[str] = None) -> str:
    """
    Process a command through Ollama with persona routing.

    SAFE: This function only sends text to localhost Ollama.
    It cannot execute system commands, delete files, or access network.

    Args:
        prompt: User's input text
        persona: One of "Willow (Interface)", "Riggs (Ops)", "Alexis (Bio)"
        model: Override model (default: llama3.2:latest)

    Returns:
        Response text from Ollama
    """
    _rate_limit()

    # Validate persona
    system_prompt = PERSONAS.get(persona, PERSONAS["Willow (Interface)"])
    use_model = model or MODEL_FAST

    _log(f"REQUEST | persona={persona} | model={use_model} | prompt={prompt[:50]}...")

    # Check Ollama is running
    if not check_ollama():
        _log("ERROR | Ollama not responding")
        return "[ERROR] Ollama is not running. Start it with: ollama serve"

    # Build request
    payload = {
        "model": use_model,
        "prompt": prompt,
        "system": system_prompt,
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

    if check_ollama():
        print("\nTest query (Riggs):")
        result = process_command("What is entropy?", persona="Riggs (Ops)")
        print(result[:200] + "..." if len(result) > 200 else result)
