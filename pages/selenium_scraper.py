import re
import time
from pathlib import Path
from urllib.parse import quote_plus

import pandas as pd
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from utils.data_cleaning import clean_price, normalize_product, store_products
from utils.ui import apply_theme, page_header

st.set_page_config(page_title="Selenium Scraper | ScrapeX", page_icon="🤖", layout="wide")
apply_theme()

page_header(
    "Selenium Browser Scraper",
    "Scrape dynamic product pages using a real Chrome browser. Choose Jumia or AliExpress, then send the results to the visual analytics pages.",
    "🤖",
)

st.warning(
    "This page needs Google Chrome installed locally. Run the app with: streamlit run main.py",
    icon="⚠️",
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


def make_driver(headless=False):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")

    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1450,1000")
    options.add_argument("--lang=en-US")

    return webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options,
    )


def scrape_jumia_selenium(search_query, max_items=40, headless=False):
    url = f"https://www.jumia.com.eg/catalog/?q={quote_plus(search_query)}"
    driver = make_driver(headless=headless)
    data = []

    try:
        driver.get(url)

        WebDriverWait(driver, 25).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "article.prd, article[class*='prd']"))
        )

        time.sleep(2.5)
        products = driver.find_elements(By.CSS_SELECTOR, "article.prd, article[class*='prd']")[:max_items]

        for product in products:
            def js_text(selector, default=""):
                try:
                    return driver.execute_script(
                        """
                        let el = arguments[0].querySelector(arguments[1]);
                        return el ? el.textContent.trim() : arguments[2];
                        """,
                        product,
                        selector,
                        default,
                    )
                except Exception:
                    return default

            title = js_text(".name, h3, .info h3")
            price = js_text(".prc, .price, [class*='prc']")
            old_price = js_text(".old, [class*='old']")
            rating = js_text(".stars, [class*='stars']")
            reviews = js_text(".rev, [class*='rev']", "0")

            try:
                link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
            except Exception:
                link = ""

            if not title or not price:
                try:
                    full_text = driver.execute_script("return arguments[0].innerText.trim();", product)
                    lines = [line.strip() for line in full_text.split("\n") if line.strip()]

                    if not title and lines:
                        title = lines[0]

                    if not price:
                        price = next((line for line in lines if "EGP" in line), "")
                except Exception:
                    pass

            if title and price:
                data.append(
                    normalize_product(
                        title=title,
                        price=price,
                        reviews=reviews,
                        rating=rating,
                        link=link,
                        category=search_query,
                        source="Jumia Selenium",
                        old_price=old_price,
                    )
                )

    finally:
        driver.quit()

    return data


def scrape_aliexpress_selenium(search_query, max_items=40, headless=False):
    url = f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(search_query)}"
    driver = make_driver(headless=headless)
    data = []

    try:
        driver.get(url)
        time.sleep(6)

        raw_items = driver.execute_script(
            """
            const maxItems = arguments[0];
            const links = Array.from(document.querySelectorAll('a[href*="/item/"], a[href*="item/"]'));
            const unique = [];
            const seen = new Set();

            for (const a of links) {
                const href = a.href || "";
                const text = (a.innerText || a.textContent || "").trim();

                if (!href || seen.has(href) || text.length < 15) continue;

                seen.add(href);
                unique.push({
                    href,
                    text,
                    title: a.getAttribute("title") || a.getAttribute("aria-label") || ""
                });

                if (unique.length >= maxItems) break;
            }

            return unique;
            """,
            max_items * 2,
        )

        for item in raw_items:
            text = item.get("text", "")
            lines = [line.strip() for line in text.split("\n") if line.strip()]

            title = item.get("title") or ""

            if not title:
                title_candidates = [
                    line for line in lines
                    if len(line) > 12
                    and "$" not in line
                    and "US" not in line
                    and "%" not in line
                    and "sold" not in line.lower()
                ]
                title = title_candidates[0] if title_candidates else ""

            price_line = ""
            for line in lines:
                if "$" in line or "EGP" in line or "US $" in line:
                    price_line = line
                    break

            rating_line = ""
            reviews_line = ""

            for line in lines:
                if re.search(r"\d+(?:\.\d+)?\s*stars?", line, re.I):
                    rating_line = line

                if "sold" in line.lower() or "review" in line.lower():
                    reviews_line = line

            if title and clean_price(price_line) is not None:
                data.append(
                    normalize_product(
                        title=title,
                        price=price_line,
                        reviews=reviews_line,
                        rating=rating_line,
                        link=item.get("href", ""),
                        category=search_query,
                        source="AliExpress Selenium",
                    )
                )

            if len(data) >= max_items:
                break

    finally:
        driver.quit()

    return data


marketplace = st.selectbox(
    "Choose Selenium marketplace",
    ["Jumia Egypt", "AliExpress"],
)

search_query = st.text_input(
    "Enter product to search:",
    value="watches for men",
    placeholder="Example: phones, laptops, headphones",
)

col1, col2 = st.columns(2)

with col1:
    max_items = st.slider("Maximum products", 10, 80, 40, 10)

with col2:
    headless = st.toggle("Run Chrome in headless mode", value=False)

run_button = st.button("🚀 Run Selenium Scraper", use_container_width=True)

if run_button:
    if not search_query.strip():
        st.error("Please enter a product name.")
        st.stop()

    with st.spinner(f"Opening Chrome and scraping {marketplace}..."):
        try:
            if marketplace == "Jumia Egypt":
                data = scrape_jumia_selenium(search_query.strip(), max_items=max_items, headless=headless)
                file_name = "jumia_selenium_data.csv"
                state_key = "jumia_data"
            else:
                data = scrape_aliexpress_selenium(search_query.strip(), max_items=max_items, headless=headless)
                file_name = "aliexpress_selenium_data.csv"
                state_key = "aliexpress_selenium_data"

            if not data:
                st.warning("No products found. Try another search query.")
                st.stop()

            store_products(st, data, state_key)
            df = pd.DataFrame(data)

            output_file = Path.cwd() / file_name
            df.to_csv(output_file, index=False, encoding="utf-8-sig")

            st.success(f"Saved {len(df)} products to {file_name}")
            st.caption(f"File location: {output_file}")
            st.dataframe(df, use_container_width=True)

            csv_data = df.to_csv(index=False).encode("utf-8-sig")
            st.download_button("⬇️ Download CSV", csv_data, file_name, "text/csv")

            st.markdown("### Continue to Visualizations")
            c1, c2, c3 = st.columns(3)
            c1.page_link("pages/network_graph.py", label="Network Graph", icon="🌐")
            c2.page_link("pages/price_heatmap.py", label="Price Heatmap", icon="🔥")
            c3.page_link("pages/scatter_3d.py", label="3D Scatter Plot", icon="🧊")

        except PermissionError:
            st.error("Close the CSV file from Excel first, then run again.")
        except Exception as e:
            st.error(f"Error while scraping {marketplace}: {e}")
