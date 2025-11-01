import streamlit as st
from ui.nav import render_top_nav
from ui.header import render_global_head
from utils.state import ensure_session_defaults

st.set_page_config(
    page_title="AI Possibility Lab — Build-to-Learn",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Inject global <head> (fonts, icons) and CSS
render_global_head()
ensure_session_defaults()

# Draw top navigation (mirrors pages/)
render_top_nav(active="Home")

# Minimal welcome (the real landing lives in pages/1_Landing.py)
st.markdown(
    """
    <div class="apl-container">
      <div class="apl-card" style="text-align:center;padding:3rem 2rem;">
        <h1 class="apl-gradient-title">AI Possibility Lab</h1>
        <p class="apl-subtitle">Use the top navigation to get started.</p>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
