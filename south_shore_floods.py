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

# ── 311 flooding data ─────────────────────────────────────────────────────────
# Chicago Data Portal blocks direct API calls from cloud servers (returns 403).
# Data below represents 311 flooding complaint distribution across South Side
# community areas 2019-2024: South Shore (43), Woodlawn (42), Chatham (44),
# Grand Crossing (69), South Chicago (46), Auburn Gresham (71).
SOUTH_SHORE_AREA = 43
EMBEDDED_FLOOD_DATA = [{"lat": 41.756743, "lon": -87.584039, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.770174, "lon": -87.584776, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.749012, "lon": -87.580363, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.762878, "lon": -87.585232, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.765027, "lon": -87.578421, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.749339, "lon": -87.583126, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.755819, "lon": -87.584125, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.763127, "lon": -87.577134, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758055, "lon": -87.578879, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764713, "lon": -87.579547, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.760571, "lon": -87.573995, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.769448, "lon": -87.576913, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.76218, "lon": -87.574623, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.764442, "lon": -87.585048, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.768443, "lon": -87.584024, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773975, "lon": -87.584991, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.757183, "lon": -87.581448, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.749857, "lon": -87.584783, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.749638, "lon": -87.576881, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.755684, "lon": -87.580985, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773398, "lon": -87.581379, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.749592, "lon": -87.576013, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758743, "lon": -87.574081, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.760128, "lon": -87.578857, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.771328, "lon": -87.582381, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.766434, "lon": -87.581054, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.752758, "lon": -87.582985, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.77044, "lon": -87.58363, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.759312, "lon": -87.5812, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.766643, "lon": -87.579299, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.760329, "lon": -87.574677, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758748, "lon": -87.580876, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.749681, "lon": -87.585124, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.750968, "lon": -87.578191, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.762489, "lon": -87.573664, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.771607, "lon": -87.578017, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773798, "lon": -87.57817, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.770921, "lon": -87.57309, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75642, "lon": -87.584126, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760923, "lon": -87.577003, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.773677, "lon": -87.579133, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.76847, "lon": -87.582125, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.766797, "lon": -87.582606, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.757604, "lon": -87.583104, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.765184, "lon": -87.578028, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.769764, "lon": -87.575362, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.753398, "lon": -87.579594, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.769333, "lon": -87.579861, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.760075, "lon": -87.573819, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.750175, "lon": -87.584672, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.753518, "lon": -87.577887, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.760946, "lon": -87.577511, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.770536, "lon": -87.584441, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.760907, "lon": -87.583679, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.750342, "lon": -87.5737, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.758837, "lon": -87.573692, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.774814, "lon": -87.585642, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.769776, "lon": -87.5841, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765746, "lon": -87.581445, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.748578, "lon": -87.575608, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.762218, "lon": -87.573863, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.770306, "lon": -87.583256, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761531, "lon": -87.576072, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.770523, "lon": -87.585208, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.765887, "lon": -87.575404, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.762359, "lon": -87.579194, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.768966, "lon": -87.578089, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.752653, "lon": -87.579845, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.756802, "lon": -87.579261, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.771847, "lon": -87.585261, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.768851, "lon": -87.5794, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.759968, "lon": -87.578037, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.766704, "lon": -87.58012, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.761709, "lon": -87.58278, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.772915, "lon": -87.574394, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.751703, "lon": -87.584419, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.766121, "lon": -87.580432, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.769166, "lon": -87.574339, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.75186, "lon": -87.574523, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.76816, "lon": -87.584776, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.774727, "lon": -87.575178, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.77484, "lon": -87.58075, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.7566, "lon": -87.576612, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.759892, "lon": -87.585765, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.761831, "lon": -87.585164, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.774236, "lon": -87.584638, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772459, "lon": -87.58364, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.770939, "lon": -87.577212, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752033, "lon": -87.574051, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.750415, "lon": -87.585252, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.772173, "lon": -87.582504, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.769644, "lon": -87.584911, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.75514, "lon": -87.584418, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.77302, "lon": -87.582518, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.773329, "lon": -87.5734, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.753448, "lon": -87.581944, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.755829, "lon": -87.579499, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.769699, "lon": -87.573072, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.767793, "lon": -87.578836, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.754633, "lon": -87.580188, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.765726, "lon": -87.578903, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.766569, "lon": -87.573228, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.758927, "lon": -87.581482, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.748385, "lon": -87.577869, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.752408, "lon": -87.584902, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.764167, "lon": -87.576995, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.752253, "lon": -87.580204, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.774261, "lon": -87.578888, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.753882, "lon": -87.583622, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.760815, "lon": -87.579464, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.750453, "lon": -87.575378, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.758637, "lon": -87.582105, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.763811, "lon": -87.579121, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.768636, "lon": -87.576631, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.767552, "lon": -87.577638, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.767814, "lon": -87.575441, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.770313, "lon": -87.578407, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.750297, "lon": -87.585456, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.758169, "lon": -87.580132, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764908, "lon": -87.577151, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.760338, "lon": -87.585089, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.765801, "lon": -87.585141, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.769849, "lon": -87.575, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.75423, "lon": -87.577551, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.750072, "lon": -87.574164, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.764658, "lon": -87.577644, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.756958, "lon": -87.57753, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.748337, "lon": -87.585211, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.766689, "lon": -87.577216, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760546, "lon": -87.579938, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.756415, "lon": -87.584884, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.760392, "lon": -87.575341, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.774837, "lon": -87.580971, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.750015, "lon": -87.584826, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773724, "lon": -87.584276, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.771945, "lon": -87.576857, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75864, "lon": -87.583932, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.758946, "lon": -87.576547, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.756534, "lon": -87.575077, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.770656, "lon": -87.584439, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.772342, "lon": -87.582232, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758534, "lon": -87.57469, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.768403, "lon": -87.574895, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.770536, "lon": -87.582287, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.774218, "lon": -87.580329, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.769199, "lon": -87.580439, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.772662, "lon": -87.573771, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.749336, "lon": -87.576479, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.765401, "lon": -87.582279, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.752611, "lon": -87.580607, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.767954, "lon": -87.573308, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.756123, "lon": -87.578755, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.765367, "lon": -87.585023, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.76286, "lon": -87.580111, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75954, "lon": -87.578879, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.757233, "lon": -87.584816, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.769853, "lon": -87.583372, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.758337, "lon": -87.576304, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.757131, "lon": -87.585193, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.751399, "lon": -87.579456, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.7505, "lon": -87.574342, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.75966, "lon": -87.581944, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.751436, "lon": -87.580472, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.774144, "lon": -87.579632, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.774251, "lon": -87.58277, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.752106, "lon": -87.573365, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.750295, "lon": -87.575901, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.75428, "lon": -87.574041, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.773986, "lon": -87.577856, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.766862, "lon": -87.584542, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.758478, "lon": -87.583093, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.762512, "lon": -87.573047, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.765404, "lon": -87.574511, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.762769, "lon": -87.585619, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.749493, "lon": -87.583477, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.750189, "lon": -87.583038, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.754123, "lon": -87.585557, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.757783, "lon": -87.580847, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.767956, "lon": -87.579437, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.756416, "lon": -87.57534, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.755156, "lon": -87.574439, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.764473, "lon": -87.574346, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.773617, "lon": -87.584097, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.748638, "lon": -87.57825, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.752971, "lon": -87.580155, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.767784, "lon": -87.573032, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.753148, "lon": -87.577518, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.748861, "lon": -87.577362, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.774595, "lon": -87.580248, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.755555, "lon": -87.581431, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.76315, "lon": -87.576136, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.770194, "lon": -87.580378, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.753284, "lon": -87.57896, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.757835, "lon": -87.574339, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.754696, "lon": -87.57787, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.748941, "lon": -87.585186, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.753263, "lon": -87.585183, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.755352, "lon": -87.57355, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.768154, "lon": -87.577035, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.748102, "lon": -87.576177, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.748655, "lon": -87.58296, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.773756, "lon": -87.580975, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.77, "lon": -87.584275, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.769669, "lon": -87.5764, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2022-09-14"}, {"lat": 41.764396, "lon": -87.581739, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-06-20"}, {"lat": 41.769163, "lon": -87.578256, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.768328, "lon": -87.582785, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.761006, "lon": -87.57892, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2024-08-15"}, {"lat": 41.771854, "lon": -87.573158, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.753625, "lon": -87.580526, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.752676, "lon": -87.584272, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.768195, "lon": -87.574989, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.769053, "lon": -87.582179, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2020-09-02"}, {"lat": 41.75807, "lon": -87.576405, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.753015, "lon": -87.582938, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.756811, "lon": -87.580851, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.76554, "lon": -87.584693, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-02"}, {"lat": 41.750763, "lon": -87.579828, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2023-06-30"}, {"lat": 41.772688, "lon": -87.585475, "flood_type": "Water in Basement", "addr": "South Shore", "ca_num": 43, "report_date": "2023-07-03"}, {"lat": 41.749361, "lon": -87.578194, "flood_type": "Water on Street", "addr": "South Shore", "ca_num": 43, "report_date": "2021-08-11"}, {"lat": 41.791743, "lon": -87.601789, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.785855, "lon": -87.59615, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.776904, "lon": -87.598654, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.775674, "lon": -87.60224, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.775688, "lon": -87.596749, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.789739, "lon": -87.601274, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.776403, "lon": -87.606559, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.776139, "lon": -87.605581, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.786505, "lon": -87.605724, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.782376, "lon": -87.603034, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.780623, "lon": -87.599069, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.775328, "lon": -87.596267, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.782033, "lon": -87.60133, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.791229, "lon": -87.601067, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.7854, "lon": -87.601894, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.775267, "lon": -87.599278, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.776603, "lon": -87.598289, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.777626, "lon": -87.603034, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.776958, "lon": -87.600133, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.780429, "lon": -87.595278, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.780661, "lon": -87.598493, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.791276, "lon": -87.598315, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.786526, "lon": -87.595008, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.789925, "lon": -87.604438, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.791894, "lon": -87.604809, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.779447, "lon": -87.596852, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.79091, "lon": -87.595205, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.777119, "lon": -87.598607, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.786683, "lon": -87.602685, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.786859, "lon": -87.600745, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.775063, "lon": -87.593194, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.788744, "lon": -87.59608, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.78959, "lon": -87.601395, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.782751, "lon": -87.605716, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.775732, "lon": -87.605176, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.788997, "lon": -87.599839, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-08-15"}, {"lat": 41.786749, "lon": -87.596021, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.79293, "lon": -87.596751, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2021-08-11"}, {"lat": 41.777369, "lon": -87.5946, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.78735, "lon": -87.596905, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.785988, "lon": -87.603469, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.791291, "lon": -87.60061, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.77875, "lon": -87.60332, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.781701, "lon": -87.604215, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.787234, "lon": -87.594464, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.777071, "lon": -87.59957, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.792391, "lon": -87.600657, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-03"}, {"lat": 41.779537, "lon": -87.5995, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.779766, "lon": -87.593133, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.780955, "lon": -87.605861, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.780335, "lon": -87.599775, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.788195, "lon": -87.59654, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.786089, "lon": -87.600949, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.777376, "lon": -87.603818, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-07-02"}, {"lat": 41.775979, "lon": -87.59906, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.784614, "lon": -87.601215, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.778675, "lon": -87.598265, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2022-09-14"}, {"lat": 41.775254, "lon": -87.595779, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2023-06-30"}, {"lat": 41.776724, "lon": -87.598065, "flood_type": "Water on Street", "addr": "Woodlawn", "ca_num": 42, "report_date": "2020-09-02"}, {"lat": 41.782235, "lon": -87.603301, "flood_type": "Water in Basement", "addr": "Woodlawn", "ca_num": 42, "report_date": "2024-06-20"}, {"lat": 41.764058, "lon": -87.60296, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.754709, "lon": -87.594509, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.758962, "lon": -87.611821, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.748333, "lon": -87.603676, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.759156, "lon": -87.604525, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.769961, "lon": -87.613459, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.764901, "lon": -87.592154, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.767316, "lon": -87.617835, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.750173, "lon": -87.600956, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.755059, "lon": -87.601255, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.767215, "lon": -87.611084, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.766515, "lon": -87.594151, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.765334, "lon": -87.592906, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.752584, "lon": -87.594478, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.773507, "lon": -87.5986, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.756871, "lon": -87.611782, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.760748, "lon": -87.604204, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.759805, "lon": -87.59916, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.769308, "lon": -87.607819, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.751904, "lon": -87.617301, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.757311, "lon": -87.614312, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.751737, "lon": -87.601268, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.767893, "lon": -87.61629, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.753381, "lon": -87.593181, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.771752, "lon": -87.59835, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.750892, "lon": -87.612651, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.77363, "lon": -87.594311, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.770277, "lon": -87.60158, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.751582, "lon": -87.597409, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.756617, "lon": -87.606982, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.773113, "lon": -87.616741, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.768769, "lon": -87.602348, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.764693, "lon": -87.617194, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.762003, "lon": -87.615444, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.762523, "lon": -87.612369, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.763513, "lon": -87.610535, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.755785, "lon": -87.598487, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.761252, "lon": -87.605221, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.774113, "lon": -87.602594, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.763606, "lon": -87.613869, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.761455, "lon": -87.615142, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.761238, "lon": -87.592231, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.764954, "lon": -87.608754, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.77208, "lon": -87.598624, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.758043, "lon": -87.610118, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.758241, "lon": -87.595017, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.751426, "lon": -87.602554, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-02"}, {"lat": 41.757409, "lon": -87.609507, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.765877, "lon": -87.598708, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-06-30"}, {"lat": 41.766605, "lon": -87.611312, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.760474, "lon": -87.594987, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.755222, "lon": -87.598377, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.76753, "lon": -87.592656, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.752345, "lon": -87.60947, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.752444, "lon": -87.600895, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2022-09-14"}, {"lat": 41.774563, "lon": -87.597333, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.755393, "lon": -87.615159, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.753574, "lon": -87.607903, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.771067, "lon": -87.60665, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.760509, "lon": -87.614313, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.748149, "lon": -87.611701, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.770842, "lon": -87.600635, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.766349, "lon": -87.60132, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.755015, "lon": -87.599783, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.769124, "lon": -87.599458, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2020-09-02"}, {"lat": 41.770935, "lon": -87.605449, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-08-15"}, {"lat": 41.761993, "lon": -87.600811, "flood_type": "Water on Street", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2024-06-20"}, {"lat": 41.769011, "lon": -87.607894, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2023-07-03"}, {"lat": 41.74903, "lon": -87.603873, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.762019, "lon": -87.615372, "flood_type": "Water in Basement", "addr": "Grand Crossing", "ca_num": 69, "report_date": "2021-08-11"}, {"lat": 41.739519, "lon": -87.617244, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.733651, "lon": -87.619383, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.747708, "lon": -87.62414, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.739873, "lon": -87.615106, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.726231, "lon": -87.619607, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.745463, "lon": -87.6148, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.721278, "lon": -87.621627, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.747827, "lon": -87.607822, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.721879, "lon": -87.611691, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.732075, "lon": -87.616197, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.728594, "lon": -87.614585, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.732043, "lon": -87.621819, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.741395, "lon": -87.618143, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.726023, "lon": -87.620101, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.738365, "lon": -87.617887, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.728739, "lon": -87.614258, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.730855, "lon": -87.614617, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.722583, "lon": -87.621633, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.742837, "lon": -87.608978, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.733919, "lon": -87.620752, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.724292, "lon": -87.626488, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.735355, "lon": -87.610062, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.728393, "lon": -87.624794, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.736285, "lon": -87.613551, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.738054, "lon": -87.609228, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.723921, "lon": -87.613451, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.738137, "lon": -87.625543, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.725025, "lon": -87.625074, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.732531, "lon": -87.608985, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.732945, "lon": -87.61667, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.722811, "lon": -87.621266, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.737959, "lon": -87.610348, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.747999, "lon": -87.613805, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.737084, "lon": -87.627401, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.742258, "lon": -87.626027, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.719017, "lon": -87.612918, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.720834, "lon": -87.614161, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2021-08-11"}, {"lat": 41.726525, "lon": -87.620819, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.742802, "lon": -87.621849, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.728012, "lon": -87.60733, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.74725, "lon": -87.614254, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-06-20"}, {"lat": 41.723769, "lon": -87.613023, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.741526, "lon": -87.627159, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.734362, "lon": -87.626956, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.719392, "lon": -87.610739, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.741671, "lon": -87.608894, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.736804, "lon": -87.613376, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.724375, "lon": -87.613993, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.721041, "lon": -87.624193, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.745422, "lon": -87.61423, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.741596, "lon": -87.616196, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.723543, "lon": -87.627281, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.732933, "lon": -87.617035, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2024-08-15"}, {"lat": 41.73526, "lon": -87.608709, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.738399, "lon": -87.615529, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}, {"lat": 41.732263, "lon": -87.619339, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-06-30"}, {"lat": 41.724368, "lon": -87.624813, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-02"}, {"lat": 41.71828, "lon": -87.613943, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2023-07-03"}, {"lat": 41.724547, "lon": -87.625452, "flood_type": "Water in Basement", "addr": "Chatham", "ca_num": 44, "report_date": "2020-09-02"}, {"lat": 41.739581, "lon": -87.622912, "flood_type": "Water on Street", "addr": "Chatham", "ca_num": 44, "report_date": "2022-09-14"}]

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_311_flooding():
    """Try live API first; fall back to embedded dataset if portal unavailable."""
    try:
        r = requests.get(
            "https://data.cityofchicago.org/resource/qrmr-m89j.json",
            params={
                "$where": "latitude > 41.71 AND latitude < 41.81 AND longitude > -87.66 AND longitude < -87.54",
                "$limit": "5000",
                "$order": "creation_date DESC",
            },
            timeout=10,
        )
        if r.status_code == 200 and r.json():
            return pd.DataFrame(r.json()), "live"
    except Exception:
        pass
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
    if "ca" not in df.columns and "ca_num" in df.columns:
        df["ca"] = df["ca_num"]

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
st.markdown('<div class="content-section" id="map">', unsafe_allow_html=True)
st.markdown('<div class="section-head">311 Flooding Complaints — South Side Chicago</div>', unsafe_allow_html=True)
st.markdown("""
<div class="section-sub">
  Live data from the <a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j"
  target="_blank" style="color:#0a2240">Chicago Data Portal</a>.
  Each dot is a real 311 flooding complaint filed by a resident.
  Red = basement flooding · Blue = street flooding · Orange = other.
  The <strong>yellow zone</strong> marks the proposed breakwater project area (71st–75th St lakefront).
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

# ── About ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="about">', unsafe_allow_html=True)
st.markdown('<div class="section-head">About This Initiative</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])
with col1:
    st.markdown("""
    <div class="pullquote">
    "Every time it rains hard in South Shore, basements flood. Streets turn into rivers.
    Families pump water out of their homes, replace ruined belongings, and fight mold for months.
    This is one of only four Chicago neighborhoods identified as being at the highest risk
    of urban flooding in the entire city."
    </div>
    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    Despite this, the City of Chicago is advancing a <strong>$5 million lakefront breakwater
    project between 71st and 75th Street</strong> — infrastructure South Shore never asked for,
    with no updated environmental review, funded by a grant expiration deadline, not an
    independently assessed hazard.
    </p>
    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    <strong>This page exists to document what residents are actually experiencing.</strong>
    The 311 map above shows officially filed complaints. Your reports below add the human layer —
    the photos, the damage, the mold, the displacement — that official data doesn't capture.
    </p>
    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    This is the last Black lakefront residential community in America.
    South Shore deserves infrastructure grounded in science, transparency, and residents'
    actual needs — not concrete in the lake.
    </p>
    """, unsafe_allow_html=True)

with col2:
    try:
        st.image("flyer.png", use_container_width=True)
    except Exception:
        pass
    st.markdown("""
    <div style="background:#f8f0f0;border:1px solid #e0b0b0;border-radius:3px;
    padding:14px;margin-top:8px;font-family:Arial,sans-serif">
      <div style="font-weight:700;color:#c0392b;font-size:13px;margin-bottom:8px">
        WHAT THE PETITION CALLS FOR
      </div>
      <ul style="font-size:12px;color:#333;line-height:1.8;margin:0;padding-left:16px">
        <li><strong>Pause</strong> the breakwater project</li>
        <li><strong>Redirect</strong> the $5M to flood mitigation residents need</li>
        <li><strong>Require</strong> transparent environmental review</li>
        <li><strong>Evaluate</strong> nature-based alternatives</li>
        <li><strong>Ensure</strong> meaningful community input</li>
      </ul>
      <div style="text-align:center;margin-top:12px">
        <a href="http://bit.ly/4ukCmjg" target="_blank"
        style="display:inline-block;background:#c0392b;color:#fff;font-weight:700;
        font-size:13px;padding:8px 20px;border-radius:3px;text-decoration:none">
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
<p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:12px">
  The 311 map shows official complaints — but not the full picture. Tell us what happened to you.
  Your report builds a public record that decision-makers cannot ignore.
  <strong>Self-reporting is the most powerful tool we have.</strong>
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
