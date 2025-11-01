import streamlit as st

def ensure_session_defaults():
    st.session_state.setdefault("canvas", {
        "what": "", "who": "", "why": "", "how": "",
        "contribution": "", "botName": ""
    })
    st.session_state.setdefault("identity", {
        "role": "", "goal": "", "rules": "",
        "knowledge": "", "specializedActions": "", "guidelines": ""
    })
    # ui & build results
    st.session_state.setdefault("ui_result", {"html": "", "css": ""})
    st.session_state.setdefault("build_files", [])
