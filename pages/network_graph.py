import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

from utils.ui import apply_theme, page_header

st.set_page_config(page_title="Network Graph | ScrapeX", page_icon="🌐", layout="wide")
apply_theme()

page_header(
    "Network Graph",
    "Map how products connect to shared price ranges, review groups, categories, and data sources.",
    "🌐",
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


def get_data():
    return (
        st.session_state.get("products_data")
        or st.session_state.get("api_data")
        or st.session_state.get("scraped_data")
        or st.session_state.get("jumia_data")
        or st.session_state.get("beautifulsoup_data")
        or st.session_state.get("serpapi_data")
        or st.session_state.get("multi_market_data")
    )


def categorize_price(price):
    try:
        price = float(price)
    except (TypeError, ValueError):
        return "Unknown Price"

    if price < 500:
        return "0–500"
    if price < 1000:
        return "500–1K"
    if price < 3000:
        return "1K–3K"
    if price < 7000:
        return "3K–7K"
    return "7K+"


def categorize_reviews(reviews):
    try:
        reviews = int(str(reviews).replace(",", "").split()[0])
    except (TypeError, ValueError):
        return "Unknown Reviews"

    if reviews < 10:
        return "0–10 reviews"
    if reviews < 50:
        return "10–50 reviews"
    if reviews < 100:
        return "50–100 reviews"
    if reviews < 500:
        return "100–500 reviews"
    return "500+ reviews"


def build_graph(data, limit=35):
    G = nx.Graph()

    for product in data[:limit]:
        name = str(product.get("title", "Product"))[:26]
        price_cat = "Price: " + categorize_price(product.get("price"))
        review_cat = "Reviews: " + categorize_reviews(product.get("reviews"))
        source = "Source: " + str(product.get("source", "Unknown"))
        category = "Category: " + str(product.get("category", "Unknown"))

        G.add_node(name, node_type="Product")
        G.add_node(price_cat, node_type="Price")
        G.add_node(review_cat, node_type="Reviews")
        G.add_node(source, node_type="Source")
        G.add_node(category, node_type="Category")

        G.add_edge(name, price_cat)
        G.add_edge(name, review_cat)
        G.add_edge(name, source)
        G.add_edge(name, category)

    return G


def draw_graph(G):
    color_map = {
        "Product": "#67e8f9",
        "Price": "#60a5fa",
        "Reviews": "#86efac",
        "Source": "#c084fc",
        "Category": "#facc15",
    }

    colors = [color_map.get(G.nodes[n].get("node_type", "Product"), "#94a3b8") for n in G.nodes]
    sizes = [1700 if G.nodes[n].get("node_type") == "Product" else 2400 for n in G.nodes]
    pos = nx.spring_layout(G, seed=42, k=0.9)

    fig, ax = plt.subplots(figsize=(16, 10), facecolor="#030712")
    ax.set_facecolor("#030712")

    nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#475569", alpha=0.55, width=1.2)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=colors, node_size=sizes, alpha=0.92)
    nx.draw_networkx_labels(G, pos, ax=ax, font_size=8, font_color="white")

    ax.set_title("Product Relationship Network", color="white", fontsize=18, pad=20)
    ax.axis("off")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


data = get_data()

if not data:
    st.info("Please run one scraper first, then return here.")
    c1, c2, c3 = st.columns(3)
    c1.page_link("pages/beautifulsoup_scraper.py", label="BeautifulSoup", icon="🍵")
    c2.page_link("pages/multi_market_scraper.py", label="Multi-Market API", icon="🛍️")
    c3.page_link("pages/selenium_scraper.py", label="Selenium", icon="🤖")
    st.stop()

df = pd.DataFrame(data)
st.dataframe(df.head(20), use_container_width=True)

limit = st.slider("Products shown in graph", 10, min(60, len(data)), min(35, len(data)), 5)

G = build_graph(data, limit=limit)
draw_graph(G)

degree_dict = dict(G.degree())
top_nodes = sorted(degree_dict.items(), key=lambda x: x[1], reverse=True)[:5]
communities = list(nx.connected_components(G))

c1, c2, c3 = st.columns(3)
c1.metric("Nodes", G.number_of_nodes())
c2.metric("Edges", G.number_of_edges())
c3.metric("Communities", len(communities))

st.markdown("### Top Connected Nodes")
for node, degree in top_nodes:
    st.markdown(f"- **{node}** — degree `{degree}`")
