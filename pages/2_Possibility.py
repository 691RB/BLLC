# pages/2_Possibility.py
import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import get_system_prompt
from ui.chat import chat_widget

st.set_page_config(
    page_title="Possibility — AI Possibility Lab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Use the label that matches your top nav list so the pill highlights correctly
render_top_nav(active="Possibility Finding")
page_header("Possibility Finder", "Clarify WHAT, WHO, WHY, HOW, contribution, and name.")
ensure_session_defaults()

canvas = st.session_state["canvas"]

# ---------- Main layout ----------
with st.container():
    left, right = st.columns([7, 5], gap="large")

# ---------- Left column: canvas inputs ----------
with left:
    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)

        with col1:
            canvas["what"] = st.text_area(
                "What", key="pf_what", value=canvas["what"], height=100,
                placeholder="What problem or need?"
            )
            canvas["who"] = st.text_area(
                "Who", key="pf_who", value=canvas["who"], height=100,
                placeholder="Who are you helping?"
            )
            canvas["why"] = st.text_area(
                "Why", key="pf_why", value=canvas["why"], height=100,
                placeholder="Why does it matter?"
            )

        with col2:
            canvas["how"] = st.text_area(
                "How", key="pf_how", value=canvas["how"], height=100,
                placeholder="How will the assistant help?"
            )
            canvas["contribution"] = st.text_area(
                "Contribution", key="pf_contribution", value=canvas["contribution"],
                height=100, placeholder="What contribution will it make?"
            )
            canvas["botName"] = st.text_input(
                "Bot Name", key="pf_bot_name", value=canvas["botName"],
                placeholder="e.g., Possibility Partner"
            )

        st.success("Saved locally", icon="✅")
        st.markdown("</div>", unsafe_allow_html=True)  # close .apl-card
    st.markdown("</div>", unsafe_allow_html=True)      # close .apl-container

# ---------- Right column: fixed chat window + widget ----------
with right:
    # Scrollable chat window that shows transcript
    st.markdown(
        '<div class="apl-card" style="height:420px; overflow:auto; padding:16px; margin-bottom:12px;">',
        unsafe_allow_html=True,
    )
    for m in st.session_state.get("possibility_transcript", []):
        who = "You" if m.get("role") == "user" else "Partner"
        st.markdown(
            f"<div style='margin:6px 0'><strong>{who}:</strong> {m.get('content','')}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Existing widget (unchanged API). Capture its return and display above.
    result = chat_widget(
        key="possibility",
        system_prompt=get_system_prompt("possibility"),
        title="Possibility Partner",
    )

    # Be tolerant to different return shapes from chat_widget
    if result is not None:
        user_msg = None
        assistant_msg = None
        if isinstance(result, dict):
            user_msg = result.get("user") or result.get("prompt")
            assistant_msg = result.get("assistant") or result.get("reply") or result.get("response")
        elif isinstance(result, (list, tuple)) and len(result) == 2:
            user_msg, assistant_msg = result
        else:
            assistant_msg = str(result)

        transcript = st.session_state.setdefault("possibility_transcript", [])
        if user_msg:
            transcript.append({"role": "user", "content": user_msg})
        if assistant_msg:
            transcript.append({"role": "assistant", "content": assistant_msg})

        st.rerun()
