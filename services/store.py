from __future__ import annotations

import hashlib
from typing import Any

import pandas as pd
import streamlit as st

from services.catalog import CATEGORIES
from services.paths import PRODUCTS_CSV, PROGRAMS_CSV, VENDORS_CSV

SALT = "care-poc-v1"


def _hp(password: str) -> str:
    return hashlib.sha256(f"{SALT}:{password}".encode("utf-8")).hexdigest()


DEMO_USERS: dict[str, dict[str, str]] = {
    "customer": {"hash": _hp("demo123"), "role": "customer", "name": "김보호자"},
    "expert": {"hash": _hp("demo123"), "role": "expert", "name": "이수현 관리사"},
    "vendor": {"hash": _hp("demo123"), "role": "vendor", "name": "성남복지용구"},
    "admin": {"hash": _hp("demo123"), "role": "admin", "name": "본사관리자"},
}


@st.cache_data(show_spinner=False)
def load_products() -> pd.DataFrame:
    df = pd.read_csv(PRODUCTS_CSV, dtype=str, encoding="utf-8-sig")
    df["price"] = pd.to_numeric(df["price"], errors="coerce").fillna(0).astype(int)
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0)
    df["review_count"] = pd.to_numeric(df["review_count"], errors="coerce").fillna(0).astype(int)
    for col in ("subsidy_eligible", "is_ad", "is_popular"):
        df[col] = df[col].fillna("N").str.upper().eq("Y")
    df["badge"] = df["badge"].fillna("")
    return df


@st.cache_data(show_spinner=False)
def load_vendors() -> pd.DataFrame:
    return pd.read_csv(VENDORS_CSV, dtype=str, encoding="utf-8-sig")


@st.cache_data(show_spinner=False)
def load_programs() -> pd.DataFrame:
    return pd.read_csv(PROGRAMS_CSV, dtype=str, encoding="utf-8-sig")


def vendor_name(vendor_id: str) -> str:
    vendors = load_vendors()
    hit = vendors[vendors["vendor_id"] == vendor_id]
    if hit.empty:
        return vendor_id
    return str(hit.iloc[0]["name"])


def get_product(product_id: str) -> dict[str, Any] | None:
    df = load_products()
    hit = df[df["id"] == product_id]
    if hit.empty:
        return None
    return hit.iloc[0].to_dict()


def search_products(
    q: str = "",
    category: str = "",
    subcategory: str = "",
    sort: str = "popular",
    subsidy_only: bool = False,
) -> pd.DataFrame:
    df = load_products()
    if q:
        needle = q.strip().lower()
        blob = (
            df["name"].fillna("")
            + " "
            + df["brand"].fillna("")
            + " "
            + df["description"].fillna("")
            + " "
            + df["subcategory"].fillna("")
        ).str.lower()
        df = df[blob.str.contains(needle, regex=False)]
    if category:
        df = df[df["category"] == category]
    if subcategory:
        df = df[df["subcategory"] == subcategory]
    if subsidy_only:
        df = df[df["subsidy_eligible"]]
    if sort == "price_asc":
        df = df.sort_values(["price", "id"])
    elif sort == "price_desc":
        df = df.sort_values(["price", "id"], ascending=[False, True])
    elif sort == "rating":
        df = df.sort_values(["rating", "review_count"], ascending=[False, False])
    else:
        df = df.sort_values(["is_popular", "review_count", "rating"], ascending=[False, False, False])
    return df.reset_index(drop=True)


def category_label(code: str) -> str:
    for item in CATEGORIES:
        if item["code"] == code:
            return item["name"]
    return code


def format_price(value: int) -> str:
    if int(value) == 0:
        return "상담"
    return f"{int(value):,}원"


def current_user() -> dict[str, str] | None:
    return st.session_state.get("user")


def login(login_id: str, password: str) -> dict[str, str] | None:
    record = DEMO_USERS.get(login_id.strip())
    if not record:
        return None
    if record["hash"] != _hp(password):
        return None
    user = {"id": login_id, "role": record["role"], "name": record["name"]}
    st.session_state["user"] = user
    return user


def logout() -> None:
    st.session_state.pop("user", None)


def compare_ids() -> list[str]:
    ids = st.session_state.setdefault("compare_ids", [])
    return list(ids)


def add_compare(product_id: str) -> None:
    ids = st.session_state.setdefault("compare_ids", [])
    if product_id not in ids and len(ids) < 4:
        ids.append(product_id)


def remove_compare(product_id: str) -> None:
    ids = st.session_state.setdefault("compare_ids", [])
    if product_id in ids:
        ids.remove(product_id)


def clear_compare() -> None:
    st.session_state["compare_ids"] = []


def consume_query_actions() -> None:
    params = st.query_params
    if params.get("logout") == "1":
        logout()
        st.query_params.clear()
        st.rerun()
    add_id = params.get("add")
    if add_id:
        add_compare(str(add_id))
        next_q = {k: v for k, v in params.items() if k != "add"}
        st.query_params.clear()
        st.query_params.update(next_q)
        st.rerun()
    drop_id = params.get("drop")
    if drop_id:
        remove_compare(str(drop_id))
        next_q = {k: v for k, v in params.items() if k != "drop"}
        st.query_params.clear()
        st.query_params.update(next_q)
        st.rerun()
