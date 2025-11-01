import streamlit as st
from typing import List, Dict, Any
from services.ai import chat

def _history_key(key: str) -> str:
    return f"chat_history_{key}"

def ensure_history(key: str):
    hk = _history_key(key)
    if hk not in st.session_state:
        st.session_state[hk] = []

def append_history(key: str, sender: str, text: str):
    ensure_history(key)
    st.session_state[_history_key(key)].append({"role": sender, "content": text})

def chat_widget(key: str, system_prompt: str, title: str):
    ensure_history(key)

    st.markdown('<div class="apl-card" style="padding:16px;">', unsafe_allow_html=True)
    st.markdown(f"**{title}**")

    # history
    for m in st.session_state[_history_key(key)]:
        who = "me" if m["role"] == "user" else "ai"
        cls = "apl-bubble me" if who == "me" else "apl-bubble"
        st.markdown(f'<div class="{cls}">{m["content"]}</div>', unsafe_allow_html=True)

    with st.form(f"form_{key}", clear_on_submit=True):
        user_text = st.text_area("Message", height=90, label_visibility="collapsed", placeholder="Ask, refine, or explore...")
        submitted = st.form_submit_button("Send", use_container_width=True)
    if submitted and user_text.strip():
        append_history(key, "user", user_text.strip())
        with st.spinner("Thinking..."):
            content = chat(system_prompt, user_text, history=st.session_state[_history_key(key)])
        append_history(key, "assistant", content)

    st.markdown('</div>', unsafe_allow_html=True)
