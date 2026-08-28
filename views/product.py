from __future__ import annotations

import streamlit as st

from services.images import product_image_path
from services.store import (
    category_label,
    format_price,
    get_product,
    search_products,
    vendor_name,
)
from ui.components import badge_html, esc, qs
from ui.layout import boot, end_shell, render_html, start_shell
from ui.media import show_product_grid


def page() -> None:
    boot("상품 상세 · 생활케어")
    pid = str(st.query_params.get("id") or "")
    item = get_product(pid)
    if not item:
        from ui.layout import chrome

        chrome(
            "catalog",
            '<div class="page-title">상품을 찾을 수 없습니다.</div><div class="section"><div class="empty">홈 또는 상품비교에서 다시 선택해 주세요.</div></div>',
        )
        return

    related_df = search_products(category=str(item["category"]))
    related = related_df[related_df["id"] != pid].head(5).to_dict("records")
    ad_note = ""
    if item.get("is_ad"):
        ad_note = '<div class="notice">이 상품은 광고 또는 유료노출입니다. 광고 여부는 적합성 판단과 분리됩니다.</div>'
    subsidy_note = ""
    if item.get("subsidy_eligible"):
        subsidy_note = (
            '<div class="notice">정부·지자체 지원 후보 상품입니다. '
            "지원 가능 여부와 금액은 전문케어관리사와 관계기관이 확인합니다.</div>"
        )

    start_shell("catalog")
    left, right = st.columns([1.1, 1.5])
    with left:
        path = product_image_path(pid)
        if path is not None:
            st.image(str(path), width="stretch")
    with right:
        render_html(
            f"""
            <div class="card-brand">{esc(item.get("brand") or "")} · {esc(category_label(str(item["category"])))}</div>
            <h2 style="margin:6px 0 8px;font-size:26px;letter-spacing:-0.04em">{esc(item["name"])}</h2>
            <div>{badge_html(item)}</div>
            <div class="card-price" style="font-size:28px;margin-top:16px">{esc(format_price(int(item["price"])))}</div>
            <div class="card-meta">가격 기준일 {esc(item.get("price_date") or "")} · 제공지역 {esc(item.get("region") or "")}</div>
            <div class="spec">
              {esc(item.get("description") or "")}<br/>
              협력업체 {esc(vendor_name(str(item.get("vendor_id") or "")))} · 평점 {esc(item.get("rating"))} · 후기 {int(item.get("review_count") or 0)}건
            </div>
            {ad_note}{subsidy_note}
            <div class="card-meta" style="margin-top:8px">AI 생성 참고 이미지이며 판매 상품 실물과 다를 수 있습니다.</div>
            <div class="login-actions" style="margin-top:18px;max-width:360px">
              <a class="btn btn-blue" href="/consult">이 상품으로 상담</a>
              <a class="btn btn-line" href="{esc(qs("/product", id=pid, add=pid))}">비교함 담기</a>
            </div>
            """
        )
    st.markdown("### 같은 분류 상품")
    show_product_grid(related, key_prefix="rel")
    end_shell()
