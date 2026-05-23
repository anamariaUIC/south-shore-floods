"""
South Shore Flooding Data Collection
Report flooding incidents, demand accountability, sign the petition.
"""

import streamlit as st
import urllib.parse
from datetime import date

st.set_page_config(
    page_title="South Shore Floods | Report Your Experience",
    page_icon="🌊",
    layout="wide",
)

st.markdown("""
<style>
/* ── Base ─────────────────────────────────────────────── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 0 2rem 0 !important; max-width: 100% !important; }
html, body, [class*="css"] {
    font-family: Georgia, "Times New Roman", serif;
    color: #1a1a1a;
}

/* ── Nav bar ──────────────────────────────────────────── */
.topnav {
    background: #0a2240;
    padding: 10px 32px;
    font-size: 13px;
    display: flex;
    gap: 24px;
    align-items: center;
}
.topnav a {
    color: #a8c8e8;
    text-decoration: none;
    font-family: Arial, sans-serif;
    font-size: 13px;
    font-weight: 500;
}
.topnav a:hover { color: #fff; }
.topnav-brand {
    color: #fff;
    font-weight: 700;
    font-size: 15px;
    margin-right: 12px;
}

/* ── Hero ─────────────────────────────────────────────── */
.hero-band {
    background: #0a2240;
    color: #fff;
    padding: 28px 48px 20px 48px;
    border-bottom: 4px solid #c0392b;
}
.hero-band h1 {
    font-size: 2.2rem;
    font-weight: 800;
    color: #fff;
    margin: 0 0 6px 0;
    line-height: 1.2;
    font-family: Arial, sans-serif;
}
.hero-band h1 span { color: #e74c3c; }
.hero-band p {
    font-size: 1.05rem;
    color: #a8c8e8;
    margin: 0;
    font-family: Arial, sans-serif;
}

/* ── Petition banner ──────────────────────────────────── */
.petition-banner {
    background: #c0392b;
    color: #fff;
    text-align: center;
    padding: 14px 24px;
    font-family: Arial, sans-serif;
}
.petition-banner a {
    color: #fff;
    font-weight: 800;
    font-size: 1.1rem;
    text-decoration: none;
    background: #fff;
    color: #c0392b;
    padding: 8px 24px;
    border-radius: 3px;
    display: inline-block;
    margin-top: 6px;
    letter-spacing: 0.03em;
}
.petition-banner p {
    margin: 0 0 6px 0;
    font-size: 1rem;
    font-weight: 600;
}

/* ── Content sections ─────────────────────────────────── */
.content-section {
    padding: 32px 48px;
    max-width: 1100px;
    margin: 0 auto;
}
.section-head {
    font-size: 1.5rem;
    font-weight: 700;
    color: #0a2240;
    font-family: Arial, sans-serif;
    border-bottom: 2px solid #c0392b;
    padding-bottom: 8px;
    margin-bottom: 16px;
}
.pullquote {
    border-left: 4px solid #c0392b;
    padding: 12px 20px;
    background: #f8f0f0;
    font-size: 1.05rem;
    font-style: italic;
    color: #2c2c2c;
    margin: 16px 0;
    line-height: 1.6;
}

/* ── Concern cards ────────────────────────────────────── */
.concerns-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-top: 16px;
}
.concern-card {
    background: #f5f8fc;
    border: 1px solid #c8d8e8;
    border-top: 3px solid #0a2240;
    border-radius: 3px;
    padding: 16px;
}
.concern-icon { font-size: 1.6rem; margin-bottom: 6px; }
.concern-title {
    font-size: 13px; font-weight: 700;
    color: #0a2240; font-family: Arial, sans-serif;
    text-transform: uppercase; letter-spacing: .04em;
    margin-bottom: 6px;
}
.concern-text { font-size: 13px; color: #444; line-height: 1.5; }

/* ── Stats strip ──────────────────────────────────────── */
.stats-strip {
    background: #0a2240;
    color: #fff;
    display: flex;
    justify-content: space-around;
    padding: 20px 32px;
    gap: 16px;
    flex-wrap: wrap;
}
.stat-item { text-align: center; }
.stat-number {
    font-size: 2rem; font-weight: 800;
    color: #e74c3c; font-family: Arial, sans-serif;
    display: block;
}
.stat-label {
    font-size: 12px; color: #a8c8e8;
    font-family: Arial, sans-serif;
    text-transform: uppercase; letter-spacing: .04em;
}

/* ── Report form ──────────────────────────────────────── */
.form-section {
    background: #f5f8fc;
    border: 1px solid #c8d8e8;
    border-radius: 4px;
    padding: 24px 28px;
    margin-top: 8px;
}
.form-head {
    font-size: 1.1rem; font-weight: 700;
    color: #0a2240; font-family: Arial, sans-serif;
    margin-bottom: 14px;
}
.field-label {
    font-size: 13px; font-weight: 700;
    color: #333; font-family: Arial, sans-serif;
    margin-bottom: 2px;
}
.photo-note {
    background: #fff8e1; border: 1px solid #f0c840;
    border-radius: 3px; padding: 10px 14px;
    font-size: 13px; color: #7a5000;
    font-family: Arial, sans-serif; line-height: 1.5;
    margin: 12px 0;
}
.photo-note a { color: #0a2240; font-weight: 700; }
.submit-note {
    font-size: 12px; color: #666;
    font-family: Arial, sans-serif;
    margin-top: 8px; line-height: 1.5;
}

/* ── Footer ───────────────────────────────────────────── */
.page-footer {
    background: #0a2240; color: #8ab0d0;
    padding: 20px 48px; margin-top: 32px;
    font-size: 12px; font-family: Arial, sans-serif;
    line-height: 1.8;
}
.page-footer a { color: #8ab0d0; }
.page-footer strong { color: #fff; }

/* Streamlit widget tweaks */
div[data-testid="stVerticalBlock"] > div { gap: 0.3rem; }
.stTextInput input, .stTextArea textarea, .stSelectbox select {
    border: 1px solid #c0c0c0 !important;
    border-radius: 3px !important;
    font-family: Arial, sans-serif !important;
    font-size: 13px !important;
}
.stButton button {
    background: #c0392b !important;
    color: #fff !important;
    border: none !important;
    border-radius: 3px !important;
    font-weight: 700 !important;
    font-size: 14px !important;
    padding: 10px 28px !important;
    font-family: Arial, sans-serif !important;
    width: 100% !important;
}
.stButton button:hover { background: #a93226 !important; }
</style>
""", unsafe_allow_html=True)

# ── Nav ────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="topnav">
  <span class="topnav-brand">🌊 South Shore Floods</span>
  <a href="#about">About</a>
  <a href="#impacts">Key Impacts</a>
  <a href="#report">Report Your Flooding</a>
  <a href="http://bit.ly/4ukCmjg" target="_blank">✍️ Sign the Petition</a>
</div>
""", unsafe_allow_html=True)

# ── Hero ───────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-band">
  <h1>Why Are <span>$5 Million Going Into the Lake</span><br>While Our Basements Flood?</h1>
  <p>South Shore deserves investments that solve the flooding we live with — every year.
     Help us document what's happening on the ground.</p>
</div>
""", unsafe_allow_html=True)

# ── Petition banner ────────────────────────────────────────────────────────────
st.markdown("""
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

# ── Stats strip ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-strip">
  <div class="stat-item">
    <span class="stat-number">$5M</span>
    <span class="stat-label">Committed to lakefront breakwaters</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">70,000</span>
    <span class="stat-label">Chicago homes flooded in 2023</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">4 ft</span>
    <span class="stat-label">Lake Michigan has dropped since 2020 peak</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">0</span>
    <span class="stat-label">Project-specific environmental studies produced</span>
  </div>
  <div class="stat-item">
    <span class="stat-number">Fall 2026</span>
    <span class="stat-label">Assumed construction start date</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ── About ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="about">', unsafe_allow_html=True)
st.markdown('<div class="section-head">About This Initiative</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1.6, 1])
with col1:
    st.markdown("""
    <div class="pullquote">
    "Every time it rains hard in South Shore, basements flood. Streets turn into rivers.
    Families pump water out of their homes, replace ruined belongings, and fight mold for months.
    This is happening right now, in one of only four Chicago neighborhoods researchers have identified
    as being at the highest risk of urban flooding in the entire city."
    </div>

    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    Despite this reality, the City of Chicago is advancing a <strong>$5 million lakefront breakwater
    project between 71st and 75th Street</strong> — infrastructure South Shore never asked for,
    with no updated environmental review, and peer-reviewed science showing it will cause permanent
    damage to our shoreline, water quality, and neighboring communities up and down the lake.
    </p>

    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    <strong>This page exists to document what residents are actually experiencing.</strong>
    Your reports create a public record that decision-makers cannot ignore.
    Tell us about flooding in your basement, your street, your alley, your park, your parking lot.
    Every report matters. Every photo matters.
    </p>

    <p style="font-size:14px;line-height:1.7;color:#333;font-family:Arial,sans-serif">
    This is the last Black lakefront residential community in America.
    South Shore deserves infrastructure investments grounded in science,
    transparency, and the real needs of residents — not concrete in the lake.
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
      <ul style="font-size:12px;color:#333;line-height:1.7;margin:0;padding-left:16px">
        <li><strong>Pause</strong> the breakwater project</li>
        <li><strong>Redirect</strong> the $5M to flood mitigation residents need</li>
        <li><strong>Require</strong> transparent environmental review</li>
        <li><strong>Evaluate</strong> nature-based alternatives</li>
        <li><strong>Ensure</strong> meaningful community input before any construction</li>
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

# ── Key Impacts ────────────────────────────────────────────────────────────────
st.markdown("""
<div class="content-section" id="impacts">
  <div class="section-head">What Breakwaters Actually Do</div>
  <p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:4px">
    Peer-reviewed science documents the following impacts.
    (<a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9813723" target="_blank"
    style="color:#0a2240">Full study: Saengsupavanich et al., Heliyon, 2022</a>)
  </p>
  <div class="concerns-grid">
    <div class="concern-card">
      <div class="concern-icon">🏖️</div>
      <div class="concern-title">Beach & Shoreline Destruction</div>
      <div class="concern-text">Breakwaters permanently interrupt sediment transport.
      The damage extends far beyond 75th Street — Promontory Point, Rainbow Beach,
      and every neighbor up and down the lake absorbs the consequences through accelerated erosion.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🌀</div>
      <div class="concern-title">Dangerous Currents</div>
      <div class="concern-text">Strong eddies between breakwater gaps dramatically increase
      drowning risk. Studies document an average of 67 victims per year at studied sites —
      a public safety crisis on a lakefront where South Shore families swim every summer.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🐟</div>
      <div class="concern-title">Water Quality & Hypoxia</div>
      <div class="concern-text">Breakwaters create water stagnation and hypoxic dead zones
      in summer, degrading water quality and driving beachgoers away from the very shoreline
      this project claims to protect.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">⛓️</div>
      <div class="concern-title">Erosion Chain Reaction</div>
      <div class="concern-text">Structures intended to protect one stretch actively accelerate
      erosion elsewhere, creating a shore-parallel seawall effect that worsens downdrift erosion
      for years after construction.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">🌿</div>
      <div class="concern-title">Ecological Damage</div>
      <div class="concern-text">Hard engineering structures destroy lake bottom habitats,
      reduce dissolved oxygen, intensify turbidity, and permanently alter the ecosystem.
      No environmental review specific to this project has ever been produced.</div>
    </div>
    <div class="concern-card">
      <div class="concern-icon">💰</div>
      <div class="concern-title">Cost & Lock-In</div>
      <div class="concern-text">Nature-based alternatives cost 2–5× less than hard structures.
      Once concrete is poured, you are locked in for generations. Neighbors in Ogden Dunes, Indiana
      spent $5M trying to undo the damage from a single breakwater.</div>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ── Report form ────────────────────────────────────────────────────────────────
st.markdown('<div class="content-section" id="report">', unsafe_allow_html=True)
st.markdown('<div class="section-head">Report Your Flooding Experience</div>', unsafe_allow_html=True)
st.markdown("""
<p style="font-size:14px;color:#333;font-family:Arial,sans-serif;margin-bottom:12px">
  Use the form below to share what you have witnessed. Your report builds a public record
  that decision-makers cannot ignore. <strong>Self-reporting is the most powerful tool we have.</strong>
</p>
""", unsafe_allow_html=True)

with st.form("flood_report", clear_on_submit=True):
    st.markdown('<div class="form-section">', unsafe_allow_html=True)
    st.markdown('<div class="form-head">Your Flooding Report</div>', unsafe_allow_html=True)

    fc1, fc2 = st.columns(2)
    with fc1:
        name = st.text_input("Your Name", placeholder="First and last name")
        email_addr = st.text_input("Your Email", placeholder="email@example.com")
    with fc2:
        address = st.text_input("Your Address or Intersection", placeholder="e.g. 73rd & Coles Ave, South Shore")
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
        ["First time I've seen it", "Yes — occasionally (1–2 times/year)",
         "Yes — frequently (every heavy rain)", "Yes — this is a chronic ongoing problem"],
        horizontal=False,
    )

    description = st.text_area(
        "Describe what happened",
        placeholder="Tell us what you witnessed — when it started, how long water stayed, any damage to property, "
                    "any response (or lack of response) from the city, how it affected your family...",
        height=130,
    )

    infrastructure = st.text_area(
        "Any known infrastructure issues nearby? (optional)",
        placeholder="e.g. blocked catch basins, broken sewer lines, no storm drains on the block...",
        height=70,
    )

    st.markdown("""
    <div class="photo-note">
      📷 <strong>Have photos or videos?</strong> Please send them directly to
      <a href="mailto:sokovic.anamarija@gmail.com">sokovic.anamarija@gmail.com</a>
      with subject line <strong>"South Shore Flooding — [your street/intersection]"</strong>.
      Photos of basement water, flooded streets, ponding in parks, and overwhelmed drains
      are especially valuable for building our public record.
    </div>
    """, unsafe_allow_html=True)

    consent = st.checkbox(
        "I consent to this report being used as part of the public record on South Shore flooding."
    )

    submitted = st.form_submit_button("Submit My Report")

    if submitted:
        if not name or not address or not description:
            st.error("Please fill in your name, address/location, and description before submitting.")
        elif not consent:
            st.error("Please check the consent box to submit your report.")
        else:
            # Build mailto link with pre-filled content
            flood_types_str = ", ".join(flood_type) if flood_type else "Not specified"
            subject = f"South Shore Flooding Report — {address}"
            body = f"""SOUTH SHORE FLOODING REPORT
============================
Name: {name}
Email: {email_addr}
Location: {address}
Date of incident: {incident_date}

Flooding locations: {flood_types_str}
Severity: {severity}
Recurrence: {recurrence}

DESCRIPTION:
{description}

INFRASTRUCTURE ISSUES:
{infrastructure if infrastructure else "None noted"}

Submitted via southshorefloods.streamlit.app
"""
            mailto = (
                "mailto:sokovic.anamarija@gmail.com"
                f"?subject={urllib.parse.quote(subject)}"
                f"&body={urllib.parse.quote(body)}"
            )

            st.success("✅ Thank you! Click the button below to send your report by email.")
            st.markdown(
                f'<a href="{mailto}" style="display:inline-block;background:#0a2240;color:#fff;'
                f'font-weight:700;font-size:14px;padding:10px 28px;border-radius:3px;'
                f'text-decoration:none;margin-top:8px">📧 Open Email to Send Report →</a>',
                unsafe_allow_html=True,
            )
            st.info(
                "Your email client will open pre-filled with your report. "
                "Hit Send — and please attach any photos you have.",
                icon="📬",
            )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ── Resources & news ───────────────────────────────────────────────────────────
st.markdown("""
<div class="content-section">
  <div class="section-head">Resources & Documentation</div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;font-family:Arial,sans-serif;font-size:13px">
    <div>
      <div style="font-weight:700;color:#0a2240;margin-bottom:8px">FOIA & Research</div>
      <ul style="line-height:1.9;color:#333;padding-left:18px">
        <li><a href="https://tinyurl.com/4sh34tdj" target="_blank" style="color:#0a2240">
          Full FOIA analysis of the breakwater project</a></li>
        <li><a href="https://pmc.ncbi.nlm.nih.gov/articles/PMC9813723" target="_blank" style="color:#0a2240">
          Peer-reviewed breakwater impact study (Heliyon, 2022)</a></li>
        <li><a href="https://wicoastalresilience.org/march-2026-water-level-update" target="_blank" style="color:#0a2240">
          Lake Michigan water level update (March 2026)</a></li>
        <li><a href="https://tinyurl.com/5n7pxjke" target="_blank" style="color:#0a2240">
          Historical Lake Michigan water level data</a></li>
      </ul>
    </div>
    <div>
      <div style="font-weight:700;color:#0a2240;margin-bottom:8px">FLOODING COVERAGE</div>
      <ul style="line-height:1.9;color:#333;padding-left:18px">
        <li><a href="https://news.uchicago.edu/story/students-identify-chicago-neighborhoods-most-risk-urban-flooding"
          target="_blank" style="color:#0a2240">UChicago: South Shore among highest-risk flood neighborhoods</a></li>
        <li><a href="https://www.wbez.org/environment/2026/04/10/flooding-chicago-climate-change-deep-tunnel-mold-metropolitan-water-reclamation-district-soaked"
          target="_blank" style="color:#0a2240">WBEZ: 70,000 Chicago homes flooded in 2023</a></li>
        <li><a href="https://www.fox32chicago.com/news/chicago-south-side-home-floods-again-family-demands-city-fix-ongoing-problem"
          target="_blank" style="color:#0a2240">Fox 32: South Side families flooded repeatedly</a></li>
        <li><a href="https://www.youtube.com/watch?v=0oJ0UtZIbx0" target="_blank" style="color:#0a2240">
          Ogden Dunes, Indiana: $5M to undo one breakwater's damage</a></li>
      </ul>
    </div>
  </div>
  <div style="margin-top:20px;background:#f0f5ff;border:1px solid #c0d0e8;border-radius:3px;
  padding:14px 18px;font-family:Arial,sans-serif;font-size:13px;color:#333">
    <strong style="color:#0a2240">CONTACT DECISION-MAKERS DIRECTLY</strong><br><br>
    <strong>Mayor Brandon Johnson</strong> · City Hall, 121 N. LaSalle St., Chicago IL 60602
    · 312-744-3300 · chicago.gov/mayor<br>
    <strong>Illinois DCEO</strong> · 500 E. Monroe St., Springfield IL 62701
    · 217-782-7500 · Chicago office: 312-814-7179 · dceo.webmaster@illinois.gov
  </div>
</div>
""", unsafe_allow_html=True)

# ── Bottom petition CTA ────────────────────────────────────────────────────────
st.markdown("""
<div style="background:#c0392b;color:#fff;text-align:center;padding:32px 24px">
  <div style="font-size:1.6rem;font-weight:800;font-family:Arial,sans-serif;margin-bottom:8px">
    The last Black lakefront residential community in America did not get a study.<br>
    It got a construction schedule.
  </div>
  <div style="font-size:14px;color:#f8c8c8;margin-bottom:16px;font-family:Arial,sans-serif">
    Construction is assumed to begin as early as <strong style="color:#fff">Fall 2026</strong>.
    The time to act is now.
  </div>
  <a href="http://bit.ly/4ukCmjg" target="_blank"
  style="display:inline-block;background:#fff;color:#c0392b;font-weight:800;
  font-size:1.1rem;padding:14px 40px;border-radius:3px;text-decoration:none;
  letter-spacing:0.03em">
  ✍️ SIGN THE PETITION — bit.ly/4ukCmjg</a>
</div>
""", unsafe_allow_html=True)

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="page-footer">
  <strong>South Shore Flooding Documentation Initiative</strong> · Chicago, IL<br>
  Questions or to send photos and documents:
  <a href="mailto:sokovic.anamarija@gmail.com">sokovic.anamarija@gmail.com</a><br>
  Sign the petition: <a href="http://bit.ly/4ukCmjg" target="_blank">bit.ly/4ukCmjg</a>
  &nbsp;·&nbsp;
  Full FOIA analysis: <a href="https://tinyurl.com/4sh34tdj" target="_blank">tinyurl.com/4sh34tdj</a><br>
  <span style="color:#5a7090;font-size:11px">
    All submissions are used to build a transparent public record on South Shore flooding.
    Photos and personal details shared with this project are used solely for community advocacy purposes.
  </span>
</div>
""", unsafe_allow_html=True)
