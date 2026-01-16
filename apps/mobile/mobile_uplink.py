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
from willow_sap.coherence import get_coherence_report, THRESHOLDS

# Add governance path for Gatekeeper
governance_path = Path(__file__).parent.parent.parent / "governance"
sys.path.insert(0, str(governance_path))
try:
    from gate import (
        validate_modification, get_state, reset_demo, pending, audit,
        verify, enter_layer, exit_layer, approve, reject
    )
    GATEKEEPER_AVAILABLE = True
except ImportError:
    GATEKEEPER_AVAILABLE = False

# === CONFIGURATION ===
st.set_page_config(
    page_title="Willow Mobile",
    layout="wide",
    initial_sidebar_state="expanded"
)

# === THE SIDEBAR (Faculty Selection) ===
st.sidebar.title("UTETY Faculty")

# Faculty organized by role
FACULTY = {
    "Campus": ["Willow"],
    "Faculty": ["Oakenscroll", "Riggs", "Hanz", "Nova", "Ada", "Alexis", "Ofshield"],
    "Administration": ["Gerald"],
}

# Flatten for radio (with section headers shown via formatting)
all_channels = []
for section, members in FACULTY.items():
    all_channels.extend(members)

mode = st.sidebar.radio(
    "Active Channel",
    all_channels,
    format_func=lambda x: {
        "Willow": "🏛️ Willow (Campus)",
        "Oakenscroll": "🔭 Oakenscroll (Theory)",
        "Riggs": "🔧 Riggs (Engineering)",
        "Hanz": "💻 Hanz (Code)",
        "Nova": "🏮 Nova (Narrative)",
        "Ada": "🖥️ Ada (Systems)",
        "Alexis": "🌿 Alexis (Bio)",
        "Ofshield": "🚪 Ofshield (Gate)",
        "Gerald": "🍗 Gerald (Dean)",
    }.get(x, x)
)

st.sidebar.divider()
st.sidebar.markdown("**System Status**")

# Live status check
ollama_status = "ONLINE" if local_api.check_ollama() else "OFFLINE"
models = local_api.list_models()
model_str = models[0] if models else "none"

st.sidebar.code(f"OLLAMA: {ollama_status}\nMODEL: {model_str}\nL5-L6: SAFE")

# ΔE Coherence Status
st.sidebar.divider()
st.sidebar.markdown("**ΔE Coherence**")
try:
    coherence_report = get_coherence_report()
    state_emoji = {"regenerative": "↑", "stable": "→", "decaying": "↓", "no_data": "○"}.get(
        coherence_report.get("status", "stable"), "→"
    )
    delta_e = coherence_report.get("average_delta_e", 0)
    ci = coherence_report.get("latest_coherence", 0) or 0
    trend = coherence_report.get("trend", "unknown")
    st.sidebar.code(f"ΔE: {delta_e:+.4f} {state_emoji}\nCᵢ: {ci:.2f}\nTrend: {trend}")
except Exception:
    st.sidebar.code("ΔE: [loading...]")

# === THE MAIN DISPLAY ===
DISPLAY_NAMES = {
    "Willow": "Willow (The Campus)",
    "Oakenscroll": "Prof. Oakenscroll",
    "Riggs": "Prof. Riggs",
    "Hanz": "Prof. Hanz",
    "Nova": "Prof. Nova Hale",
    "Ada": "Prof. Ada Turing",
    "Alexis": "Prof. Alexis",
    "Ofshield": "Prof. Ofshield",
    "Gerald": "Gerald Prime",
}
st.title(f"Connected to: {DISPLAY_NAMES.get(mode, mode)}")

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

    # Log conversation for training data
    # Extract tier from response prefix (e.g., "[Tier 2: General conversation]")
    tier_num = 2  # default
    if response and response.startswith("[Tier "):
        try:
            tier_num = int(response[6])
        except (ValueError, IndexError):
            pass
    local_api.log_conversation(
        persona=mode,
        user_input=user_input,
        assistant_response=response,
        model=local_api.MODEL_TIERS.get(tier_num, {}).get("name", "unknown"),
        tier=tier_num
    )

# 3. BUTTONS (The "Hands")
st.divider()
col1, col2, col3, col4 = st.columns(4)

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

with col4:
    if st.button("To Pickup"):
        # Summarize last few messages for user pickup
        if st.session_state.messages:
            summary_lines = []
            for msg in st.session_state.messages[-6:]:  # Last 3 exchanges
                role = "User" if msg["role"] == "user" else mode
                summary_lines.append(f"**{role}:** {msg['content'][:200]}")
            summary = "\n\n".join(summary_lines)
            if local_api.send_session_summary(mode, summary):
                st.toast("Sent to your Pickup box!")
            else:
                st.toast("Failed to send", icon="⚠️")
        else:
            st.toast("No messages to send")

# === GATEKEEPER TEST PANEL ===
if GATEKEEPER_AVAILABLE:
    st.divider()
    with st.expander("🔐 Gatekeeper v2.3.0", expanded=False):
        st.markdown("**ΔG-1 + ΔG-4 Enforced**")

        # State display
        state = get_state()
        st.code(f"""State:
  depth: {state['depth']}
  sequence: {state['sequence']}
  pending: {state['pending_count']}
  audit: {state['audit_count']}
  checksum: {'✓' if verify() else '✗'}""")

        # Test form
        st.markdown("**Test Mutation**")
        col_a, col_b = st.columns(2)

        with col_a:
            test_authority = st.selectbox(
                "Authority (ΔG-1)",
                ["human", "ai", "system"],
                key="gate_authority"
            )
            test_mod_type = st.selectbox(
                "Mod Type",
                ["state", "config", "behavior", "governance", "external"],
                key="gate_mod_type"
            )

        with col_b:
            test_gov_state = st.selectbox(
                "Gov State (ΔG-4)",
                ["", "proposed", "ratified", "active", "deprecated"],
                key="gate_gov_state"
            )
            test_prev_state = st.selectbox(
                "Prev State",
                ["", "proposed", "ratified", "active", "deprecated"],
                key="gate_prev_state"
            )

        test_target = st.text_input("Target", value="test.setting", key="gate_target")
        test_value = st.text_input("New Value", value="test_value", key="gate_value")
        test_reason = st.text_input("Reason", value="Datapad test", key="gate_reason")

        col_submit, col_reset = st.columns(2)

        with col_submit:
            if st.button("Submit to Gate", type="primary"):
                result = validate_modification(
                    mod_type=test_mod_type,
                    target=test_target,
                    new_value=test_value,
                    reason=test_reason,
                    authority=test_authority,
                    governance_state=test_gov_state,
                    prev_governance_state=test_prev_state
                )
                if result['approved']:
                    st.success(f"✓ APPROVED\nCode: {result['code']}")
                elif result['requires_human']:
                    st.warning(f"⏳ REQUIRES HUMAN\nCode: {result['code']}\n{result['reason']}")
                else:
                    st.error(f"✗ HALTED\nCode: {result['code']}\n{result['reason']}")

        with col_reset:
            if st.button("Reset Demo"):
                reset_demo()
                st.toast("Demo state reset")
                st.rerun()

        # Pending approvals
        pending_list = pending()
        if pending_list:
            st.markdown(f"**Pending Approvals ({len(pending_list)})**")
            for p in pending_list:
                with st.container():
                    st.code(f"ID: {p['request_id'][:8]}...\nTarget: {p['target']}\nValue: {p['new_value'][:30]}")
                    c1, c2 = st.columns(2)
                    with c1:
                        if st.button("Approve", key=f"approve_{p['request_id']}"):
                            approve(p['request_id'])
                            st.toast("Approved")
                            st.rerun()
                    with c2:
                        if st.button("Reject", key=f"reject_{p['request_id']}"):
                            reject(p['request_id'], "Rejected via Datapad")
                            st.toast("Rejected")
                            st.rerun()

# === FOOTER ===
st.divider()
st.caption("Die-Namic System | L5-L6 Safe Mode | ΔΣ=42")
