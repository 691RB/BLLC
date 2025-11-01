import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import get_system_prompt
from ui.chat import chat_widget

st.set_page_config(page_title="Identity — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")
render_top_nav(active="Identity")
page_header("Identity Shaper", "Craft role, goal, rules, knowledge, actions, and guidelines.")
ensure_session_defaults()

identity = st.session_state["identity"]

with st.container():
    left, right = st.columns([7,5], gap="large")

with left:
    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
        identity["role"] = st.text_area("Role", value=identity["role"], height=80)
        identity["goal"] = st.text_area("Goal", value=identity["goal"], height=80)
        identity["rules"] = st.text_area("Rules", value=identity["rules"], height=100)
        identity["knowledge"] = st.text_area("Knowledge", value=identity["knowledge"], height=100)
        identity["specializedActions"] = st.text_area("Specialized Actions", value=identity["specializedActions"], height=100)
        identity["guidelines"] = st.text_area("Guidelines", value=identity["guidelines"], height=100)
        st.success("Saved locally", icon="✅")
        st.download_button(
            "Download Identity JSON",
            data=str(identity).encode("utf-8"),
            file_name="identity.json",
            use_container_width=True
        )
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    chat_widget(
        key="identity",
        system_prompt=get_system_prompt("identity"),
        title="Identity Assistant",
    )
