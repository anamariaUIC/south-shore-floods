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

# ── Official Chicago 311 flooding data ───────────────────────────────────────
# South Shore = Chicago Community Area 43.
# We query flooding service requests directly and paginate until all matching
# records returned by the City API have been retrieved. Nothing is synthesized.

EMPTY_DF = pd.DataFrame(
    columns=["lat", "lon", "ca", "flood_type", "addr", "report_date"]
)

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_south_shore_311():
    """
    Retrieve official Chicago 311 Water in Basement / Water on Street requests
    for South Shore (Community Area 43).

    The current 311 dataset is queried first. The legacy flooding-specific
    dataset is used only if the current endpoint cannot supply usable records.
    No addresses, dates, coordinates, or complaints are generated locally.
    """
    endpoints = [
        {
            "url": "https://data.cityofchicago.org/resource/v6vf-nfxy.json",
            "where": (
                "community_area = '43' "
                "AND sr_short_code IN ('AAF','AAE') "
                "AND latitude IS NOT NULL "
                "AND longitude IS NOT NULL"
            ),
        },
        {
            "url": "https://data.cityofchicago.org/resource/qrmr-m89j.json",
            "where": (
                "community_area = '43' "
                "AND latitude IS NOT NULL "
                "AND longitude IS NOT NULL "
                "AND (sr_type = 'Water in Basement Complaint' "
                "OR sr_type = 'Water On Street Complaint')"
            ),
        },
    ]

    page_size = 5000
    errors = []

    for endpoint in endpoints:
        rows = []
        offset = 0

        try:
            while True:
                params = {
                    "$limit": page_size,
                    "$offset": offset,
                    "$order": "created_date DESC",
                    "$where": endpoint["where"],
                }

                response = requests.get(
                    endpoint["url"],
                    params=params,
                    timeout=30,
                    headers={"User-Agent": "SouthShoreFloods/1.0"},
                )
                response.raise_for_status()
                page = response.json()

                if not page:
                    break

                rows.extend(page)

                if len(page) < page_size:
                    break

                offset += page_size

            if not rows:
                errors.append(f"{endpoint['url']}: no matching records returned")
                continue

            df = pd.DataFrame(rows)
            df.columns = [str(c).lower() for c in df.columns]

            if "latitude" not in df.columns or "longitude" not in df.columns:
                errors.append(f"{endpoint['url']}: coordinate fields missing")
                continue

            df["lat"] = pd.to_numeric(df["latitude"], errors="coerce")
            df["lon"] = pd.to_numeric(df["longitude"], errors="coerce")

            # Complaint type: prefer City's descriptive field.
            if "sr_type" in df.columns:
                df["flood_type"] = df["sr_type"].fillna("Flooding complaint")
            elif "sr_short_code" in df.columns:
                code_map = {
                    "AAF": "Water in Basement Complaint",
                    "AAE": "Water On Street Complaint",
                }
                df["flood_type"] = (
                    df["sr_short_code"].astype(str).str.upper().map(code_map)
                    .fillna("Flooding complaint")
                )
            else:
                df["flood_type"] = "Flooding complaint"

            # Use only the City's address.
            if "street_address" in df.columns:
                df["addr"] = (
                    df["street_address"]
                    .fillna("Address not provided by Chicago 311")
                    .astype(str)
                )
            else:
                df["addr"] = "Address not provided by Chicago 311"

            # Use only the City's creation date.
            if "created_date" in df.columns:
                df["report_date"] = pd.to_datetime(
                    df["created_date"], errors="coerce"
                )
            else:
                df["report_date"] = pd.NaT

            if "community_area" in df.columns:
                df["ca"] = pd.to_numeric(
                    df["community_area"], errors="coerce"
                )
            else:
                # The query itself restricted the response to CA 43.
                df["ca"] = 43

            df = df.dropna(subset=["lat", "lon"]).copy()

            # Defensive validation: retain CA 43 if the field is present.
            if "community_area" in df.columns:
                df = df[df["ca"] == 43].copy()

            if df.empty:
                errors.append(
                    f"{endpoint['url']}: matching records had no usable coordinates"
                )
                continue

            # Remove exact duplicate service-request rows when a request ID is
            # available. Do NOT collapse separate complaints at the same address.
            id_col = next(
                (
                    c for c in [
                        "sr_number",
                        "service_request_number",
                        "service_request_id",
                    ]
                    if c in df.columns
                ),
                None,
            )
            if id_col:
                df = df.drop_duplicates(subset=[id_col], keep="first")

            return df.reset_index(drop=True), True, None

        except requests.RequestException as exc:
            errors.append(f"{endpoint['url']}: {exc}")
        except (ValueError, TypeError, KeyError) as exc:
            errors.append(f"{endpoint['url']}: could not parse response ({exc})")

    return EMPTY_DF.copy(), False, " | ".join(errors)


with st.spinner("Loading official Chicago 311 flooding data for South Shore..."):
    df, live, api_error = fetch_south_shore_311()

if not live:
    st.warning(
        "Official Chicago 311 flooding data is temporarily unavailable. "
        "No synthetic complaint locations are being displayed."
    )
    if api_error:
        st.caption(f"Data service detail: {api_error}")

# ── Stats strip ────────────────────────────────────────────────────────────────
total    = len(df)
basement = int(df["flood_type"].astype(str).str.contains("Basement", case=False, na=False).sum())
street   = int(df["flood_type"].astype(str).str.contains("Street",   case=False, na=False).sum())

st.markdown(f"""
<div class="stats-strip">
  <div class="stat-item">
    <span class="stat-number">{total:,}</span>
    <span class="stat-label">South Shore 311 Flooding Complaints</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{basement:,}</span>
    <span class="stat-label">Basement Flooding Reports</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">{street:,}</span>
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
st.markdown('<div class="section-head">311 Flooding Complaints — South Shore (Community Area 43)</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="section-sub">
  Official Water in Basement and Water on Street complaint records for South Shore (Community Area 43) from the
  <a href="https://data.cityofchicago.org/Service-Requests/Flooding-Complaints-to-311/qrmr-m89j"
  target="_blank" style="color:#0a2240">Chicago Data Portal</a>.
  <strong style="color:{BURGUNDY}">Burgundy</strong> = basement flooding ·
  <strong style="color:{NAVY}">Navy</strong> = street flooding.
  The orange line marks the approximate proposed $5 million breakwater wall alignment along the lakefront between East 72nd Place and East 73rd Place.<br>  <strong>Map scope:</strong> all geocoded AAF (Water in Basement) and AAE (Water on Street) records returned by Chicago 311 for Community Area 43.
  {"" if live else "<em>(City API currently unavailable — no complaint points are shown.)</em>"}
</div>
""", unsafe_allow_html=True)

# Geographic scope is defined by the City's Community Area 43 field.
# No hand-drawn polygon clipping is applied.

m = folium.Map(
    location=[41.748, -87.580],
    zoom_start=12,
    tiles="OpenStreetMap",
    control_scale=True,
)

# Proposed $5M breakwater wall — approximate alignment shown in the
# City's conceptual shoreline graphic, from East 72nd Place to East 73rd Place.
# This replaces the former orange rectangular "project zone".
#
# Coordinates are intentionally presented as an approximate conceptual alignment,
# not as surveyed engineering coordinates.
breakwater_line = [
    [41.76605, -87.55935],
    [41.76585, -87.55915],
    [41.76562, -87.55892],
    [41.76538, -87.55868],
    [41.76515, -87.55845],
    [41.76490, -87.55820],
    [41.76465, -87.55795],
]

folium.PolyLine(
    locations=breakwater_line,
    color=ORANGE,
    weight=7,
    opacity=0.95,
    tooltip="Proposed $5 million breakwater wall — approximate alignment",
    popup=folium.Popup(
        "<b>Proposed $5 million breakwater wall</b><br>"
        "Approximate conceptual alignment along the lakefront between "
        "East 72nd Place and East 73rd Place.<br><br>"
        "<i>Illustrative alignment based on the City's conceptual shoreline plan; "
        "not surveyed engineering coordinates.</i>",
        max_width=320,
    ),
).add_to(m)

# Heatmap
basement_pts = df[
    df["flood_type"].astype(str).str.contains("Basement", case=False, na=False)
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
    raw_date = row.get('report_date', pd.NaT)
    rdate = raw_date.strftime("%Y-%m-%d") if pd.notna(raw_date) else "Date not provided"
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
  <span style="color:{ORANGE};font-size:18px;font-weight:900">━</span> Proposed $5M breakwater wall<br>
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
