import pandas as pd
import streamlit as st

from utils.data_cleaning import store_products
from utils.marketplace_scrapers import (
    serpapi_ebay,
    serpapi_amazon,
    serpapi_google_shopping,
)
from utils.ui import apply_theme, page_header

st.set_page_config(page_title="Multi-Market Scraper | ScrapeX", page_icon="🛍️", layout="wide")
apply_theme()

page_header(
    "Multi-Market API Scraper",
    "Fetch product data from eBay, Amazon, Noon, and AliExpress, then send the data to the visual analytics pages.",
    "🛍️",
)

with st.sidebar:
    st.markdown("## 🛒 ScrapeX")
    st.caption("Professional product scraping dashboard")
    st.markdown("---")
    st.page_link("main.py", label="Main", icon="🏠")
    st.page_link("pages/beautifulsoup_scraper.py", label="BeautifulSoup", icon="🍵")
    st.page_link("pages/multi_market_scraper.py", label="Multi-Market", icon="🛍️")
    st.page_link("pages/selenium_scraper.py", label="Selenium", icon="🤖")
    st.page_link("pages/network_graph.py", label="NetworkX", icon="🌐")
    st.page_link("pages/price_heatmap.py", label="Heatmap", icon="🔥")
    st.page_link("pages/scatter_3d.py", label="3D Scatter", icon="🧊")
    st.page_link("pages/project_wrap_up.py", label="Wrap-Up", icon="🎬")

st.markdown(
    """
    <div class="glass-card">
        <h3 style="margin-top:0;">Recommended Setup</h3>
        <p class="small-muted">
        This page is for API-based marketplaces only: eBay, Amazon, Noon, and AliExpress.
        Browser-based scraping is now organized separately inside the Selenium Scraper page.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")

col1, col2 = st.columns([1.1, 0.9], gap="large")

with col1:
    search_query = st.text_input(
        "Search query",
        value="watches for men",
        placeholder="Example: phones, laptops, headphones",
    )

    method = st.selectbox(
        "Choose marketplace / method",
        [
            "eBay — SerpAPI eBay Search (Recommended)",
            "Amazon — SerpAPI Amazon Search (Recommended)",
            "Noon — SerpAPI Google Shopping (Recommended)",
            "AliExpress — SerpAPI Google Shopping (Recommended)",
        ],
    )

with col2:
    max_items = st.slider("Maximum products", 10, 100, 40, 10)
    amazon_domain = st.selectbox(
        "Amazon domain",
        ["amazon.eg", "amazon.com", "amazon.ae", "amazon.sa"],
        index=0,
    )

api_key = st.text_input(
    "SerpAPI Key",
    type="password",
    placeholder="Required for all Multi-Market API methods",
)
st.caption("Your key is hidden in the UI and will not be printed in error messages.")

run = st.button("🚀 Run Multi-Market API Scraper", use_container_width=True)

if run:
    if not search_query.strip():
        st.error("Please enter a search query.")
        st.stop()

    if not api_key.strip():
        st.error("Please enter your SerpAPI key.")
        st.stop()

    with st.spinner(f"Running: {method}"):
        try:
            if method == "eBay — SerpAPI eBay Search (Recommended)":
                data = serpapi_ebay(
                    api_key.strip(),
                    search_query.strip(),
                    max_items=max_items,
                )

            elif method == "Amazon — SerpAPI Amazon Search (Recommended)":
                data = serpapi_amazon(
                    api_key.strip(),
                    search_query.strip(),
                    max_items=max_items,
                    amazon_domain=amazon_domain,
                )

            elif method == "Noon — SerpAPI Google Shopping (Recommended)":
                data = serpapi_google_shopping(
                    api_key.strip(),
                    search_query.strip(),
                    market_name="Noon",
                    max_items=max_items,
                )

            elif method == "AliExpress — SerpAPI Google Shopping (Recommended)":
                data = serpapi_google_shopping(
                    api_key.strip(),
                    search_query.strip(),
                    market_name="AliExpress",
                    max_items=max_items,
                )

            else:
                data = []

            if not data:
                st.warning("No products found. Try another query or another API method.")
                st.stop()

            store_products(st, data, "multi_market_data")

            df = pd.DataFrame(data)
            st.success(f"Loaded {len(df)} products from {method}")
            st.dataframe(df, use_container_width=True)

            csv_data = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button(
                "⬇️ Download Multi-Market CSV",
                csv_data,
                "multi_market_products.csv",
                "text/csv",
            )

            st.markdown("### Continue to Visualizations")
            c1, c2, c3 = st.columns(3)
            c1.page_link("pages/network_graph.py", label="Network Graph", icon="🌐")
            c2.page_link("pages/price_heatmap.py", label="Price Heatmap", icon="🔥")
            c3.page_link("pages/scatter_3d.py", label="3D Scatter", icon="🧊")

        except Exception as e:
            error_message = str(e)
            if api_key:
                error_message = error_message.replace(api_key.strip(), "****")
            st.error(f"Scraping failed: {error_message}")
            st.info("Tip: eBay and Amazon SerpAPI options are usually the most stable.")

st.markdown("---")

with st.expander("What this page does"):
    st.markdown(
        """
        **Multi-Market API Scraper**
        - Uses SerpAPI-based methods only.
        - Covers eBay, Amazon, Noon, and AliExpress from one page.
        - The output is automatically connected to Network Graph, Price Heatmap, and 3D Scatter Plot.

        **Browser Scraping**
        - Jumia Selenium and AliExpress Selenium are now inside the Selenium Scraper page.
        """
    )
