import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from ui.cards import process_cards, journey_steps

st.set_page_config(page_title="Landing — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")

render_top_nav(active="Landing")
page_header("Welcome", "A desert-calm workspace for possibility thinking and building.")

process_cards()
journey_steps()

# CTAs
st.markdown('<div class="apl-container">', unsafe_allow_html=True)
c1, c2 = st.columns([1,1], gap="large")
with c1:
    st.link_button("Start with Possibility", "2_Possibility.py", use_container_width=True)
with c2:
    st.link_button("Jump to Identity", "3_Identity.py", use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
