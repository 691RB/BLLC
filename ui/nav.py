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
    # Topbar wrapper (styled in theme.css)
    st.markdown('<div class="apl-topbar"><div class="apl-topbar-inner">', unsafe_allow_html=True)

    # 5 equal columns → perfect horizontal row + even spacing
    cols = st.columns([1, 1, 1, 1, 1], gap="medium")
    for col, (label, path, icon) in zip(cols, PAGES):
        with col:
            st.page_link(path, label=label, icon=icon)

    st.markdown('</div></div>', unsafe_allow_html=True)
