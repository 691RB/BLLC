import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import get_system_prompt
from ui.chat import chat_widget

st.set_page_config(page_title="Possibility — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")
render_top_nav(active="Possibility")
page_header("Possibility Finder", "Clarify WHAT, WHO, WHY, HOW, contribution, and name.")
ensure_session_defaults()

canvas = st.session_state["canvas"]

with st.container():
    left, right = st.columns([7,5], gap="large")

with left:
    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            canvas["what"] = st.text_area("What", value=canvas["what"], height=100, placeholder="What problem or need?")
            canvas["who"] = st.text_area("Who", value=canvas["who"], height=100, placeholder="Who are you helping?")
            canvas["why"] = st.text_area("Why", value=canvas["why"], height=100, placeholder="Why does it matter?")
        with col2:
            canvas["how"] = st.text_area("How", value=canvas["how"], height=100, placeholder="How will the assistant help?")
            canvas["contribution"] = st.text_area("Contribution", value=canvas["contribution"], height=100, placeholder="What contribution will it make?")
            canvas["botName"] = st.text_input("Bot Name", value=canvas["botName"], placeholder="e.g., Possibility Partner")
        st.success("Saved locally", icon="✅")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import get_system_prompt
from ui.chat import chat_widget

st.set_page_config(page_title="Possibility — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")
render_top_nav(active="Possibility")
page_header("Possibility Finder", "Clarify WHAT, WHO, WHY, HOW, contribution, and name.")
ensure_session_defaults()

canvas = st.session_state["canvas"]

with st.container():
    left, right = st.columns([7,5], gap="large")

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
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    chat_widget(
        key="possibility",
        system_prompt=get_system_prompt("possibility"),
        title="Possibility Partner",
    )
