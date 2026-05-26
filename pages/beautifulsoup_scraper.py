import urllib3
from urllib.parse import quote_plus

import pandas as pd
import requests
import streamlit as st
from bs4 import BeautifulSoup

from utils.data_cleaning import normalize_product, store_products
from utils.ui import apply_theme, page_header

st.set_page_config(page_title="BeautifulSoup Scraper | ScrapeX", page_icon="🍵", layout="wide")
apply_theme()

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

page_header(
    "BeautifulSoup Static Scraper",
    "Scrape live Jumia Egypt search results using Requests and BeautifulSoup.",
    "🍵",
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

search_q = st.text_input("Enter what to search on Jumia:", value="watches", placeholder="e.g. watches, phones, laptops")
max_items = st.slider("Maximum products", min_value=10, max_value=80, value=40, step=10)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}

run = st.button("🚀 Scrape Jumia with BeautifulSoup", use_container_width=True)

if run:
    if not search_q.strip():
        st.error("Please enter a search query.")
        st.stop()

    url = f"https://www.jumia.com.eg/catalog/?q={quote_plus(search_q.strip())}"

    with st.spinner("Scraping Jumia search results..."):
        try:
            response = requests.get(url, headers=HEADERS, verify=False, timeout=30)

            with st.expander("Debug information"):
                st.write("Status code:", response.status_code)
                st.write("Fetched URL:", response.url)

            soup = BeautifulSoup(response.content, "html.parser")
            items = soup.select("article.prd, article[class*='prd']")[:max_items]

            st.caption(f"Raw product cards found: {len(items)}")

            data = []
            progress = st.progress(0)

            for i, item in enumerate(items):
                if len(items) > 0:
                    progress.progress((i + 1) / len(items))

                title_el = item.select_one("h3.name, .name, h3")
                price_el = item.select_one("div.prc, .prc, [class*='prc']")
                old_price_el = item.select_one(".old, [class*='old']")
                review_el = item.select_one(".rev, [class*='rev']")
                rating_el = item.select_one(".stars, [class*='stars']")
                link_el = item.select_one("a")

                title = title_el.get_text(strip=True) if title_el else ""
                price = price_el.get_text(strip=True) if price_el else ""
                old_price = old_price_el.get_text(strip=True) if old_price_el else ""
                reviews = review_el.get_text(strip=True) if review_el else "0"
                rating = rating_el.get_text(strip=True) if rating_el else ""
                link = link_el.get("href", "") if link_el else ""

                if link.startswith("/"):
                    link = "https://www.jumia.com.eg" + link

                if title and price:
                    data.append(
                        normalize_product(
                            title=title,
                            price=price,
                            reviews=reviews,
                            rating=rating,
                            link=link,
                            category=search_q.strip(),
                            source="Jumia BeautifulSoup",
                            old_price=old_price,
                        )
                    )

            if not data:
                st.warning("No products found. Jumia may have changed the page structure or blocked the request.")
                st.stop()

            store_products(st, data, "beautifulsoup_data")
            st.session_state.bu_prices = [item["price"] for item in data if item["price"] is not None]
            st.session_state.scraped_data = data

            df = pd.DataFrame(data)
            st.success(f"Found {len(df)} products")
            st.dataframe(df, use_container_width=True)

            csv = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Download CSV", csv, "jumia_beautifulsoup_data.csv", "text/csv")

            st.markdown("### Continue")
            c1, c2, c3 = st.columns(3)
            c1.page_link("pages/network_graph.py", label="Network Graph", icon="🌐")
            c2.page_link("pages/price_heatmap.py", label="Price Heatmap", icon="🔥")
            c3.page_link("pages/scatter_3d.py", label="3D Scatter", icon="🧊")

        except requests.exceptions.Timeout:
            st.error("Request timed out. Try again.")
        except requests.exceptions.ConnectionError:
            st.error("Connection failed. Check your internet connection.")
        except Exception as e:
            st.error(f"Error while scraping: {e}")
