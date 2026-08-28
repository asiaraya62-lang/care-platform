from __future__ import annotations

import streamlit as st

from services.store import consume_query_actions
from ui.components import footer_html, header_html, nav_html
from ui.styles import CSS


def boot(page_title: str = "생활케어") -> None:
    consume_query_actions()
    st.markdown(CSS, unsafe_allow_html=True)


def render_html(*parts: str) -> None:
    st.markdown("\n".join(parts), unsafe_allow_html=True)


def chrome(active: str, body: str, search_action: str = "/", q: str = "") -> None:
    _ = search_action
    render_html(header_html(active, q=q))
    _native_search(q)
    render_html(nav_html(active), body, footer_html())


def _native_search(q: str) -> None:
    st.markdown('<div class="wrap" style="padding:10px 0 8px">', unsafe_allow_html=True)
    with st.form("site_search", border=False):
        left, right = st.columns([6, 1], vertical_alignment="bottom")
        typed = left.text_input(
            "검색",
            value=q,
            placeholder="보행기, 욕실의자, 장기요양, 안전단말기…",
            label_visibility="collapsed",
        )
        submitted = right.form_submit_button("검색", use_container_width=True)
        if submitted:
            params = {k: v for k, v in st.query_params.items() if k != "q"}
            if typed.strip():
                params["q"] = typed.strip()
            st.query_params.clear()
            st.query_params.update(params)
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
