# pages/1_Landing.py
import streamlit as st
from ui.nav import render_top_nav
from ui.header import render_global_head
from ui.landing import render_hero, render_feature_cards, render_cta

st.set_page_config(
    page_title="Landing — AI Possibility Lab",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Global head + top nav
render_global_head()
render_top_nav(active="Landing")

# Landing content (Hero → Two cards → CTA)
render_hero()
render_feature_cards()
render_cta()

