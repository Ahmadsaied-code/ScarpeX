import numpy as np
import pandas as pd
import streamlit as st

from utils.ui import apply_theme

st.set_page_config(page_title="Price Heatmap | ScrapeX", page_icon="🔥", layout="wide")
apply_theme()

try:
    import plotly.express as px
    import plotly.graph_objects as go
except ModuleNotFoundError:
    st.error("Plotly is not installed. Run this command in the project folder:")
    st.code("pip install -r requirements.txt\n# or\npip install plotly", language="bash")
    st.stop()

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
    <style>
    .hm-hero {
      position: relative;
      overflow: hidden;
      border-radius: 34px;
      border: 1px solid rgba(255,255,255,.12);
      background:
        radial-gradient(circle at 18% 22%, rgba(248,113,113,.18), transparent 32%),
        radial-gradient(circle at 82% 14%, rgba(103,232,249,.19), transparent 32%),
        linear-gradient(135deg, rgba(15,23,42,.74), rgba(2,6,23,.50));
      padding: 34px;
      margin-bottom: 26px;
      box-shadow: 0 30px 110px rgba(0,0,0,.30);
    }

    .hm-hero::before {
      content:"";
      position:absolute;
      inset:0;
      background-image:
        linear-gradient(rgba(255,255,255,.035) 1px, transparent 1px),
        linear-gradient(90deg, rgba(255,255,255,.035) 1px, transparent 1px);
      background-size: 46px 46px;
      mask-image: radial-gradient(circle at center, black, transparent 76%);
      pointer-events:none;
    }

    .hm-grid {
      position:relative;
      z-index:2;
      display:grid;
      grid-template-columns: 1.08fr .92fr;
      gap: 28px;
      align-items:center;
    }

    .hm-pill {
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 16px;
      border-radius:999px;
      background:rgba(255,255,255,.07);
      border:1px solid rgba(255,255,255,.13);
      color:rgba(255,255,255,.78);
      font-size:13px;
      backdrop-filter:blur(16px);
      animation: fadeUp .7s ease both;
    }

    .hm-title {
      margin: 20px 0 0;
      font-size: clamp(44px, 6vw, 80px);
      line-height:1;
      letter-spacing:-.075em;
      font-weight:950;
      animation: fadeUp .8s ease both .08s;
    }

    .hm-grad {
      background: linear-gradient(90deg, #fecaca, #fca5a5, #67e8f9);
      -webkit-background-clip:text;
      color:transparent;
    }

    .hm-lead {
      margin-top:20px;
      max-width:760px;
      color:rgba(255,255,255,.63);
      line-height:1.85;
      font-size:17px;
      animation: fadeUp .8s ease both .16s;
    }

    .hm-live {
      position:relative;
      min-height: 310px;
      border-radius: 30px;
      border: 1px solid rgba(255,255,255,.12);
      background: rgba(2,6,23,.50);
      backdrop-filter: blur(20px);
      overflow:hidden;
      box-shadow: 0 28px 90px rgba(0,0,0,.24);
    }

    .hm-live::before {
      content:"";
      position:absolute;
      inset:-40%;
      background:
        conic-gradient(from 90deg, rgba(103,232,249,.0), rgba(103,232,249,.22), rgba(248,113,113,.18), rgba(192,132,252,.18), rgba(103,232,249,.0));
      animation: rotateBg 10s linear infinite;
    }

    .hm-live-inner {
      position:absolute;
      inset: 14px;
      border-radius: 24px;
      background: rgba(2,6,23,.78);
      border:1px solid rgba(255,255,255,.09);
      padding:18px;
      display:grid;
      grid-template-columns: repeat(6, 1fr);
      gap:9px;
    }

    .cell {
      border-radius: 12px;
      background: rgba(103,232,249,.10);
      animation: heatPulse var(--speed) ease-in-out infinite;
      opacity:.45;
    }

    .cell:nth-child(3n) { background: rgba(248,113,113,.18); }
    .cell:nth-child(4n) { background: rgba(192,132,252,.16); }

    .pro-panel {
      border:1px solid rgba(255,255,255,.11);
      background:rgba(255,255,255,.055);
      border-radius:28px;
      padding:22px;
      backdrop-filter: blur(20px);
      box-shadow:0 24px 80px rgba(0,0,0,.20);
    }

    .hint-card {
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.06);
      border-radius:28px;
      padding:26px;
      color:rgba(255,255,255,.64);
      line-height:1.8;
    }

    @keyframes fadeUp {
      from { opacity:0; transform: translateY(24px); }
      to { opacity:1; transform: translateY(0); }
    }

    @keyframes rotateBg {
      from { transform: rotate(0); }
      to { transform: rotate(360deg); }
    }

    @keyframes heatPulse {
      0%,100% { transform: scale(.92); opacity:.35; filter: brightness(.8); }
      50% { transform: scale(1.04); opacity:.95; filter: brightness(1.4); }
    }

    @media(max-width: 900px) {
      .hm-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

cells = "".join(
    f'<div class="cell" style="--speed:{2.4 + (i % 7) * .35}s;"></div>'
    for i in range(36)
)

st.markdown(
    f"""
    <div class="hm-hero">
      <div class="hm-grid">
        <div>
          <div class="hm-pill">🔥 Live Interactive Price Intelligence</div>
          <h1 class="hm-title">Marketplace <span class="hm-grad">Heatmap</span></h1>
          <p class="hm-lead">
            A client-ready analytical dashboard for exploring price concentration, source behavior,
            product density, and marketplace patterns with interactive hover, filters, and export.
          </p>
        </div>
        <div class="hm-live">
          <div class="hm-live-inner">{cells}</div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def collect_products():
    rows = []
    keys = [
        "beautifulsoup_data",
        "serpapi_data",
        "jumia_data",
        "multi_market_data",
        "aliexpress_selenium_data",
        "products_data",
        "api_data",
        "scraped_data",
    ]

    for key in keys:
        for item in st.session_state.get(key, []) or []:
            price = item.get("price")
            try:
                price = float(price)
            except (TypeError, ValueError):
                continue

            if price <= 0:
                continue

            rows.append(
                {
                    "title": item.get("title", "Product"),
                    "price": price,
                    "source": item.get("source", key.replace("_", " ").title()),
                    "reviews": pd.to_numeric(item.get("reviews", 0), errors="coerce"),
                    "rating": pd.to_numeric(item.get("rating", 0), errors="coerce"),
                    "category": item.get("category", ""),
                    "link": item.get("link", ""),
                }
            )

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows)
    df = df.drop_duplicates(subset=["title", "price", "source"])
    df["reviews"] = df["reviews"].fillna(0)
    df["rating"] = df["rating"].fillna(0)
    return df


df = collect_products()

if df.empty:
    st.markdown(
        """
        <div class="hint-card">
          <h3 style="margin-top:0;color:white;">No product data loaded yet.</h3>
          Run any scraper first, then return here. This page will become fully interactive once data is loaded.
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    c1.page_link("pages/beautifulsoup_scraper.py", label="BeautifulSoup", icon="🍵")
    c2.page_link("pages/multi_market_scraper.py", label="Multi-Market API", icon="🛍️")
    c3.page_link("pages/selenium_scraper.py", label="Selenium", icon="🤖")
    st.stop()

st.markdown("### Control Center")

f1, f2, f3 = st.columns([1.15, 1.15, .8])

with f1:
    sources = sorted(df["source"].dropna().unique().tolist())
    selected_sources = st.multiselect("Sources", sources, default=sources)

filtered = df[df["source"].isin(selected_sources)].copy()

if filtered.empty:
    st.warning("No data after filtering sources.")
    st.stop()

min_price = float(filtered["price"].min())
max_price = float(filtered["price"].max())

with f2:
    if min_price == max_price:
        price_range = (min_price, max_price)
        st.caption(f"Single price value detected: {min_price:,.2f}")
    else:
        price_range = st.slider(
            "Price range",
            min_value=min_price,
            max_value=max_price,
            value=(min_price, max_price),
        )

with f3:
    bins_count = st.slider("Heatmap bins", 5, 45, 18)

filtered = filtered[
    (filtered["price"] >= price_range[0]) &
    (filtered["price"] <= price_range[1])
].copy()

if filtered.empty:
    st.warning("No products in selected price range.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Products", f"{len(filtered):,}")
k2.metric("Sources", f"{filtered['source'].nunique():,}")
k3.metric("Average Price", f"{filtered['price'].mean():,.2f}")
k4.metric("Max Price", f"{filtered['price'].max():,.2f}")

st.markdown("---")

if filtered["price"].nunique() == 1:
    filtered["price_bucket"] = "Single Price"
else:
    filtered["price_bucket"] = pd.cut(filtered["price"], bins=bins_count, duplicates="drop")

heat = (
    filtered
    .groupby(["source", "price_bucket"], observed=False)
    .size()
    .reset_index(name="products")
)

heat["bucket_label"] = heat["price_bucket"].astype(str)
pivot = heat.pivot(index="source", columns="bucket_label", values="products").fillna(0)

st.markdown("### Interactive Source × Price Density")

fig = go.Figure(
    data=go.Heatmap(
        z=pivot.values,
        x=pivot.columns.tolist(),
        y=pivot.index.tolist(),
        colorscale="Turbo",
        hoverongaps=False,
        hovertemplate="<b>%{y}</b><br>Price bucket: %{x}<br>Products: %{z}<extra></extra>",
        colorbar=dict(title="Products"),
    )
)

fig.update_layout(
    height=560,
    margin=dict(l=20, r=20, t=50, b=120),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title=dict(text="Heatmap Density: Source × Price Bucket", x=0.02, xanchor="left"),
    xaxis=dict(title="Price Bucket", tickangle=-35, gridcolor="rgba(255,255,255,.08)"),
    yaxis=dict(title="Source", gridcolor="rgba(255,255,255,.08)"),
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displaylogo": False, "scrollZoom": True},
)

c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.markdown("### Animated Price Distribution")
    hist = px.histogram(
        filtered,
        x="price",
        color="source",
        nbins=bins_count,
        marginal="box",
        hover_data=["title", "reviews", "rating"],
        template="plotly_dark",
    )
    hist.update_layout(
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.035)",
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text="Source",
        bargap=.08,
    )
    st.plotly_chart(hist, use_container_width=True, config={"displaylogo": False})

with c2:
    st.markdown("### Price vs Reviews Map")
    scatter = px.scatter(
        filtered,
        x="price",
        y="reviews",
        color="source",
        size=np.maximum(filtered["rating"], 1),
        hover_name="title",
        hover_data=["rating", "category"],
        template="plotly_dark",
    )
    scatter.update_layout(
        height=470,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.035)",
        margin=dict(l=20, r=20, t=40, b=20),
        legend_title_text="Source",
    )
    st.plotly_chart(scatter, use_container_width=True, config={"displaylogo": False, "scrollZoom": True})

st.markdown("### Source Summary")
summary = (
    filtered
    .groupby("source")
    .agg(
        products=("title", "count"),
        avg_price=("price", "mean"),
        min_price=("price", "min"),
        max_price=("price", "max"),
        avg_reviews=("reviews", "mean"),
        avg_rating=("rating", "mean"),
    )
    .round(2)
    .sort_values("products", ascending=False)
)

st.dataframe(summary, use_container_width=True)

with st.expander("View filtered product data"):
    st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Download Filtered Heatmap Data",
    csv,
    "scrapex_filtered_heatmap_data.csv",
    "text/csv",
    use_container_width=True,
)
