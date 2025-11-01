# ui/header.py
import pathlib
import streamlit as st

CSS_CACHE_KEY = "__apl_css_injected__"

def render_global_head():
    if st.session_state.get(CSS_CACHE_KEY):
        return

    st.markdown(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>html, body, [class^="st-"]{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }</style>
        """,
        unsafe_allow_html=True,
    )

    css_path = pathlib.Path(__file__).with_name("theme.css")
    try:
        st.markdown(f"<style>{css_path.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.session_state[CSS_CACHE_KEY] = True
