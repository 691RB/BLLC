import streamlit as st
<p class="lp-meta">Mary Lou Fulton College of Learning and Teaching Innovation | Arizona State University<br/>Created by R. Beghetto (2025)</p>
</section>
""",
unsafe_allow_html=True,
)


def render_feature_cards():
st.markdown('<div class="apl-container">', unsafe_allow_html=True)
c1, c2 = st.columns([1, 1], gap="large")

with c1:
st.markdown('<div class="lp-card">', unsafe_allow_html=True)
st.markdown('<div class="lp-badge">' + LIGHTBULB + '</div>', unsafe_allow_html=True)
st.markdown('<h3 class="lp-card-title">Build to Learn</h3>', unsafe_allow_html=True)
st.markdown(
'<p class="lp-card-text">Transform your ideas into reality by building custom AI solutions. Learn through hands-on creation and experimentation with cutting-edge AI technology.</p>',
unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

with c2:
st.markdown('<div class="lp-card">', unsafe_allow_html=True)
st.markdown('<div class="lp-badge">' + ROCKET + '</div>', unsafe_allow_html=True)
st.markdown('<h3 class="lp-card-title">Learn to Create</h3>', unsafe_allow_html=True)
st.markdown(
'<p class="lp-card-text">Apply your knowledge to develop functional AI tools. Iterate and refine through continuous learning cycles to create impactful solutions.</p>',
unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


def render_journey():
st.markdown(
"""
<section class="apl-container">
<h2 class="lp-journey-title">Your Journey</h2>
<div class="lp-journey">
<div class="lp-step"><span class="lp-step-icon">💡</span><span>Inspiration</span></div>
<div class="lp-connector"></div>
<div class="lp-step"><span class="lp-step-icon">🔍</span><span>Problem Finding</span></div>
<div class="lp-connector"></div>
<div class="lp-step"><span class="lp-step-icon">👥</span><span>Collaboration</span></div>
<div class="lp-connector"></div>
<div class="lp-step"><span class="lp-step-icon">🛡️</span><span>Bot Identity</span></div>
<div class="lp-connector"></div>
<div class="lp-step"><span class="lp-step-icon">🛠️</span><span>UI Design</span></div>
<div class="lp-connector"></div>
<div class="lp-step"><span class="lp-step-icon">✨</span><span>Deployment</span></div>
</div>
</section>
""",
unsafe_allow_html=True,
)


def render_cta():
st.markdown(
"""
<div class="lp-cta-wrap">
<a class="lp-cta" href="2_Possibility.py">Let's Build! <span class="lp-arrow">→</span></a>
</div>
""",
unsafe_allow_html=True,
)
