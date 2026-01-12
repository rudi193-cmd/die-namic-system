#!/usr/bin/env python3
"""
Eyes - Event-triggered screen capture

GOVERNANCE: This script must be started by human action only.
AI cannot invoke this script directly.
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    from PIL import ImageGrab
except ImportError:
    print("Need pillow: pip install pillow")
    sys.exit(1)

try:
    import pygetwindow as gw
except ImportError:
    print("Need pygetwindow: pip install pygetwindow")
    sys.exit(1)

try:
    import pyperclip
except ImportError:
    pyperclip = None  # Optional - clipboard detection disabled

# Config
HEARTBEAT_SECONDS = 12
OUT_DIR = Path(r"C:\Users\Sean\screenshots")
AUDIT_LOG = OUT_DIR / "eyes_audit.log"

# Auth detection patterns
# GOVERNANCE HS-006: Auth detection is for AUDIT ONLY.
# This data MUST NOT be used to infer trust state.
# Trust flows FROM human TO AI, explicitly declared.
# See: governance/HARD_STOPS.md
AUTH_PATTERNS = [
    "sign in", "log in", "login", "verify", "choose an account",
    "authenticate", "2fa", "two-factor", "two factor", "password",
    "oauth", "authorization", "authorize", "accounts.google",
    "accounts.microsoft", "login.microsoftonline", "confirm your identity"
]

# State
last_window = None
last_title = ""
last_clipboard = ""
last_heartbeat = time.time()
last_auth_state = False
frame_count = 0


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG, "a") as f:
        f.write(f"{msg} | {timestamp}\n")


def get_active_window_title():
    try:
        win = gw.getActiveWindow()
        return win.title if win else ""
    except:
        return ""


def is_auth_title(title):
    title_lower = title.lower()
    return any(pattern in title_lower for pattern in AUTH_PATTERNS)


def capture(reason):
    global frame_count
    frame_count += 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    out_file = OUT_DIR / f"screen_{timestamp}.png"

    try:
        img = ImageGrab.grab()
        img.save(out_file)
        print(f"[{reason}] {out_file}")
    except Exception as e:
        print(f"[{reason}] FAILED: {e}")


def main():
    global last_window, last_title, last_clipboard, last_heartbeat, last_auth_state

    # Consent
    print("Eyes (event-triggered) will capture your screen.")
    consent = input("Continue? (yes/no): ").strip().lower()
    if consent != "yes":
        print("Aborted.")
        return

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    log(f"EYES_ON | heartbeat={HEARTBEAT_SECONDS}s | mode=events | user={os.environ.get('USERNAME', 'unknown')}")

    print(f"Eyes online. Heartbeat: {HEARTBEAT_SECONDS}s + event triggers")
    print("Triggers: window focus, title change, clipboard, auth detection")
    print("Press Ctrl+C to stop")

    try:
        while True:
            now = time.time()
            current_title = get_active_window_title()

            # Event: Window/title changed
            if current_title != last_title and current_title:
                if last_title == "":
                    capture("FOCUS")
                else:
                    capture("TITLE")
                last_title = current_title
                last_heartbeat = now

            # Event: Auth flow detected
            is_auth = is_auth_title(current_title)
            if is_auth and not last_auth_state:
                capture("AUTH")
                log(f"AUTH_DETECTED | title={current_title}")
                last_heartbeat = now
            last_auth_state = is_auth

            # Event: Clipboard changed
            if pyperclip:
                try:
                    clip = pyperclip.paste()
                    if clip != last_clipboard and clip:
                        capture("CLIPBOARD")
                        last_clipboard = clip
                        last_heartbeat = now
                except:
                    pass

            # Heartbeat
            if now - last_heartbeat >= HEARTBEAT_SECONDS:
                capture("HEARTBEAT")
                last_heartbeat = now

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        log(f"EYES_OFF | frames={frame_count}")
        print(f"\nEyes off. {frame_count} frames captured.")


if __name__ == "__main__":
    main()
