from __future__ import annotations

import streamlit as st

from views.catalog import page as catalog_page
from views.compare import page as compare_page
from views.consult import page as consult_page
from views.home import page as home_page
from views.login import page as login_page
from views.product import page as product_page
from views.support import page as support_page

st.set_page_config(
    page_title="생활케어",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="collapsed",
)

pages = [
    st.Page(home_page, title="홈", url_path="home", default=True),
    st.Page(catalog_page, title="상품비교", url_path="catalog"),
    st.Page(product_page, title="상품", url_path="product"),
    st.Page(support_page, title="정부지원", url_path="support"),
    st.Page(compare_page, title="비교함", url_path="compare"),
    st.Page(consult_page, title="돌봄상담", url_path="consult"),
    st.Page(login_page, title="로그인", url_path="login"),
]

pg = st.navigation(pages, position="hidden")
pg.run()
