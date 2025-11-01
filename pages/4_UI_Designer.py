import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import generate_ui_cached
from ui.previews import html_preview, code_block

st.set_page_config(page_title="UI Designer — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")
render_top_nav(active="UI")
page_header("UI Designer", "Generate a simple, elegant UI preview from your identity.")
ensure_session_defaults()

identity = st.session_state["identity"]

st.markdown('<div class="apl-container">', unsafe_allow_html=True)
with st.container(border=False):
    st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
    if st.button("Generate UI from Identity", type="primary", use_container_width=True):
        with st.spinner("Generating UI (cached)…"):
            st.session_state["ui_result"] = generate_ui_cached(identity)

    ui = st.session_state.get("ui_result", {"html": "", "css": ""})
    if ui.get("html"):
        st.success("UI ready — preview below")
        html_preview(ui["html"], ui.get("css"), height=800)
        st.divider()
        code_block("HTML", ui["html"], "generated.html")
        code_block("CSS", ui.get("css", ""), "styles.css")
    else:
        st.info("Click **Generate UI from Identity** to preview.", icon="✨")
    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
