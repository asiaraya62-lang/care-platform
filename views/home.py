from __future__ import annotations

import streamlit as st

from services.catalog import CATEGORIES
from services.store import current_user, load_programs, search_products
from ui.components import category_panel, esc, qs
from ui.layout import boot, end_shell, render_html, start_shell
from ui.media import show_banner, show_product_grid


def page() -> None:
    boot("생활케어")
    q = str(st.query_params.get("q") or "").strip()
    if q:
        _search_home(q)
        return
    _portal_home()


def _search_home(q: str) -> None:
    rows = search_products(q=q).to_dict("records")
    programs = load_programs()
    blob = (
        programs["name"].fillna("")
        + programs["benefit"].fillna("")
        + programs["agency"].fillna("")
    )
    hits = programs[blob.str.contains(q, regex=False)].to_dict("records")
    start_shell("home", q=q)
    render_html(
        f'<div class="page-title">‘{esc(q)}’ 검색 결과 · 상품 {len(rows)}건 · 지원사업 {len(hits)}건</div>'
    )
    st.subheader("상품·서비스")
    show_product_grid(rows, key_prefix="search")
    render_html(
        '<div class="section"><div class="section-head"><h2>정부·지자체 지원사업</h2></div>'
        + _program_cards(hits)
        + "</div>"
    )
    end_shell()


def _portal_home() -> None:
    user = current_user()
    if user:
        side_login = f"""
        <div class="panel side-box">
          <h3>{esc(user['name'])} 님</h3>
          <p>역할: {esc(user['role'])}. 배정된 케이스와 상담은 다음 단계에서 연결됩니다.</p>
          <div class="login-actions">
            <a class="btn btn-blue" href="/consult">돌봄상담</a>
            <a class="btn btn-line" href="/?logout=1">로그아웃</a>
          </div>
        </div>
        """
    else:
        side_login = """
        <div class="panel side-box">
          <h3>로그인</h3>
          <p>데모 계정으로 고객·전문가·업체·관리자 화면을 나눠 볼 수 있습니다.</p>
          <div class="login-actions">
            <a class="btn btn-blue" href="/login">로그인</a>
            <a class="btn btn-line" href="/consult">비회원 상담</a>
          </div>
          <ul class="quick-list">
            <li><a href="/consult">불편사항 입력하기</a></li>
            <li><a href="/support">우리 지역 지원사업</a></li>
            <li><a href="/catalog?cat=emergency">안전단말기</a></li>
          </ul>
        </div>
        """

    popular = search_products(sort="popular").head(10).to_dict("records")
    cheap = search_products(sort="price_asc")
    cheap = cheap[cheap["price"] > 0].head(10).to_dict("records")
    programs = load_programs().head(6).to_dict("records")

    start_shell("home")
    left, center, right = st.columns([1.15, 2.4, 1.15])
    with left:
        render_html(category_panel())
    with center:
        show_banner(
            "consult",
            "/consult",
            "퇴원 후 돌봄, 한곳에서 연결",
            "불편사항을 입력하면 상품·지원·지역업체를 함께 안내합니다.",
        )
        g1, g2 = st.columns(2)
        with g1:
            show_banner(
                "gov",
                "/support",
                "정부·지자체 지원",
                "성남시 시범 데이터 · 출처와 기준일 표시",
            )
        with g2:
            show_banner(
                "compare",
                "/catalog",
                "가격·후기·지역 비교",
                "광고 상품은 따로 표시합니다",
            )
        show_banner(
            "emergency",
            qs("/catalog", cat="emergency"),
            "긴급 안전단말기",
            "PoC는 모의 경보 · 112 자동연결 없음",
        )
    with right:
        render_html(
            side_login
            + """
            <div class="panel side-box" style="margin-top:12px">
              <h3>오늘 안내</h3>
              <ul class="quick-list">
                <li><a href="/support">장기요양 복지용구 연 한도</a></li>
                <li><a href="/catalog?cat=home">욕실 안전손잡이 시공</a></li>
                <li><a href="/catalog?cat=life">정기 청소·방제 구독</a></li>
              </ul>
            </div>
            """
        )

    st.markdown("### 오늘의 돌봄 추천")
    show_product_grid(popular, key_prefix="pop")
    st.markdown("### 낮은 가격순")
    show_product_grid(cheap, key_prefix="cheap")
    for cat in CATEGORIES:
        rows = search_products(category=cat["code"]).head(5).to_dict("records")
        st.markdown(f"### {cat['name']}")
        show_product_grid(rows, key_prefix=cat["code"])
    render_html(
        '<div class="section"><div class="section-head"><h2>정부·지자체 지원사업 후보</h2><a href="/support">전체 보기</a></div>'
        + _program_cards(programs)
        + "</div>"
    )
    end_shell()


def _program_cards(rows: list[dict]) -> str:
    if not rows:
        return '<div class="empty">등록된 지원사업이 없습니다.</div>'
    cards = []
    for row in rows:
        cards.append(
            f"""
            <a class="program" href="{esc(qs("/support", pid=row["program_id"]))}">
              <b>{esc(row["name"])}</b>
              <p>{esc(row["benefit"])} · 대상 {esc(row["region"])} · {esc(row["care_rule"])}</p>
              <div class="src">출처 {esc(row["source_url"])} · 확인일 {esc(row["verified_on"])}</div>
            </a>
            """
        )
    return f'<div class="program-list">{"".join(cards)}</div>'
