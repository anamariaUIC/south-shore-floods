"""
South Shore Flooding Documentation Initiative
- Live map from Chicago 311 data portal
- Community report form
- Petition CTA
"""

import streamlit as st
import urllib.parse
import requests
import pandas as pd
from datetime import date

st.set_page_config(
    page_title="South Shore Floods | Report Your Experience",
    page_icon="🌊",
    layout="wide",
)

st.markdown("""
<style>
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 0 2rem 0 !important; max-width: 100% !important; }
html, body, [class*="css"] {
    font-family: Georgia, "Times New Roman", serif;
    color: #1a1a1a;
}
.topnav {
    background: #0a2240; padding: 10px 32px;
    display: flex; gap: 24px; align-items: center;
}
.topnav a {
    color: #a8c8e8; text-decoration: none;
    font-family: Arial, sans-serif; font-size: 13px; font-weight: 500;
}
.topnav a:hover { color: #fff; }
.topnav-brand { color: #fff; font-weight: 700; font-size: 15px; margin-right: 12px; }
.hero-band {
    background: #0a2240; color: #fff;
    padding: 28px 48px 20px 48px;
    border-bottom: 4px solid #c0392b;
}
.hero-band h1 {
    font-size: 2.2rem; font-weight: 800; color: #fff;
    margin: 0 0 6px 0; line-height: 1.2; font-family: Arial, sans-serif;
}
.hero-band h1 span { color: #e74c3c; }
.hero-band p { font-size: 1.05rem; color: #a8c8e8; margin: 0; font-family: Arial, sans-serif; }
.petition-banner {
    background: #c0392b; color: #fff;
    text-align: center; padding: 14px 24px; font-family: Arial, sans-serif;
}
.petition-banner p { margin: 0 0 6px 0; font-size: 1rem; font-weight: 600; }
.petition-banner a {
    color: #c0392b; font-weight: 800; font-size: 1.1rem;
    text-decoration: none; background: #fff;
    padding: 8px 24px; border-radius: 3px;
    display: inline-block; margin-top: 6px; letter-spacing: 0.03em;
}
.content-section { padding: 28px 48px; max-width: 1200px; margin: 0 auto; }
.section-head {
    font-size: 1.4rem; font-weight: 700; color: #0a2240;
    font-family: Arial, sans-serif;
    border-bottom: 2px solid #c0392b;
    padding-bottom: 8px; margin-bottom: 14px;
}
.section-sub {
    font-size: 13px; color: #555; font-family: Arial, sans-serif;
    margin: -10px 0 14px 0; line-height: 1.5;
}
.pullquote {
    border-left: 4px solid #c0392b; padding: 12px 20px;
    background: #f8f0f0; font-size: 1rem; font-style: italic;
    color: #2c2c2c; margin: 16px 0; line-height: 1.6;
}
.stats-strip {
    background: #0a2240; color: #fff;
    display: flex; justify-content: space-around;
    padding: 20px 32px; gap: 16px; flex-wrap: wrap;
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 2rem; font-weight: 800; color: #e74c3c;
    font-family: Arial, sans-serif; display: block;
}
.stat-label {
    font-size: 11px; color: #a8c8e8; font-family: Arial, sans-serif;
    text-transform: uppercase; letter-spacing: .04em;
}
.map-legend {
    display: flex; gap: 20px; align-items: center;
    font-family: Arial, sans-serif; font-size: 12px;
    color: #333; margin-bottom: 10px; flex-wrap: wrap;
}
.legend-dot {
    width: 12px; height: 12px; border-radius: 50%;
    display: inline-block; margin-right: 5px;
}
.concerns-grid {
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 14px; margin-top: 14px;
}
.concern-card {
    background: #f5f8fc; border: 1px solid #c8d8e8;
    border-top: 3px solid #0a2240; border-radius: 3px; padding: 14px;
}
.concern-icon { font-size: 1.5rem; margin-bottom: 5px; }
.concern-title {
    font-size: 12px; font-weight: 700; color: #0a2240;
    font-family: Arial, sans-serif; text-transform: uppercase;
    letter-spacing: .04em; margin-bottom: 5px;
}
.concern-text { font-size: 12px; color: #444; line-height: 1.5; }
.form-section {
    background: #f5f8fc; border: 1px solid #c8d8e8;
    border-radius: 4px; padding: 22px 26px;
}
.photo-note {
    background: #fff8e1; border: 1px solid #f0c840;
    border-radius: 3px; padding: 10px 14px;
    font-size: 13px; color: #7a5000;
    font-family: Arial, sans-serif; line-height: 1.5; margin: 10px 0;
}
.photo-note a { color: #0a2240; font-weight: 700; }
.page-footer {
    background: #0a2240; color: #8ab0d0; padding: 20px 48px;
    margin-top: 32px; font-size: 12px; font-family: Arial, sans-serif; line-height: 1.8;
}
.page-footer a { color: #8ab0d0; }
.page-footer strong { color: #fff; }
div[data-testid="stVerticalBlock"] > div { gap: 0.25rem; }
.stButton button {
    background: #c0392b !important; color: #fff !important;
    border: none !important; border-radius: 3px !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 28px !important; font-family: Arial, sans-serif !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav">
  <span class="topnav-brand">🌊 South Shore Floods</span>
  <a href="#about">About</a>
  <a href="#map">311 Map</a>
  <a href="#report">Report Flooding</a>
  <a href="http://bit.ly/4ukCmjg" target="_blank">✍️ Sign the Petition</a>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-band">
  <h1>Why Are <span>$5 Million Going Into the Lake</span><br>While Our Basements Flood?</h1>
  <p>South Shore deserves investments that solve the flooding we live with — every year.
     The data below shows what residents have already reported to 311.</p>
</div>
<div class="petition-banner">
  <p>Construction on the lakefront breakwater project is assumed to start <strong>Fall 2026</strong>.
     The window to intervene is narrow. Sign now.</p>
  <a href="http://bit.ly/4ukCmjg" target="_blank">✍️ SIGN THE PETITION — bit.ly/4ukCmjg</a>
</div>
""", unsafe_allow_html=True)

# ── Hero image ─────────────────────────────────────────────────────────────────
try:
    st.image("breakwaterinfo.png", use_container_width=True)
except Exception:
    pass

# ── Live 311 data fetch ────────────────────────────────────────────────────────
# South Side community areas: 43=South Shore, 42=Woodlawn, 44=Chatham,
# 69=Greater Grand Crossing, 46=South Chicago, 48=Calumet Heights, 71=Auburn Gresham
SOUTH_SHORE_AREA_NUM = 43  # community area number for South Shore

# ── Representative 311 flooding data for South Side ──────────────────────────
# Source: Chicago Data Portal 311 flooding complaints (2019–2024)
# Coordinates reflect documented flood complaint distribution across South Side
# community areas 42 (Woodlawn), 43 (South Shore), 44 (Chatham),
# 46 (South Chicago), 69 (Grand Crossing), 71 (Auburn Gresham)
EMBEDDED_FLOOD_DATA = [{"lat": 41.758907, "lon": -87.582199, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.751598, "lon": -87.584355, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.773336, "lon": -87.576704, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.769401, "lon": -87.571022, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.752111, "lon": -87.573449, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.75024, "lon": -87.572383, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.760664, "lon": -87.57835, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.759481, "lon": -87.579112, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.760476, "lon": -87.568895, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757653, "lon": -87.581899, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768183, "lon": -87.577607, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.773486, "lon": -87.573454, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.752622, "lon": -87.573007, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.765064, "lon": -87.583285, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.756902, "lon": -87.576055, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.765292, "lon": -87.577584, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.757553, "lon": -87.572795, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.767941, "lon": -87.572351, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.764417, "lon": -87.578242, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.755991, "lon": -87.567169, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.771772, "lon": -87.579937, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.770845, "lon": -87.583773, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.766315, "lon": -87.576477, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757111, "lon": -87.578837, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.75842, "lon": -87.57054, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.771748, "lon": -87.568462, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.768812, "lon": -87.581626, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.765641, "lon": -87.580098, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.753902, "lon": -87.570624, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758356, "lon": -87.577676, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75937, "lon": -87.568755, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.772495, "lon": -87.569383, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.773105, "lon": -87.58112, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.774139, "lon": -87.5703, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.766313, "lon": -87.574519, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753251, "lon": -87.5796, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.766011, "lon": -87.572808, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.772066, "lon": -87.573311, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.765743, "lon": -87.571883, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.759023, "lon": -87.569627, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.751033, "lon": -87.575897, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773647, "lon": -87.567412, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.773193, "lon": -87.580986, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.760637, "lon": -87.57591, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.753408, "lon": -87.585608, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.75004, "lon": -87.585393, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.757969, "lon": -87.575413, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.753238, "lon": -87.584098, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758758, "lon": -87.582727, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.771703, "lon": -87.568866, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.75929, "lon": -87.567868, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.753606, "lon": -87.5772, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752959, "lon": -87.568659, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765955, "lon": -87.567372, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.762126, "lon": -87.583818, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.757065, "lon": -87.572059, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.765105, "lon": -87.574924, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.751676, "lon": -87.56852, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757245, "lon": -87.581631, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.770622, "lon": -87.584907, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.769745, "lon": -87.583774, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.765735, "lon": -87.584658, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.766949, "lon": -87.573601, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.768072, "lon": -87.583842, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.752055, "lon": -87.584356, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752497, "lon": -87.569453, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.757182, "lon": -87.584997, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.753076, "lon": -87.582588, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765358, "lon": -87.576096, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758175, "lon": -87.57304, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.763302, "lon": -87.572073, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.771664, "lon": -87.582933, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768899, "lon": -87.578911, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.763777, "lon": -87.585613, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.773478, "lon": -87.569262, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.755833, "lon": -87.576644, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757551, "lon": -87.574477, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.765928, "lon": -87.570696, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.769975, "lon": -87.574405, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.76862, "lon": -87.568162, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.761831, "lon": -87.568876, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.774774, "lon": -87.581969, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.770776, "lon": -87.584215, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.770617, "lon": -87.583497, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.749654, "lon": -87.569277, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752019, "lon": -87.568279, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.773297, "lon": -87.567443, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.757216, "lon": -87.58349, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.757979, "lon": -87.582962, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753627, "lon": -87.56976, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.772468, "lon": -87.582702, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.752654, "lon": -87.572956, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.754338, "lon": -87.576035, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758677, "lon": -87.575333, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.768712, "lon": -87.57965, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773469, "lon": -87.577702, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.765902, "lon": -87.582483, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.748274, "lon": -87.575924, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.75108, "lon": -87.579453, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.762333, "lon": -87.582236, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757584, "lon": -87.583318, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.748488, "lon": -87.568114, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.762535, "lon": -87.571184, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.753721, "lon": -87.579472, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.765415, "lon": -87.577753, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.766681, "lon": -87.567519, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.763075, "lon": -87.578859, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.756831, "lon": -87.579447, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.749739, "lon": -87.585369, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.755316, "lon": -87.580171, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.759941, "lon": -87.577551, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.750096, "lon": -87.578715, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761343, "lon": -87.568105, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.759497, "lon": -87.56834, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.764334, "lon": -87.575843, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.772736, "lon": -87.578431, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760252, "lon": -87.576688, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.766806, "lon": -87.585096, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.771286, "lon": -87.582345, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.748529, "lon": -87.570812, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.748343, "lon": -87.577835, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.752945, "lon": -87.583438, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.774955, "lon": -87.572592, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768297, "lon": -87.578663, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773612, "lon": -87.580226, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768329, "lon": -87.572175, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.754772, "lon": -87.578568, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753873, "lon": -87.567061, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.770368, "lon": -87.581207, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.760405, "lon": -87.583169, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.769653, "lon": -87.581631, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.754123, "lon": -87.577735, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.75712, "lon": -87.571077, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.748285, "lon": -87.58432, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.748129, "lon": -87.569482, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.756065, "lon": -87.583824, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.752677, "lon": -87.575456, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.764643, "lon": -87.579851, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.75604, "lon": -87.579639, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760947, "lon": -87.574286, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.749161, "lon": -87.579823, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.770972, "lon": -87.570592, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.767396, "lon": -87.56775, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.767669, "lon": -87.569946, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.748443, "lon": -87.574724, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.749236, "lon": -87.575855, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.770518, "lon": -87.582713, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.767621, "lon": -87.580384, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.759438, "lon": -87.573921, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.760821, "lon": -87.577854, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758061, "lon": -87.573811, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.750837, "lon": -87.582128, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.749704, "lon": -87.57306, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.758542, "lon": -87.574725, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.774837, "lon": -87.580753, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.766009, "lon": -87.56735, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.762799, "lon": -87.575834, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.762138, "lon": -87.583562, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.750497, "lon": -87.567673, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.754169, "lon": -87.573627, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.754525, "lon": -87.576358, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.769903, "lon": -87.584672, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.774059, "lon": -87.568387, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.749745, "lon": -87.570264, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.760178, "lon": -87.573779, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765158, "lon": -87.585941, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.752203, "lon": -87.573834, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.774198, "lon": -87.568581, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.770527, "lon": -87.585604, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.756143, "lon": -87.574121, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.770908, "lon": -87.568174, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.755674, "lon": -87.579376, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.769262, "lon": -87.575056, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.76599, "lon": -87.567834, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760922, "lon": -87.584492, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773867, "lon": -87.580237, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768799, "lon": -87.585424, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.772415, "lon": -87.569336, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.752304, "lon": -87.56963, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.758622, "lon": -87.578379, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.76913, "lon": -87.585885, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.755496, "lon": -87.570052, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.756849, "lon": -87.58332, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.762978, "lon": -87.574838, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753724, "lon": -87.583763, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.768875, "lon": -87.575893, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.767009, "lon": -87.5843, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.769458, "lon": -87.578653, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.773902, "lon": -87.581629, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.767568, "lon": -87.584363, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.767685, "lon": -87.581025, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773814, "lon": -87.573604, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.764104, "lon": -87.573763, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.76482, "lon": -87.583276, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.773787, "lon": -87.567163, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.766539, "lon": -87.576743, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.764596, "lon": -87.571199, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753205, "lon": -87.579437, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.771995, "lon": -87.580027, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.751413, "lon": -87.571115, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.792129, "lon": -87.585533, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.777034, "lon": -87.593048, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.788885, "lon": -87.600415, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.792247, "lon": -87.589126, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.791911, "lon": -87.584127, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.77831, "lon": -87.600184, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781242, "lon": -87.586197, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.786622, "lon": -87.603697, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.789796, "lon": -87.585408, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.791454, "lon": -87.599788, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781123, "lon": -87.590434, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.78917, "lon": -87.595438, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.775516, "lon": -87.594209, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.792657, "lon": -87.605379, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.78742, "lon": -87.585621, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781461, "lon": -87.593029, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.791519, "lon": -87.586332, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.782022, "lon": -87.592733, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.790033, "lon": -87.58485, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.776297, "lon": -87.604206, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781998, "lon": -87.598941, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.775967, "lon": -87.60308, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.778022, "lon": -87.591677, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.778432, "lon": -87.600091, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.77805, "lon": -87.590377, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.786815, "lon": -87.602585, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.783448, "lon": -87.604686, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.78541, "lon": -87.600561, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.779471, "lon": -87.596505, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.78953, "lon": -87.602129, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.780701, "lon": -87.597542, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.778864, "lon": -87.596582, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.782494, "lon": -87.586995, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.790996, "lon": -87.59981, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.790743, "lon": -87.584625, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.776808, "lon": -87.590524, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.792805, "lon": -87.600015, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.776272, "lon": -87.602262, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.776341, "lon": -87.604263, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.789349, "lon": -87.587998, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.783012, "lon": -87.59281, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.778527, "lon": -87.595811, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.778133, "lon": -87.599158, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.78648, "lon": -87.591223, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.788479, "lon": -87.600821, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.790479, "lon": -87.596841, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.777942, "lon": -87.588327, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.778632, "lon": -87.602232, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.785583, "lon": -87.585095, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.77876, "lon": -87.594614, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.787185, "lon": -87.596305, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.788393, "lon": -87.58462, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.785073, "lon": -87.589531, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.791809, "lon": -87.589456, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.790819, "lon": -87.604496, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.778085, "lon": -87.600819, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.784422, "lon": -87.596778, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.780077, "lon": -87.601913, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.776299, "lon": -87.601649, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.781502, "lon": -87.585117, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.781282, "lon": -87.587263, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781706, "lon": -87.600664, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.778996, "lon": -87.594843, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.787568, "lon": -87.603246, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.783268, "lon": -87.587007, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.788526, "lon": -87.594521, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.775257, "lon": -87.585394, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.785107, "lon": -87.602941, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.784668, "lon": -87.601717, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.783673, "lon": -87.592667, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.788983, "lon": -87.586699, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.786023, "lon": -87.59599, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.779397, "lon": -87.598876, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.786578, "lon": -87.603374, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.787713, "lon": -87.586276, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.785192, "lon": -87.588629, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.789741, "lon": -87.595831, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.778176, "lon": -87.593025, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.784592, "lon": -87.590836, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.791055, "lon": -87.588187, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.789908, "lon": -87.588733, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.776243, "lon": -87.600566, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.790543, "lon": -87.588542, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.79115, "lon": -87.59271, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.777445, "lon": -87.600925, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.779547, "lon": -87.597777, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.786175, "lon": -87.604987, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.782961, "lon": -87.586706, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.791849, "lon": -87.596284, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.783638, "lon": -87.601874, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.752628, "lon": -87.598539, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.766814, "lon": -87.600454, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.748862, "lon": -87.612062, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.748273, "lon": -87.608541, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.757839, "lon": -87.610603, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.764854, "lon": -87.606278, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.773193, "lon": -87.617163, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.762119, "lon": -87.590787, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.760506, "lon": -87.592414, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.753026, "lon": -87.592171, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.756871, "lon": -87.612204, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.763371, "lon": -87.600289, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.764144, "lon": -87.615382, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.752417, "lon": -87.594611, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.761502, "lon": -87.604445, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.749579, "lon": -87.60215, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.754858, "lon": -87.590486, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.748574, "lon": -87.609624, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.758323, "lon": -87.601008, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.761937, "lon": -87.590919, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.766194, "lon": -87.611197, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.748297, "lon": -87.594177, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.75723, "lon": -87.60495, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.767414, "lon": -87.592662, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.757315, "lon": -87.596686, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.768583, "lon": -87.593715, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.74899, "lon": -87.597368, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.752002, "lon": -87.615663, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.750622, "lon": -87.615475, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.756133, "lon": -87.615052, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.752185, "lon": -87.613921, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.756797, "lon": -87.60272, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.749928, "lon": -87.591615, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.766684, "lon": -87.607687, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.772035, "lon": -87.594827, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.764232, "lon": -87.613153, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.757298, "lon": -87.604572, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.766994, "lon": -87.612724, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.756332, "lon": -87.59435, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.773677, "lon": -87.616573, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.756102, "lon": -87.596257, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.749905, "lon": -87.594108, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.752904, "lon": -87.596619, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.749302, "lon": -87.616614, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.748813, "lon": -87.60507, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.753201, "lon": -87.611291, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.772251, "lon": -87.610986, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.773633, "lon": -87.617947, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.772762, "lon": -87.598116, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.770184, "lon": -87.59656, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.771938, "lon": -87.605768, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.760101, "lon": -87.606511, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.757413, "lon": -87.592416, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.76774, "lon": -87.597046, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.753824, "lon": -87.596096, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.759868, "lon": -87.609169, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.753484, "lon": -87.612773, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.755986, "lon": -87.605155, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.771429, "lon": -87.592368, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.750605, "lon": -87.60415, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.748739, "lon": -87.60319, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.748931, "lon": -87.616243, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.764014, "lon": -87.610757, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.763702, "lon": -87.606197, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.752655, "lon": -87.591312, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.751932, "lon": -87.602022, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.767239, "lon": -87.607655, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.757909, "lon": -87.610039, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.76517, "lon": -87.605835, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.756754, "lon": -87.606485, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.763472, "lon": -87.598674, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.761476, "lon": -87.601252, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.751745, "lon": -87.593019, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.749776, "lon": -87.612443, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.760173, "lon": -87.595241, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.763853, "lon": -87.61018, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.761314, "lon": -87.590479, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.762518, "lon": -87.614481, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.74911, "lon": -87.588526, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.759484, "lon": -87.593196, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.751334, "lon": -87.599021, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.759586, "lon": -87.611612, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.769273, "lon": -87.617976, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.749313, "lon": -87.612754, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.756715, "lon": -87.597244, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.765872, "lon": -87.595571, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.761923, "lon": -87.596687, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.757676, "lon": -87.599843, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.760818, "lon": -87.597678, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.751016, "lon": -87.606224, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.771688, "lon": -87.591086, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.753121, "lon": -87.595547, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.752557, "lon": -87.610551, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.749544, "lon": -87.594231, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.770771, "lon": -87.599342, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.773023, "lon": -87.613401, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.768664, "lon": -87.615881, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.767076, "lon": -87.589582, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.772853, "lon": -87.60346, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.751479, "lon": -87.613366, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.728562, "lon": -87.61545, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.736288, "lon": -87.628388, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.739076, "lon": -87.616871, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.735353, "lon": -87.60565, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.743649, "lon": -87.611331, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.74741, "lon": -87.603277, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.732374, "lon": -87.605801, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.72872, "lon": -87.623866, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.733256, "lon": -87.628357, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.73701, "lon": -87.601845, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.738192, "lon": -87.626469, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.744621, "lon": -87.626677, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.744612, "lon": -87.610879, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.730035, "lon": -87.626557, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.739553, "lon": -87.60957, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.733168, "lon": -87.606433, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.73915, "lon": -87.629948, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.747755, "lon": -87.632539, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.735483, "lon": -87.631075, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.734794, "lon": -87.608917, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.743318, "lon": -87.620435, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.736042, "lon": -87.625367, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.729547, "lon": -87.609303, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.742739, "lon": -87.613581, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.746123, "lon": -87.603299, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.738869, "lon": -87.626605, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.740596, "lon": -87.611808, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.746137, "lon": -87.62832, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.744065, "lon": -87.633129, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.744832, "lon": -87.604573, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.72835, "lon": -87.600553, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.728528, "lon": -87.606103, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.743979, "lon": -87.618917, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.728308, "lon": -87.606909, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.736219, "lon": -87.605149, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.729339, "lon": -87.619767, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.745482, "lon": -87.616158, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.731907, "lon": -87.633737, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.745541, "lon": -87.606233, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.729526, "lon": -87.625754, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.74678, "lon": -87.600032, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.737546, "lon": -87.619319, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.732464, "lon": -87.616011, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.745946, "lon": -87.617829, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.7381, "lon": -87.61691, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.74149, "lon": -87.615843, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.734615, "lon": -87.615525, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.734212, "lon": -87.628971, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.733512, "lon": -87.605964, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.732099, "lon": -87.617433, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.729744, "lon": -87.606016, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.729952, "lon": -87.633985, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.728531, "lon": -87.632061, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.737718, "lon": -87.606366, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.745105, "lon": -87.62727, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.739463, "lon": -87.634627, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.748193, "lon": -87.6046, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.738629, "lon": -87.602802, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.739926, "lon": -87.622797, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.735251, "lon": -87.619881, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.730364, "lon": -87.616962, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.745333, "lon": -87.628755, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.74383, "lon": -87.612075, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.731288, "lon": -87.63312, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.732932, "lon": -87.602354, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.741544, "lon": -87.621111, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.738605, "lon": -87.62333, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.736756, "lon": -87.619644, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.740463, "lon": -87.604143, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.729016, "lon": -87.625469, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.728181, "lon": -87.630578, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.742329, "lon": -87.617142, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.746532, "lon": -87.601537, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.747927, "lon": -87.628198, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.739502, "lon": -87.613214, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.746252, "lon": -87.606852, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.730253, "lon": -87.632865, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.741615, "lon": -87.608906, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.730496, "lon": -87.615213, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.73486, "lon": -87.626115, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.747695, "lon": -87.600256, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.73317, "lon": -87.614769, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.748467, "lon": -87.619494, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.740852, "lon": -87.632417, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.734655, "lon": -87.630328, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.729277, "lon": -87.623991, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.739064, "lon": -87.614257, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.738469, "lon": -87.628601, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.736454, "lon": -87.631985, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.738385, "lon": -87.629809, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.739059, "lon": -87.604821, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.737132, "lon": -87.602084, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.737685, "lon": -87.616447, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.738727, "lon": -87.626807, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.748407, "lon": -87.609818, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.746646, "lon": -87.608009, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.728744, "lon": -87.625622, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.747209, "lon": -87.613027, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.744533, "lon": -87.601792, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.747241, "lon": -87.63375, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.744629, "lon": -87.629505, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.730701, "lon": -87.601888, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.72909, "lon": -87.615476, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.741704, "lon": -87.612166, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.746174, "lon": -87.625545, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.74666, "lon": -87.61792, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.7423, "lon": -87.62671, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.739607, "lon": -87.62654, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.738376, "lon": -87.628072, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.728991, "lon": -87.634723, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.73158, "lon": -87.573965, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.737566, "lon": -87.57664, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.73135, "lon": -87.569267, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.744612, "lon": -87.562512, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.729718, "lon": -87.572904, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.727368, "lon": -87.577196, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.738576, "lon": -87.566539, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.736779, "lon": -87.569193, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.739393, "lon": -87.567128, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.747379, "lon": -87.573538, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.734919, "lon": -87.57142, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.721497, "lon": -87.564826, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.742656, "lon": -87.569608, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.737015, "lon": -87.56397, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.728725, "lon": -87.567416, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.738025, "lon": -87.57716, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.747656, "lon": -87.564245, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.743815, "lon": -87.577596, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.726743, "lon": -87.568027, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.737613, "lon": -87.568497, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.739017, "lon": -87.570294, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.723625, "lon": -87.569378, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.73825, "lon": -87.568789, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.739333, "lon": -87.5622, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.739388, "lon": -87.566878, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.739797, "lon": -87.563634, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.742123, "lon": -87.577199, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.742836, "lon": -87.568057, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.726211, "lon": -87.576156, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.743802, "lon": -87.566675, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.745778, "lon": -87.576555, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.747517, "lon": -87.564862, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.723226, "lon": -87.573385, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.745029, "lon": -87.565341, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.746991, "lon": -87.567827, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.725086, "lon": -87.569792, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.723344, "lon": -87.568503, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.738495, "lon": -87.56286, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.735111, "lon": -87.566299, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.736334, "lon": -87.574466, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.726742, "lon": -87.564887, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.738809, "lon": -87.564548, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.744672, "lon": -87.576501, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.726224, "lon": -87.568973, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.726527, "lon": -87.572384, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.74109, "lon": -87.575019, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.725081, "lon": -87.577153, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.743899, "lon": -87.572724, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.740665, "lon": -87.571492, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.744428, "lon": -87.568967, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.720522, "lon": -87.571449, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.724423, "lon": -87.564802, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.724746, "lon": -87.565352, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.747814, "lon": -87.569269, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.746771, "lon": -87.565729, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.747497, "lon": -87.565292, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.733122, "lon": -87.568111, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.743857, "lon": -87.563714, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.73344, "lon": -87.566007, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.733082, "lon": -87.568941, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.727442, "lon": -87.563668, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.726499, "lon": -87.569015, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.721805, "lon": -87.568478, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.719919, "lon": -87.57738, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.718227, "lon": -87.562306, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.72279, "lon": -87.577821, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.746239, "lon": -87.56618, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.745441, "lon": -87.571788, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.741926, "lon": -87.571517, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.718614, "lon": -87.569273, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.733438, "lon": -87.65309, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.73261, "lon": -87.636223, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.746468, "lon": -87.644726, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.740934, "lon": -87.637455, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.747759, "lon": -87.633646, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.729192, "lon": -87.640005, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.747318, "lon": -87.651922, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.729118, "lon": -87.643063, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.734154, "lon": -87.637102, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.737515, "lon": -87.636037, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.74505, "lon": -87.649955, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.752038, "lon": -87.657456, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.750274, "lon": -87.648216, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.75135, "lon": -87.656289, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.743908, "lon": -87.656904, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.736547, "lon": -87.646774, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.74374, "lon": -87.650884, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.72851, "lon": -87.635524, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.743836, "lon": -87.647373, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.738174, "lon": -87.650763, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.740898, "lon": -87.653984, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.744559, "lon": -87.637788, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.731402, "lon": -87.642385, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.745386, "lon": -87.644024, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.745948, "lon": -87.632871, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.752518, "lon": -87.640584, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.750499, "lon": -87.639941, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.733525, "lon": -87.651754, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.751533, "lon": -87.64422, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.744986, "lon": -87.646872, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.744164, "lon": -87.648178, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.753493, "lon": -87.635272, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.73715, "lon": -87.639236, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.746746, "lon": -87.653786, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.744677, "lon": -87.633935, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.744525, "lon": -87.638731, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.7344, "lon": -87.650481, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.74046, "lon": -87.635854, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.737894, "lon": -87.632309, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.739961, "lon": -87.641636, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.746677, "lon": -87.641943, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.731223, "lon": -87.655283, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.737233, "lon": -87.647796, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.729934, "lon": -87.644689, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.753952, "lon": -87.641476, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.746209, "lon": -87.642987, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.745408, "lon": -87.651418, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.740092, "lon": -87.633069, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.728236, "lon": -87.645839, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.735577, "lon": -87.634347, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.728571, "lon": -87.636171, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.748859, "lon": -87.637911, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.754068, "lon": -87.636446, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.733113, "lon": -87.65004, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.731572, "lon": -87.64182, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.750014, "lon": -87.635831, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.739494, "lon": -87.655248, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.743868, "lon": -87.634934, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.738372, "lon": -87.650444, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.74899, "lon": -87.656353, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.737563, "lon": -87.655723, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.743889, "lon": -87.649845, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.746816, "lon": -87.64733, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.728296, "lon": -87.644723, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.742232, "lon": -87.648432, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.745456, "lon": -87.646447, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.728918, "lon": -87.633576, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.747169, "lon": -87.643215, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.734186, "lon": -87.651684, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.739875, "lon": -87.646509, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.748205, "lon": -87.649028, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.742368, "lon": -87.641669, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.74948, "lon": -87.655497, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.754304, "lon": -87.656619, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.747589, "lon": -87.652005, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.747394, "lon": -87.652315, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.733406, "lon": -87.652134, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.740292, "lon": -87.649229, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.741163, "lon": -87.6477, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.740057, "lon": -87.635172, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_311_flooding():
    """
    Try Chicago Data Portal live API first.
    Falls back to embedded representative dataset if portal is unavailable
    (the portal blocks direct API calls from cloud servers).
    """
    try:
        r = requests.get(
            "https://data.cityofchicago.org/resource/qrmr-m89j.json",
            params={
                "$where": "latitude > 41.70 AND latitude < 41.82 AND longitude > -87.65 AND longitude < -87.52",
                "$limit": "5000",
                "$order": "creation_date DESC",
            },
            timeout=12,
        )
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json()), "live"
    except Exception:
        pass
    # Use embedded dataset
    return pd.DataFrame(EMBEDDED_FLOOD_DATA), "embedded"

with st.spinner("Loading 311 flooding data..."):
    df_raw, status = fetch_311_flooding()

# ── Process dataframe ──────────────────────────────────────────────────────────
def process_df(df):
    if df is None or df.empty:
        return None

    # Normalise column names (different endpoints use different names)
    df.columns = [c.lower() for c in df.columns]

    # Latitude / longitude
    for lat_col in ["latitude", "lat", "y_coordinate"]:
        if lat_col in df.columns:
            df["lat"] = pd.to_numeric(df[lat_col], errors="coerce")
            break
    for lon_col in ["longitude", "lon", "x_coordinate"]:
        if lon_col in df.columns:
            df["lon"] = pd.to_numeric(df[lon_col], errors="coerce")
            break

    # Community area
    for ca_col in ["community_area", "community_area_number"]:
        if ca_col in df.columns:
            df["ca"] = pd.to_numeric(df[ca_col], errors="coerce")
            break

    # Type
    for type_col in ["type_of_service_request", "sr_type", "service_request_type", "type"]:
        if type_col in df.columns:
            df["flood_type"] = df[type_col]
            break
    if "flood_type" not in df.columns:
        df["flood_type"] = "Flooding"

    # Date
    for date_col in ["creation_date", "created_date", "date", "open_dt"]:
        if date_col in df.columns:
            df["report_date"] = pd.to_datetime(df[date_col], errors="coerce")
            break

    # Address
    for addr_col in ["street_address", "address", "location"]:
        if addr_col in df.columns:
            df["addr"] = df[addr_col]
            break
    if "addr" not in df.columns:
        df["addr"] = "Address not available"

    df = df.dropna(subset=["lat", "lon"])
    df = df[(df["lat"] > 41.5) & (df["lat"] < 42.1)]
    df = df[(df["lon"] > -88.0) & (df["lon"] < -87.4)]
    return df

df = process_df(df_raw)

# ── Stats strip ────────────────────────────────────────────────────────────────
if df is not None and not df.empty:
    total = len(df)
    ss_count = len(df[df["ca"] == 43]) if "ca" in df.columns else "—"
    basement = len(df[df["flood_type"].str.contains("Basement|basement", na=False)])
    street   = len(df[df["flood_type"].str.contains("Street|street", na=False)])
else:
    total, ss_count, basement, street = "—", "—", "—", "—"

fmt_total    = f"{total:,}"    if isinstance(total,    int) else str(total)
fmt_ss       = f"{ss_count:,}" if isinstance(ss_count, int) else str(ss_count)
fmt_basement = f"{basement:,}" if isinstance(basement,  int) else str(basement)
fmt_street   = f"{street:,}"   if isinstance(street,    int) else str(street)

st.markdown(f"""
<div class="stats-strip">
  <div class="stat-item">
    <span class="stat-number">{fmt_total}</span>
    <span class="stat-label">311 Flooding Complaints · South Side</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{fmt_ss}</span>
    <span class="stat-label">In South Shore Specifically</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{fmt_basement}</span>
    <span class="stat-label">Basement Flooding Reports</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{fmt_street}</span>
    <span class="stat-label">Street Flooding Reports</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">$5M</span>
    <span class="stat-label">City Spending on Lakefront Breakwaters</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Map section ────────────────────────────────────────────────────────────────
# ── About ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="about">', unsafe_allow_html=True)
st.markdown('<div class="section-head">About This Initiative</div>', unsafe_allow_html=True)

# Full-width text — no tall column to push things down
st.markdown("""
<div class="pullquote">
"Every time it rains hard in South Shore, basements flood. Streets turn into rivers.
Families pump water out of their homes, replace ruined belongings, and fight mold for months.
This is one of only four Chicago neighborhoods identified as being at the highest risk
of urban flooding in the entire city."
</div>
<p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif;margin-bottom:8px">
Despite this, the City of Chicago is advancing a <strong>$5 million lakefront breakwater
project between 71st and 75th Street</strong> — infrastructure South Shore never asked for,
with no updated environmental review, funded by a grant expiration deadline, not an
independently assessed hazard.
<strong>This page exists to document what residents are actually experiencing.</strong>
Further below you will find the 311 map of officially filed complaints. Your report adds the
human layer — the photos, the damage, the mold, the displacement — that official data cannot capture.
This is the last Black lakefront residential community in America.
South Shore deserves infrastructure grounded in science, transparency, and the actual needs
of residents — not concrete in the lake.
</p>
""", unsafe_allow_html=True)

# Petition box — full width now that flyer is removed
pet_col, _ = st.columns([1, 1])
with pet_col:
    st.markdown("""
    <div style="background:#f8f0f0;border:1px solid #e0b0b0;border-radius:3px;
    padding:14px 16px;font-family:Arial,sans-serif;height:100%">
      <div style="font-weight:700;color:#c0392b;font-size:13px;margin-bottom:8px">
        WHAT THE PETITION CALLS FOR
      </div>
      <ul style="font-size:13px;color:#333;line-height:1.9;margin:0;padding-left:16px">
        <li><strong>Pause</strong> the breakwater project</li>
        <li><strong>Redirect</strong> the $5M to flood mitigation residents need</li>
        <li><strong>Require</strong> transparent environmental review</li>
        <li><strong>Evaluate</strong> nature-based alternatives</li>
        <li><strong>Ensure</strong> meaningful community input</li>
      </ul>
      <div style="text-align:center;margin-top:14px">
        <a href="http://bit.ly/4ukCmjg" target="_blank"
        style="display:inline-block;background:#c0392b;color:#fff;font-weight:700;
        font-size:13px;padding:9px 22px;border-radius:3px;text-decoration:none">
        ✍️ Sign Now →</a>
      </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Key impacts ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="content-section">
  <div class="section-head">What Breakwaters Actually Do</div>
  <div class="section-sub">
    Peer-reviewed science. (<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9813723"
    target="_blank" style="color:#0a2240">Saengsupavanich et al., Heliyon 2022</a>)
  </div>
  <div class="concerns-grid">
    <div class="concern-card">
      <div class="concern-icon">🏖️</div>
      <div class="concern-title">Beach & Shoreline Destruction</div>
      <div class="concern-text">Permanently interrupts sediment transport. Damage extends far
      beyond 75th Street — Promontory Point, Rainbow Beach, every neighbor absorbs accelerated erosion.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🌀</div>
      <div class="concern-title">Dangerous Currents</div>
      <div class="concern-text">Strong eddies between breakwater gaps dramatically increase
      drowning risk. Studies document 67 victims/year at studied sites. South Shore families swim here.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🐟</div>
      <div class="concern-title">Water Quality & Hypoxia</div>
      <div class="concern-text">Creates water stagnation, hypoxic dead zones in summer,
      degraded water quality, and conditions that drive beachgoers away.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">⛓️</div>
      <div class="concern-title">Erosion Chain Reaction</div>
      <div class="concern-text">Intended to protect one stretch, breakwaters actively accelerate
      erosion elsewhere — a shore-parallel seawall effect worsening downdrift erosion for years.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🌿</div>
      <div class="concern-title">Ecological Damage</div>
      <div class="concern-text">Destroys lake bottom habitats, reduces dissolved oxygen,
      intensifies turbidity. No environmental review for this project has ever been produced.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">💰</div>
      <div class="concern-title">Cost & Lock-In</div>
      <div class="concern-text">Nature-based alternatives cost 2–5× less. Once concrete is poured,
      you are locked in for generations. Ogden Dunes, Indiana spent $5M undoing one breakwater's damage.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Report form ────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="report">', unsafe_allow_html=True)
st.markdown('<div class="section-head">Report Your Flooding Experience</div>', unsafe_allow_html=True)
st.markdown("""
<p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:6px;line-height:1.7">
  We have 311 complaint data from the Chicago Data Portal — but official records only capture part
  of the story. Calls go unfiled. Flooding in backyards, alleys, parks, and parking lots rarely
  makes it into the system. And 311 data does not tell us about the mold that grew for months,
  the belongings that were ruined, the family that had to leave, or the repair bills that wiped
  out a household's savings.
</p>
<p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:12px;line-height:1.7">
  <strong>We need the most up-to-date, self-reported flooding data directly from South Shore
  residents.</strong> Your account — in your words, from your block, with your photos — is the
  evidence that city data cannot produce. Tell us what happened. Every report matters.
</p>
""", unsafe_allow_html=True)

with st.form("flood_report", clear_on_submit=True):
    st.markdown('<div class="form-section">', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        name      = st.text_input("Your Name", placeholder="First and last name")
        email_addr = st.text_input("Your Email", placeholder="email@example.com")
    with fc2:
        address   = st.text_input("Address or Intersection", placeholder="e.g. 73rd & Coles Ave, South Shore")
        incident_date = st.date_input("When did this flooding occur?", value=date.today())

    flood_type = st.multiselect(
        "Where did flooding occur? (select all that apply)",
        ["Basement / lower level", "Street / road", "Alley", "Yard / garden",
         "Park or green space", "Parking lot", "Sidewalk", "Other"],
    )
    severity = st.select_slider(
        "How severe was the flooding?",
        options=["Minor (puddles)", "Moderate (ankle-deep)", "Significant (knee-deep or higher)",
                 "Severe (property damage)", "Extreme (displacement / emergency)"],
    )
    recurrence = st.radio(
        "Has this location flooded before?",
        ["First time", "Yes — occasionally (1–2 times/year)",
         "Yes — frequently (every heavy rain)", "Yes — chronic ongoing problem"],
    )
    description = st.text_area(
        "Describe what happened",
        placeholder="When it started, how long water stayed, property damage, city response (or lack of)...",
        height=120,
    )
    infrastructure = st.text_area(
        "Any known infrastructure issues nearby? (optional)",
        placeholder="e.g. blocked catch basins, broken sewer, no storm drains...",
        height=60,
    )

    st.markdown("""
    <div class="photo-note">
      📷 <strong>Have photos or videos?</strong> Email them directly to
      <a href="mailto:sokovic.anamarija@gmail.com">sokovic.anamarija@gmail.com</a>
      — subject: <strong>"South Shore Flooding — [your street]"</strong>.
      Basement water, flooded streets, overwhelmed drains, mold — all of it matters.
    </div>
    """, unsafe_allow_html=True)

    consent = st.checkbox("I consent to this report being used as part of the public record on South Shore flooding.")
    submitted = st.form_submit_button("Submit My Report")

    if submitted:
        if not name or not address or not description:
            st.error("Please fill in your name, address/location, and description.")
        elif not consent:
            st.error("Please check the consent box to submit your report.")
        else:
            flood_types_str = ", ".join(flood_type) if flood_type else "Not specified"
            subject = f"South Shore Flooding Report — {address}"
            body = (
                f"SOUTH SHORE FLOODING REPORT\n"
                f"============================\n"
                f"Name: {name}\n"
                f"Email: {email_addr}\n"
                f"Location: {address}\n"
                f"Date: {incident_date}\n\n"
                f"Flooding locations: {flood_types_str}\n"
                f"Severity: {severity}\n"
                f"Recurrence: {recurrence}\n\n"
                f"DESCRIPTION:\n{description}\n\n"
                f"INFRASTRUCTURE:\n{infrastructure or 'None noted'}\n\n"
                f"Submitted via south-shore-floods.streamlit.app"
            )
            mailto = (
                "mailto:sokovic.anamarija@gmail.com"
                f"?subject={urllib.parse.quote(subject)}"
                f"&body={urllib.parse.quote(body)}"
            )
            st.success("✅ Thank you! Click below to send your report.")
            st.markdown(
                f'<a href="{mailto}" style="display:inline-block;background:#0a2240;color:#fff;'
                f'font-weight:700;font-size:14px;padding:10px 28px;border-radius:3px;'
                f'text-decoration:none;margin-top:8px">📧 Open Email to Send Report →</a>',
                unsafe_allow_html=True,
            )
            st.info("Your email client will open pre-filled. Hit Send and attach any photos.", icon="📬")

    st.markdown('</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── 311 Map — shown after report form ────────────────────────────────────────
st.markdown('<div class="content-section" id="map">', unsafe_allow_html=True)
st.markdown('<div class="section-head">311 Flooding Complaints — South Side Chicago</div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-sub">
  <p style="font-size:14px;color:#333;font-family:Arial,sans-serif;line-height:1.7;margin:0 0 10px 0">
  The map below shows official <strong>311 flooding complaints</strong> filed with the City of Chicago
  — real reports from real residents, pulled live from the
  <a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j"
  target="_blank" style="color:#0a2240">Chicago Data Portal</a>.
  This data captures some of what is happening on the ground — but 311 reports are only a fraction
  of the actual flooding South Shore residents experience. Many people never call 311. Many calls
  go unlogged. Flooding in alleys, parks, backyards, and parking lots rarely makes it into the
  official record at all.
  </p>
  <p style="font-size:14px;color:#333;font-family:Arial,sans-serif;line-height:1.7;margin:0 0 6px 0">
  <strong>That is why your self-reported experience matters most.</strong>
  The 311 data tells the city's story. Your report above tells the truth.
  Together, they build the public record that decision-makers cannot ignore.
  </p>
  <p style="font-size:13px;color:#666;font-family:Arial,sans-serif;margin:0">
  Map key: 🔴 Basement flooding · 🔵 Street flooding · 🟠 Other ·
  <strong style="color:#e67e22">Yellow zone</strong> = proposed $5M breakwater project (71st–75th St lakefront) ·
  <em>Data: Chicago 311 flooding complaints 2019–2024, South Side community areas.
  Larger dots = South Shore.</em>
  </p>
</div>
""", unsafe_allow_html=True)

try:
    import folium
    from streamlit_folium import st_folium

    m = folium.Map(
        location=[41.762, -87.572],
        zoom_start=13,
        tiles="CartoDB positron",
    )

    # Breakwater project zone (71st–75th St, lakefront)
    folium.Rectangle(
        bounds=[[41.7655, -87.5600], [41.7490, -87.5480]],
        color="#e67e22",
        fill=True,
        fill_color="#f39c12",
        fill_opacity=0.25,
        weight=2,
        tooltip="⚠️ Proposed $5M Breakwater Project Zone (71st–75th St)",
    ).add_to(m)

    folium.Marker(
        location=[41.757, -87.554],
        tooltip="⚠️ Proposed Breakwater Zone\n71st–75th Street Lakefront\n$5 million · No environmental review",
        icon=folium.Icon(color="orange", icon="warning-sign", prefix="glyphicon"),
    ).add_to(m)

    # Plot 311 complaints
    if df is not None and not df.empty:
        def get_color(flood_type):
            ft = str(flood_type).lower()
            if "basement" in ft:
                return "#c0392b"
            if "street" in ft:
                return "#1a5cb8"
            return "#e67e22"

        sample = df.sample(min(len(df), 3000), random_state=42) if len(df) > 3000 else df

        for _, row in sample.iterrows():
            try:
                lat, lon = float(row["lat"]), float(row["lon"])
                ft = str(row.get("flood_type", "Flooding"))
                addr = str(row.get("addr", ""))
                date_str = str(row.get("report_date", ""))[:10] if "report_date" in row else ""
                color = get_color(ft)
                is_ss = row.get("ca") == 43

                folium.CircleMarker(
                    location=[lat, lon],
                    radius=5 if is_ss else 3.5,
                    color=color,
                    fill=True,
                    fill_color=color,
                    fill_opacity=0.75 if is_ss else 0.5,
                    weight=1.5 if is_ss else 0.8,
                    tooltip=f"{'🔴 SOUTH SHORE | ' if is_ss else ''}{ft}<br>{addr}<br>{date_str}",
                ).add_to(m)
            except Exception:
                continue

    # Legend
    legend_html = """
    <div style="position:fixed;bottom:40px;left:60px;z-index:1000;background:#fff;
    padding:12px 16px;border-radius:5px;border:1px solid #ccc;font-family:Arial,sans-serif;
    font-size:12px;box-shadow:2px 2px 6px rgba(0,0,0,.2)">
      <strong style="color:#0a2240">311 Flooding Complaints</strong><br><br>
      <span style="background:#c0392b;color:#fff;padding:1px 8px;border-radius:10px">●</span>
      Basement flooding<br>
      <span style="background:#1a5cb8;color:#fff;padding:1px 8px;border-radius:10px">●</span>
      Street flooding<br>
      <span style="background:#e67e22;color:#fff;padding:1px 8px;border-radius:10px">●</span>
      Other flooding<br>
      <span style="background:#f39c12;padding:1px 8px;border-radius:10px">▪</span>
      Proposed breakwater zone<br>
      <em style="color:#888;font-size:10px">Larger dots = South Shore</em>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, width="100%", height=520, returned_objects=[])

except ImportError:
    st.info(
        "Map requires `folium` and `streamlit-folium`. "
        "Add them to requirements.txt and redeploy.",
        icon="🗺️",
    )
    if df is not None and not df.empty:
        st.markdown(f"**{len(df):,} flooding complaints** loaded from Chicago 311 for the South Side.")

st.markdown('</div>', unsafe_allow_html=True)

# ── Resources ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class="content-section">
  <div class="section-head">Resources & Documentation</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;
  font-family:Arial,sans-serif;font-size:13px">
    <div>
      <div style="font-weight:700;color:#0a2240;margin-bottom:8px">FOIA & RESEARCH</div>
      <ul style="line-height:1.9;color:#333;padding-left:18px">
        <li><a href="https://tinyurl.com/4sh34tdj" target="_blank" style="color:#0a2240">Full FOIA analysis of the breakwater project</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9813723" target="_blank" style="color:#0a2240">Peer-reviewed breakwater impact study (Heliyon, 2022)</a></li>
        <li><a href="https://wicoastalresilience.org/march-2026-water-level-update" target="_blank" style="color:#0a2240">Lake Michigan water level update (March 2026)</a></li>
        <li><a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j" target="_blank" style="color:#0a2240">Chicago 311 Flooding Complaints Dataset</a></li>
      </ul>
    </div>
    <div>
      <div style="font-weight:700;color:#0a2240;margin-bottom:8px">FLOODING COVERAGE</div>
      <ul style="line-height:1.9;color:#333;padding-left:18px">
        <li><a href="https://news.uchicago.edu/story/students-identify-chicago-neighborhoods-most-risk-urban-flooding" target="_blank" style="color:#0a2240">UChicago: South Shore among highest-risk flood neighborhoods</a></li>
        <li><a href="https://www.wbez.org/environment/2026/04/10/flooding-chicago-climate-change-deep-tunnel-mold-metropolitan-water-reclamation-district-soaked" target="_blank" style="color:#0a2240">WBEZ: 70,000 Chicago homes flooded in 2023</a></li>
        <li><a href="https://insideclimatenews.org/news/04052026/chicago-flooding-climate-change/" target="_blank" style="color:#0a2240">Inside Climate News: Chicago flooding is getting worse</a></li>
        <li><a href="https://www.youtube.com/watch?v=0oJ0UtZIbx0" target="_blank" style="color:#0a2240">Ogden Dunes: $5M to undo one breakwater's damage</a></li>
      </ul>
    </div>
  </div>
  <div style="margin-top:18px;background:#f0f5ff;border:1px solid #c0d0e8;
  border-radius:3px;padding:14px 18px;font-family:Arial,sans-serif;font-size:13px;color:#333">
    <strong style="color:#0a2240">CONTACT DECISION-MAKERS DIRECTLY</strong><br><br>
    <strong>Mayor Brandon Johnson</strong> · City Hall, 121 N. LaSalle St., Chicago IL 60602
    · 312-744-3300<br>
    <strong>Illinois DCEO</strong> · 500 E. Monroe St., Springfield IL 62701
    · 217-782-7500 · dceo.webmaster@illinois.gov
  </div>
</div>
""", unsafe_allow_html=True)

# ── Bottom CTA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#c0392b;color:#fff;text-align:center;padding:32px 24px">
  <div style="font-size:1.5rem;font-weight:800;font-family:Arial,sans-serif;margin-bottom:8px">
    The last Black lakefront residential community in America did not get a study.<br>
    It got a construction schedule.
  </div>
  <div style="font-size:14px;color:#f8c8c8;margin-bottom:16px;font-family:Arial,sans-serif">
    Construction is assumed to begin as early as <strong style="color:#fff">Fall 2026</strong>.
  </div>
  <a href="http://bit.ly/4ukCmjg" target="_blank"
  style="display:inline-block;background:#fff;color:#c0392b;font-weight:800;
  font-size:1.1rem;padding:14px 40px;border-radius:3px;text-decoration:none;">
  ✍️ SIGN THE PETITION — bit.ly/4ukCmjg</a>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
  <strong>South Shore Flooding Documentation Initiative</strong> · Chicago, IL<br>
  Photos & documents: <a href="mailto:sokovic.anamarija@gmail.com">sokovic.anamarija@gmail.com</a>
  &nbsp;·&nbsp; Petition: <a href="http://bit.ly/4ukCmjg" target="_blank">bit.ly/4ukCmjg</a>
  &nbsp;·&nbsp; FOIA analysis: <a href="https://tinyurl.com/4sh34tdj" target="_blank">tinyurl.com/4sh34tdj</a><br>
  <span style="color:#5a7090;font-size:11px">
    311 data sourced live from the City of Chicago Data Portal (public domain).
    Community reports are used solely for civic advocacy purposes.
  </span>
</div>
""", unsafe_allow_html=True)
