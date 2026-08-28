from __future__ import annotations

from typing import Any

import streamlit as st

from services.images import banner_image_path, product_image_path, program_image_path
from services.store import format_price
from ui.components import badge_html, esc, qs


def show_banner(name: str, href: str, title: str, caption: str) -> None:
    path = banner_image_path(name)
    if path is not None:
        st.image(str(path), width="stretch")
    st.markdown(
        f'<a href="{esc(href)}" style="text-decoration:none;color:#1864ab;font-weight:700">{esc(title)}</a>'
        f'<div style="font-size:13px;color:#495057;margin:4px 0 10px">{esc(caption)}</div>',
        unsafe_allow_html=True,
    )


def show_product_grid(rows: list[dict[str, Any]], columns: int = 5, key_prefix: str = "p") -> None:
    if not rows:
        st.markdown('<div class="empty">조건에 맞는 상품이 없습니다.</div>', unsafe_allow_html=True)
        return
    _ = key_prefix
    for start in range(0, len(rows), columns):
        cols = st.columns(columns)
        chunk = rows[start : start + columns]
        for col, row in zip(cols, chunk):
            with col:
                path = product_image_path(str(row["id"]))
                if path is not None:
                    st.image(str(path), width="stretch")
                st.markdown(
                    f'<div style="font-size:11px;color:#868e96">{esc(row.get("brand") or "")}</div>'
                    f'<div>{badge_html(row)}</div>'
                    f'<a href="{esc(qs("/product", id=row["id"]))}" style="font-weight:600;text-decoration:none;color:#212529">{esc(row["name"])}</a>'
                    f'<div style="color:#c92a2a;font-weight:700;margin-top:4px">{esc(format_price(int(row.get("price") or 0)))}</div>'
                    f'<div style="font-size:11px;color:#868e96">★ {esc(row.get("rating"))} · {esc(row.get("region") or "")}</div>'
                    f'<div style="margin:8px 0 18px"><a href="{esc(qs("/product", id=row["id"]))}">상세</a>'
                    f' · <a href="{esc(qs("/", add=row["id"]))}">비교</a></div>',
                    unsafe_allow_html=True,
                )


def show_program_grid(rows: list[dict[str, Any]], columns: int = 2) -> None:
    if not rows:
        st.info("등록된 지원사업이 없습니다.")
        return
    for start in range(0, len(rows), columns):
        cols = st.columns(columns, gap="medium")
        chunk = rows[start : start + columns]
        for col, row in zip(cols, chunk):
            with col:
                with st.container(border=True):
                    photo, body = st.columns([1, 2.2])
                    with photo:
                        path = program_image_path(str(row["program_id"]))
                        if path is not None:
                            st.image(str(path), width="stretch")
                    with body:
                        st.markdown(f"**{esc(row['name'])}**")
                        st.caption(str(row.get("benefit") or ""))
                        st.caption(
                            f"대상 {row.get('region') or ''} · {row.get('care_rule') or ''} · "
                            f"주관 {row.get('agency') or ''} · 신청 {row.get('apply_period') or ''}"
                        )
                        st.caption(f"확인일 {row.get('verified_on') or ''} · 후보 안내, 최종은 기관 결정")
                        st.markdown(
                            f'<a href="{esc(qs("/support", pid=row["program_id"]))}">자세히 보기</a>'
                            f' · <a href="{esc(row.get("source_url") or "#")}" target="_blank">출처</a>',
                            unsafe_allow_html=True,
                        )
