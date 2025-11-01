# ui/landing.py
import streamlit as st

# --- Inline SVG icons ---
LIGHTBULB = """
<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M9 18h6" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M10 22h4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M12 2a7 7 0 0 0-4 12c.5.5 1 1.5 1 2.5V17h6v-.5c0-1 .5-2 1-2.5A7 7 0 0 0 12 2Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

ROCKET = """
<svg width="34" height="34" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
  <path d="M5 15c-1 3-3 4-3 4s1 0 4-1c.5 0 1-.5 1.5-1.5L9 14l-3-1Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
  <path d="M14 10l-4 4" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/>
  <path d="M14 3c4 0 7 3 7 7 0 4-3 7-7 7-2 0-3.5-.5-5-1.5L6 17l1.5-3c-1-1.5-1.5-3-1.5-5 0-4 3-6 8-6Z" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

def render_hero():
    st.markdown(
        """
<section class="lp-hero">
  <h1 class="lp-title">AI Possibility Lab</h1>
  <p class="lp-tagline">Build to Learn, Learn to Create</p>
  <p class="lp-meta">Mary Lou Fulton College of Learning and Teaching Innovation | Arizona State University<br/>Created by R. Beghetto (2025)</p>
</section>
        """,
        unsafe_allow_html=True,
    )

def render_feature_cards():
    # Build each card as ONE html string so nesting is preserved.
    left_card = f"""
<div class="lp-card">
  <div class="lp-badge">{LIGHTBULB}</div>
  <h3 class="lp-card-title">Build to Learn</h3>
  <p class="lp-card-text">
    Transform your ideas into reality by building custom AI solutions.
    Learn through hands-on creation and experimentation with cutting-edge AI technology.
  </p>
</div>
"""
    right_card = f"""
<div class="lp-card">
  <div class="lp-badge">{ROCKET}</div>
  <h3 class="lp-card-title">Learn to Create</h3>
  <p class="lp-card-text">
    Apply your knowledge to develop functional AI tools.
    Iterate and refine through continuous learning cycles to create impactful solutions.
  </p>
</div>
"""

    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 1], gap="large")
    c1.markdown(left_card, unsafe_allow_html=True)
    c2.markdown(right_card, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

def render_cta():
    # Inline style guarantees no underline even before CSS loads.
    st.markdown(
        """
<div class="lp-cta-wrap">
  <a class="lp-cta" style="text-decoration:none" href="pages/2_Possibility.py">
    Let's Build! <span class="lp-arrow">→</span>
  </a>
</div>
        """,
        unsafe_allow_html=True,
    )
