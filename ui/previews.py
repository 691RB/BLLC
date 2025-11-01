import streamlit as st
import streamlit.components.v1 as components

def html_preview(html: str, css: str | None = None, height: int = 800):
    """
    Renders a sandboxed preview using components.html.
    """
    merged = f"""
    <style>{css or ""}</style>
    {html}
    """
    components.html(merged, height=height, scrolling=True)

def code_block(label: str, content: str, file_name: str):
    with st.expander(label, expanded=False):
        st.code(content, language="html" if file_name.endswith(".html") else "css")
        st.download_button("Download", data=content.encode("utf-8"), file_name=file_name, mime="text/plain", use_container_width=True)
