import re
import textwrap

import streamlit as st

from utils.ui import apply_theme

st.set_page_config(page_title="Wrap-Up | ScrapeX", page_icon="🎬", layout="wide")
apply_theme()

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

HTML = r"""
<style>
.block-container{max-width:1320px;padding-top:1.3rem}
.final-shell{position:relative;overflow:hidden;border-radius:36px;border:1px solid rgba(255,255,255,.12);background:radial-gradient(circle at 16% 15%,rgba(103,232,249,.18),transparent 30%),radial-gradient(circle at 82% 20%,rgba(192,132,252,.21),transparent 32%),radial-gradient(circle at 45% 90%,rgba(34,197,94,.11),transparent 34%),linear-gradient(135deg,rgba(15,23,42,.75),rgba(2,6,23,.50));padding:34px;box-shadow:0 35px 120px rgba(0,0,0,.34)}
.final-shell::before{content:"";position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.035) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.035) 1px,transparent 1px);background-size:44px 44px;mask-image:radial-gradient(circle at center,black,transparent 78%);pointer-events:none}
.hero-layout{position:relative;z-index:2;display:grid;grid-template-columns:1.04fr .96fr;gap:30px;align-items:center}
.top-badge{display:inline-flex;align-items:center;gap:8px;border-radius:999px;border:1px solid rgba(255,255,255,.13);background:rgba(255,255,255,.07);color:rgba(255,255,255,.78);padding:10px 16px;font-size:13px;backdrop-filter:blur(16px);animation:rise .75s ease both}
.main-title{margin:22px 0 0;font-size:clamp(50px,7vw,92px);line-height:.98;letter-spacing:-.078em;font-weight:950;animation:rise .85s ease both .08s}
.grad{background:linear-gradient(90deg,#a5f3fc,#93c5fd,#d8b4fe);-webkit-background-clip:text;color:transparent}
.lead{margin-top:24px;max-width:760px;color:rgba(255,255,255,.64);line-height:1.86;font-size:18px;animation:rise .85s ease both .16s}
.action-row{display:flex;flex-wrap:wrap;gap:14px;margin-top:30px;animation:rise .85s ease both .24s}
.cta{display:inline-flex;align-items:center;justify-content:center;min-height:54px;padding:0 24px;border-radius:18px;text-decoration:none!important;font-weight:900;transition:.22s ease}
.cta.primary{background:#67e8f9;color:#06111d!important;box-shadow:0 18px 55px rgba(103,232,249,.25)}
.cta.primary:hover{transform:translateY(-4px);background:#a5f3fc}
.cta.secondary{color:white!important;background:rgba(255,255,255,.075);border:1px solid rgba(255,255,255,.13);backdrop-filter:blur(18px)}
.cta.secondary:hover{transform:translateY(-4px);background:rgba(255,255,255,.11)}
.visual-stage{position:relative;min-height:430px;border-radius:34px;border:1px solid rgba(255,255,255,.14);background:rgba(2,6,23,.58);overflow:hidden;box-shadow:0 35px 120px rgba(0,0,0,.36);backdrop-filter:blur(24px);animation:stageIn .9s ease both .12s,floatStage 7s ease-in-out infinite 1s}
.visual-stage::before{content:"";position:absolute;inset:-45%;background:conic-gradient(from 0deg,rgba(103,232,249,0),rgba(103,232,249,.22),rgba(192,132,252,.20),rgba(34,197,94,.12),rgba(103,232,249,0));animation:spinBg 13s linear infinite}
.stage-inner{position:absolute;inset:14px;border-radius:28px;background:rgba(2,6,23,.78);border:1px solid rgba(255,255,255,.09);overflow:hidden}
.ring{position:absolute;left:50%;top:46%;border-radius:999px;border:1px solid rgba(103,232,249,.21);transform:translate(-50%,-50%) rotate(var(--a));animation:ringMove var(--speed) linear infinite}
.r1{width:290px;height:290px;--a:0deg;--speed:12s}.r2{width:370px;height:145px;--a:22deg;--speed:16s}.r3{width:250px;height:365px;--a:-25deg;--speed:20s}
.dot{position:absolute;left:50%;top:-10px;width:20px;height:20px;border-radius:999px;background:#67e8f9;box-shadow:0 0 28px rgba(103,232,249,.95)}
.cube-core{position:absolute;left:50%;top:46%;width:145px;height:145px;transform:translate(-50%,-50%);border-radius:32px;border:1px solid rgba(103,232,249,.32);background:rgba(103,232,249,.10);box-shadow:0 0 90px rgba(103,232,249,.23);animation:cubeTurn 10s linear infinite}
.stage-stats{position:absolute;left:22px;right:22px;bottom:22px;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:13px}
.stage-stat{border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.08);border-radius:22px;padding:18px;backdrop-filter:blur(18px)}
.stage-stat b{display:block;font-size:30px;letter-spacing:-.05em}.stage-stat span{display:block;margin-top:6px;color:rgba(255,255,255,.53);font-size:12px}
.module-grid{position:relative;z-index:2;display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:14px;margin-top:28px}
.module-card{min-height:116px;border-radius:24px;border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.06);text-decoration:none!important;color:white!important;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:8px;backdrop-filter:blur(18px);transition:.22s ease}
.module-card:hover{transform:translateY(-8px) scale(1.02);background:rgba(103,232,249,.13);border-color:rgba(103,232,249,.36);box-shadow:0 24px 70px rgba(103,232,249,.13)}
.module-card .icon{width:46px;height:46px;border-radius:17px;display:grid;place-items:center;background:rgba(103,232,249,.13);font-size:23px}.module-card span{font-size:13px;color:rgba(255,255,255,.74);font-weight:850}
.section-head{position:relative;z-index:2;margin:58px 0 24px}.section-head small{display:block;color:#67e8f9;text-transform:uppercase;letter-spacing:.26em;font-weight:950;font-size:12px;margin-bottom:10px}.section-head h2{margin:0;font-size:clamp(32px,4.4vw,56px);line-height:1.06;letter-spacing:-.055em}
.metrics{position:relative;z-index:2;display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}.metric-box{border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.065);border-radius:28px;padding:25px;backdrop-filter:blur(20px);transition:.22s ease}.metric-box:hover{transform:translateY(-7px);background:rgba(255,255,255,.095)}.metric-box strong{display:block;font-size:36px;letter-spacing:-.05em}.metric-box span{display:block;margin-top:8px;color:rgba(255,255,255,.56);line-height:1.55;font-size:13px}
.feature-grid{position:relative;z-index:2;display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}.feature-box{position:relative;overflow:hidden;border:1px solid rgba(255,255,255,.11);background:rgba(255,255,255,.06);border-radius:30px;padding:28px;min-height:270px;backdrop-filter:blur(20px)}.feature-box::after{content:"";position:absolute;right:-90px;top:-90px;width:210px;height:210px;border-radius:50%;background:rgba(103,232,249,.13);filter:blur(24px)}.feature-box h3{position:relative;z-index:2;margin:0 0 16px;font-size:27px}.feature-box ul{position:relative;z-index:2;display:grid;gap:13px;list-style:none;padding:0;margin:0}.feature-box li{color:rgba(255,255,255,.61);line-height:1.6}.feature-box li::before{content:"✓";color:#86efac;font-weight:950;margin-right:10px}
.solo-box{position:relative;z-index:2;display:grid;grid-template-columns:auto 1fr;gap:22px;align-items:center;border:1px solid rgba(255,255,255,.12);background:linear-gradient(135deg,rgba(103,232,249,.09),rgba(192,132,252,.10));border-radius:32px;padding:30px;backdrop-filter:blur(22px);box-shadow:0 26px 90px rgba(0,0,0,.22)}
.avatar{width:86px;height:86px;border-radius:28px;display:grid;place-items:center;background:linear-gradient(135deg,rgba(103,232,249,.28),rgba(192,132,252,.25));border:1px solid rgba(255,255,255,.14);font-size:38px;animation:chipPulse 4s ease-in-out infinite}.solo-box h3{margin:0 0 8px;font-size:32px}.solo-box p{margin:0;color:rgba(255,255,255,.63);line-height:1.8;font-size:16px}
.tech-cloud{position:relative;z-index:2;display:flex;flex-wrap:wrap;gap:12px}.chip{border:1px solid rgba(255,255,255,.12);background:rgba(255,255,255,.065);border-radius:999px;padding:12px 16px;color:rgba(255,255,255,.74);font-weight:850;backdrop-filter:blur(16px);animation:chipPulse 4.2s ease-in-out infinite}.chip:nth-child(2n){animation-delay:.4s}.chip:nth-child(3n){animation-delay:.8s}
.closing{position:relative;z-index:2;margin-top:54px;border-radius:34px;border:1px solid rgba(255,255,255,.13);background:linear-gradient(135deg,rgba(103,232,249,.12),rgba(192,132,252,.12));padding:38px;text-align:center;backdrop-filter:blur(20px);box-shadow:0 30px 100px rgba(0,0,0,.26)}.closing h2{margin:0 0 14px;font-size:clamp(34px,5vw,60px);letter-spacing:-.065em}.closing p{max-width:800px;margin:0 auto;color:rgba(255,255,255,.64);line-height:1.8;font-size:17px}
@keyframes rise{from{opacity:0;transform:translateY(26px)}to{opacity:1;transform:translateY(0)}}@keyframes stageIn{from{opacity:0;transform:perspective(900px) rotateX(12deg) rotateY(-12deg) scale(.93)}to{opacity:1;transform:perspective(900px) rotateX(6deg) rotateY(-6deg) scale(1)}}@keyframes floatStage{0%,100%{transform:perspective(900px) rotateX(6deg) rotateY(-6deg) translateY(0)}50%{transform:perspective(900px) rotateX(8deg) rotateY(-3deg) translateY(-12px)}}@keyframes spinBg{from{transform:rotate(0)}to{transform:rotate(360deg)}}@keyframes ringMove{from{transform:translate(-50%,-50%) rotate(var(--a))}to{transform:translate(-50%,-50%) rotate(calc(var(--a) + 360deg))}}@keyframes cubeTurn{0%{transform:translate(-50%,-50%) rotateX(0) rotateY(0) rotateZ(0)}100%{transform:translate(-50%,-50%) rotateX(360deg) rotateY(360deg) rotateZ(16deg)}}@keyframes chipPulse{0%,100%{transform:translateY(0);filter:brightness(1)}50%{transform:translateY(-5px);filter:brightness(1.18)}}
@media(max-width:980px){.hero-layout,.feature-grid,.solo-box{grid-template-columns:1fr}.module-grid,.metrics{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.final-shell{padding:22px}.module-grid,.metrics,.stage-stats{grid-template-columns:1fr}}
</style>
<div class="final-shell">
<div class="hero-layout">
<div>
<div class="top-badge">🎬 Final Project Showcase</div>
<h1 class="main-title">ScrapeX <span class="grad">Product Intelligence</span> Dashboard</h1>
<p class="lead">A premium multi-source data acquisition platform that collects product data, normalizes it, visualizes it, and turns marketplace listings into business-ready insight.</p>
<div class="action-row"><a class="cta primary" href="/multi_market_scraper" target="_self">Open Multi-Market →</a><a class="cta secondary" href="/price_heatmap" target="_self">View Heatmap</a></div>
</div>
<div class="visual-stage"><div class="stage-inner"><div class="ring r1"><div class="dot"></div></div><div class="ring r2"><div class="dot"></div></div><div class="ring r3"><div class="dot"></div></div><div class="cube-core"></div><div class="stage-stats"><div class="stage-stat"><b>5</b><span>Marketplaces</span></div><div class="stage-stat"><b>3</b><span>Scraping Modes</span></div><div class="stage-stat"><b>CSV</b><span>Export Ready</span></div></div></div></div>
</div>
<div class="module-grid">
<a class="module-card" href="/beautifulsoup_scraper" target="_self"><div class="icon">🍵</div><span>BeautifulSoup</span></a>
<a class="module-card" href="/multi_market_scraper" target="_self"><div class="icon">🛍️</div><span>Multi-Market</span></a>
<a class="module-card" href="/selenium_scraper" target="_self"><div class="icon">🤖</div><span>Selenium</span></a>
<a class="module-card" href="/network_graph" target="_self"><div class="icon">🌐</div><span>NetworkX</span></a>
<a class="module-card" href="/price_heatmap" target="_self"><div class="icon">🔥</div><span>Heatmap</span></a>
<a class="module-card" href="/scatter_3d" target="_self"><div class="icon">🧊</div><span>3D Scatter</span></a>
</div>
<div class="section-head"><small>Executive Summary</small><h2>A complete acquisition-to-insight product.</h2></div>
<div class="metrics">
<div class="metric-box"><strong>Jumia</strong><span>BeautifulSoup and Selenium product collection.</span></div>
<div class="metric-box"><strong>eBay</strong><span>Structured marketplace collection through SerpAPI.</span></div>
<div class="metric-box"><strong>Amazon+</strong><span>API workflow for Amazon, Noon, and AliExpress.</span></div>
<div class="metric-box"><strong>Analytics</strong><span>NetworkX, interactive heatmap, and 3D product universe.</span></div>
</div>
<div class="section-head"><small>Professional Build</small><h2>Designed to impress clients and instructors.</h2></div>
<div class="feature-grid">
<div class="feature-box"><h3>Core System</h3><ul><li>Modern Streamlit interface with premium dark visual design.</li><li>Multi-market API page for eBay, Amazon, Noon, and AliExpress.</li><li>Selenium browser scraper for Jumia and AliExpress dynamic pages.</li><li>Reusable product schema shared across every visualization page.</li></ul></div>
<div class="feature-box"><h3>Client-Ready Output</h3><ul><li>Interactive charts with hover, filters, and export options.</li><li>Relationship graph for product-source-price analysis.</li><li>Heatmap for price concentration and marketplace patterns.</li><li>3D product universe for price, reviews, and rating exploration.</li></ul></div>
</div>
<div class="section-head"><small>Developer</small><h2>Built solo from scraping to visualization.</h2></div>
<div class="solo-box"><div class="avatar">👨‍💻</div><div><h3>Solo Developer</h3><p>This project was built individually: scraping workflow, user interface, marketplace integration, data normalization, visual analytics, export flow, and final presentation.</p></div></div>
<div class="section-head"><small>Tech Stack</small><h2>Tools used across the project.</h2></div>
<div class="tech-cloud"><div class="chip">Python</div><div class="chip">Streamlit</div><div class="chip">BeautifulSoup</div><div class="chip">Requests</div><div class="chip">Selenium</div><div class="chip">SerpAPI</div><div class="chip">Pandas</div><div class="chip">NetworkX</div><div class="chip">Plotly</div><div class="chip">CSV Export</div></div>
<div class="closing"><h2>Thank you for exploring <span class="grad">ScrapeX</span>.</h2><p>ScrapeX demonstrates how web scraping, APIs, browser automation, data cleaning, and professional visualization can work together as a complete data acquisition product.</p></div>
</div>
"""

def render_safe_html(html: str):
    cleaned = textwrap.dedent(html).strip()
    if hasattr(st, "html"):
        st.html(cleaned)
    else:
        minified = re.sub(r"\n\s*", "", cleaned)
        st.markdown(minified, unsafe_allow_html=True)

render_safe_html(HTML)

st.markdown("### Quick Feedback")
selected = st.feedback("faces")
if selected is not None:
    st.success("Thank you for your feedback! ⭐")
