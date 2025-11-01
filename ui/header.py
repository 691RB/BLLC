# ui/header.py
import pathlib
import streamlit as st

def render_global_head():
    # Always (re)inject to avoid stale sessions on Cloud
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
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Theme CSS not found: {e}")
