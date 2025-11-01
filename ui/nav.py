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
    # Open our topbar + row wrapper
    st.markdown(
        '<div class="apl-topbar"><div class="apl-topbar-inner"><div class="apl-nav-row">',
        unsafe_allow_html=True,
    )

    # Streamlit-native links (correct routing), now inside our flex row
    for label, path, icon in PAGES:
        st.page_link(path, label=label, icon=icon)

    # Close wrappers
    st.markdown("</div></div></div>", unsafe_allow_html=True)
