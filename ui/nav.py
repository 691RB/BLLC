import streamlit as st

PAGES = [
    ("Home", None),  # app.py
    ("Landing", "1_Landing"),
    ("Possibility", "2_Possibility"),
    ("Identity", "3_Identity"),
    ("UI", "4_UI_Designer"),
    ("Build", "5_Build"),
]

def _link(label: str, file_stub: str | None, active: bool) -> str:
    if hasattr(st, "page_link") and file_stub:
        # Use Streamlit's built-in page linker when available
        return st.page_link(f"pages/{file_stub}.py", label=label, use_container_width=False)
    # Fallback: render as a styled pill; not clickable without page_link
    cls = "apl-pill active" if active else "apl-pill"
    return f'<span class="{cls}">{label}</span>'

def render_top_nav(active: str):
    # Inject theme CSS on every page
    try:
        with open("ui/theme.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception:
        pass

    st.markdown(
        """
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap" rel="stylesheet">
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="apl-topbar"><div class="apl-topbar-inner">', unsafe_allow_html=True)
    st.markdown('<div class="apl-brand">AI Possibility Lab</div>', unsafe_allow_html=True)

    # Right-justified nav
    st.markdown('<div class="apl-nav">', unsafe_allow_html=True)
    for label, stub in PAGES:
        is_active = (label == active)
        if hasattr(st, "page_link") and stub:
            _link(label, stub, is_active)
        else:
            st.markdown(_link(label, stub, is_active), unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div></div>', unsafe_allow_html=True)
