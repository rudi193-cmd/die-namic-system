#!/usr/bin/env python3
"""
Willow Inbox Watcher

Monitors Willow inbox for new items, processes on arrival, routes to destinations.

GOVERNANCE: This script must be started by human action only.
AI cannot invoke this script directly.
"""

import os
import sys
import time
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

# Config
INBOX_PATH = Path(r"G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Inbox")
OUTBOX_PATH = Path(r"G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Outbox")
JOURNAL_PATH = Path(r"G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\JOURNAL.md")
STATE_FILE = Path(r"C:\Users\Sean\.willow\watcher_state.json")
EVENT_LOG = Path(r"C:\Users\Sean\.willow\events.log")
POLL_INTERVAL = 5  # seconds

# File type routing
ROUTES = {
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".gif": "image",
    ".gdoc": "gdoc",
    ".gsheet": "gsheet",
    ".md": "document",
    ".txt": "document",
    ".docx": "document",
    ".pdf": "document",
}


def ensure_dirs():
    """Create necessary directories."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_state() -> Dict:
    """Load watcher state (known files and their hashes)."""
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"known_files": {}, "last_run": None}


def save_state(state: Dict):
    """Save watcher state."""
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def log_event(event_type: str, details: str):
    """Log event to event log (for AI consumption)."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{event_type} | {timestamp} | {details}\n"

    with open(EVENT_LOG, "a") as f:
        f.write(entry)

    print(f"[{event_type}] {details}")


def get_file_hash(filepath: Path) -> str:
    """Get hash of file for change detection."""
    try:
        # For gdoc files (cloud shortcuts), use mtime since content isn't local
        if filepath.suffix in [".gdoc", ".gsheet", ".gslides"]:
            stat = filepath.stat()
            return f"mtime:{stat.st_mtime}"

        # For real files, hash content
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f"error:{e}"


def classify_file(filepath: Path) -> Dict:
    """Classify a file and determine routing."""
    name = filepath.name
    suffix = filepath.suffix.lower()

    # Determine type
    file_type = ROUTES.get(suffix, "unknown")

    # Detect source from filename patterns
    source = "unknown"
    if "Screenshot_" in name:
        # Parse app from filename like Screenshot_20260111_215047_Claude.jpg
        parts = name.split("_")
        if len(parts) >= 4:
            source = parts[-1].replace(suffix, "")
    elif name.startswith("20"):
        source = "camera"

    # Determine route
    if file_type == "gdoc":
        route = "journal.dynamic"  # Needs API to read
    elif file_type == "image":
        route = "journal.safe"  # Can process locally
    elif file_type == "unknown":
        route = "journal.unknown"
    else:
        route = "journal.safe"

    return {
        "name": name,
        "type": file_type,
        "source": source,
        "route": route,
        "path": str(filepath),
        "size": filepath.stat().st_size if filepath.exists() else 0,
    }


def process_new_file(filepath: Path) -> Dict:
    """Process a new file in the inbox."""
    classification = classify_file(filepath)

    log_event("NEW_FILE", f"{classification['name']} | type={classification['type']} | source={classification['source']} | route={classification['route']}")

    # For now, just classify - actual processing would happen here
    # Future: OCR images, extract gdoc content via API, etc.

    return classification


def scan_inbox() -> List[Path]:
    """Scan inbox for all files."""
    if not INBOX_PATH.exists():
        return []

    files = []
    for item in INBOX_PATH.iterdir():
        if item.is_file():
            files.append(item)

    return files


def main():
    """Main watcher loop."""
    # Consent
    print("Willow Inbox Watcher")
    print(f"Watching: {INBOX_PATH}")
    print(f"Poll interval: {POLL_INTERVAL}s")
    consent = input("Start watching? (yes/no): ").strip().lower()
    if consent != "yes":
        print("Aborted.")
        return

    ensure_dirs()
    state = load_state()

    log_event("WATCHER_ON", f"inbox={INBOX_PATH}")
    print(f"\nWatcher online. Press Ctrl+C to stop.\n")

    try:
        while True:
            current_files = scan_inbox()

            for filepath in current_files:
                file_key = str(filepath)
                file_hash = get_file_hash(filepath)

                # Check if new or changed
                if file_key not in state["known_files"]:
                    # New file
                    process_new_file(filepath)
                    state["known_files"][file_key] = {
                        "hash": file_hash,
                        "first_seen": datetime.now().isoformat(),
                        "processed": True,
                    }
                elif state["known_files"][file_key]["hash"] != file_hash:
                    # Changed file
                    log_event("FILE_CHANGED", filepath.name)
                    state["known_files"][file_key]["hash"] = file_hash
                    state["known_files"][file_key]["last_changed"] = datetime.now().isoformat()

            # Check for deleted files
            known_keys = list(state["known_files"].keys())
            current_keys = [str(f) for f in current_files]
            for key in known_keys:
                if key not in current_keys:
                    log_event("FILE_REMOVED", Path(key).name)
                    del state["known_files"][key]

            state["last_run"] = datetime.now().isoformat()
            save_state(state)

            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        pass
    finally:
        log_event("WATCHER_OFF", f"known_files={len(state['known_files'])}")
        save_state(state)
        print(f"\nWatcher off. Tracking {len(state['known_files'])} files.")


if __name__ == "__main__":
    main()
