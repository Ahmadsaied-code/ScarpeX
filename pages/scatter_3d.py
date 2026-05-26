import math
import numpy as np
import pandas as pd
import streamlit as st

from utils.ui import apply_theme

st.set_page_config(page_title="3D Product Universe | ScrapeX", page_icon="🧊", layout="wide")
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
    .space-hero {
      position: relative;
      overflow: hidden;
      border-radius: 34px;
      border: 1px solid rgba(255,255,255,.12);
      background:
        radial-gradient(circle at 18% 18%, rgba(103,232,249,.18), transparent 32%),
        radial-gradient(circle at 82% 22%, rgba(192,132,252,.22), transparent 32%),
        linear-gradient(135deg, rgba(15,23,42,.74), rgba(2,6,23,.50));
      padding: 34px;
      margin-bottom: 26px;
      box-shadow: 0 30px 110px rgba(0,0,0,.32);
    }

    .space-hero::before {
      content:"";
      position:absolute;
      inset:0;
      background-image:
        radial-gradient(circle, rgba(255,255,255,.22) 1px, transparent 1px);
      background-size: 38px 38px;
      mask-image: radial-gradient(circle at center, black, transparent 78%);
      animation: starMove 18s linear infinite;
    }

    .space-grid {
      position:relative;
      z-index:2;
      display:grid;
      grid-template-columns: 1.05fr .95fr;
      gap: 28px;
      align-items:center;
    }

    .space-pill {
      display:inline-flex;
      align-items:center;
      gap:8px;
      padding:10px 16px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.13);
      background:rgba(255,255,255,.07);
      color:rgba(255,255,255,.78);
      font-size:13px;
      backdrop-filter:blur(16px);
      animation: fadeUp .75s ease both;
    }

    .space-title {
      margin:20px 0 0;
      font-size: clamp(44px, 6vw, 82px);
      line-height:1;
      letter-spacing:-.075em;
      font-weight:950;
      animation: fadeUp .8s ease both .08s;
    }

    .space-grad {
      background: linear-gradient(90deg, #a5f3fc, #93c5fd, #d8b4fe);
      -webkit-background-clip:text;
      color:transparent;
    }

    .space-lead {
      margin-top:20px;
      max-width:760px;
      color:rgba(255,255,255,.63);
      line-height:1.85;
      font-size:17px;
      animation: fadeUp .8s ease both .16s;
    }

    .cube-stage {
      position:relative;
      min-height: 350px;
      border-radius: 32px;
      border:1px solid rgba(255,255,255,.12);
      background: rgba(2,6,23,.55);
      backdrop-filter: blur(22px);
      overflow:hidden;
      box-shadow: 0 28px 95px rgba(0,0,0,.25);
      perspective: 900px;
      animation: panelFloat 7s ease-in-out infinite;
    }

    .cube {
      position:absolute;
      left:50%;
      top:46%;
      width: 142px;
      height: 142px;
      transform-style: preserve-3d;
      animation: rotateCube 9s linear infinite;
    }

    .face {
      position:absolute;
      inset:0;
      border-radius: 22px;
      border:1px solid rgba(103,232,249,.35);
      background: rgba(103,232,249,.12);
      box-shadow: 0 0 60px rgba(103,232,249,.18);
    }

    .f1 { transform: translateZ(71px); }
    .f2 { transform: rotateY(90deg) translateZ(71px); }
    .f3 { transform: rotateY(180deg) translateZ(71px); }
    .f4 { transform: rotateY(-90deg) translateZ(71px); }
    .f5 { transform: rotateX(90deg) translateZ(71px); }
    .f6 { transform: rotateX(-90deg) translateZ(71px); }

    .orbit {
      position:absolute;
      left:50%;
      top:46%;
      width: 330px;
      height: 130px;
      border-radius:999px;
      border:1px solid rgba(255,255,255,.13);
      transform: translate(-50%, -50%) rotate(-18deg);
      animation: orbitSpin 12s linear infinite;
    }

    .orbit::before {
      content:"";
      position:absolute;
      left:50%;
      top:-10px;
      width:20px;
      height:20px;
      border-radius:999px;
      background:#67e8f9;
      box-shadow:0 0 25px rgba(103,232,249,.9);
    }

    .floating-card {
      position:absolute;
      z-index:3;
      border:1px solid rgba(255,255,255,.12);
      background: rgba(255,255,255,.08);
      border-radius: 20px;
      padding: 14px 16px;
      backdrop-filter: blur(18px);
      animation: floatCard 4s ease-in-out infinite;
    }

    .floating-card b {
      display:block;
      font-size:22px;
    }

    .floating-card span {
      display:block;
      margin-top:4px;
      color:rgba(255,255,255,.55);
      font-size:12px;
    }

    .fc1 { left:22px; bottom:22px; }
    .fc2 { right:22px; bottom:22px; animation-delay:.5s; }
    .fc3 { right:22px; top:22px; animation-delay:1s; }

    .hint-card {
      border:1px solid rgba(255,255,255,.12);
      background:rgba(255,255,255,.06);
      border-radius:28px;
      padding:26px;
      color:rgba(255,255,255,.64);
      line-height:1.8;
    }

    @keyframes starMove {
      from { background-position: 0 0; }
      to { background-position: 220px 220px; }
    }

    @keyframes fadeUp {
      from { opacity:0; transform: translateY(24px); }
      to { opacity:1; transform: translateY(0); }
    }

    @keyframes rotateCube {
      0% { transform: translate(-50%, -50%) rotateX(0deg) rotateY(0deg); }
      100% { transform: translate(-50%, -50%) rotateX(360deg) rotateY(360deg); }
    }

    @keyframes orbitSpin {
      from { transform: translate(-50%, -50%) rotate(-18deg); }
      to { transform: translate(-50%, -50%) rotate(342deg); }
    }

    @keyframes panelFloat {
      0%,100% { transform: translateY(0); }
      50% { transform: translateY(-10px); }
    }

    @keyframes floatCard {
      0%,100% { transform: translateY(0); }
      50% { transform: translateY(-8px); }
    }

    @media(max-width: 900px) {
      .space-grid { grid-template-columns: 1fr; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="space-hero">
      <div class="space-grid">
        <div>
          <div class="space-pill">🧊 Interactive 3D Product Universe</div>
          <h1 class="space-title">3D <span class="space-grad">Product Intelligence</span></h1>
          <p class="space-lead">
            Rotate, zoom, hover, and animate the product universe. Each point represents
            a product, connecting price, reviews, rating, and source in a single premium visualization.
          </p>
        </div>

        <div class="cube-stage">
          <div class="orbit"></div>
          <div class="cube">
            <div class="face f1"></div><div class="face f2"></div><div class="face f3"></div>
            <div class="face f4"></div><div class="face f5"></div><div class="face f6"></div>
          </div>
          <div class="floating-card fc1"><b>Price</b><span>X Axis</span></div>
          <div class="floating-card fc2"><b>Reviews</b><span>Y Axis</span></div>
          <div class="floating-card fc3"><b>Rating</b><span>Z Axis</span></div>
        </div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)


def collect_products():
    rows = []
    keys = [
        "api_3d_data",
        "products_data",
        "multi_market_data",
        "beautifulsoup_data",
        "jumia_data",
        "aliexpress_selenium_data",
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
                    "reviews": pd.to_numeric(item.get("reviews", 0), errors="coerce"),
                    "rating": pd.to_numeric(item.get("rating", 0), errors="coerce"),
                    "source": item.get("source", key.replace("_", " ").title()),
                    "category": item.get("category", ""),
                    "link": item.get("link", ""),
                }
            )

    if not rows:
        return pd.DataFrame()

    df = pd.DataFrame(rows).drop_duplicates(subset=["title", "price", "source"])
    df["reviews"] = df["reviews"].fillna(0)
    df["rating"] = df["rating"].fillna(0)
    return df


df = collect_products()

if df.empty:
    st.markdown(
        """
        <div class="hint-card">
          <h3 style="margin-top:0;color:white;">No product data loaded yet.</h3>
          Run a scraper first, then return here. The 3D chart will become interactive once products are loaded.
        </div>
        """,
        unsafe_allow_html=True,
    )
    c1, c2, c3 = st.columns(3)
    c1.page_link("pages/beautifulsoup_scraper.py", label="BeautifulSoup", icon="🍵")
    c2.page_link("pages/multi_market_scraper.py", label="Multi-Market API", icon="🛍️")
    c3.page_link("pages/selenium_scraper.py", label="Selenium", icon="🤖")
    st.stop()

st.markdown("### 3D Control Center")
f1, f2, f3 = st.columns([1.2, 1.2, .8])

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
        price_range = st.slider("Price range", min_price, max_price, (min_price, max_price))

with f3:
    max_points = st.slider("Max points", 20, max(20, min(300, len(filtered))), min(120, len(filtered)))

filtered = filtered[
    (filtered["price"] >= price_range[0]) &
    (filtered["price"] <= price_range[1])
].head(max_points)

if filtered.empty:
    st.warning("No products in selected price range.")
    st.stop()

k1, k2, k3, k4 = st.columns(4)
k1.metric("Products", f"{len(filtered):,}")
k2.metric("Sources", f"{filtered['source'].nunique():,}")
k3.metric("Avg Price", f"{filtered['price'].mean():,.2f}")
k4.metric("Avg Reviews", f"{filtered['reviews'].mean():,.0f}")

st.markdown("### Interactive Rotatable 3D Scatter")

size_values = np.sqrt(np.maximum(filtered["reviews"], 1)) + 8
size_values = np.clip(size_values, 8, 38)
filtered = filtered.copy()
filtered["point_size"] = size_values

fig = px.scatter_3d(
    filtered,
    x="price",
    y="reviews",
    z="rating",
    color="source",
    size="point_size",
    hover_name="title",
    hover_data={
        "price": ":,.2f",
        "reviews": True,
        "rating": ":.2f",
        "source": True,
        "category": True,
        "point_size": False,
    },
    template="plotly_dark",
)

# Camera animation frames
frames = []
for i in range(48):
    angle = 2 * math.pi * i / 48
    frames.append(
        go.Frame(
            name=str(i),
            layout=dict(
                scene_camera=dict(
                    eye=dict(
                        x=2.1 * math.cos(angle),
                        y=2.1 * math.sin(angle),
                        z=1.25,
                    )
                )
            ),
        )
    )

fig.frames = frames

fig.update_traces(
    marker=dict(
        opacity=0.88,
        line=dict(width=0.8, color="rgba(255,255,255,.7)"),
    )
)

fig.update_layout(
    height=720,
    margin=dict(l=0, r=0, t=50, b=0),
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    title=dict(text="3D Product Universe: Price × Reviews × Rating", x=0.02, xanchor="left"),
    scene=dict(
        bgcolor="rgba(255,255,255,.025)",
        xaxis=dict(title="Price", gridcolor="rgba(255,255,255,.12)", zerolinecolor="rgba(255,255,255,.18)"),
        yaxis=dict(title="Reviews", gridcolor="rgba(255,255,255,.12)", zerolinecolor="rgba(255,255,255,.18)"),
        zaxis=dict(title="Rating", gridcolor="rgba(255,255,255,.12)", zerolinecolor="rgba(255,255,255,.18)"),
        camera=dict(eye=dict(x=1.8, y=1.8, z=1.2)),
    ),
    updatemenus=[
        dict(
            type="buttons",
            showactive=False,
            x=0.02,
            y=1.08,
            xanchor="left",
            yanchor="top",
            buttons=[
                dict(
                    label="▶ Rotate Camera",
                    method="animate",
                    args=[
                        None,
                        {
                            "frame": {"duration": 85, "redraw": True},
                            "fromcurrent": True,
                            "transition": {"duration": 0},
                        },
                    ],
                )
            ],
        )
    ],
)

st.plotly_chart(
    fig,
    use_container_width=True,
    config={"displaylogo": False, "scrollZoom": True},
)

c1, c2 = st.columns([1, 1], gap="large")

with c1:
    st.markdown("### Source Price Ranking")
    ranking = (
        filtered.groupby("source")
        .agg(products=("title", "count"), avg_price=("price", "mean"), avg_reviews=("reviews", "mean"), avg_rating=("rating", "mean"))
        .round(2)
        .sort_values("products", ascending=False)
    )
    st.dataframe(ranking, use_container_width=True)

with c2:
    st.markdown("### 2D Executive View")
    bubble = px.scatter(
        filtered,
        x="price",
        y="reviews",
        color="source",
        size="point_size",
        hover_name="title",
        template="plotly_dark",
    )
    bubble.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.035)",
        margin=dict(l=20, r=20, t=30, b=20),
    )
    st.plotly_chart(bubble, use_container_width=True, config={"displaylogo": False})

with st.expander("View 3D source data"):
    st.dataframe(filtered, use_container_width=True)

csv = filtered.to_csv(index=False).encode("utf-8-sig")
st.download_button(
    "⬇️ Download 3D Filtered Data",
    csv,
    "scrapex_3d_filtered_data.csv",
    "text/csv",
    use_container_width=True,
)
