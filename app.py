# app.py
import streamlit as st

st.set_page_config(
    page_title="AI Possibility Lab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Always send users to the canonical Landing page in a multipage app.
# This stops the current script and runs pages/1_Landing.py. :contentReference[oaicite:3]{index=3}
st.switch_page("pages/1_Landing.py")
