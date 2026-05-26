import json
import re
import time
from urllib.parse import quote_plus, urljoin

import requests
from bs4 import BeautifulSoup

from utils.data_cleaning import clean_price, normalize_product


DEFAULT_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9,ar;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def dedupe_products(products, limit=50):
    seen = set()
    clean = []

    for item in products:
        title = str(item.get("title", "")).strip()
        price = item.get("price")
        source = str(item.get("source", "")).strip()

        if not title or title.lower() == "no title":
            continue

        key = (title[:80].lower(), str(price), source.lower())
        if key in seen:
            continue

        seen.add(key)
        clean.append(item)

        if len(clean) >= limit:
            break

    return clean


def safe_get(url, timeout=35):
    response = requests.get(url, headers=DEFAULT_HEADERS, timeout=timeout)
    response.raise_for_status()
    return response


def serpapi_get(params):
    response = requests.get("https://serpapi.com/search", params=params, timeout=45)

    try:
        payload = response.json()
    except Exception:
        payload = {}

    if response.status_code != 200:
        message = payload.get("error") or payload.get("message") or response.reason
        raise RuntimeError(f"SerpAPI error {response.status_code}: {message}")

    if isinstance(payload, dict) and payload.get("error"):
        raise RuntimeError(f"SerpAPI error: {payload.get('error')}")

    return payload


def make_link(base_url, link):
    if not link:
        return ""
    return urljoin(base_url, link)


def extract_json_objects(obj, source, category, base_url="", limit=60):
    products = []

    def get_title(d):
        keys = [
            "title", "name", "productName", "product_name", "displayName",
            "display_name", "productTitle", "description"
        ]
        for key in keys:
            val = d.get(key)
            if isinstance(val, str):
                val = val.strip()
                if 8 <= len(val) <= 220 and not val.startswith("http"):
                    return val
        return ""

    def get_link(d):
        keys = [
            "url", "link", "productUrl", "product_url", "canonicalUrl",
            "canonical_url", "href", "webUrl"
        ]
        for key in keys:
            val = d.get(key)
            if isinstance(val, str) and val.strip():
                return make_link(base_url, val.strip())
        return ""

    def find_price(value, depth=0):
        if depth > 3:
            return None

        if isinstance(value, (int, float)):
            return float(value)

        if isinstance(value, str):
            return clean_price(value)

        if isinstance(value, dict):
            preferred = [
                "price", "salePrice", "sale_price", "sellingPrice", "selling_price",
                "currentPrice", "current_price", "amount", "value", "minPrice",
                "maxPrice", "raw", "extracted"
            ]

            for key in preferred:
                if key in value:
                    found = find_price(value[key], depth + 1)
                    if found is not None:
                        return found

            for val in value.values():
                found = find_price(val, depth + 1)
                if found is not None:
                    return found

        return None

    def walk(value):
        if len(products) >= limit:
            return

        if isinstance(value, dict):
            title = get_title(value)
            price = find_price(value)
            link = get_link(value)
            rating = value.get("rating") or value.get("averageRating") or value.get("ratingValue")
            reviews = value.get("reviews") or value.get("reviewCount") or value.get("ratingsTotal") or 0

            if title and price is not None:
                products.append(
                    normalize_product(
                        title=title,
                        price=price,
                        reviews=reviews,
                        rating=rating,
                        link=link,
                        category=category,
                        source=source,
                    )
                )

            for child in value.values():
                walk(child)

        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(obj)
    return dedupe_products(products, limit=limit)


def extract_ld_json_products(soup, source, category, base_url, limit=50):
    products = []

    for script in soup.select("script[type='application/ld+json']"):
        try:
            data = json.loads(script.get_text(strip=True))
        except Exception:
            continue

        products.extend(extract_json_objects(data, source, category, base_url, limit))

        if len(products) >= limit:
            break

    return dedupe_products(products, limit=limit)


def extract_next_data_products(soup, source, category, base_url, limit=50):
    script = soup.find("script", id="__NEXT_DATA__")
    if not script:
        return []

    try:
        data = json.loads(script.get_text(strip=True))
    except Exception:
        return []

    return extract_json_objects(data, source, category, base_url, limit)


def scrape_noon_direct(query, max_items=50):
    base_url = "https://www.noon.com"
    url = f"https://www.noon.com/egypt-en/search/?q={quote_plus(query)}"

    response = safe_get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    products = []
    products.extend(extract_ld_json_products(soup, "Noon Direct", query, base_url, max_items))
    products.extend(extract_next_data_products(soup, "Noon Direct", query, base_url, max_items))

    cards = soup.select(
        "[data-qa='product-name'], [class*='product'], a[href*='/egypt-en/'], a[href*='/uae-en/']"
    )

    for card in cards:
        text = card.get_text(" ", strip=True)
        if len(text) < 10:
            continue

        parent = card
        for _ in range(4):
            if parent.parent:
                parent = parent.parent

        full_text = parent.get_text(" ", strip=True)
        price_match = re.search(r"(?:EGP|AED|SAR|جنيه|د\.إ|ر\.س)?\s*[\d,]+(?:\.\d+)?", full_text)
        price = price_match.group(0) if price_match else ""

        title = text[:180]

        link_el = parent.select_one("a[href]")
        link = make_link(base_url, link_el.get("href", "")) if link_el else ""

        if title and clean_price(price) is not None:
            products.append(
                normalize_product(
                    title=title,
                    price=price,
                    reviews=0,
                    rating=None,
                    link=link,
                    category=query,
                    source="Noon Direct",
                )
            )

        if len(products) >= max_items:
            break

    return dedupe_products(products, max_items)


def scrape_amazon_direct(query, max_items=50, amazon_domain="amazon.eg"):
    base_url = f"https://www.{amazon_domain}"
    url = f"{base_url}/s?k={quote_plus(query)}"

    response = safe_get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    page_text = soup.get_text(" ", strip=True).lower()
    if "captcha" in page_text or "robot check" in page_text:
        raise RuntimeError("Amazon returned a CAPTCHA / robot-check page. Use the SerpAPI Amazon option instead.")

    cards = soup.select("div[data-component-type='s-search-result']")
    products = []

    for card in cards[:max_items]:
        title_el = card.select_one("h2 span, span.a-size-medium, span.a-size-base-plus")
        price_el = card.select_one(".a-price .a-offscreen")
        rating_el = card.select_one("span.a-icon-alt")
        reviews_el = card.select_one("span.a-size-base.s-underline-text, a.a-link-normal.s-underline-text span")
        link_el = card.select_one("a.a-link-normal.s-no-outline, h2 a")

        title = title_el.get_text(strip=True) if title_el else ""
        price = price_el.get_text(strip=True) if price_el else ""
        rating = rating_el.get_text(strip=True) if rating_el else ""
        reviews = reviews_el.get_text(strip=True) if reviews_el else 0
        link = make_link(base_url, link_el.get("href", "")) if link_el else ""

        if title and price:
            products.append(
                normalize_product(
                    title=title,
                    price=price,
                    reviews=reviews,
                    rating=rating,
                    link=link,
                    category=query,
                    source=f"Amazon Direct ({amazon_domain})",
                )
            )

    return dedupe_products(products, max_items)


def scrape_aliexpress_selenium(query, max_items=40, headless=False):
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager

    url = f"https://www.aliexpress.com/wholesale?SearchText={quote_plus(query)}"

    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--window-size=1450,1000")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-gpu")
    options.add_argument("--lang=en-US")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    products = []

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
                    if len(line) > 12 and "$" not in line and "US" not in line and "%" not in line
                ]
                title = title_candidates[0] if title_candidates else ""

            price_line = ""
            for line in lines:
                if "$" in line or "EGP" in line or "US" in line:
                    price_line = line
                    break

            rating_line = ""
            reviews_line = ""

            for line in lines:
                if re.search(r"\d+(?:\.\d+)?\s*stars?", line, re.I):
                    rating_line = line
                if "sold" in line.lower() or "review" in line.lower():
                    reviews_line = line

            price_value = clean_price(price_line)

            if title and price_value is not None:
                products.append(
                    normalize_product(
                        title=title,
                        price=price_line,
                        reviews=reviews_line,
                        rating=rating_line,
                        link=item.get("href", ""),
                        category=query,
                        source="AliExpress Selenium",
                    )
                )

            if len(products) >= max_items:
                break

    finally:
        driver.quit()

    return dedupe_products(products, max_items)




def serpapi_ebay(api_key, query, max_items=50):
    params = {
        "engine": "ebay",
        "api_key": api_key,
        "_nkw": query,
        "output": "json",
    }

    results = serpapi_get(params)
    organic = results.get("organic_results", [])[:max_items]
    products = []

    for item in organic:
        price = item.get("price", "")
        if isinstance(price, dict):
            price = price.get("raw") or price.get("extracted") or ""

        products.append(
            normalize_product(
                title=item.get("title", "No title"),
                price=price,
                reviews=item.get("reviews", 0),
                rating=item.get("rating", None),
                link=item.get("link", ""),
                category=query,
                source="eBay SerpAPI",
            )
        )

    return dedupe_products(products, max_items)


def serpapi_amazon(api_key, query, max_items=50, amazon_domain="amazon.eg"):
    params = {
        "engine": "amazon",
        "api_key": api_key,
        "k": query,
        "amazon_domain": amazon_domain,
    }

    results = serpapi_get(params)
    organic = results.get("organic_results", [])[:max_items]
    products = []

    for item in organic:
        price = item.get("price", "")
        if isinstance(price, dict):
            price = price.get("raw") or price.get("extracted") or ""

        link = item.get("link", "")
        if not link and item.get("asin"):
            link = f"https://www.{amazon_domain}/dp/{item.get('asin')}"

        products.append(
            normalize_product(
                title=item.get("title", "No title"),
                price=price,
                reviews=item.get("reviews", 0),
                rating=item.get("rating", None),
                link=link,
                category=query,
                source=f"Amazon SerpAPI ({amazon_domain})",
            )
        )

    return dedupe_products(products, max_items)


def serpapi_google_shopping(api_key, query, market_name, max_items=50, gl="us", hl="en"):
    marketplace_query = f"{market_name} {query}"

    attempts = [
        {
            "engine": "google_shopping",
            "api_key": api_key,
            "q": marketplace_query,
            "gl": gl,
            "hl": hl,
            "google_domain": "google.com",
        },
        {
            "engine": "google_shopping",
            "api_key": api_key,
            "q": marketplace_query,
            "gl": "us",
            "hl": "en",
            "google_domain": "google.com",
        },
        {
            "engine": "google_shopping_light",
            "api_key": api_key,
            "q": marketplace_query,
            "gl": "us",
            "hl": "en",
            "google_domain": "google.com",
        },
    ]

    last_error = None
    results = None

    for params in attempts:
        try:
            results = serpapi_get(params)
            break
        except Exception as exc:
            last_error = exc
            continue

    if results is None:
        raise RuntimeError(str(last_error))

    shopping = results.get("shopping_results", []) or results.get("organic_results", [])
    shopping = shopping[: max_items * 2]

    products = []
    market_lower = market_name.lower()

    for item in shopping:
        source_text = str(item.get("source", "")).lower()
        link_text = str(item.get("product_link") or item.get("link") or "").lower()

        if market_lower not in source_text and market_lower not in link_text:
            if len(products) >= max(5, max_items // 3):
                continue

        price = item.get("price") or item.get("extracted_price") or ""

        products.append(
            normalize_product(
                title=item.get("title", "No title"),
                price=price,
                reviews=item.get("reviews", 0),
                rating=item.get("rating", None),
                link=item.get("product_link") or item.get("link") or "",
                category=query,
                source=f"{market_name.title()} Google Shopping API",
            )
        )

        if len(products) >= max_items:
            break

    return dedupe_products(products, max_items)
