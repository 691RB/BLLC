# ui/nav.py
import streamlit as st

PAGES = [
    ("Landing", "pages/1_Landing.py", "🏠"),
    ("Possibility Finding", "pages/2_Possibility.py", "🔍"),
    ("Bot Identity", "pages/3_Identity.py", "🪪"),
    ("UI Design", "pages/4_UI_Designer.py", "🛠️"),
    ("Build App", "pages/5_Build.py", "✨"),
]

def render_top_nav(active: str = "Landing"):
    # one responsive row; pills styled via CSS in theme.css
    cols = st.columns(len(PAGES), gap="small")
    for col, (label, path, icon) in zip(cols, PAGES):
        with col:
            st.page_link(path, label=label, icon=icon)
