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

# Make sure the top pill highlights correctly
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

        # Add unique keys to avoid StreamlitDuplicateElementId
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

# ---------- Helpers to display chat output ----------
def _normalize_messages(items):
    """Best-effort normalization into [{'role','content'}, ...]"""
    out = []
    for it in items or []:
        if isinstance(it, dict):
            role = (it.get("role") or it.get("sender") or it.get("type") or "assistant").lower()
            role = "user" if role in ("user", "human", "you") else "assistant"
            content = it.get("content") or it.get("text") or it.get("message") or ""
            if isinstance(content, (list, dict)):
                content = str(content)
            out.append({"role": role, "content": str(content)})
        elif isinstance(it, (list, tuple)) and len(it) >= 2:
            out.append({"role": "user", "content": str(it[0])})
            out.append({"role": "assistant", "content": str(it[1])})
        elif isinstance(it, str):
            out.append({"role": "assistant", "content": it})
    return out

def gather_chat_history(key_base="possibility"):
    """
    Some chat widgets store messages in session_state rather than returning them.
    We look for common keys and render whichever is present & longest.
    """
    candidates_keys = [
        f"{key_base}_transcript",
        f"{key_base}_history",
        f"{key_base}_messages",
        f"{key_base}_chat",
        "chat_history",
        "messages",
        "transcript",
    ]
    candidates = []
    for k in candidates_keys:
        v = st.session_state.get(k)
        if isinstance(v, list) and v:
            candidates.append(_normalize_messages(v))
    if candidates:
        return max(candidates, key=len)
    # fall back to our own transcript if we created one earlier
    return st.session_state.get(f"{key_base}_transcript", [])

# ---------- Right column: fixed chat window + widget ----------
with right:
    # Scrollable chat window that shows transcript (from widget or our fallback)
    hist = gather_chat_history("possibility")

    st.markdown(
        '<div class="apl-card" style="height:420px; overflow:auto; padding:16px; margin-bottom:12px;">',
        unsafe_allow_html=True,
    )
    for m in hist:
        who = "You" if m.get("role") == "user" else "Partner"
        st.markdown(
            f"<div style='margin:6px 0'><strong>{who}:</strong> {m.get('content','')}</div>",
            unsafe_allow_html=True,
        )
    st.markdown("</div>", unsafe_allow_html=True)

    # Your existing widget. If it returns something, append it to our transcript.
    result = chat_widget(
        key="possibility",
        system_prompt=get_system_prompt("possibility"),
        title="Possibility Partner",
    )

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

        # Maintain our own transcript so we always have something to render.
        transcript_key = "possibility_transcript"
        transcript = st.session_state.setdefault(transcript_key, [])
        if user_msg:
            transcript.append({"role": "user", "content": user_msg})
        if assistant_msg:
            transcript.append({"role": "assistant", "content": assistant_msg})
        st.rerun()
