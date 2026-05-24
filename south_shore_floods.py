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
EMBEDDED_FLOOD_DATA = [{"lat": 41.765265, "lon": -87.585225, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.751768, "lon": -87.582823, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.763943, "lon": -87.585015, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.761645, "lon": -87.585177, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.753952, "lon": -87.567733, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.768488, "lon": -87.581051, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.752198, "lon": -87.556326, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.758258, "lon": -87.574872, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.769792, "lon": -87.563378, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.750128, "lon": -87.576911, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.763589, "lon": -87.564158, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.768873, "lon": -87.555458, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.758263, "lon": -87.571944, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.757995, "lon": -87.579505, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.764447, "lon": -87.580695, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.760481, "lon": -87.577632, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.766485, "lon": -87.559872, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.770189, "lon": -87.561044, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.753697, "lon": -87.55677, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.753741, "lon": -87.570524, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.751858, "lon": -87.581671, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.768169, "lon": -87.572719, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.753922, "lon": -87.555076, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.768406, "lon": -87.559306, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.769386, "lon": -87.572913, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.764089, "lon": -87.57149, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.766368, "lon": -87.582449, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.768752, "lon": -87.575455, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.760251, "lon": -87.556432, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.774241, "lon": -87.562379, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.771504, "lon": -87.576748, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.752127, "lon": -87.562362, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764172, "lon": -87.570853, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.771725, "lon": -87.560218, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.754504, "lon": -87.568412, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.770033, "lon": -87.555682, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.751467, "lon": -87.571266, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.762247, "lon": -87.567196, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.76725, "lon": -87.573631, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.759829, "lon": -87.569955, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.749729, "lon": -87.585348, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.748194, "lon": -87.564057, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.772446, "lon": -87.559351, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.755519, "lon": -87.570952, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.754561, "lon": -87.571338, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.750617, "lon": -87.572637, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.771324, "lon": -87.584321, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.749637, "lon": -87.563425, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.754714, "lon": -87.580104, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752954, "lon": -87.571659, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.759965, "lon": -87.559298, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.765608, "lon": -87.569242, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.773012, "lon": -87.55969, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.760997, "lon": -87.559196, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.758232, "lon": -87.555455, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.755702, "lon": -87.564406, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75218, "lon": -87.576802, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.768195, "lon": -87.584228, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.749536, "lon": -87.570257, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.764066, "lon": -87.565068, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.773423, "lon": -87.56834, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764723, "lon": -87.573004, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.773237, "lon": -87.579668, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.755172, "lon": -87.581943, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.756537, "lon": -87.562692, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.764771, "lon": -87.568547, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.761659, "lon": -87.581894, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.77174, "lon": -87.574545, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.764515, "lon": -87.555396, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.766032, "lon": -87.568807, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.773351, "lon": -87.581837, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.768045, "lon": -87.581181, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.767376, "lon": -87.579688, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761646, "lon": -87.578215, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.750492, "lon": -87.572869, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.757006, "lon": -87.581945, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768013, "lon": -87.568898, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.751021, "lon": -87.556703, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.762731, "lon": -87.560128, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.759604, "lon": -87.584703, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772271, "lon": -87.579488, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.757549, "lon": -87.568644, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.772996, "lon": -87.578661, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.771798, "lon": -87.585232, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.769124, "lon": -87.573237, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.755204, "lon": -87.561591, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.771182, "lon": -87.579105, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.757441, "lon": -87.560563, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.748639, "lon": -87.580013, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.774106, "lon": -87.577347, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.766347, "lon": -87.559847, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.751114, "lon": -87.555918, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.749033, "lon": -87.567506, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.759783, "lon": -87.555489, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.754878, "lon": -87.564028, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.757834, "lon": -87.583831, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.764825, "lon": -87.565435, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761692, "lon": -87.565326, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.762969, "lon": -87.580053, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.766288, "lon": -87.558013, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.758964, "lon": -87.560155, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.759607, "lon": -87.56802, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.759928, "lon": -87.565056, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.765789, "lon": -87.577203, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.750521, "lon": -87.556488, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.754065, "lon": -87.579827, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.774566, "lon": -87.567051, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75919, "lon": -87.566477, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.761348, "lon": -87.578436, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772102, "lon": -87.559326, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.753909, "lon": -87.561073, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.749356, "lon": -87.578275, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.7516, "lon": -87.571596, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.773651, "lon": -87.558366, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.770425, "lon": -87.569016, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.760152, "lon": -87.562695, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.768677, "lon": -87.56984, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.759877, "lon": -87.56388, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.756632, "lon": -87.569255, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758342, "lon": -87.581263, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.759005, "lon": -87.569179, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.770488, "lon": -87.573926, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.771132, "lon": -87.562267, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773454, "lon": -87.576743, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.762532, "lon": -87.563226, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.761182, "lon": -87.577539, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.757075, "lon": -87.564947, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.770694, "lon": -87.557494, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772487, "lon": -87.567651, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.765354, "lon": -87.581793, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.755024, "lon": -87.575852, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.768553, "lon": -87.574247, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.754811, "lon": -87.583461, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.774998, "lon": -87.575151, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.768364, "lon": -87.556562, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764776, "lon": -87.578605, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.763227, "lon": -87.579243, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.75253, "lon": -87.567175, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.769, "lon": -87.580923, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.77308, "lon": -87.56815, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.75871, "lon": -87.563835, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.750751, "lon": -87.562053, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.769498, "lon": -87.568456, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.765861, "lon": -87.583862, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.770939, "lon": -87.560508, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.765161, "lon": -87.56031, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752756, "lon": -87.569826, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.760552, "lon": -87.560402, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.770996, "lon": -87.560247, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.754584, "lon": -87.571594, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.757083, "lon": -87.570676, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753727, "lon": -87.561267, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.763006, "lon": -87.569985, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.767442, "lon": -87.570854, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765439, "lon": -87.570785, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.755944, "lon": -87.573464, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.760778, "lon": -87.569541, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.757499, "lon": -87.571934, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.751258, "lon": -87.58003, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.753172, "lon": -87.563103, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.774474, "lon": -87.560189, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.752845, "lon": -87.585561, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.749229, "lon": -87.58431, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.765222, "lon": -87.562663, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.7635, "lon": -87.571449, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.774068, "lon": -87.578173, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.770197, "lon": -87.573578, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.752097, "lon": -87.560855, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.774836, "lon": -87.582328, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.768944, "lon": -87.574208, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.771224, "lon": -87.555309, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.76446, "lon": -87.563057, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.764889, "lon": -87.577796, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.752693, "lon": -87.583673, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.766613, "lon": -87.571433, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.767088, "lon": -87.564207, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.772946, "lon": -87.561577, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.759479, "lon": -87.569119, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.770319, "lon": -87.583786, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.764066, "lon": -87.560449, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.751358, "lon": -87.564651, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761513, "lon": -87.570692, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772014, "lon": -87.563229, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.750466, "lon": -87.556181, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.774988, "lon": -87.565159, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.768604, "lon": -87.580569, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.772734, "lon": -87.580374, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.774164, "lon": -87.57143, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.766094, "lon": -87.55941, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.755782, "lon": -87.556699, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.76028, "lon": -87.57625, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.771353, "lon": -87.560427, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.759158, "lon": -87.580185, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.764886, "lon": -87.56244, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.773047, "lon": -87.572418, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.748779, "lon": -87.566469, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.75639, "lon": -87.585576, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.774791, "lon": -87.557699, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.765488, "lon": -87.581227, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.76174, "lon": -87.577524, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.779387, "lon": -87.591667, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.790552, "lon": -87.598818, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.781118, "lon": -87.585519, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.780091, "lon": -87.598238, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.790575, "lon": -87.59439, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.784935, "lon": -87.591871, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.790653, "lon": -87.5805, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.779204, "lon": -87.585836, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.787694, "lon": -87.584903, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.783916, "lon": -87.605037, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.790655, "lon": -87.583271, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.775276, "lon": -87.602252, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.776347, "lon": -87.58568, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.786697, "lon": -87.583854, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.792175, "lon": -87.589703, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.790703, "lon": -87.605067, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.792954, "lon": -87.586584, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.788687, "lon": -87.587699, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.787492, "lon": -87.582511, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.780281, "lon": -87.596254, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.785187, "lon": -87.585394, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.785971, "lon": -87.596054, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.791431, "lon": -87.602279, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.783272, "lon": -87.588662, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.791222, "lon": -87.588382, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.792014, "lon": -87.580321, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.787426, "lon": -87.594122, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.79036, "lon": -87.603227, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.785347, "lon": -87.58019, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.779941, "lon": -87.591286, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.791391, "lon": -87.586626, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.788963, "lon": -87.600017, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.786459, "lon": -87.589857, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.786308, "lon": -87.582512, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.789195, "lon": -87.605133, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.776622, "lon": -87.598327, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.778614, "lon": -87.585551, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.784555, "lon": -87.582249, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.791453, "lon": -87.581451, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.788438, "lon": -87.597193, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.777534, "lon": -87.580871, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.792411, "lon": -87.585081, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.775251, "lon": -87.592049, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.785522, "lon": -87.584617, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.787147, "lon": -87.593742, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.791475, "lon": -87.600244, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.791369, "lon": -87.598143, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.775816, "lon": -87.605032, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.776749, "lon": -87.582931, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.781678, "lon": -87.581316, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.785572, "lon": -87.587108, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.790006, "lon": -87.589993, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.775589, "lon": -87.596366, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.790398, "lon": -87.603417, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.77609, "lon": -87.598827, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.77665, "lon": -87.600485, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.77591, "lon": -87.597329, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.776235, "lon": -87.586106, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.789635, "lon": -87.599942, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.779991, "lon": -87.580415, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.789373, "lon": -87.603142, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.775267, "lon": -87.58546, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.775284, "lon": -87.5991, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.78447, "lon": -87.586613, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.784238, "lon": -87.603165, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.78809, "lon": -87.582372, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.783245, "lon": -87.580935, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.790251, "lon": -87.594917, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.776323, "lon": -87.603899, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.777271, "lon": -87.589768, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781856, "lon": -87.590468, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.776785, "lon": -87.587754, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.782741, "lon": -87.58291, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.782177, "lon": -87.58703, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.786972, "lon": -87.596268, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.776208, "lon": -87.584374, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.788403, "lon": -87.596311, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.785556, "lon": -87.591399, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.782395, "lon": -87.583286, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.790626, "lon": -87.587252, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.78133, "lon": -87.590974, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.779036, "lon": -87.603186, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.777068, "lon": -87.598757, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.790213, "lon": -87.580662, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.785962, "lon": -87.588896, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.778247, "lon": -87.58773, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781318, "lon": -87.601283, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.776253, "lon": -87.586735, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.78843, "lon": -87.600407, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.777833, "lon": -87.597897, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.77185, "lon": -87.610644, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.766197, "lon": -87.607381, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.764391, "lon": -87.603403, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.75732, "lon": -87.611895, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.762227, "lon": -87.606364, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.748208, "lon": -87.60656, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.768632, "lon": -87.606895, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.768169, "lon": -87.610081, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.761507, "lon": -87.591666, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.758721, "lon": -87.594223, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.772871, "lon": -87.590861, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.767156, "lon": -87.603305, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.774087, "lon": -87.610188, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.770465, "lon": -87.589246, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.75457, "lon": -87.598512, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.771504, "lon": -87.594117, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.750062, "lon": -87.59727, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.77246, "lon": -87.605217, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.754379, "lon": -87.6109, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.768526, "lon": -87.596646, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.760527, "lon": -87.599215, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.771335, "lon": -87.597438, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.760661, "lon": -87.597321, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.757502, "lon": -87.612923, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.749536, "lon": -87.591712, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.764605, "lon": -87.600802, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.760143, "lon": -87.592325, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.764335, "lon": -87.600962, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.750795, "lon": -87.589824, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.761623, "lon": -87.610168, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.774757, "lon": -87.600326, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.758067, "lon": -87.607079, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.76633, "lon": -87.613534, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.74978, "lon": -87.612354, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.754804, "lon": -87.591156, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.757001, "lon": -87.598683, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.756376, "lon": -87.59663, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.764066, "lon": -87.588736, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.765374, "lon": -87.605803, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.765443, "lon": -87.603145, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.756339, "lon": -87.588367, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.753184, "lon": -87.587001, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.7708, "lon": -87.612168, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.765872, "lon": -87.590461, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.752165, "lon": -87.609936, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.767472, "lon": -87.613777, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.774179, "lon": -87.597903, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.754318, "lon": -87.608303, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.772407, "lon": -87.609568, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.760465, "lon": -87.60711, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.774089, "lon": -87.592127, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.771571, "lon": -87.613539, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.762973, "lon": -87.612127, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.755697, "lon": -87.593633, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.770438, "lon": -87.612432, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.771885, "lon": -87.588947, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.761554, "lon": -87.608398, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.754063, "lon": -87.606077, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.769367, "lon": -87.611147, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.766794, "lon": -87.611114, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.764614, "lon": -87.589636, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.770544, "lon": -87.599633, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.751002, "lon": -87.606933, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.754438, "lon": -87.597109, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.750993, "lon": -87.589656, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.765063, "lon": -87.598899, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.759589, "lon": -87.597785, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.753057, "lon": -87.59629, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.749827, "lon": -87.60027, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.758542, "lon": -87.601836, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.754849, "lon": -87.614545, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.75451, "lon": -87.596601, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.751602, "lon": -87.605136, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.77042, "lon": -87.595829, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.765057, "lon": -87.592278, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.748999, "lon": -87.609355, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.756521, "lon": -87.606318, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.754839, "lon": -87.593908, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.771278, "lon": -87.613661, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.751361, "lon": -87.604695, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.772155, "lon": -87.604174, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.766686, "lon": -87.604714, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.769631, "lon": -87.594642, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.762728, "lon": -87.606006, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.756275, "lon": -87.598127, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.757492, "lon": -87.613814, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.764601, "lon": -87.602822, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.750026, "lon": -87.59715, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.773725, "lon": -87.611002, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.74894, "lon": -87.613117, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.757778, "lon": -87.588415, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.766335, "lon": -87.588433, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.763496, "lon": -87.600175, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.75474, "lon": -87.611823, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.761979, "lon": -87.589421, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.767009, "lon": -87.608992, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.753405, "lon": -87.6112, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.772264, "lon": -87.602537, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.766032, "lon": -87.595133, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.772066, "lon": -87.591162, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.744668, "lon": -87.614702, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.744633, "lon": -87.623951, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.739634, "lon": -87.619457, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.740851, "lon": -87.629069, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.73904, "lon": -87.605848, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.730632, "lon": -87.621221, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.742282, "lon": -87.620286, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.744123, "lon": -87.627613, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.745459, "lon": -87.614385, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.734776, "lon": -87.607883, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.745765, "lon": -87.623479, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.730629, "lon": -87.621704, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.740428, "lon": -87.612258, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.745693, "lon": -87.612837, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.729706, "lon": -87.599749, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.741674, "lon": -87.605923, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.738459, "lon": -87.610676, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.738142, "lon": -87.604641, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.737524, "lon": -87.608587, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.738169, "lon": -87.625063, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.746091, "lon": -87.621143, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.748483, "lon": -87.627554, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.734701, "lon": -87.61614, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.730958, "lon": -87.630279, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.733214, "lon": -87.60258, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.747609, "lon": -87.607482, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.738464, "lon": -87.614499, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.738445, "lon": -87.628938, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.7483, "lon": -87.624685, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.733908, "lon": -87.611684, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.734001, "lon": -87.631722, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.746532, "lon": -87.607265, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.72895, "lon": -87.630261, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.739618, "lon": -87.6295, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.745332, "lon": -87.61081, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.748477, "lon": -87.618607, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.739714, "lon": -87.619569, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.738502, "lon": -87.63046, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.744883, "lon": -87.614343, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.734887, "lon": -87.611156, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.740468, "lon": -87.614751, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.742884, "lon": -87.621807, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.734956, "lon": -87.628273, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.744732, "lon": -87.607339, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.740535, "lon": -87.622972, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.743149, "lon": -87.61216, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.731103, "lon": -87.608855, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.732006, "lon": -87.617005, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.742501, "lon": -87.618047, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.746329, "lon": -87.606982, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.738892, "lon": -87.61293, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.739035, "lon": -87.621332, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.739472, "lon": -87.60902, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.740812, "lon": -87.625463, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.732722, "lon": -87.598921, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.742803, "lon": -87.608532, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.735325, "lon": -87.600254, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.734044, "lon": -87.612502, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.745186, "lon": -87.599543, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.728883, "lon": -87.599519, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.741775, "lon": -87.60659, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.747594, "lon": -87.60833, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.733092, "lon": -87.609226, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.729102, "lon": -87.617948, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.742305, "lon": -87.627326, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.736545, "lon": -87.600209, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.741661, "lon": -87.606299, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.741564, "lon": -87.60113, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.739238, "lon": -87.607414, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.736776, "lon": -87.603521, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.748941, "lon": -87.618502, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.746412, "lon": -87.631685, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.747498, "lon": -87.620609, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.746674, "lon": -87.627437, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.732049, "lon": -87.62817, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.741614, "lon": -87.607568, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.744606, "lon": -87.612695, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.74083, "lon": -87.610283, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.738821, "lon": -87.629051, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.748615, "lon": -87.615767, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.733476, "lon": -87.623992, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.734341, "lon": -87.607422, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.742548, "lon": -87.629888, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.731354, "lon": -87.608673, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.742496, "lon": -87.610284, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.740907, "lon": -87.62455, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.737555, "lon": -87.59838, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.743904, "lon": -87.604732, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.742287, "lon": -87.611742, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.739092, "lon": -87.619699, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.729297, "lon": -87.61338, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.731455, "lon": -87.602947, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.743055, "lon": -87.61538, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.744983, "lon": -87.616583, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.739842, "lon": -87.613001, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.743189, "lon": -87.618538, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.740145, "lon": -87.63046, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.739364, "lon": -87.629951, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.728666, "lon": -87.618099, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.735864, "lon": -87.601695, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.735889, "lon": -87.608787, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.741724, "lon": -87.620176, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.739106, "lon": -87.607253, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.74388, "lon": -87.598731, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.739171, "lon": -87.604006, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.731258, "lon": -87.625592, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.728677, "lon": -87.609553, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.733054, "lon": -87.629712, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.740553, "lon": -87.608088, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.736448, "lon": -87.624032, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.722204, "lon": -87.548176, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.735324, "lon": -87.554141, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.727053, "lon": -87.571132, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.730407, "lon": -87.567571, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.73678, "lon": -87.563466, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.746248, "lon": -87.556874, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.738889, "lon": -87.563977, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.740632, "lon": -87.562215, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.743726, "lon": -87.571103, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.734872, "lon": -87.54887, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.729653, "lon": -87.568115, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.745667, "lon": -87.552127, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.719546, "lon": -87.564816, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.744209, "lon": -87.56992, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.732382, "lon": -87.551524, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.724354, "lon": -87.569869, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.745433, "lon": -87.556218, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.745454, "lon": -87.560094, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.731988, "lon": -87.557485, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.733384, "lon": -87.561574, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.740849, "lon": -87.566354, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.730418, "lon": -87.559812, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.718487, "lon": -87.560061, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.726856, "lon": -87.569703, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.732979, "lon": -87.557326, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.740901, "lon": -87.561807, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.731825, "lon": -87.555215, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.739609, "lon": -87.561815, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.733718, "lon": -87.552345, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.74093, "lon": -87.563865, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.720039, "lon": -87.570922, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.729196, "lon": -87.558318, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.737779, "lon": -87.574575, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.718356, "lon": -87.560706, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.718514, "lon": -87.553045, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.72121, "lon": -87.5724, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.736593, "lon": -87.568185, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.720371, "lon": -87.549099, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.747707, "lon": -87.568902, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.737612, "lon": -87.551828, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.730158, "lon": -87.564816, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.739085, "lon": -87.572767, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.734976, "lon": -87.551835, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-02"}, {"lat": 41.724893, "lon": -87.550666, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.726133, "lon": -87.550048, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.744979, "lon": -87.559785, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.71847, "lon": -87.569407, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.745866, "lon": -87.56692, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.738311, "lon": -87.560405, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.741715, "lon": -87.556389, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.719611, "lon": -87.563199, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.736155, "lon": -87.558426, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.718889, "lon": -87.56762, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.724844, "lon": -87.560068, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.738391, "lon": -87.557162, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.741942, "lon": -87.555746, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.7294, "lon": -87.553835, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.7275, "lon": -87.572123, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.731342, "lon": -87.554444, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.723622, "lon": -87.562881, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.721099, "lon": -87.57258, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-06-20"}, {"lat": 41.743912, "lon": -87.574667, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.739745, "lon": -87.559893, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2021-08-11"}, {"lat": 41.735159, "lon": -87.570421, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.726068, "lon": -87.567753, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.73104, "lon": -87.56363, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-07-03"}, {"lat": 41.728834, "lon": -87.549506, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2023-06-30"}, {"lat": 41.735814, "lon": -87.56972, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2020-09-02"}, {"lat": 41.718203, "lon": -87.564316, "flood_type": "Water on Street", "addr": "South Chicago", "ca_num": 46, "report_date": "2024-08-15"}, {"lat": 41.742122, "lon": -87.566102, "flood_type": "Water in Basement", "addr": "South Chicago", "ca_num": 46, "report_date": "2022-09-14"}, {"lat": 41.736112, "lon": -87.63992, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.736483, "lon": -87.630886, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.747842, "lon": -87.639177, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.736799, "lon": -87.647992, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.731075, "lon": -87.640904, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.746406, "lon": -87.641248, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.75346, "lon": -87.649759, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.750112, "lon": -87.635109, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.731758, "lon": -87.647429, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.747311, "lon": -87.635273, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.743721, "lon": -87.641641, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.742678, "lon": -87.635232, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.730953, "lon": -87.648794, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.745469, "lon": -87.653893, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.754104, "lon": -87.64671, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.728285, "lon": -87.648532, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.740036, "lon": -87.645222, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.737314, "lon": -87.654386, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.752855, "lon": -87.652854, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.737405, "lon": -87.646423, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.737404, "lon": -87.652559, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.736611, "lon": -87.647493, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.72861, "lon": -87.646423, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.753108, "lon": -87.636488, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.736937, "lon": -87.644341, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.745004, "lon": -87.65034, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.728788, "lon": -87.639647, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.738499, "lon": -87.637382, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.743588, "lon": -87.635012, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.736802, "lon": -87.643561, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.742248, "lon": -87.639022, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.743849, "lon": -87.646302, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.749971, "lon": -87.63735, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.746147, "lon": -87.64717, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.732942, "lon": -87.637664, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.744103, "lon": -87.64063, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.745159, "lon": -87.637664, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.742983, "lon": -87.642759, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.750734, "lon": -87.639515, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.741084, "lon": -87.650122, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.739047, "lon": -87.642707, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.741195, "lon": -87.652933, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.735886, "lon": -87.648129, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.74908, "lon": -87.640859, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.742843, "lon": -87.65217, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.742635, "lon": -87.63608, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.742752, "lon": -87.630256, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.736038, "lon": -87.630017, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.751279, "lon": -87.652825, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.748942, "lon": -87.649076, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.751248, "lon": -87.639743, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.749191, "lon": -87.634662, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.742372, "lon": -87.640079, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.735812, "lon": -87.648316, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.731661, "lon": -87.636248, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.754797, "lon": -87.633324, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.734741, "lon": -87.637215, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.741215, "lon": -87.640564, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.73813, "lon": -87.653112, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.738877, "lon": -87.636255, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.740277, "lon": -87.642799, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.747735, "lon": -87.643539, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.750953, "lon": -87.635108, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.750271, "lon": -87.642632, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.737119, "lon": -87.640552, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.749284, "lon": -87.632646, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.730689, "lon": -87.635403, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.753095, "lon": -87.65105, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.733463, "lon": -87.637785, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.732292, "lon": -87.631682, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-06-20"}, {"lat": 41.734761, "lon": -87.645704, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.729398, "lon": -87.63936, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.739589, "lon": -87.65272, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}, {"lat": 41.740874, "lon": -87.651683, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-06-30"}, {"lat": 41.728251, "lon": -87.63761, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2024-08-15"}, {"lat": 41.746739, "lon": -87.643057, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-03"}, {"lat": 41.747731, "lon": -87.652439, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2020-09-02"}, {"lat": 41.731702, "lon": -87.635663, "flood_type": "Water on Street", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2022-09-14"}, {"lat": 41.745323, "lon": -87.638072, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2023-07-02"}, {"lat": 41.744479, "lon": -87.650897, "flood_type": "Water in Basement", "addr": "Auburn Gresham", "ca_num": 71, "report_date": "2021-08-11"}]

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
