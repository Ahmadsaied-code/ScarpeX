# ScrapeX — Professional Product Intelligence Dashboard

A professional Streamlit project for scraping and visualizing product data from Jumia and eBay.

## Features

- Jumia static scraping using BeautifulSoup
- Browser scraping for Jumia and AliExpress using Selenium
- Multi-market API scraping for eBay, Amazon, Noon, and AliExpress
- Unified product data structure
- Network graph visualization
- Price heatmap
- 3D scatter plot
- CSV export
- Professional Spline-ready landing page

## Project Structure

```text
scrapex_professional_project/
├── main.py
├── pages/
│   ├── beautifulsoup_scraper.py
│   ├── selenium_scraper.py
│   ├── multi_market_scraper.py
│   ├── network_graph.py
│   ├── price_heatmap.py
│   ├── scatter_3d.py
│   └── project_wrap_up.py
├── utils/
│   ├── ui.py
│   └── data_cleaning.py
├── requirements.txt
└── README.md
```

## How to Run

Open terminal inside the project folder:

```bash
pip install -r requirements.txt
streamlit run main.py
```

## Spline Integration

1. Open your design in Spline.
2. Click Export.
3. Copy the Viewer URL.
4. Paste it in the sidebar field called `Spline Viewer URL`.

## Notes

- Selenium requires Google Chrome installed locally.
- SerpAPI requires your own API key.
- The API key is not hard-coded for security.


## New in Version 2

The project now includes `pages/multi_market_scraper.py`, which supports:

- AliExpress — Selenium browser scraping
- Amazon — SerpAPI Amazon Search
- Noon — SerpAPI Google Shopping
- AliExpress — SerpAPI Google Shopping

The recommended options are the SerpAPI methods for Amazon and AliExpress because these stores often use dynamic pages and anti-bot protection.

After running any marketplace scraper, the collected data is automatically stored in Streamlit session state and can be used by:

- Network Graph
- Price Heatmap
- 3D Scatter Plot


## Version 3 Fix

- Fixed SerpAPI Google Shopping 400 errors caused by unstable country/location parameters.
- Removed `location=Egypt` from Google Shopping API requests.
- Added fallback attempts using `google_shopping` and `google_shopping_light`.
- Hid the SerpAPI key from error messages.

## Version 4 Update

Removed direct HTML marketplace options from the Multi-Market Scraper dropdown:

- Noon Egypt — Direct HTML Scraper
- Amazon Egypt — Direct HTML Scraper

The remaining options are SerpAPI and AliExpress Selenium.

## Version 5 Reorganization

- Removed the standalone SerpAPI eBay page.
- Added eBay SerpAPI inside the Multi-Market Scraper page.
- Moved AliExpress Selenium into the Selenium Scraper page with Jumia.
- Removed AliExpress Selenium from the Multi-Market Scraper page.
- Multi-Market Scraper now contains API-based sources only.
- Selenium Scraper now contains browser-based sources only.


## Version 6 Update

- Reordered the sidebar navigation:
  1. Main
  2. BeautifulSoup
  3. Multi-Market
  4. Selenium
  5. NetworkX
  6. Heatmap
  7. 3D Scatter
  8. Wrap-Up

- Rebuilt the Wrap-Up page with a professional animated design:
  - Animated hero section
  - Floating labels
  - Orbit / 3D-style panel
  - Project pipeline timeline
  - Feature cards
  - Team cards
  - Tech stack chips
  - Presentation-ready closing section


## Version 7 Update

- Rebuilt Wrap-Up as a native Streamlit page instead of an embedded iframe.
- Removed the second team member and changed the page to a solo-developer presentation.
- Added clickable module cards and clickable timeline dots.
- Upgraded Heatmap to an interactive Plotly dashboard with filters, KPIs, hover, distribution charts, scatter analysis, and CSV export.


## Version 8 Fixes

- Added Plotly to requirements.txt.
- Heatmap page now handles missing Plotly gracefully instead of showing a traceback.
- Rebuilt Heatmap as a professional interactive dashboard with animated CSS header, Plotly heatmap, filters, KPIs, hover, scatter view, and CSV export.
- Rebuilt 3D Scatter as a Plotly-powered interactive 3D chart with rotate camera animation.
- Rebuilt Wrap-Up as native Streamlit HTML, not an iframe/middle box.
- Removed the second team member and changed presentation to Solo Developer.


## Version 9 Cleanup

- Removed the visible project-flow/timeline content from the Wrap-Up page.
- Removed the Analytics Impact block.
- Kept the page professional with animated hero, clickable modules, solo developer card, and client-ready summary.
- No HTML/code snippets are intended to be displayed in the app interface.

## Version 10 Hotfix

- Fixed Wrap-Up page rendering so raw HTML is not shown to users.
- Uses Streamlit native HTML renderer when available.
- Uses a minified unsafe HTML fallback to avoid Markdown code-block rendering.
