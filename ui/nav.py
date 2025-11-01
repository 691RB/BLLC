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
    # container that our CSS targets
    st.markdown('<div class="apl-topbar"><div class="apl-topbar-inner"><nav class="apl-nav">', unsafe_allow_html=True)

    # Use Streamlit-native links so navigation is correct and instantaneous
    # (this runs the target page just like the sidebar nav). :contentReference[oaicite:2]{index=2}
    for label, path, icon in PAGES:
        st.page_link(path, label=label, icon=icon)

    st.markdown('</nav></div></div>', unsafe_allow_html=True)
