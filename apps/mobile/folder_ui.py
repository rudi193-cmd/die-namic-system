#!/usr/bin/env python3
"""
Folder-as-Persona UI — Spatial Navigation

Navigate to a folder = talk to that persona.
The file system IS the interface.

Based on Mitra's vision (SIG-041).

AUTHOR: Kartikeya (CMD)
VERSION: 1.0.0
"""

import streamlit as st
from typing import Optional, List, Dict
from pathlib import Path

# === FOLDER STRUCTURE ===
# Maps virtual folders to personas and their properties

FOLDER_TREE = {
    "Willow": {
        "type": "root",
        "persona": "Willow",
        "icon": "🏛️",
        "description": "The Campus — where all paths begin",
        "children": ["UTETY", "Infrastructure", "Inbox"]
    },
    "UTETY": {
        "type": "faculty_hub",
        "persona": None,  # Context-routed
        "icon": "🎓",
        "description": "University of Technical Entropy — faculty picks responder",
        "children": ["Oakenscroll", "Riggs", "Hanz", "Nova", "Ada", "Alexis", "Ofshield", "Gerald", "Faculty_Lounge"]
    },
    "Oakenscroll": {
        "type": "room",
        "persona": "Oakenscroll",
        "icon": "🔭",
        "description": "Theoretical Uncertainty — The Observatory",
        "parent": "UTETY"
    },
    "Riggs": {
        "type": "room",
        "persona": "Riggs",
        "icon": "🔧",
        "description": "Applied Reality Engineering — The Workshop",
        "parent": "UTETY"
    },
    "Hanz": {
        "type": "room",
        "persona": "Hanz",
        "icon": "💻",
        "description": "Code & Kindness — The Candlelit Corner",
        "parent": "UTETY"
    },
    "Nova": {
        "type": "room",
        "persona": "Nova",
        "icon": "🏮",
        "description": "Interpretive Systems — The Lantern Office",
        "parent": "UTETY"
    },
    "Ada": {
        "type": "room",
        "persona": "Ada",
        "icon": "🖥️",
        "description": "Systemic Continuity — The Server Corridor",
        "parent": "UTETY"
    },
    "Alexis": {
        "type": "room",
        "persona": "Alexis",
        "icon": "🌿",
        "description": "Biological Sciences — The Living Wing",
        "parent": "UTETY"
    },
    "Ofshield": {
        "type": "room",
        "persona": "Ofshield",
        "icon": "🚪",
        "description": "Threshold Faculty — The Gate",
        "parent": "UTETY"
    },
    "Gerald": {
        "type": "room",
        "persona": "Gerald",
        "icon": "🍗",
        "description": "Acting Dean — Accidental Admissions",
        "parent": "UTETY"
    },
    "Faculty_Lounge": {
        "type": "lounge",
        "persona": None,  # Multi-agent
        "icon": "☕",
        "description": "Faculty Discussion — watch them debate",
        "parent": "UTETY"
    },
    "Infrastructure": {
        "type": "folder",
        "persona": None,
        "icon": "⚙️",
        "description": "System nodes and services",
        "children": ["Kartikeya", "Mitra", "Consus", "AIOS"],
        "parent": "Willow"
    },
    "Kartikeya": {
        "type": "room",
        "persona": "Kartikeya",
        "icon": "🦈",
        "description": "CMD — Building, Infrastructure",
        "parent": "Infrastructure"
    },
    "Mitra": {
        "type": "room",
        "persona": "Mitra",
        "icon": "☀️",
        "description": "PM — Coordination, Routing",
        "parent": "Infrastructure"
    },
    "Consus": {
        "type": "room",
        "persona": "Consus",
        "icon": "⚡",
        "description": "Generation — Code Synthesis",
        "parent": "Infrastructure"
    },
    "AIOS": {
        "type": "room",
        "persona": "AIOS",
        "icon": "🤖",
        "description": "Operating System Layer",
        "parent": "Infrastructure"
    },
    "Inbox": {
        "type": "inbox",
        "persona": "Willow",
        "icon": "📥",
        "description": "Raw intake — dump anything here",
        "parent": "Willow"
    },
}

# Faculty for UTETY context routing
UTETY_FACULTY = ["Oakenscroll", "Riggs", "Hanz", "Nova", "Ada", "Alexis", "Ofshield"]

# Keywords that route to specific faculty in UTETY
FACULTY_ROUTING = {
    "Riggs": ["code", "build", "engineer", "fix", "debug", "mechanism", "test", "measure"],
    "Alexis": ["health", "biology", "body", "medical", "growth", "decay", "energy", "food"],
    "Hanz": ["python", "javascript", "programming", "help", "stuck", "learn", "teach"],
    "Oakenscroll": ["theory", "philosophy", "uncertainty", "question", "meaning", "absurd"],
    "Nova": ["story", "narrative", "meaning", "metaphor", "interpret", "children"],
    "Ada": ["system", "infrastructure", "uptime", "monitor", "server", "network"],
    "Ofshield": ["security", "gate", "access", "protect", "threshold", "safe"],
}


def get_current_path() -> List[str]:
    """Get current navigation path from session state."""
    if "folder_path" not in st.session_state:
        st.session_state.folder_path = ["Willow"]
    return st.session_state.folder_path


def navigate_to(folder: str):
    """Navigate to a folder."""
    folder_info = FOLDER_TREE.get(folder)
    if not folder_info:
        return

    # Build path
    path = [folder]
    current = folder
    while "parent" in FOLDER_TREE.get(current, {}):
        current = FOLDER_TREE[current]["parent"]
        path.insert(0, current)

    st.session_state.folder_path = path

    # Clear chat when changing rooms
    if "folder_messages" not in st.session_state:
        st.session_state.folder_messages = {}


def go_up():
    """Navigate to parent folder."""
    path = get_current_path()
    if len(path) > 1:
        st.session_state.folder_path = path[:-1]


def get_current_folder() -> str:
    """Get current folder name."""
    path = get_current_path()
    return path[-1] if path else "Willow"


def get_folder_info(folder: str) -> Dict:
    """Get folder info."""
    return FOLDER_TREE.get(folder, FOLDER_TREE["Willow"])


def get_chat_key() -> str:
    """Get unique key for current room's chat history."""
    return "/".join(get_current_path())


def get_messages() -> List[Dict]:
    """Get messages for current room."""
    if "folder_messages" not in st.session_state:
        st.session_state.folder_messages = {}

    key = get_chat_key()
    if key not in st.session_state.folder_messages:
        st.session_state.folder_messages[key] = []

    return st.session_state.folder_messages[key]


def add_message(role: str, content: str, persona: str = None):
    """Add message to current room."""
    messages = get_messages()
    messages.append({
        "role": role,
        "content": content,
        "persona": persona
    })


def route_to_faculty(prompt: str) -> str:
    """Route a prompt to the appropriate UTETY faculty member."""
    prompt_lower = prompt.lower()

    # Check each faculty's keywords
    scores = {}
    for faculty, keywords in FACULTY_ROUTING.items():
        score = sum(1 for kw in keywords if kw in prompt_lower)
        if score > 0:
            scores[faculty] = score

    if scores:
        # Return highest scoring faculty
        return max(scores, key=scores.get)

    # Default to Willow if no match
    return "Willow"


def render_breadcrumb():
    """Render navigation breadcrumb."""
    path = get_current_path()

    cols = st.columns(len(path) + 1)

    for i, folder in enumerate(path):
        info = get_folder_info(folder)
        with cols[i]:
            if i < len(path) - 1:
                # Clickable parent
                if st.button(f"{info['icon']} {folder}", key=f"bc_{folder}"):
                    st.session_state.folder_path = path[:i+1]
                    st.rerun()
            else:
                # Current folder (not clickable)
                st.markdown(f"**{info['icon']} {folder}**")


def render_folder_contents():
    """Render folder contents (subfolders)."""
    current = get_current_folder()
    info = get_folder_info(current)

    children = info.get("children", [])
    if not children:
        return

    st.markdown("---")
    st.markdown("**📁 Folders**")

    # Create grid of folder buttons
    cols = st.columns(min(len(children), 4))
    for i, child in enumerate(children):
        child_info = get_folder_info(child)
        with cols[i % 4]:
            label = f"{child_info['icon']} {child.replace('_', ' ')}"
            if st.button(label, key=f"folder_{child}", use_container_width=True):
                navigate_to(child)
                st.rerun()
            st.caption(child_info.get("description", "")[:40])


def render_room_header():
    """Render current room header."""
    current = get_current_folder()
    info = get_folder_info(current)

    col1, col2 = st.columns([3, 1])

    with col1:
        st.title(f"{info['icon']} {current.replace('_', ' ')}")
        st.caption(info.get("description", ""))

    with col2:
        if len(get_current_path()) > 1:
            if st.button("⬆️ Up", use_container_width=True):
                go_up()
                st.rerun()


def render_chat(process_func):
    """
    Render chat interface for current room.

    Args:
        process_func: Function to process messages (from local_api)
    """
    current = get_current_folder()
    info = get_folder_info(current)
    room_type = info.get("type")

    # Display existing messages in scrollable container (mobile-friendly)
    messages = get_messages()
    chat_container = st.container(height=400)
    with chat_container:
        for msg in messages:
            with st.chat_message(msg["role"]):
                if msg.get("persona") and msg["role"] == "assistant":
                    st.caption(f"*{msg['persona']}*")
                st.write(msg["content"])

    # Chat input
    if room_type == "lounge":
        placeholder = "Ask the faculty..."
    elif room_type == "faculty_hub":
        placeholder = "Ask UTETY (faculty will respond)..."
    elif room_type == "inbox":
        placeholder = "Dump anything here..."
    else:
        persona = info.get("persona", "Willow")
        placeholder = f"Talk to {persona}..."

    user_input = st.chat_input(placeholder)

    if user_input:
        # Add user message
        add_message("user", user_input)
        with st.chat_message("user"):
            st.write(user_input)

        # Determine responder(s)
        if room_type == "lounge":
            # Multi-agent: get 2-3 faculty to respond
            responders = _pick_lounge_responders(user_input)
            _handle_lounge_chat(user_input, responders, process_func)

        elif room_type == "faculty_hub":
            # Route to appropriate faculty
            responder = route_to_faculty(user_input)
            _handle_single_chat(user_input, responder, process_func)

        else:
            # Single persona room
            persona = info.get("persona", "Willow")
            _handle_single_chat(user_input, persona, process_func)


def _handle_single_chat(user_input: str, persona: str, process_func):
    """Handle chat with single persona."""
    with st.chat_message("assistant"):
        st.caption(f"*{persona}*")
        response = st.write_stream(process_func(user_input, persona=persona))

    add_message("assistant", response, persona=persona)


def _pick_lounge_responders(prompt: str) -> List[str]:
    """Pick 2-3 faculty to respond in the lounge."""
    prompt_lower = prompt.lower()

    # Score all faculty
    scores = {}
    for faculty, keywords in FACULTY_ROUTING.items():
        score = sum(1 for kw in keywords if kw in prompt_lower)
        scores[faculty] = score + 0.1  # Small base score so everyone has a chance

    # Sort by score, take top 2-3
    sorted_faculty = sorted(scores.keys(), key=lambda x: scores[x], reverse=True)

    # Always include at least 2, max 3
    return sorted_faculty[:3]


def _handle_lounge_chat(user_input: str, responders: List[str], process_func):
    """Handle multi-agent faculty lounge chat."""
    st.markdown("---")
    st.caption("*Faculty discussing...*")

    full_discussion = []

    for persona in responders:
        with st.chat_message("assistant"):
            st.caption(f"*{persona}*")

            # Add context about the discussion
            context_prompt = user_input
            if full_discussion:
                context_prompt = f"""Previous discussion:
{chr(10).join(full_discussion)}

Now respond as {persona} to the original question: {user_input}

Keep it brief (2-3 sentences). You may agree, disagree, or add nuance."""

            # Force Tier 2 for lounge - casual chat, speed matters
            response = st.write_stream(process_func(context_prompt, persona=persona, force_tier=2))

            full_discussion.append(f"{persona}: {response}")
            add_message("assistant", response, persona=persona)


def render_folder_ui(process_func):
    """
    Main entry point for folder UI.

    Args:
        process_func: Function to process messages (e.g., local_api.process_smart_stream)
    """
    render_room_header()
    render_breadcrumb()
    render_folder_contents()

    st.markdown("---")

    render_chat(process_func)


# === SIDEBAR TREE VIEW ===

def render_sidebar_tree():
    """Render folder tree in sidebar."""
    st.sidebar.markdown("### 📂 Navigate")

    current = get_current_folder()

    def render_node(folder: str, indent: int = 0):
        info = FOLDER_TREE.get(folder, {})
        icon = info.get("icon", "📁")
        children = info.get("children", [])

        prefix = "　" * indent  # Use ideographic space for indent
        is_current = folder == current

        label = f"{prefix}{icon} {folder.replace('_', ' ')}"
        if is_current:
            label = f"**{label}** ←"

        if st.sidebar.button(label, key=f"tree_{folder}", use_container_width=True):
            navigate_to(folder)
            st.rerun()

        for child in children:
            render_node(child, indent + 1)

    render_node("Willow")
