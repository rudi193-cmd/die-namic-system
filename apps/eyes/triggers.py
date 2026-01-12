#!/usr/bin/env python3
"""
Eyes Trigger Layer — Classification, Routing, Actions

Routes screenshots to projects based on window title patterns.
Fires triggers when specific patterns are detected.
"""

import os
import shutil
import json
from pathlib import Path
from datetime import datetime

# Routing table: pattern → (project, handler, priority)
# Priority: 1=critical (immediate), 2=normal, 3=background
ROUTES = {
    # Claude instances
    "Project Manager CLAUDE": ("pm-claude", "mitra", 2),
    "Claude — Control+Alt+Space": ("die-namic", "cmd", 2),
    "Claude —": ("claude-generic", None, 3),

    # ChatGPT instances
    "ChatGPT": ("chatgpt", None, 3),

    # Dev tools
    "Visual Studio Code": ("dev", "code", 3),
    "GitHub": ("dev", "github", 2),

    # Google workspace
    "Google Docs": ("gdocs", None, 3),
    "Google Drive": ("gdrive", None, 3),

    # Willow-specific
    "Sweet-Pea": ("willow", "inbox", 2),

    # Triggers (not routing, just detection)
    "Divergence": ("trigger", "divergence", 1),
    "PENDING": ("trigger", "signal_waiting", 2),
    "% context": ("trigger", "context_warning", 1),
}

# Trigger actions: handler → action function name
TRIGGER_ACTIONS = {
    "divergence": "on_divergence",
    "signal_waiting": "on_signal_waiting",
    "context_warning": "on_context_warning",
}

# Output directories
BASE_OUT = Path(r"C:\Users\Sean\screenshots")
ROUTED_DIR = BASE_OUT / "routed"
TRIGGER_LOG = BASE_OUT / "triggers.log"
STATE_FILE = BASE_OUT / "eyes" / "trigger_state.json"


def log_trigger(msg):
    """Log trigger events."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {msg}\n"
    with open(TRIGGER_LOG, "a", encoding="utf-8") as f:
        f.write(line)
    print(f"[TRIGGER] {msg}")


def load_state():
    """Load trigger state."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"last_triggers": {}, "counts": {}}


def save_state(state):
    """Save trigger state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)


def classify(title):
    """
    Classify a window title into project/handler.
    Returns: (project, handler, priority) or (None, None, None)
    """
    if not title:
        return None, None, None

    title_lower = title.lower()

    for pattern, (project, handler, priority) in ROUTES.items():
        if pattern.lower() in title_lower:
            return project, handler, priority

    return "unknown", None, 3


def route_screenshot(filepath, title):
    """
    Route a screenshot to the appropriate project folder.
    Returns: destination path or None
    """
    project, handler, priority = classify(title)

    if not project or project == "unknown":
        return None

    # Create project subfolder
    dest_dir = ROUTED_DIR / project
    dest_dir.mkdir(parents=True, exist_ok=True)

    # Copy (not move) to preserve original
    src = Path(filepath)
    dest = dest_dir / src.name
    shutil.copy2(src, dest)

    log_trigger(f"ROUTED | {src.name} → {project}/{handler or 'default'} | pri={priority}")

    return dest


def check_triggers(title, filepath=None):
    """
    Check if title matches any trigger patterns.
    Returns list of triggered actions.
    """
    triggered = []
    state = load_state()
    now = datetime.now().isoformat()

    if not title:
        return triggered

    title_lower = title.lower()

    for pattern, (project, handler, priority) in ROUTES.items():
        if project != "trigger":
            continue

        if pattern.lower() in title_lower:
            # Debounce: don't fire same trigger within 60s
            last = state["last_triggers"].get(handler, "")
            if last:
                from datetime import datetime as dt
                try:
                    last_time = dt.fromisoformat(last)
                    delta = (dt.now() - last_time).total_seconds()
                    if delta < 60:
                        continue
                except:
                    pass

            triggered.append({
                "handler": handler,
                "pattern": pattern,
                "priority": priority,
                "title": title,
                "filepath": filepath,
                "timestamp": now
            })

            state["last_triggers"][handler] = now
            state["counts"][handler] = state["counts"].get(handler, 0) + 1

            log_trigger(f"FIRED | {handler} | pattern='{pattern}' | title='{title[:50]}'")

    save_state(state)
    return triggered


def on_divergence(trigger_info):
    """Handle divergence detection."""
    log_trigger(f"ACTION | divergence | Should pull and diff")
    # Future: auto git pull, show diff
    return {"action": "divergence_detected", "status": "logged"}


def on_signal_waiting(trigger_info):
    """Handle signal waiting for pickup."""
    log_trigger(f"ACTION | signal_waiting | Check QUEUE.md")
    # Future: parse queue, alert on pending signals for cmd
    return {"action": "signal_pending", "status": "logged"}


def on_context_warning(trigger_info):
    """Handle context percentage warning."""
    log_trigger(f"ACTION | context_warning | TSI alert")
    # Future: extract %, update local TSI, warn if low
    return {"action": "context_warning", "status": "logged"}


def execute_triggers(triggered):
    """Execute all triggered actions."""
    results = []

    for t in triggered:
        handler = t["handler"]
        action_name = TRIGGER_ACTIONS.get(handler)

        if action_name and action_name in globals():
            action_fn = globals()[action_name]
            result = action_fn(t)
            results.append({"handler": handler, "result": result})

    return results


def process_screenshot(filepath, title):
    """
    Full processing pipeline for a screenshot.
    1. Classify
    2. Route
    3. Check triggers
    4. Execute actions
    """
    project, handler, priority = classify(title)

    # Route to project folder
    routed_path = route_screenshot(filepath, title)

    # Check and execute triggers
    triggered = check_triggers(title, filepath)
    if triggered:
        execute_triggers(triggered)

    return {
        "project": project,
        "handler": handler,
        "priority": priority,
        "routed_to": str(routed_path) if routed_path else None,
        "triggers_fired": len(triggered)
    }


# CLI for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_title = " ".join(sys.argv[1:])
    else:
        test_title = "Project Manager CLAUDE / Ping test"

    print(f"Testing: '{test_title}'")
    project, handler, priority = classify(test_title)
    print(f"  Project: {project}")
    print(f"  Handler: {handler}")
    print(f"  Priority: {priority}")

    triggered = check_triggers(test_title)
    print(f"  Triggers: {len(triggered)}")
    for t in triggered:
        print(f"    - {t['handler']}: {t['pattern']}")
