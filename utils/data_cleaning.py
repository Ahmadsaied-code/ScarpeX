import re


def clean_price(price_text):
    try:
        nums = re.findall(r"[\d,]+(?:\.\d+)?", str(price_text))
        if not nums:
            return None
        return float(nums[0].replace(",", ""))
    except Exception:
        return None


def clean_rating(rating_text):
    try:
        match = re.search(r"(\d+(?:\.\d+)?)", str(rating_text))
        return float(match.group(1)) if match else None
    except Exception:
        return None


def clean_reviews(reviews_text):
    try:
        text = str(reviews_text).replace(",", "")
        match = re.search(r"(\d+)", text)
        return int(match.group(1)) if match else 0
    except Exception:
        return 0


def normalize_product(title, price, reviews=0, rating=None, link="", category="", source="", old_price=None):
    price_value = clean_price(price)
    rating_value = clean_rating(rating)
    reviews_value = clean_reviews(reviews)

    return {
        "title": str(title).strip() if title else "No title",
        "price": price_value,
        "price_text": str(price).strip() if price else "",
        "old_price": old_price or "",
        "rating": rating_value,
        "rating_text": str(rating).strip() if rating else "",
        "reviews": reviews_value,
        "link": link or "",
        "category": category or "",
        "source": source or "",
    }


def store_products(st, data, source_key):
    st.session_state[source_key] = data
    st.session_state.products_data = data

    st.session_state.api_data = [
        {
            "title": item.get("title"),
            "price": item.get("price"),
            "reviews": item.get("reviews"),
            "link": item.get("link"),
            "source": item.get("source"),
        }
        for item in data
    ]

    st.session_state.api_prices = [
        item.get("price") for item in data if item.get("price") is not None
    ]

    st.session_state.api_3d_data = [
        {
            "title": item.get("title"),
            "price": item.get("price") or 0,
            "rating": item.get("rating") or 0,
            "reviews": item.get("reviews") or 0,
            "source": item.get("source"),
        }
        for item in data
    ]
