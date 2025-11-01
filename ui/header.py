# ui/header.py
import pathlib
import streamlit as st

def render_global_head() -> None:
    """Inject Inter font + theme CSS on every page."""
    st.markdown(
        """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
<style>
  html, body, [class^="st-"]{
    font-family: Inter, system-ui, -apple-system, Segoe UI, Roboto, Helvetica, Arial, sans-serif;
  }
</style>
        """,
        unsafe_allow_html=True,
    )

    css_path = pathlib.Path(__file__).with_name("theme.css")
    try:
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except Exception:
        # Silent: page still works without custom CSS
        pass


def page_header(title: str, subtitle: str = "") -> None:
    """
    Backward-compatible page header used by inner pages
    (e.g., pages/2_Possibility.py). Also guarantees CSS injection.
    """
    render_global_head()

    subtitle_html = (
        f'<div style="font-size:16px;color:#7a6f64;margin-top:2px;">{subtitle}</div>'
        if subtitle else ""
    )

    st.markdown(
        f"""
<div class="apl-container" style="padding-top:8px;padding-bottom:8px;">
  <h1 style="
      font-size:32px;
      line-height:1.2;
      margin:0 0 4px 0;
      color: var(--ink, #2D2A26);
      font-weight:800;">
    {title}
  </h1>
  {subtitle_html}
</div>
        """,
        unsafe_allow_html=True,
    )
