import streamlit as st
from utils.ui import apply_theme, render_hero, render_feature_grid, render_spline_panel

st.set_page_config(
    page_title="ScrapeX | Product Intelligence Dashboard",
    page_icon="🛒",
    layout="wide",
)

apply_theme()

with st.sidebar:
    st.markdown("## 🛒 ScrapeX")
    st.caption("Professional product scraping dashboard")
    st.markdown("---")
    spline_url = st.text_input(
        "Spline Viewer URL",
        placeholder="Paste your Spline URL here",
        type="default",
    )
    st.caption("Optional: Export → Viewer URL from Spline.")
    st.markdown("---")
    st.page_link("main.py", label="Main", icon="🏠")
    st.page_link("pages/beautifulsoup_scraper.py", label="BeautifulSoup", icon="🍵")
    st.page_link("pages/multi_market_scraper.py", label="Multi-Market", icon="🛍️")
    st.page_link("pages/selenium_scraper.py", label="Selenium", icon="🤖")
    st.page_link("pages/network_graph.py", label="NetworkX", icon="🌐")
    st.page_link("pages/price_heatmap.py", label="Heatmap", icon="🔥")
    st.page_link("pages/scatter_3d.py", label="3D Scatter", icon="🧊")
    st.page_link("pages/project_wrap_up.py", label="Wrap-Up", icon="🎬")

left, right = st.columns([1.05, 0.95], gap="large")

with left:
    render_hero()

with right:
    render_spline_panel(spline_url)

st.markdown("---")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Sources", "5", "Jumia / eBay / Noon / Amazon / AliExpress")
c2.metric("Exports", "CSV", "Ready")
c3.metric("Visuals", "3+", "Network / Heatmap / 3D")
c4.metric("UI", "Pro", "Spline-ready")

st.markdown("## Project Modules")
st.markdown(
    "<p class='small-muted'>Choose a workflow from the sidebar or start with scraping, then move to visualizations.</p>",
    unsafe_allow_html=True,
)
render_feature_grid()

st.markdown(
    """
    <div class="footer-note">
        Built for DSAI 103 — Data Acquisition in Data Science.
    </div>
    """,
    unsafe_allow_html=True,
)
