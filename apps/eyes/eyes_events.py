#!/usr/bin/env python3
"""
Eyes - Event-triggered screen capture with trigger layer

GOVERNANCE: This script must be started by human action only.
AI cannot invoke this script directly.
"""

import os
import sys
import time
import threading
from datetime import datetime
from pathlib import Path

# Trigger layer
try:
    from triggers import process_screenshot, classify
    TRIGGERS_AVAILABLE = True
except ImportError:
    TRIGGERS_AVAILABLE = False

try:
    from PIL import ImageGrab
except ImportError:
    print("Need pillow: pip install pillow")
    sys.exit(1)

# Window title detection - try multiple methods
try:
    import ctypes
    user32 = ctypes.windll.user32

    def get_active_window_title_native():
        hwnd = user32.GetForegroundWindow()
        length = user32.GetWindowTextLengthW(hwnd)
        buf = ctypes.create_unicode_buffer(length + 1)
        user32.GetWindowTextW(hwnd, buf, length + 1)
        return buf.value

    GET_WINDOW_TITLE = get_active_window_title_native
    print("Using native Windows API for window detection")
except:
    try:
        import pygetwindow as gw
        GET_WINDOW_TITLE = lambda: gw.getActiveWindow().title if gw.getActiveWindow() else ""
        print("Using pygetwindow for window detection")
    except ImportError:
        GET_WINDOW_TITLE = lambda: ""
        print("Warning: No window detection available")

try:
    import pyperclip
except ImportError:
    pyperclip = None  # Optional - clipboard detection disabled

try:
    from pynput import mouse, keyboard
    PYNPUT_AVAILABLE = True
except ImportError:
    PYNPUT_AVAILABLE = False
    print("Note: pip install pynput for mouse/keystroke detection")

# Config
HEARTBEAT_SECONDS = 12
IDLE_THRESHOLD_SECONDS = 30  # Consider idle after 30s no input
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

# Activity tracking (mouse/keyboard)
# GOVERNANCE: We track THAT activity happens, not WHAT.
# No keystroke content. No mouse coordinates. Just presence.
last_activity = time.time()
is_idle = False
keystroke_count = 0  # Count only, no content
mouse_move_count = 0


def log(msg):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(AUDIT_LOG, "a") as f:
        f.write(f"{msg} | {timestamp}\n")


def on_mouse_move(x, y):
    """Track mouse activity (not position)."""
    global last_activity, mouse_move_count
    last_activity = time.time()
    mouse_move_count += 1


def on_mouse_click(x, y, button, pressed):
    """Track click activity."""
    global last_activity
    if pressed:
        last_activity = time.time()


def on_key_press(key):
    """Track keystroke activity (not content)."""
    global last_activity, keystroke_count
    last_activity = time.time()
    keystroke_count += 1


def start_activity_listeners():
    """Start mouse/keyboard listeners in background threads."""
    if not PYNPUT_AVAILABLE:
        return None, None

    mouse_listener = mouse.Listener(
        on_move=on_mouse_move,
        on_click=on_mouse_click
    )
    keyboard_listener = keyboard.Listener(
        on_press=on_key_press
    )

    mouse_listener.start()
    keyboard_listener.start()

    return mouse_listener, keyboard_listener


def get_active_window_title():
    try:
        return GET_WINDOW_TITLE()
    except:
        return ""


def is_auth_title(title):
    title_lower = title.lower()
    return any(pattern in title_lower for pattern in AUTH_PATTERNS)


def capture(reason, title=None):
    global frame_count
    frame_count += 1
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    out_file = OUT_DIR / f"screen_{timestamp}.png"

    try:
        img = ImageGrab.grab()
        img.save(out_file)
        print(f"[{reason}] {out_file}")

        # Process through trigger layer
        if TRIGGERS_AVAILABLE and title:
            result = process_screenshot(str(out_file), title)
            if result["triggers_fired"] > 0:
                print(f"  → {result['triggers_fired']} trigger(s) fired")
            if result["routed_to"]:
                print(f"  → routed to {result['project']}")

    except Exception as e:
        print(f"[{reason}] FAILED: {e}")


def main():
    global last_window, last_title, last_clipboard, last_heartbeat, last_auth_state
    global last_activity, is_idle, keystroke_count, mouse_move_count

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-consent", action="store_true",
                        help="Skip consent prompt (for background service)")
    args = parser.parse_args()

    # Consent
    print("Eyes (event-triggered) will capture your screen.")
    if not args.no_consent:
        consent = input("Continue? (yes/no): ").strip().lower()
        if consent != "yes":
            print("Aborted.")
            return
    else:
        print("Background mode: consent assumed from human startup.")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # Start activity listeners
    mouse_listener, keyboard_listener = start_activity_listeners()
    activity_mode = "full" if PYNPUT_AVAILABLE else "limited"

    log(f"EYES_ON | heartbeat={HEARTBEAT_SECONDS}s | mode=events | activity={activity_mode} | user={os.environ.get('USERNAME', 'unknown')}")

    print(f"Eyes online. Heartbeat: {HEARTBEAT_SECONDS}s + event triggers")
    triggers = ["window focus", "title change", "clipboard", "auth detection"]
    if PYNPUT_AVAILABLE:
        triggers.extend(["mouse activity", "keystroke activity", "idle detection"])
    print(f"Triggers: {', '.join(triggers)}")
    if TRIGGERS_AVAILABLE:
        print("Trigger layer: ACTIVE (routing + pattern detection)")
    else:
        print("Trigger layer: DISABLED (triggers.py not found)")
    print("Press Ctrl+C to stop")

    try:
        while True:
            now = time.time()
            current_title = get_active_window_title()

            # Event: Window/title changed
            if current_title != last_title and current_title:
                if last_title == "":
                    capture("FOCUS", current_title)
                else:
                    capture("TITLE", current_title)
                last_title = current_title
                last_heartbeat = now

            # Event: Auth flow detected
            is_auth = is_auth_title(current_title)
            if is_auth and not last_auth_state:
                capture("AUTH", current_title)
                log(f"AUTH_DETECTED | title={current_title}")
                last_heartbeat = now
            last_auth_state = is_auth

            # Event: Idle detection and return from idle
            if PYNPUT_AVAILABLE:
                idle_duration = now - last_activity

                # Went idle
                if not is_idle and idle_duration >= IDLE_THRESHOLD_SECONDS:
                    is_idle = True
                    capture("IDLE", current_title)
                    log(f"IDLE_START | after={IDLE_THRESHOLD_SECONDS}s inactivity")

                # Returned from idle
                elif is_idle and idle_duration < 1:
                    is_idle = False
                    capture("RETURN", current_title)
                    log(f"IDLE_END | keys={keystroke_count} | mouse={mouse_move_count}")
                    keystroke_count = 0
                    mouse_move_count = 0
                    last_heartbeat = now

            # Event: Clipboard changed
            if pyperclip:
                try:
                    clip = pyperclip.paste()
                    if clip != last_clipboard and clip:
                        capture("CLIPBOARD", current_title)
                        last_clipboard = clip
                        last_heartbeat = now
                except:
                    pass

            # Heartbeat
            if now - last_heartbeat >= HEARTBEAT_SECONDS:
                capture("HEARTBEAT", current_title)
                last_heartbeat = now

            time.sleep(0.1)

    except KeyboardInterrupt:
        pass
    finally:
        # Stop listeners
        if mouse_listener:
            mouse_listener.stop()
        if keyboard_listener:
            keyboard_listener.stop()

        log(f"EYES_OFF | frames={frame_count} | total_keys={keystroke_count} | total_mouse={mouse_move_count}")
        print(f"\nEyes off. {frame_count} frames captured.")
        if PYNPUT_AVAILABLE:
            print(f"Activity: {keystroke_count} keystrokes, {mouse_move_count} mouse moves")


if __name__ == "__main__":
    main()
