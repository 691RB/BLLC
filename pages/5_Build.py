import streamlit as st
from ui.nav import render_top_nav
from ui.header import page_header
from utils.state import ensure_session_defaults
from services.ai import generate_files_cached
from utils.downloads import make_zip

st.set_page_config(page_title="Build — AI Possibility Lab", layout="wide", initial_sidebar_state="collapsed")
render_top_nav(active="Build")
page_header("Build Files", "Generate a small scaffold and download as a zip.")
ensure_session_defaults()

identity = st.session_state["identity"]
ui_result = st.session_state.get("ui_result", None)

st.markdown('<div class="apl-container">', unsafe_allow_html=True)
with st.container(border=False):
    st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)

    if st.button("Generate App Files", type="primary", use_container_width=True):
        with st.spinner("Generating files (cached)…"):
            files = generate_files_cached(identity, ui_result)
            st.session_state["build_files"] = files

    files = st.session_state.get("build_files", [])
    if files:
        st.success(f"Generated {len(files)} files.")
        for f in files:
            name = f.get("name", "file.txt")
            content = f.get("content", "")
            desc = f.get("description", "")
            st.markdown(f"**{name}**  \n_{desc}_")
            st.code(content, language="python" if name.endswith(".py") else None)
            st.download_button(
                f"Download {name}",
                data=content.encode("utf-8"),
                file_name=name,
                mime=f.get("mime", "text/plain"),
                use_container_width=True
            )
        # Zip all
        zip_bytes = make_zip(files)
        st.download_button(
            "Download All as ZIP",
            data=zip_bytes,
            file_name="scaffold.zip",
            mime="application/zip",
            use_container_width=True
        )
    else:
        st.info("Click **Generate App Files** to create a scaffold.", icon="🧱")

    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
