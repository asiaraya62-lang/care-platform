from __future__ import annotations

import streamlit as st

from services.store import (
    category_label,
    format_price,
    get_product,
    vendor_name,
)
from ui.components import esc, qs
from ui.layout import boot, chrome


def page() -> None:
    boot("비교함 · 생활케어")
    ids = st.session_state.get("compare_ids") or []
    items = [get_product(pid) for pid in ids]
    items = [row for row in items if row]
    if len(items) < 2:
        body = f"""
        <div class="page-title">상품 비교</div>
        <div class="section">
          <div class="empty">비교는 2개 이상부터 가능합니다. 상품 카드의 ‘비교’를 눌러 담아 주세요. 현재 {len(items)}개.</div>
        </div>
        """
        chrome("compare", body)
        return

    headers = ["항목"] + [esc(row["name"]) for row in items]
    def cells(label: str, values: list[str]) -> str:
        tds = "".join(f"<td>{v}</td>" for v in values)
        return f"<tr><th>{esc(label)}</th>{tds}</tr>"

    rows = [
        cells("브랜드", [esc(r.get("brand")) for r in items]),
        cells("분류", [esc(category_label(str(r["category"]))) for r in items]),
        cells("가격", [esc(format_price(int(r["price"]))) for r in items]),
        cells("지원 가능 표시", ["예" if r.get("subsidy_eligible") else "아니오" for r in items]),
        cells("광고", ["광고" if r.get("is_ad") else "일반" for r in items]),
        cells("지역", [esc(r.get("region")) for r in items]),
        cells("업체", [esc(vendor_name(str(r.get("vendor_id") or ""))) for r in items]),
        cells("평점", [esc(r.get("rating")) for r in items]),
        cells("기준일", [esc(r.get("price_date")) for r in items]),
        cells(
            "상세",
            [f'<a href="{esc(qs("/product", id=r["id"]))}">보기</a>' for r in items],
        ),
    ]
    body = f"""
    <div class="page-title">상품 비교 · {len(items)}개</div>
    <div class="section">
      <p style="font-size:13px;color:#495057;margin-top:0">광고 상품이 있어도 적합성을 자동으로 높이지 않습니다. 최종 선택은 전문가 검토 후 진행합니다.</p>
      <table class="compare-table">
        <tr>{''.join(f'<th>{h}</th>' for h in headers)}</tr>
        {''.join(rows)}
      </table>
    </div>
    """
    chrome("compare", body)
