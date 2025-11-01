import pathlib
import streamlit as st

CSS_CACHE_KEY = "__apl_css_injected__"


def render_global_head():
    """Inject Google Fonts and our theme.css once per session."""
    if st.session_state.get(CSS_CACHE_KEY):
        return

    # 1) Google Fonts (Inter)
    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.googleapis.com">
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,400;0,14..32,600;0,14..32,700;1,14..32,600&display=swap" rel="stylesheet">
        <style>html, body, [class^="st-"]{ font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif; }</style>
        """,
        unsafe_allow_html=True,
    )

    # 2) App theme CSS
    css_path = pathlib.Path(__file__).with_name("theme.css")
    try:
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        pass

    st.session_state[CSS_CACHE_KEY] = True


def page_header(title: str, subtitle: str = ""):
    st.markdown(
        f"""
        <div class="apl-container">
          <div style="padding: 8px 4px;">
            <div class="apl-gradient-title">{title}</div>
            <div class="apl-subtitle">{subtitle}</div>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
