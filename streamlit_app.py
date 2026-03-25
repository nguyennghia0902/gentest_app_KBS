import streamlit as st

home_page = st.Page("st_home.py", title="Trang chủ", icon="🏠")
gen_test_page = st.Page("st_gentest_app.py", title="Tạo đề kiểm tra", icon="📝")

pg = st.navigation([home_page, gen_test_page])

st.markdown("""
<style>
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stText"] {
    font-size: 1.15rem !important;
}

[data-testid="stRadio"] label {
    font-size: 1.1rem !important;
}

[data-testid="stCode"] code,
[data-testid="stCode"] pre {
    font-size: 1.05rem !important;
    line-height: 1.6 !important;
}
</style>
""", unsafe_allow_html=True)

pg.run()