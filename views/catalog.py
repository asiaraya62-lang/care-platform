from __future__ import annotations

import streamlit as st

from services.catalog import CATEGORIES, category_by_code
from services.store import search_products
from ui.components import esc, qs
from ui.layout import boot, end_shell, render_html, start_shell
from ui.media import show_product_grid


def page() -> None:
    boot("상품비교 · 생활케어")
    q = str(st.query_params.get("q") or "").strip()
    cat = str(st.query_params.get("cat") or "").strip()
    sub = str(st.query_params.get("sub") or "").strip()
    sort = str(st.query_params.get("sort") or "popular").strip()
    subsidy = str(st.query_params.get("gov") or "") == "1"

    rows = search_products(
        q=q, category=cat, subcategory=sub, sort=sort, subsidy_only=subsidy
    ).to_dict("records")
    cat_info = category_by_code(cat)
    title = cat_info["name"] if cat_info else "전체 상품·서비스"
    if sub:
        title = f"{title} · {sub}"
    if q:
        title = f"‘{q}’ 검색 · {title}"

    cat_links = ['<a href="/catalog">전체</a>']
    for item in CATEGORIES:
        cls = "on" if item["code"] == cat else ""
        cat_links.append(
            f'<a class="{cls}" href="{esc(qs("/catalog", cat=item["code"], q=q))}">{esc(item["name"])}</a>'
        )

    sorts = [
        ("popular", "인기순"),
        ("price_asc", "낮은 가격"),
        ("price_desc", "높은 가격"),
        ("rating", "평점순"),
    ]
    sort_links = []
    for code, label in sorts:
        cls = "on" if sort == code else ""
        sort_links.append(
            f'<a class="{cls}" href="{esc(qs("/catalog", cat=cat, sub=sub, q=q, sort=code, gov="1" if subsidy else ""))}">{esc(label)}</a>'
        )
    gov_cls = "on" if subsidy else ""
    gov_link = qs("/catalog", cat=cat, sub=sub, q=q, sort=sort, gov="" if subsidy else "1")

    sub_links = ""
    if cat_info:
        bits = []
        for s in cat_info["subs"]:
            cls = "on" if s == sub else ""
            bits.append(
                f'<a class="{cls}" href="{esc(qs("/catalog", cat=cat, sub=s, q=q, sort=sort))}">{esc(s)}</a>'
            )
        sub_links = f'<div class="sub-links" style="margin-top:8px">{"".join(bits)}</div>'

    start_shell("catalog", q=q)
    render_html(
        f"""
        <div class="page-title">{esc(title)} <span style="font-size:14px;color:#868e96;font-weight:400">{len(rows)}개</span></div>
        <div class="filter-bar">{" · ".join(cat_links)}</div>
        <div class="filter-bar">
          {" · ".join(sort_links)}
          · <a class="{gov_cls}" href="{esc(gov_link)}">정부지원 가능만</a>
          {sub_links}
        </div>
        """
    )
    show_product_grid(rows, key_prefix="cat")
    end_shell()
