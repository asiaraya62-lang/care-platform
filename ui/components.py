from __future__ import annotations

import html
from typing import Any
from urllib.parse import urlencode

from services.catalog import CATEGORIES, category_by_code
from services.store import (
    compare_ids,
    current_user,
    format_price,
    vendor_name,
)


def esc(value: Any) -> str:
    return html.escape("" if value is None else str(value))


def qs(path: str, **params: Any) -> str:
    cleaned = {k: v for k, v in params.items() if v not in (None, "", False)}
    if not cleaned:
        return path
    return f"{path}?{urlencode(cleaned, doseq=True)}"


def badge_html(row: dict[str, Any]) -> str:
    bits = []
    if row.get("is_ad"):
        bits.append('<span class="badge ad">광고</span>')
    if row.get("subsidy_eligible"):
        bits.append('<span class="badge gov">지원가능</span>')
    if row.get("is_popular"):
        bits.append('<span class="badge pop">인기</span>')
    badge = str(row.get("badge") or "")
    if badge in ("구독",):
        bits.append('<span class="badge sub">구독</span>')
    if badge == "상담":
        bits.append('<span class="badge pop">상담</span>')
    return "".join(bits)


def thumb_style(row: dict[str, Any]) -> str:
    cat = category_by_code(str(row.get("category") or ""))
    color = cat["tone"] if cat else "#1864ab"
    return f"background:{color};"


def product_img_src(row: dict[str, Any]) -> str:
    return ""


def product_card(row: dict[str, Any], show_compare: bool = True) -> str:
    name = esc(row["name"])
    brand = esc(row.get("brand") or "")
    price = format_price(int(row.get("price") or 0))
    rating = row.get("rating") or 0
    reviews = int(row.get("review_count") or 0)
    compare_link = qs("/", add=row["id"]) if show_compare else ""
    compare_btn = (
        f'<a href="{esc(compare_link)}">비교</a>' if show_compare else ""
    )
    img = product_img_src(row)
    if img:
        photo = f'<img src="{esc(img)}" alt="{name}" />'
    else:
        photo = f'<div class="thumb-fallback" style="{thumb_style(row)}">{esc(row.get("subcategory") or "")}</div>'
    return f"""
    <div class="card">
      <a href="{esc(qs('/product', id=row['id']))}">
        <div class="thumb">
          {photo}
          <div class="badges">{badge_html(row)}</div>
        </div>
      </a>
      <div class="card-body">
        <div class="card-brand">{brand}</div>
        <a class="card-name" href="{esc(qs('/product', id=row['id']))}">{name}</a>
        <div class="card-price">{esc(price)}</div>
        <div class="card-meta">★ {esc(rating)} · 후기 {reviews:,} · {esc(row.get("region") or "")}</div>
        <div class="card-actions">
          <a href="{esc(qs('/product', id=row['id']))}">상세</a>
          {compare_btn}
        </div>
      </div>
    </div>
    """


def product_grid(rows: list[dict[str, Any]], columns: int = 5) -> str:
    klass = {4: "grid grid-4", 6: "grid grid-6"}.get(columns, "grid")
    cards = "".join(product_card(r) for r in rows)
    return f'<div class="{klass}">{cards}</div>'


def header_html(active: str, search_action: str = "/", q: str = "") -> str:
    _ = search_action
    _ = q
    user = current_user()
    if user:
        auth = (
            f'<span>{esc(user["name"])}</span>'
            f'<a href="/?logout=1">로그아웃</a>'
        )
    else:
        auth = '<a class="util-strong" href="/login">로그인</a><a href="/login">회원가입</a>'
    nav = []
    items = [
        ("home", "/", "홈"),
        ("catalog", "/catalog", "상품비교"),
        ("support", "/support", "정부지원"),
        ("consult", "/consult", "돌봄상담"),
        ("compare", "/compare", "비교함"),
    ]
    for key, href, label in items:
        cls = "active" if key == active else ""
        nav.append(f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>')
    compared = len(compare_ids())
    return f"""
    <div class="topbar">
      <div class="topbar-inner">
        <div>통합 생활케어 플랫폼 · 성남시 시범 PoC · 가상데이터</div>
        <div>
          <a href="/support">지원사업 출처 확인</a>
          <a href="/consult">전문가 상담</a>
          {auth}
        </div>
      </div>
    </div>
    <div class="header">
      <div class="header-inner">
        <a class="logo" href="/">
          <div class="logo-mark">케어</div>
          <div class="logo-text"><b>생활케어</b><span>돌봄 상품 · 지원 · 지역연결</span></div>
        </a>
        <div class="header-utils">
          <a href="/compare">비교함 {compared}</a>
          <a href="/consult">돌봄상담</a>
        </div>
      </div>
    </div>
    """


def nav_html(active: str) -> str:
    nav = []
    items = [
        ("home", "/", "홈"),
        ("catalog", "/catalog", "상품비교"),
        ("support", "/support", "정부지원"),
        ("consult", "/consult", "돌봄상담"),
        ("compare", "/compare", "비교함"),
    ]
    for key, href, label in items:
        cls = "active" if key == active else ""
        nav.append(f'<a class="{cls}" href="{esc(href)}">{esc(label)}</a>')
    return f"""
    <div class="nav">
      <div class="nav-inner">
        <div class="nav-left">
          <a class="cat-btn" href="/catalog">전체 카테고리</a>
          <div class="nav-links">{''.join(nav)}</div>
        </div>
        <div class="nav-right">AI 추천은 사전 안내 · 최종 확인은 전문가</div>
      </div>
    </div>
    """


def footer_html() -> str:
    n = len(compare_ids())
    tray = ""
    if n:
        names = []
        from services.store import get_product

        for pid in compare_ids():
            item = get_product(pid)
            label = item["name"] if item else pid
            names.append(
                f'<span>{esc(label)} <a href="{esc(qs("/", drop=pid))}">×</a></span>'
            )
        tray = f"""
        <div class="tray">
          <div class="tray-inner">
            <div class="tray-items">비교함 {n}/4 {' '.join(names)}</div>
            <div><a class="btn btn-blue" href="/compare">비교하기</a></div>
          </div>
        </div>
        """
    return f"""
    {tray}
    <div class="footer">
      <div class="footer-inner">
        <b>생활케어 플랫폼 PoC</b><br/>
        본 화면의 상품·가격·지원사업은 시연용 가상정보입니다. 정부지원 승인 여부는 관계기관이 결정합니다.
        광고·유료노출 상품은 적합성 평가와 분리되어 있으며 따로 표시합니다.<br/>
        개인정보 처리방침 · 이용약관 · 제3자 제공 안내 · 고객센터 031-000-0000<br/>
        사업자 가상등록 · 기준일 2026-08-28
      </div>
    </div>
    """


def category_panel() -> str:
    items = []
    for cat in CATEGORIES:
        items.append(
            f"""<a class="cat-item" href="{esc(qs('/catalog', cat=cat['code']))}">
              <div class="cat-dot" style="background:{esc(cat['tone'])}">{esc(cat['short'][:2])}</div>
              <div>{esc(cat['name'])}<small>{esc(cat['blurb'])}</small></div>
            </a>"""
        )
    items.append(
        f"""<a class="cat-item" href="/support">
          <div class="cat-dot" style="background:#495057">지원</div>
          <div>공공지원 연계<small>보조금·서류 안내</small></div>
        </a>"""
    )
    return f'<div class="panel cat-panel">{"".join(items)}</div>'
