from __future__ import annotations

import streamlit as st

from services.store import current_user, login
from ui.layout import boot


def page() -> None:
    boot("로그인 · 생활케어")
    st.markdown(
        """
        <div class="wrap" style="padding-top:16px">
          <a href="/" style="text-decoration:none;color:#1864ab;font-weight:700">← 생활케어 홈</a>
        </div>
        <div class="login-card">
          <h2>로그인</h2>
          <p class="hint">
            PoC 데모 계정 (비밀번호 모두 demo123)<br/>
            customer 고객 · expert 전문케어관리사 · vendor 협력업체 · admin 관리자
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user = current_user()
    if user:
        st.success(f"{user['name']} 님으로 로그인되어 있습니다.")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("홈으로", use_container_width=True):
                st.switch_page("홈")
        with col2:
            if st.button("로그아웃", use_container_width=True):
                from services.store import logout

                logout()
                st.rerun()
        return

    with st.form("login_form"):
        login_id = st.text_input("아이디", placeholder="customer")
        password = st.text_input("비밀번호", type="password", placeholder="demo123")
        submitted = st.form_submit_button("로그인", use_container_width=True)
        if submitted:
            result = login(login_id, password)
            if result:
                st.rerun()
            else:
                st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

    st.caption("비밀번호는 해시로만 비교하며, 이 화면 입력값이 데이터베이스에 평문으로 저장되지 않습니다.")
