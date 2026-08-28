from __future__ import annotations

from datetime import datetime

import streamlit as st

from ui.layout import boot


def page() -> None:
    boot("돌봄상담 · 생활케어")
    st.markdown(
        """
        <div class="wrap" style="padding:16px 0 0">
          <a href="/" style="text-decoration:none;color:#1864ab;font-weight:700">← 생활케어 홈</a>
          <h2 style="margin:12px 0 8px">돌봄 상담 접수</h2>
          <p style="color:#495057;font-size:14px">
            건강·거동·주거 상황을 입력하면 다음 단계에서 AI 요약과 전문케어관리사 검토가 붙습니다.
            지금은 가상 데이터만 브라우저 세션에 저장합니다. 실제 진단서를 올리지 마세요.
          </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cases = st.session_state.setdefault("intake_cases", [])

    with st.form("intake"):
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("나이대", ["65–69", "70–74", "75–79", "80세 이상"])
            region = st.selectbox("거주지역", ["성남시 수정구", "성남시 중원구", "성남시 분당구"])
            grade = st.selectbox(
                "장기요양·장애",
                ["해당 없음", "장기요양 1등급", "장기요양 2등급", "장기요양 3등급", "장기요양 4–5등급", "등록장애인"],
            )
        with col2:
            mobility = st.selectbox("거동", ["독립 보행", "보조기 보행", "휠체어", "와상"])
            housing = st.multiselect("주거 불편", ["계단", "문턱", "욕실 미끄러움", "안전손잡이 없음", "독거"])
            consent = st.checkbox("민감정보(건강·장애) 처리에 동의합니다. (PoC 가상)")
        trouble = st.text_area(
            "지금 가장 불편한 점",
            placeholder="예: 퇴원 후 화장실 이동과 목욕이 어렵습니다.",
        )
        submitted = st.form_submit_button("상담 접수", use_container_width=True)
        if submitted:
            if not consent:
                st.error("민감정보 동의가 없으면 건강·장애 관련 분석을 진행할 수 없습니다.")
            elif not trouble.strip():
                st.error("불편사항을 입력해 주세요.")
            else:
                cases.append(
                    {
                        "at": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "age": age,
                        "region": region,
                        "grade": grade,
                        "mobility": mobility,
                        "housing": ", ".join(housing) or "없음",
                        "trouble": trouble.strip(),
                        "status": "신규접수",
                    }
                )
                st.session_state["intake_cases"] = cases
                st.success("접수가 저장되었습니다. 다음 단계에서 AI 추천과 전문가 배정이 연결됩니다.")

    if cases:
        st.subheader("내 상담 목록 (이 브라우저 세션)")
        st.dataframe(cases, use_container_width=True, hide_index=True)
