#!/usr/bin/env python3
"""
Mobile Auth — Context-Aware Authentication Layer

Layered security based on location and context:
- Local network (192.168.x.x, 10.x.x.x) → PIN only
- External/unknown → Full auth (user + password)
- Known device → Session persistence
- Unknown device → Full verification
- AI nodes → API key + origin fingerprint

User Types:
- human: Real users (password + PIN)
- faculty: Faculty personas (password + PIN, limited scope)
- node: AI systems (API key + origin signature)

AUTHOR: Kartikeya (CMD)
VERSION: 2.0.0
"""

import streamlit as st
import hashlib
import json
import time
import uuid
import secrets
import ipaddress
from pathlib import Path
from datetime import datetime, timedelta
from typing import Optional, Dict, Tuple, List

# === CONFIGURATION ===
AUTH_CONFIG_PATH = Path(__file__).parent / "auth_config.json"
DEVICES_PATH = Path(__file__).parent / "known_devices.json"
SESSION_DURATION_HOURS = 24
PIN_SESSION_HOURS = 4  # Shorter for PIN-only auth

# User type definitions
USER_TYPES = {
    "human": {"auth_methods": ["password", "pin"], "can_manage_users": True},
    "faculty": {"auth_methods": ["password", "pin"], "can_manage_users": False},
    "node": {"auth_methods": ["api_key"], "can_manage_users": False},
}

# Pre-seeded accounts (created on first run if not exists)
SEED_ACCOUNTS = {
    # Humans
    "sean": {
        "user_type": "human",
        "role": "admin",
        "display_name": "SweetPea",
        "password_hash": None,  # Set on first run
        "pin_hash": None,
    },
    # Faculty (Claude personas)
    "oakenscroll": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Oakenscroll",
        "domain": "Theory, Physics of Absurdity",
    },
    "riggs": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Riggs",
        "domain": "Applied Reality Engineering",
    },
    "hanz": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Hanz",
        "domain": "Coding, Emotional Support",
    },
    "nova": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Nova Hale",
        "domain": "Narrative",
    },
    "ada": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Ada Turing",
        "domain": "Systems",
    },
    "alexis": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Alexis",
        "domain": "Biology, Living Systems",
    },
    "ofshield": {
        "user_type": "faculty",
        "role": "faculty",
        "display_name": "Prof. Ofshield",
        "domain": "Gate, Security",
    },
    "gerald": {
        "user_type": "faculty",
        "role": "dean",
        "display_name": "Gerald Prime",
        "domain": "Absurdist Dispatches, The Binder",
    },
    "willow": {
        "user_type": "faculty",
        "role": "campus",
        "display_name": "Willow",
        "domain": "Integration, The Whole Brain",
    },
    # AI Nodes
    "aios": {
        "user_type": "node",
        "role": "system",
        "display_name": "AIOS",
        "domain": "Operating System Layer",
        "api_key": None,  # Generated on setup
        "allowed_origins": ["localhost", "127.0.0.1"],
    },
    "consus": {
        "user_type": "node",
        "role": "system",
        "display_name": "Consus",
        "domain": "Generation, Code Synthesis",
        "api_key": None,
        "allowed_origins": ["localhost", "127.0.0.1"],
    },
    "kartikeya": {
        "user_type": "node",
        "role": "system",
        "display_name": "Kartikeya (CMD)",
        "domain": "Building, Infrastructure",
        "api_key": None,
        "allowed_origins": ["localhost", "127.0.0.1"],
    },
    "pm_claude": {
        "user_type": "node",
        "role": "system",
        "display_name": "PM Claude",
        "domain": "Coordination, Routing",
        "api_key": None,
        "allowed_origins": ["localhost", "127.0.0.1"],
    },
    "stats_tracking": {
        "user_type": "node",
        "role": "system",
        "display_name": "Stats Tracking",
        "domain": "Analytics, Metrics",
        "api_key": None,
        "allowed_origins": ["localhost", "127.0.0.1"],
    },
}

# Default config structure
DEFAULT_CONFIG = {
    "users": {},
    "security": {
        "local_networks": ["192.168.0.0/16", "10.0.0.0/8", "172.16.0.0/12"],
        "require_full_auth_external": True,
        "max_failed_attempts": 5,
        "lockout_minutes": 15,
        "allow_device_remember": True,
        "node_require_origin_match": True,
    },
    "initialized": False,
}


def _hash(value: str) -> str:
    """SHA-256 hash for passwords/PINs."""
    return hashlib.sha256(value.encode()).hexdigest()


def _generate_api_key() -> str:
    """Generate a secure API key for node auth."""
    return f"wlw_{secrets.token_urlsafe(32)}"


def _hash_api_key(key: str) -> str:
    """Hash API key for storage (we only store hashes)."""
    return _hash(key)


def _load_config() -> dict:
    """Load auth config, create default if missing."""
    if AUTH_CONFIG_PATH.exists():
        with open(AUTH_CONFIG_PATH) as f:
            return json.load(f)
    return DEFAULT_CONFIG.copy()


def _save_config(config: dict):
    """Save auth config."""
    with open(AUTH_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)


def _seed_accounts(config: dict) -> Tuple[dict, Dict[str, str]]:
    """
    Seed initial accounts from SEED_ACCOUNTS.
    Returns (updated_config, new_api_keys) where new_api_keys maps node_name -> plaintext key.
    """
    new_api_keys = {}

    for username, seed_data in SEED_ACCOUNTS.items():
        if username not in config["users"]:
            user_data = seed_data.copy()

            # Generate API key for nodes
            if user_data.get("user_type") == "node" and user_data.get("api_key") is None:
                plaintext_key = _generate_api_key()
                user_data["api_key_hash"] = _hash_api_key(plaintext_key)
                user_data["api_key_prefix"] = plaintext_key[:12]  # For identification
                del user_data["api_key"]  # Don't store plaintext
                new_api_keys[username] = plaintext_key

            config["users"][username] = user_data

    return config, new_api_keys


def _load_devices() -> dict:
    """Load known devices."""
    if DEVICES_PATH.exists():
        with open(DEVICES_PATH) as f:
            return json.load(f)
    return {"devices": {}}


def _save_devices(devices: dict):
    """Save known devices."""
    with open(DEVICES_PATH, 'w') as f:
        json.dump(devices, f, indent=2)


def _get_client_context() -> Dict:
    """
    Gather client context for auth decisions.
    Returns IP, network type, device fingerprint hints.
    """
    # Get headers from Streamlit (using new API)
    try:
        headers = dict(st.context.headers) if hasattr(st, 'context') else {}
    except:
        headers = {}

    # Try to get real IP (check forwarded headers first)
    client_ip = headers.get('X-Forwarded-For', headers.get('X-Real-IP', '127.0.0.1'))
    if ',' in client_ip:
        client_ip = client_ip.split(',')[0].strip()

    # Determine if local network
    config = _load_config()
    is_local = False

    # Localhost is always local
    if client_ip in ['127.0.0.1', 'localhost', '::1']:
        is_local = True
    else:
        try:
            ip_obj = ipaddress.ip_address(client_ip)
            for network in config["security"]["local_networks"]:
                if ip_obj in ipaddress.ip_network(network):
                    is_local = True
                    break
        except ValueError:
            # Can't parse IP, assume external
            pass

    # Device fingerprint (basic - user agent based)
    user_agent = headers.get('User-Agent', 'unknown')
    device_hint = _hash(user_agent)[:16]

    return {
        "ip": client_ip,
        "is_local": is_local,
        "device_hint": device_hint,
        "user_agent": user_agent,
        "timestamp": datetime.now().isoformat()
    }


def _check_device_remembered(device_hint: str, username: str) -> Optional[Dict]:
    """Check if device is remembered for this user."""
    devices = _load_devices()
    key = f"{username}:{device_hint}"

    if key in devices["devices"]:
        device = devices["devices"][key]
        expires = datetime.fromisoformat(device["expires"])
        if datetime.now() < expires:
            return device
        else:
            # Expired, remove it
            del devices["devices"][key]
            _save_devices(devices)

    return None


def _remember_device(device_hint: str, username: str, auth_level: str):
    """Remember this device for the user."""
    devices = _load_devices()
    key = f"{username}:{device_hint}"

    devices["devices"][key] = {
        "username": username,
        "auth_level": auth_level,
        "created": datetime.now().isoformat(),
        "expires": (datetime.now() + timedelta(days=30)).isoformat(),
        "device_hint": device_hint
    }

    _save_devices(devices)


def _check_lockout(username: str) -> Tuple[bool, int]:
    """Check if user is locked out. Returns (is_locked, minutes_remaining)."""
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = {}

    config = _load_config()
    max_attempts = config["security"]["max_failed_attempts"]
    lockout_mins = config["security"]["lockout_minutes"]

    if username in st.session_state.failed_attempts:
        attempts, last_attempt = st.session_state.failed_attempts[username]
        elapsed = (datetime.now() - last_attempt).total_seconds() / 60

        if attempts >= max_attempts and elapsed < lockout_mins:
            return True, int(lockout_mins - elapsed)
        elif elapsed >= lockout_mins:
            # Reset after lockout period
            del st.session_state.failed_attempts[username]

    return False, 0


def _record_failed_attempt(username: str):
    """Record a failed login attempt."""
    if "failed_attempts" not in st.session_state:
        st.session_state.failed_attempts = {}

    if username in st.session_state.failed_attempts:
        attempts, _ = st.session_state.failed_attempts[username]
        st.session_state.failed_attempts[username] = (attempts + 1, datetime.now())
    else:
        st.session_state.failed_attempts[username] = (1, datetime.now())


def _clear_failed_attempts(username: str):
    """Clear failed attempts on successful login."""
    if "failed_attempts" in st.session_state and username in st.session_state.failed_attempts:
        del st.session_state.failed_attempts[username]


# === NODE AUTHENTICATION ===

def validate_api_key(api_key: str, origin_ip: str = None) -> Optional[Dict]:
    """
    Validate an API key for node authentication.
    Returns user data if valid, None otherwise.
    """
    if not api_key or not api_key.startswith("wlw_"):
        return None

    config = _load_config()
    key_hash = _hash_api_key(api_key)

    for username, user_data in config["users"].items():
        if user_data.get("user_type") != "node":
            continue

        if user_data.get("api_key_hash") == key_hash:
            # Check origin if required
            if config["security"].get("node_require_origin_match") and origin_ip:
                allowed = user_data.get("allowed_origins", [])
                if allowed and origin_ip not in allowed:
                    # Check if origin is in allowed networks
                    origin_allowed = False
                    try:
                        ip_obj = ipaddress.ip_address(origin_ip)
                        for network in config["security"]["local_networks"]:
                            if ip_obj in ipaddress.ip_network(network):
                                origin_allowed = True
                                break
                    except ValueError:
                        pass

                    if not origin_allowed:
                        return None

            return {"username": username, **user_data}

    return None


def get_node_fingerprint(headers: Dict) -> str:
    """
    Generate a fingerprint for a node based on its request characteristics.
    Used to identify and track node sessions.
    """
    components = [
        headers.get("User-Agent", ""),
        headers.get("X-Node-ID", ""),
        headers.get("X-Project-ID", ""),
        headers.get("X-Session-ID", ""),
    ]
    return _hash("|".join(components))[:24]


def authenticate_node_request(api_key: str, headers: Dict = None) -> Optional[Dict]:
    """
    Full node authentication: API key + origin validation + fingerprinting.
    Returns session info if authenticated.
    """
    headers = headers or {}
    origin_ip = headers.get("X-Forwarded-For", headers.get("X-Real-IP", "127.0.0.1"))
    if "," in origin_ip:
        origin_ip = origin_ip.split(",")[0].strip()

    user_data = validate_api_key(api_key, origin_ip)
    if not user_data:
        return None

    fingerprint = get_node_fingerprint(headers)

    return {
        "authenticated": True,
        "username": user_data["username"],
        "display_name": user_data.get("display_name", user_data["username"]),
        "user_type": "node",
        "role": user_data.get("role", "system"),
        "domain": user_data.get("domain", ""),
        "fingerprint": fingerprint,
        "origin_ip": origin_ip,
        "timestamp": datetime.now().isoformat(),
    }


# === USER MANAGEMENT ===

def list_users(user_type: str = None) -> List[Dict]:
    """List all users, optionally filtered by type."""
    config = _load_config()
    users = []

    for username, data in config["users"].items():
        if user_type and data.get("user_type") != user_type:
            continue
        users.append({
            "username": username,
            "display_name": data.get("display_name", username),
            "user_type": data.get("user_type", "human"),
            "role": data.get("role", "user"),
            "domain": data.get("domain", ""),
            "has_password": bool(data.get("password_hash")),
            "has_pin": bool(data.get("pin_hash")),
            "has_api_key": bool(data.get("api_key_hash")),
            "api_key_prefix": data.get("api_key_prefix", ""),
        })

    return users


def create_user(
    username: str,
    display_name: str,
    user_type: str,
    role: str = "user",
    password: str = None,
    pin: str = None,
    domain: str = "",
    allowed_origins: List[str] = None,
) -> Tuple[bool, str, Optional[str]]:
    """
    Create a new user account.
    Returns (success, message, api_key_if_node).
    """
    config = _load_config()

    if username in config["users"]:
        return False, f"User '{username}' already exists", None

    if user_type not in USER_TYPES:
        return False, f"Invalid user type: {user_type}", None

    user_data = {
        "user_type": user_type,
        "role": role,
        "display_name": display_name,
        "domain": domain,
        "created": datetime.now().isoformat(),
    }

    api_key = None

    if user_type == "node":
        # Generate API key for nodes
        api_key = _generate_api_key()
        user_data["api_key_hash"] = _hash_api_key(api_key)
        user_data["api_key_prefix"] = api_key[:12]
        user_data["allowed_origins"] = allowed_origins or ["localhost", "127.0.0.1"]
    else:
        # Human/faculty need password and/or PIN
        if password:
            user_data["password_hash"] = _hash(password)
        if pin:
            user_data["pin_hash"] = _hash(pin)

    config["users"][username] = user_data
    _save_config(config)

    return True, f"User '{username}' created successfully", api_key


def update_user(
    username: str,
    display_name: str = None,
    password: str = None,
    pin: str = None,
    role: str = None,
    domain: str = None,
    allowed_origins: List[str] = None,
) -> Tuple[bool, str]:
    """Update an existing user."""
    config = _load_config()

    if username not in config["users"]:
        return False, f"User '{username}' not found"

    user_data = config["users"][username]

    if display_name:
        user_data["display_name"] = display_name
    if role:
        user_data["role"] = role
    if domain is not None:
        user_data["domain"] = domain
    if password:
        user_data["password_hash"] = _hash(password)
    if pin:
        user_data["pin_hash"] = _hash(pin)
    if allowed_origins is not None and user_data.get("user_type") == "node":
        user_data["allowed_origins"] = allowed_origins

    user_data["updated"] = datetime.now().isoformat()
    config["users"][username] = user_data
    _save_config(config)

    return True, f"User '{username}' updated"


def delete_user(username: str) -> Tuple[bool, str]:
    """Delete a user account."""
    config = _load_config()

    if username not in config["users"]:
        return False, f"User '{username}' not found"

    # Prevent deleting the last admin
    user_data = config["users"][username]
    if user_data.get("role") == "admin":
        admin_count = sum(1 for u in config["users"].values() if u.get("role") == "admin")
        if admin_count <= 1:
            return False, "Cannot delete the last admin account"

    del config["users"][username]
    _save_config(config)

    return True, f"User '{username}' deleted"


def regenerate_api_key(username: str) -> Tuple[bool, str, Optional[str]]:
    """Regenerate API key for a node account."""
    config = _load_config()

    if username not in config["users"]:
        return False, f"User '{username}' not found", None

    user_data = config["users"][username]
    if user_data.get("user_type") != "node":
        return False, f"User '{username}' is not a node account", None

    new_key = _generate_api_key()
    user_data["api_key_hash"] = _hash_api_key(new_key)
    user_data["api_key_prefix"] = new_key[:12]
    user_data["key_regenerated"] = datetime.now().isoformat()

    config["users"][username] = user_data
    _save_config(config)

    return True, f"API key regenerated for '{username}'", new_key


def init_first_run() -> Tuple[bool, Dict[str, str]]:
    """
    Initialize on first run. Seeds accounts if needed.
    Returns (needs_human_setup, new_api_keys).
    """
    config = _load_config()
    new_api_keys = {}

    # Seed accounts if not initialized
    if not config.get("initialized"):
        config, new_api_keys = _seed_accounts(config)
        config["initialized"] = True
        _save_config(config)

    # Check if human admin has credentials set
    needs_setup = True
    for user, data in config["users"].items():
        if data.get("user_type") == "human" and data.get("role") == "admin":
            if data.get("password_hash") and data.get("pin_hash"):
                needs_setup = False
                break

    return needs_setup, new_api_keys


def setup_credentials(new_api_keys: Dict[str, str] = None):
    """First-run setup UI for credentials."""
    st.title("🔐 First-Time Setup")
    st.markdown("Set up your authentication credentials.")

    # Show generated API keys if this is first run
    if new_api_keys:
        st.warning("**IMPORTANT:** Save these API keys now. They will NOT be shown again!")
        with st.expander("🔑 Generated Node API Keys", expanded=True):
            for node_name, api_key in new_api_keys.items():
                st.code(f"{node_name}: {api_key}", language=None)
            st.caption("Store these securely. You'll need them to authenticate node connections.")

    with st.form("setup_form"):
        st.subheader("Create Admin Account")

        username = st.text_input("Username", value="sean")
        display_name = st.text_input("Display Name", value="SweetPea")
        password = st.text_input("Password (for external access)", type="password")
        password_confirm = st.text_input("Confirm Password", type="password")
        pin = st.text_input("PIN (4-6 digits, for local/quick access)", type="password", max_chars=6)
        pin_confirm = st.text_input("Confirm PIN", type="password", max_chars=6)

        submitted = st.form_submit_button("Complete Setup", type="primary")

        if submitted:
            errors = []

            if not username:
                errors.append("Username required")
            if not password or len(password) < 8:
                errors.append("Password must be at least 8 characters")
            if password != password_confirm:
                errors.append("Passwords don't match")
            if not pin or not pin.isdigit() or len(pin) < 4:
                errors.append("PIN must be 4-6 digits")
            if pin != pin_confirm:
                errors.append("PINs don't match")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                config = _load_config()
                # Update existing seeded user or create new
                if username in config["users"]:
                    config["users"][username]["password_hash"] = _hash(password)
                    config["users"][username]["pin_hash"] = _hash(pin)
                    config["users"][username]["display_name"] = display_name
                else:
                    config["users"][username] = {
                        "user_type": "human",
                        "password_hash": _hash(password),
                        "pin_hash": _hash(pin),
                        "role": "admin",
                        "display_name": display_name
                    }
                _save_config(config)
                st.success("Setup complete! Refreshing...")
                time.sleep(1)
                st.rerun()

    return False  # Not authenticated yet


def render_login() -> bool:
    """
    Render appropriate login UI based on context.
    Returns True if authenticated, False otherwise.
    """
    # Check if already authenticated this session
    if st.session_state.get("authenticated"):
        return True

    # First run check - seeds accounts and checks if human setup needed
    needs_setup, new_api_keys = init_first_run()

    # Store new API keys in session to persist across reruns during setup
    if new_api_keys:
        st.session_state.new_api_keys = new_api_keys

    if needs_setup:
        return setup_credentials(st.session_state.get("new_api_keys"))

    # Clear stored API keys after setup complete
    if "new_api_keys" in st.session_state:
        del st.session_state.new_api_keys

    # Get client context
    context = _get_client_context()
    config = _load_config()

    # Check for remembered device
    for username, user_data in config["users"].items():
        remembered = _check_device_remembered(context["device_hint"], username)
        if remembered:
            # Auto-login from remembered device (still show quick PIN for security)
            return _render_pin_login(username, user_data, context, remembered=True)

    # Context-based auth selection
    if context["is_local"]:
        # Local network: PIN-first, with option for full login
        return _render_local_login(context)
    else:
        # External: Full authentication required
        return _render_full_login(context)


def _render_local_login(context: Dict) -> bool:
    """Local network login - PIN primary, full login secondary."""
    st.title("🏠 Local Access")
    st.caption(f"Network: Local ({context['ip']})")

    config = _load_config()

    tab1, tab2 = st.tabs(["Quick PIN", "Full Login"])

    with tab1:
        return _render_pin_form(config, context)

    with tab2:
        return _render_full_form(config, context)


def _render_full_login(context: Dict) -> bool:
    """External network login - Full auth required."""
    st.title("🔐 Secure Login")
    st.caption(f"External access detected ({context['ip']})")
    st.warning("Full authentication required for external access.")

    config = _load_config()
    return _render_full_form(config, context)


def _render_pin_login(username: str, user_data: Dict, context: Dict, remembered: bool = False) -> bool:
    """Quick PIN login for known user/device."""
    st.title(f"👋 Welcome back, {user_data.get('display_name', username)}")

    if remembered:
        st.caption("Remembered device - PIN to confirm")

    config = _load_config()

    # Check lockout
    locked, mins = _check_lockout(username)
    if locked:
        st.error(f"Account locked. Try again in {mins} minutes.")
        return False

    with st.form("pin_form"):
        pin = st.text_input("Enter PIN", type="password", max_chars=6)
        submitted = st.form_submit_button("Unlock", type="primary")

        if submitted:
            if user_data.get("pin_hash") == _hash(pin):
                _clear_failed_attempts(username)
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.display_name = user_data.get("display_name", username)
                st.session_state.role = user_data.get("role", "user")
                st.session_state.auth_level = "pin"
                st.session_state.auth_context = context
                st.rerun()
            else:
                _record_failed_attempt(username)
                st.error("Invalid PIN")

    # Option to use full login instead
    if st.button("Use full login instead"):
        st.session_state.force_full_login = True
        st.rerun()

    return False


def _render_pin_form(config: Dict, context: Dict) -> bool:
    """PIN entry form."""
    # Filter to users with PINs (human/faculty only, not nodes)
    pin_users = [
        u for u, d in config["users"].items()
        if d.get("pin_hash") and d.get("user_type") in ("human", "faculty", None)
    ]

    if not pin_users:
        st.warning("No users with PIN configured.")
        return False

    with st.form("pin_form"):
        username = st.selectbox(
            "User",
            options=pin_users,
            format_func=lambda x: config["users"][x].get("display_name", x)
        )
        pin = st.text_input("PIN", type="password", max_chars=6)
        remember = st.checkbox("Remember this device", value=True)
        submitted = st.form_submit_button("Unlock", type="primary")

        if submitted:
            # Check lockout
            locked, mins = _check_lockout(username)
            if locked:
                st.error(f"Account locked. Try again in {mins} minutes.")
                return False

            user_data = config["users"].get(username, {})
            if user_data.get("pin_hash") == _hash(pin):
                _clear_failed_attempts(username)

                if remember and config["security"]["allow_device_remember"]:
                    _remember_device(context["device_hint"], username, "pin")

                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.display_name = user_data.get("display_name", username)
                st.session_state.role = user_data.get("role", "user")
                st.session_state.auth_level = "pin"
                st.session_state.auth_context = context
                st.rerun()
            else:
                _record_failed_attempt(username)
                st.error("Invalid PIN")

    return False


def _render_full_form(config: Dict, context: Dict) -> bool:
    """Full username/password form."""
    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        remember = st.checkbox("Remember this device", value=False)
        submitted = st.form_submit_button("Login", type="primary")

        if submitted:
            # Check lockout
            locked, mins = _check_lockout(username)
            if locked:
                st.error(f"Account locked. Try again in {mins} minutes.")
                return False

            user_data = config["users"].get(username, {})
            if user_data and user_data.get("password_hash") == _hash(password):
                _clear_failed_attempts(username)

                if remember and config["security"]["allow_device_remember"]:
                    _remember_device(context["device_hint"], username, "full")

                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.display_name = user_data.get("display_name", username)
                st.session_state.role = user_data.get("role", "user")
                st.session_state.auth_level = "full"
                st.session_state.auth_context = context
                st.rerun()
            else:
                _record_failed_attempt(username)
                st.error("Invalid username or password")

    return False


def require_auth(func):
    """Decorator to require authentication for a page/function."""
    def wrapper(*args, **kwargs):
        if not render_login():
            st.stop()
        return func(*args, **kwargs)
    return wrapper


def logout():
    """Clear authentication state."""
    keys_to_clear = ['authenticated', 'username', 'display_name', 'role',
                     'auth_level', 'auth_context', 'force_full_login']
    for key in keys_to_clear:
        if key in st.session_state:
            del st.session_state[key]


def get_current_user() -> Optional[Dict]:
    """Get current authenticated user info."""
    if st.session_state.get("authenticated"):
        return {
            "username": st.session_state.get("username"),
            "display_name": st.session_state.get("display_name"),
            "role": st.session_state.get("role"),
            "auth_level": st.session_state.get("auth_level"),
            "context": st.session_state.get("auth_context", {})
        }
    return None


def render_auth_status():
    """Render auth status in sidebar."""
    user = get_current_user()
    if user:
        st.sidebar.divider()
        st.sidebar.markdown("**Session**")
        auth_icon = "🔐" if user["auth_level"] == "full" else "📍"
        network_icon = "🏠" if user["context"].get("is_local") else "🌐"
        st.sidebar.code(f"{auth_icon} {user['display_name']}\n{network_icon} {user['auth_level'].upper()}")

        if st.sidebar.button("Logout", key="logout_btn"):
            logout()
            st.rerun()


# === ADMIN PANEL ===

def render_admin_panel():
    """Render user management admin panel. Only for admin users."""
    user = get_current_user()
    if not user or user.get("role") != "admin":
        st.warning("Admin access required.")
        return

    st.markdown("### User Management")

    # Tabs for different user types
    tab_humans, tab_faculty, tab_nodes, tab_create = st.tabs([
        "Humans", "Faculty", "Nodes", "Create User"
    ])

    with tab_humans:
        _render_user_list("human")

    with tab_faculty:
        _render_user_list("faculty")

    with tab_nodes:
        _render_node_list()

    with tab_create:
        _render_create_user_form()


def _render_user_list(user_type: str):
    """Render list of human/faculty users."""
    users = list_users(user_type)

    if not users:
        st.info(f"No {user_type} users found.")
        return

    for u in users:
        with st.expander(f"{u['display_name']} (@{u['username']})", expanded=False):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Role:** {u['role']}")
                st.markdown(f"**Domain:** {u['domain'] or 'N/A'}")
            with col2:
                st.markdown(f"**Has Password:** {'Yes' if u['has_password'] else 'No'}")
                st.markdown(f"**Has PIN:** {'Yes' if u['has_pin'] else 'No'}")

            # Edit form
            with st.form(f"edit_{u['username']}"):
                new_display = st.text_input("Display Name", value=u['display_name'])
                new_password = st.text_input("New Password (leave blank to keep)", type="password")
                new_pin = st.text_input("New PIN (leave blank to keep)", type="password", max_chars=6)

                col_save, col_del = st.columns(2)
                with col_save:
                    if st.form_submit_button("Save Changes"):
                        success, msg = update_user(
                            u['username'],
                            display_name=new_display if new_display != u['display_name'] else None,
                            password=new_password if new_password else None,
                            pin=new_pin if new_pin else None,
                        )
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)

                with col_del:
                    if st.form_submit_button("Delete User", type="secondary"):
                        success, msg = delete_user(u['username'])
                        if success:
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)


def _render_node_list():
    """Render list of node accounts with API key management."""
    nodes = list_users("node")

    if not nodes:
        st.info("No node accounts found.")
        return

    for n in nodes:
        with st.expander(f"{n['display_name']} (@{n['username']})", expanded=False):
            st.markdown(f"**Domain:** {n['domain'] or 'N/A'}")
            st.markdown(f"**API Key Prefix:** `{n['api_key_prefix']}...`")

            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"Regenerate API Key", key=f"regen_{n['username']}"):
                    success, msg, new_key = regenerate_api_key(n['username'])
                    if success and new_key:
                        st.warning("**Save this key now!** It won't be shown again.")
                        st.code(new_key, language=None)
                    elif not success:
                        st.error(msg)

            with col2:
                if st.button(f"Delete Node", key=f"del_{n['username']}"):
                    success, msg = delete_user(n['username'])
                    if success:
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)


def _render_create_user_form():
    """Render form to create new user."""
    with st.form("create_user_form"):
        st.subheader("Create New User")

        user_type = st.selectbox("User Type", ["human", "faculty", "node"])
        username = st.text_input("Username (lowercase, no spaces)")
        display_name = st.text_input("Display Name")
        role = st.selectbox("Role", ["user", "faculty", "admin", "system", "dean", "campus"])
        domain = st.text_input("Domain (optional)", help="Area of expertise or responsibility")

        # Conditional fields based on type
        password = None
        pin = None
        origins = None

        if user_type in ("human", "faculty"):
            password = st.text_input("Password", type="password")
            pin = st.text_input("PIN (4-6 digits)", type="password", max_chars=6)
        else:
            origins_str = st.text_input(
                "Allowed Origins (comma-separated)",
                value="localhost,127.0.0.1",
                help="IP addresses or hostnames allowed to use this API key"
            )
            origins = [o.strip() for o in origins_str.split(",") if o.strip()]

        submitted = st.form_submit_button("Create User", type="primary")

        if submitted:
            # Validate
            errors = []
            if not username or " " in username:
                errors.append("Username required (no spaces)")
            if not display_name:
                errors.append("Display name required")
            if user_type in ("human", "faculty"):
                if password and len(password) < 8:
                    errors.append("Password must be at least 8 characters")
                if pin and (not pin.isdigit() or len(pin) < 4):
                    errors.append("PIN must be 4-6 digits")

            if errors:
                for e in errors:
                    st.error(e)
            else:
                success, msg, api_key = create_user(
                    username=username.lower(),
                    display_name=display_name,
                    user_type=user_type,
                    role=role,
                    password=password,
                    pin=pin,
                    domain=domain,
                    allowed_origins=origins,
                )

                if success:
                    st.success(msg)
                    if api_key:
                        st.warning("**Save this API key now!** It won't be shown again.")
                        st.code(api_key, language=None)
                else:
                    st.error(msg)
