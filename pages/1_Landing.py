# pages/1_Landing.py
import streamlit as st
from ui.nav import render_top_nav
from ui.header import render_global_head
from ui.landing import render_hero, render_feature_cards, render_journey, render_cta

st.set_page_config(
    page_title="Landing — AI Possibility Lab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_global_head()
render_top_nav(active="Landing")
render_hero()
render_feature_cards()
render_journey()
render_cta()
