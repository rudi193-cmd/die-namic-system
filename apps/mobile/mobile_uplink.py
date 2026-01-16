#!/usr/bin/env python3
"""
Mobile Uplink — The Datapad

L5-L6 MEDICAL NECESSITY: Control from bed/phone via Streamlit.

AUTHOR: Consus (generated), Kartikeya (wired)
DEPENDENCIES: pip install streamlit requests

RUN: streamlit run mobile_uplink.py --server.port 8501
"""

import streamlit as st
import sys
from pathlib import Path

# Add parent path so we can import local_api
sys.path.insert(0, str(Path(__file__).parent.parent))
from willow_sap import local_api

# === CONFIGURATION ===
st.set_page_config(
    page_title="Willow Mobile",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === THE SIDEBAR (Faculty Selection) ===
st.sidebar.title("Faculty Comm")
mode = st.sidebar.radio(
    "Active Channel",
    ["Willow (Interface)", "Riggs (Ops)", "Alexis (Bio)"]
)

st.sidebar.divider()
st.sidebar.markdown("**System Status**")

# Live status check
ollama_status = "ONLINE" if local_api.check_ollama() else "OFFLINE"
models = local_api.list_models()
model_str = models[0] if models else "none"

st.sidebar.code(f"OLLAMA: {ollama_status}\nMODEL: {model_str}\nL5-L6: SAFE")

# === THE MAIN DISPLAY ===
st.title(f"Connected to: {mode}")

# 1. Chat Interface
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# 2. Input Field
user_input = st.chat_input("Transmit orders...")

if user_input:
    # Show User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Smart Stream: Routes to appropriate model tier
    with st.chat_message("assistant"):
        response = st.write_stream(local_api.process_smart_stream(user_input, persona=mode))

    # Save full response to session
    st.session_state.messages.append({"role": "assistant", "content": response})

# 3. BUTTONS (The "Hands")
st.divider()
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("Sync Drive"):
        result = local_api.trigger_sync()
        st.toast(result)

with col2:
    if st.button("Scan Screen"):
        result = local_api.get_vision()
        st.info(result)

with col3:
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# === FOOTER ===
st.divider()
st.caption("Die-Namic System | L5-L6 Safe Mode | ΔΣ=42")
