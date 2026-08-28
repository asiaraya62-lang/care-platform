from __future__ import annotations

import streamlit as st

from services.catalog import CATEGORIES
from services.store import current_user, load_programs, search_products
from ui.components import category_panel, esc, product_grid, qs
from ui.layout import boot, chrome


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
    body = f"""
    <div class="page-title">‘{esc(q)}’ 검색 결과 · 상품 {len(rows)}건 · 지원사업 {len(hits)}건</div>
    <div class="section">
      <div class="section-head"><h2>상품·서비스</h2><a href="/catalog">자세히 보기</a></div>
      {product_grid(rows) if rows else '<div class="empty">일치하는 상품이 없습니다. 보행기, 욕실, 단말기처럼 다른 단어로 찾아 보세요.</div>'}
    </div>
    <div class="section">
      <div class="section-head"><h2>정부·지자체 지원사업</h2><a href="/support">전체 보기</a></div>
      {_program_cards(hits) if hits else '<div class="empty">검색어에 맞는 지원사업이 없습니다. 출처와 기준일은 각 사업 상세에서 확인합니다.</div>'}
    </div>
    """
    chrome("home", body, search_action="/", q=q)


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

    sections = []
    for cat in CATEGORIES:
        rows = search_products(category=cat["code"]).head(5).to_dict("records")
        subs = "".join(
            f'<a href="{esc(qs("/catalog", cat=cat["code"], sub=s))}">{esc(s)}</a>'
            for s in cat["subs"][:5]
        )
        sections.append(
            f"""
            <div class="section">
              <div class="section-head">
                <h2>{esc(cat["name"])}</h2>
                <div class="sub-links">{subs}</div>
                <a href="{esc(qs("/catalog", cat=cat["code"]))}">{esc(cat["short"])} 더보기</a>
              </div>
              {product_grid(rows)}
            </div>
            """
        )

    body = f"""
    <div class="hero">
      {category_panel()}
      <div class="banners">
        <a class="banner b1" href="/consult">
          <b>퇴원 후 돌봄,<br/>한곳에서 연결</b>
          <span>불편사항을 입력하면 상품·지원·지역업체를 함께 안내합니다.</span>
        </a>
        <a class="banner b2" href="/support">
          <b>정부·지자체 지원</b>
          <span>성남시 시범 데이터 · 출처와 기준일 표시</span>
        </a>
        <a class="banner b3" href="/catalog">
          <b>가격·후기·지역 비교</b>
          <span>광고 상품은 따로 표시합니다</span>
        </a>
        <a class="banner b4" href="{esc(qs("/catalog", cat="emergency"))}">
          <b>긴급 안전단말기</b>
          <span>PoC는 모의 경보 · 112 자동연결 없음</span>
        </a>
      </div>
      <div style="display:flex;flex-direction:column;gap:12px;">
        {side_login}
        <div class="panel side-box">
          <h3>오늘 안내</h3>
          <ul class="quick-list">
            <li><a href="/support">장기요양 복지용구 연 한도</a></li>
            <li><a href="/catalog?cat=home">욕실 안전손잡이 시공</a></li>
            <li><a href="/catalog?cat=life">정기 청소·방제 구독</a></li>
          </ul>
        </div>
      </div>
    </div>
    <div class="section">
      <div class="section-head">
        <h2>오늘의 돌봄 추천</h2>
        <a href="/catalog">인기순 전체</a>
      </div>
      {product_grid(popular)}
    </div>
    <div class="section">
      <div class="section-head">
        <h2>낮은 가격순</h2>
        <a href="/catalog?sort=price_asc">가격비교</a>
      </div>
      {product_grid(cheap)}
    </div>
    {''.join(sections)}
    <div class="section">
      <div class="section-head">
        <h2>정부·지자체 지원사업 후보</h2>
        <a href="/support">전체 보기</a>
      </div>
      {_program_cards(programs)}
    </div>
    """
    chrome("home", body, search_action="/")


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
