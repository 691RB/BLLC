import streamlit as st

PAGES = [
("Landing", "1_Landing", "home"),
("Possibility Finding", "2_Possibility", "search"),
("Bot Identity", "3_Identity", "id-card"),
("UI Design", "4_UI_Designer", "wrench"),
("Build App", "5_Build", "sparkles"),
]

# Minimal Lucide-like SVGs (names are just labels; we inline the path)
ICONS = {
"home": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 9l9-7 9 7"/><path d="M9 22V12h6v10"/></svg>',
"search": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="8"/><path d="M21 21l-3.5-3.5"/></svg>',
"id-card": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 8h10"/><circle cx="8.5" cy="14" r="1.5"/><path d="M12 13h5"/><path d="M12 16h5"/></svg>',
"wrench": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a4 4 0 1 0-5.7 5.7l-6.3 6.3 2 2 6.3-6.3a4 4 0 0 0 5.7-5.7z"/></svg>',
"sparkles": '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l1.5 4.5L18 9l-4.5 1.5L12 15l-1.5-4.5L6 9l4.5-1.5L12 3z"/><path d="M19 16l.8 2.2L22 19l-2.2.8L19 22l-.8-2.2L16 19l2.2-.8L19 16z"/></svg>',
}


def _pill(label: str, href: str, icon: str, active: bool) -> str:
return f"""
<a class="apl-pill {'is-active' if active else ''}" href="{href}">
<span class="apl-pill-icon">{ICONS.get(icon,'')}</span>
<span>{label}</span>
</a>
"""


def render_top_nav(active: str = "Landing"):
st.markdown('<div class="apl-topbar"><div class="apl-topbar-inner">', unsafe_allow_html=True)
# left: nothing (screenshot shows just the pill group)

# right: pill nav
markup = [
'<nav class="apl-nav">',
]
for label, stub, icon in PAGES:
href = f"pages/{stub}.py"
is_active = (label == active)
markup.append(_pill(label, href, icon, is_active))
markup.append('</nav>')

st.markdown("".join(markup), unsafe_allow_html=True)
st.markdown('</div></div>', unsafe_allow_html=True)
