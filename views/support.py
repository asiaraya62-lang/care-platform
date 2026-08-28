from __future__ import annotations

import streamlit as st

from services.images import program_image_path
from services.store import load_programs
from ui.components import esc
from ui.layout import boot, end_shell, start_shell
from ui.media import show_program_grid


def page() -> None:
    boot("정부지원 · 생활케어")
    pid = str(st.query_params.get("pid") or "")
    q = str(st.query_params.get("q") or "").strip()
    programs = load_programs()
    if q:
        blob = programs.astype(str).agg(" ".join, axis=1)
        programs = programs[blob.str.contains(q, regex=False)]
    rows = programs.to_dict("records")
    selected = next((r for r in rows if r["program_id"] == pid), None)

    start_shell("support", q=q)
    st.markdown('<div class="page-title">정부·지자체 지원사업</div>', unsafe_allow_html=True)

    if selected:
        photo, body = st.columns([1, 2.2])
        with photo:
            path = program_image_path(str(selected["program_id"]))
            if path is not None:
                st.image(str(path), width="stretch")
        with body:
            st.subheader(str(selected["name"]))
            st.caption(
                f"주관 {selected['agency']} · 지역 {selected['region']} · 신청 {selected['apply_period']}"
            )
            st.write(
                f"나이 {selected['age_rule']} · 소득 {selected['income_rule']} · 돌봄 {selected['care_rule']}"
            )
            st.write(f"지원내용 {selected['benefit']}")
            st.write(f"필요서류 {selected['documents']}")
            st.info("이 정보는 후보 안내입니다. 자격과 금액은 기관이 최종 결정합니다.")
            st.markdown(
                f'출처 <a href="{esc(selected["source_url"])}" target="_blank">{esc(selected["source_url"])}</a>'
                f' · 최종확인일 {esc(selected["verified_on"])}',
                unsafe_allow_html=True,
            )

    st.markdown(f"### 성남시 시범 목록 · {len(rows)}건")
    st.caption("규칙 기반 목록입니다. AI가 사업을 지어내지 않도록 등록된 행만 보여 줍니다.")
    show_program_grid(rows)
    end_shell()
