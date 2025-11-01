import streamlit as st

def render_global_head():
    # fonts & CSS injection is handled in nav; this can include any universal tags later
    pass

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
