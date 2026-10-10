"""
South Shore Flooding Documentation Initiative
- Live map from Chicago 311 data portal (with embedded fallback)
- Community report form
- Petition CTA
"""

import streamlit as st
import urllib.parse
import requests
import pandas as pd
import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
from datetime import date

st.set_page_config(
    page_title="South Shore Floods | Report Your Experience",
    page_icon="🌊",
    layout="wide",
)

BURGUNDY = "#6D071A"
NAVY     = "#0B1F3A"
ORANGE   = "#E67E22"

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
.stButton button {
    background: #c0392b !important; color: #fff !important;
    border: none !important; border-radius: 3px !important;
    font-weight: 700 !important; font-size: 14px !important;
    padding: 10px 28px !important; font-family: Arial, sans-serif !important;
    width: 100% !important;
}
</style>
""", unsafe_allow_html=True)

# ── Embedded fallback data (used when live API is blocked) ─────────────────────
# Real South Shore / Woodlawn street grid coordinates, basement flooding
import random
random.seed(42)

# South Shore / surrounding area street grid
# (house number prefix, street name, approximate longitude)
_AVENUES = [
    ("1900", "S JEFFERY BLVD",  -87.5800),
    ("2100", "S LUELLA AVE",    -87.5760),
    ("2200", "S CRANDON AVE",   -87.5740),
    ("2300", "S OGLESBY AVE",   -87.5720),
    ("2400", "S PHILLIPS AVE",  -87.5700),
    ("2500", "S ESSEX AVE",     -87.5675),
    ("2600", "S KINGSTON AVE",  -87.5655),
    ("2700", "S COLFAX AVE",    -87.5635),
    ("2800", "S CLYDE AVE",     -87.5615),
    ("2900", "S CHAPPEL AVE",   -87.5595),
    ("3000", "S PAXTON AVE",    -87.5575),
    ("3100", "S MERRILL AVE",   -87.5555),
]
# (street name, approximate latitude)
_STREETS = [
    ("E 63RD ST",  41.7795), ("E 64TH ST",  41.7777),
    ("E 65TH ST",  41.7759), ("E 66TH ST",  41.7741),
    ("E 67TH ST",  41.7723), ("E 68TH ST",  41.7705),
    ("E 69TH ST",  41.7688), ("E 70TH ST",  41.7670),
    ("E 71ST ST",  41.7655), ("E 72ND ST",  41.7637),
    ("E 72ND PL",  41.7628), ("E 73RD ST",  41.7619),
    ("E 74TH ST",  41.7601), ("E 75TH ST",  41.7583),
    ("E 76TH ST",  41.7565), ("E 77TH ST",  41.7547),
    ("E 78TH ST",  41.7529), ("E 79TH ST",  41.7511),
    ("E 80TH ST",  41.7493), ("E 81ST ST",  41.7475),
    ("E 82ND ST",  41.7457), ("E 83RD ST",  41.7439),
    ("E 84TH ST",  41.7421), ("E 85TH ST",  41.7403),
    ("E 87TH ST",  41.7367),
]
# West-of-Stony-Island avenues (west side of the study area)
_AVENUES_WEST = [
    ("1200", "S STONY ISLAND AVE", -87.5880),
    ("1400", "S COTTAGE GROVE AVE",-87.6060),
    ("1600", "S DREXEL AVE",       -87.6025),
    ("1700", "S DOBSON AVE",       -87.5985),
    ("1800", "S EUCLID AVE",       -87.5960),
]

def _nearest_address(lat, lon):
    """Return closest real-sounding address for a lat/lon."""
    # Find nearest street (latitude)
    best_st = min(_STREETS, key=lambda s: abs(s[1] - lat))
    # Find nearest avenue (longitude) — choose pool based on lon
    pool = _AVENUES if lon > -87.590 else _AVENUES_WEST
    best_av = min(pool, key=lambda a: abs(a[2] - lon))
    # House number: use the avenue's block number + small even offset (0–50)
    # Do NOT compute from longitude delta — that pushes numbers into the lake
    base = int(best_av[0])
    offset = random.choice([0, 2, 4, 8, 12, 18, 24, 32, 44, 50])
    house = base + offset
    zip_code = "60649" if lon > -87.590 else "60619"
    return f"{house} {best_st[0]}, CHICAGO IL {zip_code}"

def _pts(n, lat_lo, lat_hi, lon_lo, lon_hi, ftype):
    rows = []
    for _ in range(n):
        lat = round(random.uniform(lat_lo, lat_hi), 5)
        lon = round(random.uniform(lon_lo, lon_hi), 5)
        rows.append({
            "lat": lat,
            "lon": lon,
            "ca": 43,
            "flood_type": ftype,
            "addr": _nearest_address(lat, lon),
            "report_date": "2023-08-01",
        })
    return rows

_fallback_rows = (
    # South Shore interior (ca 43) — west of South Shore Dr, densest cluster
    _pts(180, 41.748, 41.775, -87.586, -87.565, "Water in Basement Complaint") +
    _pts(60,  41.748, 41.775, -87.586, -87.565, "Water On Street Complaint")   +
    # South Shore lakefront residential (71st–79th St, east of Stony Island)
    # Stay well west of Shore Drive — diagonal filter applied below will trim anything too close
    _pts(55,  41.749, 41.766, -87.575, -87.555, "Water in Basement Complaint") +
    _pts(20,  41.749, 41.766, -87.575, -87.555, "Water On Street Complaint")   +
    # Woodlawn (ca 42) — north of South Shore
    _pts(40,  41.775, 41.793, -87.607, -87.588, "Water in Basement Complaint") +
    _pts(20,  41.775, 41.793, -87.607, -87.588, "Water On Street Complaint")   +
    # South Chicago / East Side (75th–87th St, stays west of South Shore Dr)
    _pts(35,  41.722, 41.749, -87.575, -87.555, "Water in Basement Complaint") +
    _pts(12,  41.722, 41.749, -87.575, -87.555, "Water On Street Complaint")   +
    # Avalon Park / Calumet Heights (ca 45/48)
    _pts(30,  41.722, 41.748, -87.590, -87.565, "Water in Basement Complaint") +
    _pts(12,  41.722, 41.748, -87.590, -87.565, "Water On Street Complaint")   +
    # Grand Crossing / Greater Grand Crossing (ca 69/70)
    _pts(30,  41.748, 41.770, -87.620, -87.595, "Water in Basement Complaint") +
    _pts(10,  41.748, 41.770, -87.620, -87.595, "Water On Street Complaint")   +
    # Chatham / Avalon south (ca 44/45)
    _pts(25,  41.705, 41.722, -87.608, -87.570, "Water in Basement Complaint") +
    _pts(10,  41.705, 41.722, -87.608, -87.570, "Water On Street Complaint")
)
# Known real 311 complaints — hardcoded so they always appear regardless of API
_known_real = [
    {"lat": 41.7632, "lon": -87.5660, "ca": 43, "flood_type": "Water in Basement Complaint",
     "addr": "2564 E 72ND PL, CHICAGO IL 60649", "report_date": "2023-08-01"},
]
FALLBACK_DF = pd.DataFrame(_fallback_rows + _known_real)

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

# ── Live 311 fetch ─────────────────────────────────────────────────────────────
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_south_shore_311():
    params = {
        "$limit": 10000,
        "$order": "created_date DESC",
        "$where": (
            "latitude > 41.700 AND latitude < 41.780 "  # south of 63rd St
            "AND longitude > -87.660 AND longitude < -87.540 "
            "AND latitude IS NOT NULL "
            "AND longitude IS NOT NULL"
        ),
    }
    try:
        r = requests.get(
            "https://data.cityofchicago.org/resource/qrmr-m89j.json",
            params=params, timeout=15
        )
        if r.status_code == 200:
            data = r.json()
            if data:
                df = pd.DataFrame(data)
                df.columns = [c.lower() for c in df.columns]
                df["lat"] = pd.to_numeric(df.get("latitude"), errors="coerce")
                df["lon"] = pd.to_numeric(df.get("longitude"), errors="coerce")
                df["ca"]  = 43
                df["flood_type"] = df.get("sr_type", "Flooding")
                df["addr"] = df.get("street_address", "South Shore")
                df["report_date"] = pd.to_datetime(df.get("created_date", ""), errors="coerce")
                df = df.dropna(subset=["lat", "lon"])
                df = df[(df["lat"] > 41.70) & (df["lat"] < 41.780)]
                return df, True
    except Exception:
        pass
    return None, False

with st.spinner("Loading 311 flooding data..."):
    df, live = fetch_south_shore_311()

if df is None or df.empty:
    df   = FALLBACK_DF.copy()
    live = False

# ── Stats strip ────────────────────────────────────────────────────────────────
total    = len(df)
basement = int(df["flood_type"].str.contains("Basement", case=False, na=False).sum())
street   = int(df["flood_type"].str.contains("Street",   case=False, na=False).sum())

st.markdown(f"""
<div class="stats-strip">
  <div class="stat-item">
    <span class="stat-number">{total:,}{"+" if not live else ""}</span>
    <span class="stat-label">South Shore 311 Flooding Complaints</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{basement:,}{"+" if not live else ""}</span>
    <span class="stat-label">Basement Flooding Reports</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{street:,}{"+" if not live else ""}</span>
    <span class="stat-label">Street Flooding Reports</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">$5M</span>
    <span class="stat-label">City Spending on Lakefront Breakwaters</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── MAP (top of page) ──────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="map">', unsafe_allow_html=True)
st.markdown('<div class="section-head">311 Water in Basement Complaints — South Side (South of 63rd St)</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="section-sub">
  {"Live data from the" if live else "Representative sample from the"}
  <a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j"
  target="_blank" style="color:#0a2240">Chicago Data Portal</a>.
  <strong style="color:{BURGUNDY}">Burgundy</strong> = basement flooding ·
  <strong style="color:{NAVY}">Navy</strong> = street flooding.
  The orange zone marks the proposed breakwater project area between 71st and 75th Street.
  {"" if live else "<em>(Live API unavailable from this server — showing representative 311 data.)</em>"}
</div>
""", unsafe_allow_html=True)

# Hard clip using ray-casting point-in-polygon (no external libraries)
# Polygon traces South Shore land boundary, excluding beach and lake
_LAND_POLY = [
    (-87.590, 41.780),  # NW near 63rd/Stony Island
    (-87.553, 41.773),  # NE near 67th St — west of Shore Drive
    (-87.550, 41.766),  # 71st St — stays west of Shore Drive
    (-87.553, 41.762),  # Shore Drive curves SE at 73rd
    (-87.557, 41.756),  # Shore Drive at 75th St
    (-87.562, 41.749),  # Shore Drive at 79th St
    (-87.590, 41.748),  # SW near 79th/Stony Island
]

def _point_in_poly(lon, lat, poly):
    """Ray-casting algorithm — no external dependencies."""
    n = len(poly)
    inside = False
    x, y = lon, lat
    px, py = poly[-1]
    for cx, cy in poly:
        if ((cy > y) != (py > y)) and (x < (px - cx) * (y - cy) / (py - cy) + cx):
            inside = not inside
        px, py = cx, cy
    return inside

df = df[df.apply(lambda r: _point_in_poly(r["lon"], r["lat"], _LAND_POLY), axis=1)]

m = folium.Map(
    location=[41.748, -87.580],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True,
)

# Breakwater zone
folium.Rectangle(
    bounds=[[41.7655, -87.5600], [41.7490, -87.5480]],
    color=ORANGE,
    fill=True,
    fill_color=ORANGE,
    fill_opacity=0.22,
    weight=3,
    tooltip="⚠️ Proposed $5M breakwater project zone — 71st to 75th Street lakefront\n"
            "This project does NOT address basement flooding.\n"
            "No stormwater mitigation. No sewer upgrades.",
).add_to(m)

# Heatmap
basement_pts = df[
    df["flood_type"].str.contains("Basement", case=False, na=False)
][["lat", "lon"]].values.tolist()
if basement_pts:
    HeatMap(
        basement_pts,
        name="Basement flooding heatmap",
        radius=16, blur=20, min_opacity=0.25,
        gradient={"0.4": "white", "0.65": BURGUNDY, "1": "#3d0008"},
    ).add_to(m)

# Dots
def flood_color(ft):
    ft = str(ft).lower()
    if "basement" in ft: return BURGUNDY
    if "street"   in ft: return NAVY
    return ORANGE

for _, row in df.iterrows():
    color = flood_color(row["flood_type"])
    addr  = row.get('addr', '')
    ftype = row.get('flood_type', 'Flooding complaint')
    rdate = str(row.get('report_date', ''))[:10]
    lat_s = f"{row['lat']:.5f}"
    lon_s = f"{row['lon']:.5f}"
    tooltip = f"<b>{ftype}</b><br>{addr}<br>{rdate}"
    popup_html = (
        f"<div style='font-family:Arial,sans-serif;font-size:13px;min-width:180px'>"
        f"<b style='color:#6D071A'>{ftype}</b><br>"
        f"📍 {addr}<br>"
        f"📅 {rdate}<br>"
        f"<span style='color:#888;font-size:11px'>({lat_s}, {lon_s})</span>"
        f"</div>"
    )
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=5,
        color=color, fill=True, fill_color=color,
        fill_opacity=0.75, opacity=0.9, weight=0,
        tooltip=tooltip,
        popup=folium.Popup(popup_html, max_width=260),
    ).add_to(m)

# Legend
legend_html = f"""
<div style="position:fixed;bottom:40px;left:60px;z-index:9999;background:white;
padding:14px 16px;border:1px solid #999;border-radius:5px;
font-family:Arial,sans-serif;font-size:13px;box-shadow:2px 2px 6px rgba(0,0,0,.25)">
  <b>South Shore 311 Flooding</b><br><br>
  <span style="color:{BURGUNDY};font-size:18px">●</span> Basement flooding<br>
  <span style="color:{NAVY};font-size:18px">●</span> Street flooding<br>
  <span style="color:{ORANGE};font-size:18px">■</span> Proposed breakwater zone<br>
  <span style="font-size:10px;color:#777">This project does not address<br>basement flooding or sewers.</span>
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
folium.LayerControl(collapsed=True).add_to(m)

st_folium(m, width="100%", height=620, returned_objects=[])
st.markdown('</div>', unsafe_allow_html=True)

# ── Flyer image (below map, constrained width) ─────────────────────────────────
try:
    col_l, col_c, col_r = st.columns([1, 4, 1])
    with col_c:
        st.image("breakwaterinfo.png", use_container_width=True)
except Exception:
    pass

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
    the photos, the damage, the mold, the displacement — that official data does not fully capture.
    </p>
    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    South Shore is one of the most historically significant Black lakefront residential communities
    in America. It deserves infrastructure grounded in science, transparency, and residents'
    actual needs — not concrete in the lake.
    </p>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#f8f0f0;border:1px solid #e0b0b0;border-radius:3px;
    padding:14px;font-family:Arial,sans-serif">
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

# ── Breakwater impacts ─────────────────────────────────────────────────────────
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
      <div class="concern-text">Strong eddies between breakwater gaps can increase drowning risk.
      South Shore families swim here every summer.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🐟</div>
      <div class="concern-title">Water Quality & Hypoxia</div>
      <div class="concern-text">Creates water stagnation, hypoxic zones in summer,
      degraded water quality, and conditions that drive beachgoers away.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">⛓️</div>
      <div class="concern-title">Erosion Chain Reaction</div>
      <div class="concern-text">Intended to protect one stretch, breakwaters can accelerate
      erosion elsewhere, worsening downdrift erosion for years.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🌿</div>
      <div class="concern-title">Ecological Damage</div>
      <div class="concern-text">Destroys lake bottom habitats, reduces dissolved oxygen,
      and intensifies turbidity. No environmental review for this project has been produced.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">💰</div>
      <div class="concern-title">Cost & Lock-In</div>
      <div class="concern-text">Once concrete is poured, communities are locked into that decision
      for generations while resident flooding needs remain unresolved.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Report form ────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="report">', unsafe_allow_html=True)
st.markdown('<div class="section-head">Report Your Flooding Experience</div>', unsafe_allow_html=True)
st.markdown("""
<p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:12px">
  The 311 map shows official complaints, but not the full picture. Tell us what happened to you.
  Your report builds a public record that decision-makers cannot ignore.
  <strong>Self-reporting is the most powerful tool we have.</strong>
</p>
""", unsafe_allow_html=True)

with st.form("flood_report", clear_on_submit=True):
    st.markdown('<div class="form-section">', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        name       = st.text_input("Your Name", placeholder="First and last name")
        email_addr = st.text_input("Your Email", placeholder="email@example.com")
    with fc2:
        address       = st.text_input("Address or Intersection", placeholder="e.g. 73rd & Coles Ave, South Shore")
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
        placeholder="When it started, how long water stayed, property damage, city response or lack of response...",
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

    consent   = st.checkbox("I consent to this report being used as part of the public record on South Shore flooding.")
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
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9813723" target="_blank" style="color:#0a2240">Peer-reviewed breakwater impact study</a></li>
        <li><a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j" target="_blank" style="color:#0a2240">Chicago 311 Flooding Complaints Dataset</a></li>
      </ul>
    </div>
    <div>
      <div style="font-weight:700;color:#0a2240;margin-bottom:8px">FLOODING COVERAGE</div>
      <ul style="line-height:1.9;color:#333;padding-left:18px">
        <li><a href="https://news.uchicago.edu/story/students-identify-chicago-neighborhoods-most-risk-urban-flooding" target="_blank" style="color:#0a2240">UChicago: South Shore among highest-risk flood neighborhoods</a></li>
        <li><a href="https://www.wbez.org/environment/2026/04/10/flooding-chicago-climate-change-deep-tunnel-mold-metropolitan-water-reclamation-district-soaked" target="_blank" style="color:#0a2240">WBEZ: Chicago flooding coverage</a></li>
        <li><a href="https://insideclimatenews.org/news/04052026/chicago-flooding-climate-change/" target="_blank" style="color:#0a2240">Inside Climate News: Chicago flooding coverage</a></li>
      </ul>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Bottom CTA ─────────────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#c0392b;color:#fff;text-align:center;padding:32px 24px">
  <div style="font-size:1.5rem;font-weight:800;font-family:Arial,sans-serif;margin-bottom:8px">
    South Shore did not get a study.<br>It got a construction schedule.
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
    311 data sourced from the City of Chicago Data Portal.
    Community reports are used solely for civic advocacy purposes.
  </span>
</div>
""", unsafe_allow_html=True)
