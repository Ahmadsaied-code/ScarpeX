import html
import streamlit as st
import streamlit.components.v1 as components


def apply_theme():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

        :root {
            --bg: #030712;
            --card: rgba(255,255,255,0.065);
            --border: rgba(255,255,255,0.12);
            --text: #ffffff;
            --muted: rgba(255,255,255,0.58);
            --cyan: #67e8f9;
            --blue: #60a5fa;
            --purple: #c084fc;
            --green: #86efac;
        }

        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        .stApp {
            background:
              radial-gradient(circle at 15% 15%, rgba(59,130,246,0.20), transparent 34%),
              radial-gradient(circle at 85% 20%, rgba(168,85,247,0.18), transparent 32%),
              radial-gradient(circle at 50% 90%, rgba(34,197,94,0.10), transparent 32%),
              #030712;
            color: white;
        }

        header[data-testid="stHeader"] {
            background: rgba(3,7,18,0.25);
            backdrop-filter: blur(18px);
        }

        section[data-testid="stSidebar"] {
            background: rgba(2,6,23,0.88);
            border-right: 1px solid rgba(255,255,255,0.08);
        }

        .block-container {
            max-width: 1220px;
            padding-top: 2rem;
            padding-bottom: 4rem;
        }

        h1, h2, h3 {
            letter-spacing: -0.04em;
        }

        div[data-testid="stMetric"] {
            background: rgba(255,255,255,0.065);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 22px;
            padding: 18px;
            box-shadow: 0 22px 80px rgba(0,0,0,0.16);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 20px;
            overflow: hidden;
            border: 1px solid rgba(255,255,255,0.10);
        }

        .glass-card {
            background: rgba(255,255,255,0.065);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 28px;
            padding: 26px;
            box-shadow: 0 26px 90px rgba(0,0,0,0.22);
            backdrop-filter: blur(20px);
        }

        .soft-card {
            background: rgba(255,255,255,0.045);
            border: 1px solid rgba(255,255,255,0.10);
            border-radius: 24px;
            padding: 20px;
            backdrop-filter: blur(18px);
        }

        .small-muted {
            color: rgba(255,255,255,0.58);
            line-height: 1.7;
        }

        .pill {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            border-radius: 999px;
            background: rgba(255,255,255,0.07);
            border: 1px solid rgba(255,255,255,0.12);
            padding: 9px 14px;
            color: rgba(255,255,255,0.72);
            font-size: 13px;
            margin-bottom: 12px;
        }

        .hero-title {
            font-size: clamp(42px, 6vw, 76px);
            line-height: 1.02;
            font-weight: 900;
            margin: 0;
            letter-spacing: -0.065em;
        }

        .gradient-text {
            background: linear-gradient(90deg, #a5f3fc, #93c5fd, #d8b4fe);
            -webkit-background-clip: text;
            color: transparent;
        }

        .hero-desc {
            color: rgba(255,255,255,0.62);
            font-size: 18px;
            line-height: 1.8;
            max-width: 760px;
            margin-top: 20px;
        }

        .big-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: #67e8f9;
            color: #06111d !important;
            text-decoration: none !important;
            border-radius: 18px;
            padding: 15px 22px;
            font-weight: 900;
            box-shadow: 0 20px 60px rgba(103,232,249,0.18);
        }

        .ghost-button {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: rgba(255,255,255,0.065);
            color: white !important;
            text-decoration: none !important;
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 18px;
            padding: 15px 22px;
            font-weight: 800;
        }

        .feature-grid {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 16px;
            margin-top: 24px;
        }

        .feature {
            background: rgba(255,255,255,0.055);
            border: 1px solid rgba(255,255,255,0.11);
            border-radius: 24px;
            padding: 22px;
            min-height: 210px;
            transition: 0.2s ease;
        }

        .feature:hover {
            transform: translateY(-6px);
            background: rgba(255,255,255,0.085);
        }

        .feature-icon {
            width: 48px;
            height: 48px;
            border-radius: 16px;
            background: rgba(103,232,249,0.13);
            display: grid;
            place-items: center;
            margin-bottom: 14px;
            font-size: 23px;
        }

        .feature h3 {
            margin: 0 0 10px 0;
            font-size: 20px;
        }

        .feature p {
            margin: 0;
            color: rgba(255,255,255,0.56);
            line-height: 1.65;
            font-size: 14px;
        }

        .footer-note {
            color: rgba(255,255,255,0.45);
            font-size: 13px;
            text-align: center;
            margin-top: 35px;
        }

        .stButton > button,
        .stDownloadButton > button {
            border-radius: 15px !important;
            border: 1px solid rgba(255,255,255,0.14) !important;
            background: rgba(255,255,255,0.08) !important;
            color: white !important;
            font-weight: 800 !important;
            padding: 0.65rem 1rem !important;
        }

        .stButton > button:hover,
        .stDownloadButton > button:hover {
            background: rgba(103,232,249,0.18) !important;
            border-color: rgba(103,232,249,0.4) !important;
        }

        @media (max-width: 900px) {
            .feature-grid {
                grid-template-columns: repeat(2, minmax(0, 1fr));
            }
        }

        @media (max-width: 560px) {
            .feature-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_hero():
    st.markdown(
        """
        <div class="pill">↗ Professional Data Acquisition Dashboard</div>
        <h1 class="hero-title">
            Turn Product Scraping Into a
            <span class="gradient-text"> 3D Data Experience.</span>
        </h1>
        <p class="hero-desc">
            A polished Streamlit project for scraping products from Jumia and eBay, comparing sources,
            visualizing price behavior, building relationship graphs, and exporting clean CSV files.
        </p>
        <div style="display:flex; gap:14px; flex-wrap:wrap; margin-top:26px;">
            <a class="big-button" href="/multi_market_scraper" target="_self">Start Multi-Market API →</a>
            <a class="ghost-button" href="/multi_market_scraper" target="_self">Multi-Market Scraper</a>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_grid():
    st.markdown(
        """
        <div class="feature-grid">
            <div class="feature">
                <div class="feature-icon">🍵</div>
                <h3>BeautifulSoup</h3>
                <p>Static scraping from Jumia search pages with clean price and review extraction.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔑</div>
                <h3>Multi-Market API</h3>
                <p>API-based product collection for eBay, Amazon, Noon, and AliExpress using one organized page.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🤖</div>
                <h3>Selenium</h3>
                <p>Browser-based scraping workflow for Jumia and AliExpress in one Selenium page.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🛍️</div>
                <h3>Multi-Market</h3>
                <p>Collect products from Noon, Amazon, and AliExpress using direct scraping or API-based methods.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_spline_panel(spline_url=""):
    safe_url = html.escape(spline_url.strip()) if spline_url else ""
    if safe_url:
        body = f"""
        <spline-viewer url="{safe_url}" style="width:100%;height:100%;"></spline-viewer>
        """
        script = '<script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js"></script>'
    else:
        body = """
        <div class="mock-cube"></div>
        <div class="panel-content">
          <div class="label">Live 3D Dashboard</div>
          <h2>Product Intelligence Hub</h2>
          <div class="metric-grid">
            <div><b>Jumia</b><span>BeautifulSoup + Selenium</span></div>
            <div><b>eBay</b><span>SerpAPI Integration</span></div>
            <div><b>Network</b><span>Product Relationships</span></div>
            <div><b>Heatmap</b><span>Price Distribution</span></div>
          </div>
          <p class="hint">Add your Spline Viewer URL from the sidebar to replace this 3D mockup.</p>
        </div>
        """
        script = ""

    components.html(
        f"""
        {script}
        <style>
        body {{
            margin:0;
            background: transparent;
            font-family: Inter, Arial, sans-serif;
        }}
        .panel {{
            position: relative;
            height: 520px;
            border-radius: 34px;
            overflow: hidden;
            background:
              radial-gradient(circle at 80% 20%, rgba(59,130,246,0.36), transparent 35%),
              radial-gradient(circle at 10% 90%, rgba(168,85,247,0.30), transparent 35%),
              rgba(2,6,23,0.72);
            border: 1px solid rgba(255,255,255,0.14);
            box-shadow: 0 38px 110px rgba(0,0,0,0.40);
        }}
        .panel::before {{
            content:"";
            position:absolute;
            inset:0;
            background: linear-gradient(125deg, rgba(59,130,246,0.20), transparent 45%, rgba(168,85,247,0.16));
        }}
        .panel-content {{
            position: relative;
            z-index: 2;
            padding: 26px;
            color: white;
        }}
        .label {{
            color: rgba(255,255,255,0.55);
            font-size: 13px;
            margin-bottom: 4px;
        }}
        h2 {{
            margin: 0;
            font-size: 28px;
            letter-spacing: -0.04em;
        }}
        .metric-grid {{
            margin-top: 35px;
            display: grid;
            grid-template-columns: repeat(2,1fr);
            gap: 16px;
        }}
        .metric-grid div {{
            min-height: 110px;
            padding: 22px;
            border-radius: 25px;
            background: rgba(255,255,255,0.075);
            border: 1px solid rgba(255,255,255,0.10);
            backdrop-filter: blur(18px);
            animation: float 5s ease-in-out infinite;
        }}
        .metric-grid div:nth-child(2) {{ animation-delay:.4s; }}
        .metric-grid div:nth-child(3) {{ animation-delay:.7s; }}
        .metric-grid div:nth-child(4) {{ animation-delay:1s; }}
        b {{
            display:block;
            font-size: 30px;
        }}
        span {{
            display:block;
            margin-top:6px;
            color:rgba(255,255,255,0.52);
            font-size:13px;
        }}
        .hint {{
            position:absolute;
            left:26px;
            right:26px;
            bottom:26px;
            padding:18px;
            border-radius:22px;
            background:rgba(0,0,0,0.25);
            border:1px solid rgba(255,255,255,0.10);
            color:rgba(255,255,255,0.62);
            line-height:1.6;
            margin:0;
        }}
        .mock-cube {{
            position:absolute;
            left:50%;
            top:54%;
            width:155px;
            height:155px;
            transform:translate(-50%,-50%);
            border-radius:32px;
            border:1px solid rgba(103,232,249,0.30);
            background:rgba(103,232,249,0.09);
            box-shadow:0 0 75px rgba(103,232,249,0.25);
            animation:spin 8s linear infinite;
            z-index:1;
        }}
        @keyframes float {{
            0%,100% {{ transform:translateY(0); }}
            50% {{ transform:translateY(-13px); }}
        }}
        @keyframes spin {{
            0% {{ transform:translate(-50%,-50%) rotateX(0deg) rotateY(0deg) rotateZ(0deg); }}
            100% {{ transform:translate(-50%,-50%) rotateX(360deg) rotateY(360deg) rotateZ(12deg); }}
        }}
        </style>
        <div class="panel">{body}</div>
        """,
        height=540,
    )


def page_header(title, subtitle, icon="✨"):
    st.markdown(
        f"""
        <div class="pill">{icon} ScrapeX Module</div>
        <h1 style="font-size:46px;line-height:1.05;margin:0 0 10px 0;">{title}</h1>
        <p class="small-muted" style="font-size:17px;margin-bottom:25px;">{subtitle}</p>
        """,
        unsafe_allow_html=True,
    )


def normalized_dataframe(data):
    import pandas as pd
    if not data:
        return pd.DataFrame()
    return pd.DataFrame(data)
