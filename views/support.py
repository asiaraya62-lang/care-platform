from __future__ import annotations

import streamlit as st

from services.store import load_programs
from ui.components import esc
from ui.layout import boot, chrome


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

    detail = ""
    if selected:
        detail = f"""
        <div class="section">
          <div class="section-head"><h2>{esc(selected["name"])}</h2></div>
          <p style="font-size:14px;line-height:1.6">
            주관 {esc(selected["agency"])} · 지역 {esc(selected["region"])}<br/>
            나이 {esc(selected["age_rule"])} · 소득 {esc(selected["income_rule"])} · 돌봄 {esc(selected["care_rule"])}<br/>
            지원내용 {esc(selected["benefit"])}<br/>
            신청기간 {esc(selected["apply_period"])} · 필요서류 {esc(selected["documents"])}
          </p>
          <div class="notice">
            이 정보는 후보 안내입니다. 자격과 금액은 기관이 최종 결정합니다.
            출처 <a href="{esc(selected["source_url"])}" target="_blank">{esc(selected["source_url"])}</a>
            · 최종확인일 {esc(selected["verified_on"])}
          </div>
        </div>
        """

    cards = []
    for row in rows:
        cards.append(
            f"""
            <a class="program" href="/support?pid={esc(row['program_id'])}">
              <b>{esc(row["name"])}</b>
              <p>{esc(row["benefit"])} · {esc(row["region"])} · {esc(row["apply_period"])}</p>
              <div class="src">출처 {esc(row["source_url"])} · 확인일 {esc(row["verified_on"])}</div>
            </a>
            """
        )

    body = f"""
    <div class="page-title">정부·지자체 지원사업</div>
    {detail}
    <div class="section">
      <div class="section-head"><h2>성남시 시범 목록 · {len(rows)}건</h2></div>
      <p style="font-size:13px;color:#495057">규칙 기반 목록입니다. AI가 사업을 지어내지 않도록 등록된 행만 보여 줍니다.</p>
      <div class="program-list">{''.join(cards)}</div>
    </div>
    """
    chrome("support", body, search_action="/support", q=q)
