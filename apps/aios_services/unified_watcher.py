#!/usr/bin/env python3
"""
Unified Watcher — monitors multiple paths with same logic.

GOVERNANCE: Human must invoke. AI cannot.
"""

import os
import sys
import time
import json
import hashlib
import argparse
from datetime import datetime
from pathlib import Path

# Watch targets
WATCH_PATHS = [
    Path(r"G:\My Drive\Willow\Auth Users\Sweet-Pea-Rudi19\Inbox"),
    Path(r"G:\My Drive\Aios Input"),
    Path(r"G:\My Drive\Claude Handoff Documents"),
    Path(r"G:\My Drive\UTETY"),
]

QUEUE_PATH = Path(r"C:\Users\Sean\die-namic-system\bridge_ring\instance_signals\QUEUE.md")
STATE_FILE = Path(r"C:\Users\Sean\.willow\unified_state.json")
EVENT_LOG = Path(r"C:\Users\Sean\.willow\unified_events.log")
POLL_INTERVAL = 5

ROUTES = {
    ".jpg": "image", ".jpeg": "image", ".png": "image", ".gif": "image",
    ".gdoc": "gdoc", ".gsheet": "gsheet", ".gslides": "gslides",
    ".md": "document", ".txt": "document", ".docx": "document", ".pdf": "document",
}


def ensure_dirs():
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)


def load_state():
    if STATE_FILE.exists():
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {"known_files": {}, "last_queue_hash": None, "last_run": None}


def save_state(state):
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def log(entry):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"{timestamp} | {entry}\n"
    with open(EVENT_LOG, "a") as f:
        f.write(line)
    print(f"[{timestamp}] {entry}")


def get_file_hash(filepath):
    try:
        if filepath.suffix in [".gdoc", ".gsheet", ".gslides"]:
            return f"mtime:{filepath.stat().st_mtime}"
        with open(filepath, "rb") as f:
            return hashlib.md5(f.read()).hexdigest()
    except:
        return None


def classify(filepath):
    suffix = filepath.suffix.lower()
    file_type = ROUTES.get(suffix, "unknown")

    # Detect source from path
    source = "unknown"
    path_str = str(filepath)
    if "Willow" in path_str:
        source = "willow"
    elif "Aios Input" in path_str:
        source = "aios"
    elif "Handoff" in path_str:
        source = "handoff"
    elif "UTETY" in path_str:
        source = "utety"

    return {"name": filepath.name, "type": file_type, "source": source, "path": str(filepath)}


def check_queue(state):
    """Check QUEUE.md for new signals."""
    if not QUEUE_PATH.exists():
        return

    current_hash = get_file_hash(QUEUE_PATH)
    if current_hash != state.get("last_queue_hash"):
        log(f"QUEUE_CHANGED | {QUEUE_PATH.name}")
        state["last_queue_hash"] = current_hash


def scan_path(path):
    if not path.exists():
        return []
    files = []
    for item in path.iterdir():
        if item.is_file():
            files.append(item)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-consent", action="store_true")
    args = parser.parse_args()

    print("Unified Watcher")
    print(f"Watching: {len(WATCH_PATHS)} paths + QUEUE.md")

    if not args.no_consent:
        if input("Start? (yes/no): ").strip().lower() != "yes":
            return
    else:
        print("Background mode.")

    ensure_dirs()
    state = load_state()
    log(f"WATCHER_ON | paths={len(WATCH_PATHS)}")

    try:
        while True:
            # Check each watch path
            for watch_path in WATCH_PATHS:
                for filepath in scan_path(watch_path):
                    key = str(filepath)
                    file_hash = get_file_hash(filepath)

                    if key not in state["known_files"]:
                        info = classify(filepath)
                        log(f"NEW | {info['source']} | {info['name']} | type={info['type']}")
                        state["known_files"][key] = {"hash": file_hash, "first_seen": datetime.now().isoformat()}
                    elif state["known_files"][key].get("hash") != file_hash:
                        log(f"CHANGED | {filepath.name}")
                        state["known_files"][key]["hash"] = file_hash

            # Check queue
            check_queue(state)

            state["last_run"] = datetime.now().isoformat()
            save_state(state)
            time.sleep(POLL_INTERVAL)

    except KeyboardInterrupt:
        pass
    finally:
        log(f"WATCHER_OFF | files={len(state['known_files'])}")
        save_state(state)


if __name__ == "__main__":
    main()
