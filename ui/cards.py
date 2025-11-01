import streamlit as st

def process_cards():
    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    with st.container(border=False):
        c1, c2, c3 = st.columns([1,1,1], gap="large")
        with c1:
            st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
            st.markdown("#### Define Possibility")
            st.write("Clarify WHAT, WHO, WHY, HOW, and your assistant’s contribution.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c2:
            st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
            st.markdown("#### Shape Identity")
            st.write("Craft ROLE, GOAL, RULES, KNOWLEDGE, ACTIONS, and GUIDELINES.")
            st.markdown('</div>', unsafe_allow_html=True)
        with c3:
            st.markdown('<div class="apl-card" style="padding:18px;">', unsafe_allow_html=True)
            st.markdown("#### Generate & Build")
            st.write("Preview UI, generate files, and download a scaffold.")
            st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

def journey_steps():
    st.markdown('<div class="apl-container">', unsafe_allow_html=True)
    with st.container(border=False):
        st.markdown('<div class="apl-card" style="padding:22px;">', unsafe_allow_html=True)
        st.markdown("### Journey")
        st.write("1) Explore possibilities → 2) Shape identity → 3) UI preview → 4) Build files → 5) Iterate.")
        st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
