import json
import re
from pathlib import Path
from statistics import median

import streamlit as st

st.set_page_config(
    page_title="July · Talent Agency Prospects",
    layout="centered",
)

# ----------------------------------------------------------------------------
# Styling — make it read like a product, not a Streamlit demo.
# ----------------------------------------------------------------------------
st.markdown(
    """
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

      html, body, [class*="css"], .stMarkdown, .stApp { font-family: 'Inter', -apple-system, sans-serif; }

      #MainMenu, footer, header {visibility: hidden;}
      .stDeployButton, div[data-testid="stToolbar"] {display: none;}
      .stApp { background: #0c0c0f; }
      .block-container { padding-top: 2.0rem; padding-bottom: 3rem; max-width: 720px; }

      /* Hero */
      .hero-title { font-size: 1.65rem; font-weight: 800; letter-spacing: -0.02em; margin: 0 0 .35rem; color: #fff; }
      .hero-sub { color: #a5a5b0; font-size: 0.95rem; line-height: 1.5; margin: 0; }
      .hero-by { color: #6f6f7c; font-size: 0.82rem; margin-top: .5rem; }

      /* Metric strip */
      .strip { display: flex; gap: .55rem; flex-wrap: wrap; margin: 1.15rem 0 .4rem; }
      .tile { flex: 1 1 0; min-width: 78px; background: #16161c; border: 1px solid #24242e;
              border-radius: 12px; padding: .7rem .75rem; }
      .tile .num { font-size: 1.5rem; font-weight: 800; color: #fff; line-height: 1; letter-spacing: -0.02em; }
      .tile .lbl { font-size: 0.72rem; color: #8b8b97; margin-top: .3rem; text-transform: uppercase; letter-spacing: .04em; }

      /* Section headers */
      .section { font-size: 0.82rem; font-weight: 700; text-transform: uppercase; letter-spacing: .09em;
                 color: #7b7b88; margin: 1.7rem 0 .7rem; display: flex; align-items: center; gap: .5rem; }
      .section .count { color: #4c4c58; font-weight: 600; }

      /* Agency card */
      .card { background: #131318; border: 1px solid #23232e; border-radius: 15px;
              padding: .95rem 1.05rem .9rem; margin-bottom: .7rem; }
      .card.dim { background: #101014; border-color: #1d1d26; }
      .card-top { display: flex; align-items: flex-start; gap: .8rem; }
      .score { flex: 0 0 auto; width: 46px; height: 46px; border-radius: 11px; display: flex;
               align-items: center; justify-content: center; font-weight: 800; font-size: 1.2rem;
               color: #0c0c0f; }
      .head { flex: 1 1 auto; min-width: 0; }
      .name { font-size: 1.06rem; font-weight: 700; color: #fbfbfd; letter-spacing: -0.01em; line-height: 1.2; }
      .meta { font-size: 0.83rem; color: #9494a1; margin-top: .18rem; }
      .meta b { color: #c7c7d2; font-weight: 600; }
      .why { font-size: 0.9rem; color: #c2c2ce; line-height: 1.5; margin: .6rem 0 .55rem; }
      .pills { display: flex; flex-wrap: wrap; gap: .32rem; }
      .pill { font-size: 0.7rem; color: #9a9aa6; background: #1c1c24; border: 1px solid #26262f;
              border-radius: 999px; padding: .16rem .5rem; white-space: nowrap; }
      .pill b { color: #d7d7e0; font-weight: 700; }
      .flag { font-size: 0.8rem; color: #e6b25c; background: rgba(230,178,92,.08);
              border: 1px solid rgba(230,178,92,.22); border-radius: 9px; padding: .4rem .6rem; margin-top: .6rem; }

      /* Expander tidy */
      div[data-testid="stExpander"] { border: none !important; }
      div[data-testid="stExpander"] details { background: #0f0f14; border: 1px solid #20202a;
              border-radius: 11px; }
      .dline { font-size: 0.86rem; line-height: 1.55; margin: .12rem 0; color: #cfcfd8; }
      .dline .k { color: #83838f; }
      a { color: #9d86ff !important; text-decoration: none; }
      a:hover { text-decoration: underline; }
    </style>
    """,
    unsafe_allow_html=True,
)


@st.cache_data
def load_agencies():
    path = Path(__file__).parent / "agencies.json"
    with open(path, "r", encoding="utf-8") as fh:
        data = json.load(fh)
    return sorted(data, key=lambda a: a["score"], reverse=True)


agencies = load_agencies()
scores = [a["score"] for a in agencies]


def score_color(s):
    if s >= 80:
        return "#3ddc84"   # green
    if s >= 75:
        return "#39d3c3"   # teal
    if s >= 70:
        return "#4aa3ff"   # blue
    if s >= 60:
        return "#e6b25c"   # amber
    return "#7f7f8c"       # grey


def hook(agency):
    """The reasoning, minus the 'Scores NN because' scaffolding, for quick scanning."""
    t = re.sub(r"^Scores\s+\d+\s+because\s+", "", agency["reasoning"])
    return t[0].upper() + t[1:]


def clean(url):
    return url.replace("https://", "").replace("http://", "").rstrip("/")


# ----------------------------------------------------------------------------
# Hero
# ----------------------------------------------------------------------------
st.markdown(
    """
    <div class="hero-title">Talent-agency prospects for July</div>
    <div class="hero-sub">15 real creator-management agencies, scored for fit with July's
    CRM&nbsp;+&nbsp;media-kits&nbsp;+&nbsp;payments platform. Every field verified on the agency's
    live site — nothing estimated.</div>
    <div class="hero-by">Built by Rishi Kesan · research only, no outreach sent</div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# At-a-glance strip
# ----------------------------------------------------------------------------
strong_n = sum(1 for s in scores if s > 70)
st.markdown(
    f"""
    <div class="strip">
      <div class="tile"><div class="num">15</div><div class="lbl">Agencies</div></div>
      <div class="tile"><div class="num">{int(median(scores))}</div><div class="lbl">Median fit</div></div>
      <div class="tile"><div class="num">{strong_n}</div><div class="lbl">Strong&nbsp;fit&nbsp;&gt;70</div></div>
      <div class="tile"><div class="num">100%</div><div class="lbl">Verified live</div></div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ----------------------------------------------------------------------------
# Optional filter — tucked away so the default view stays clean
# ----------------------------------------------------------------------------
with st.expander("Filter"):
    min_score = st.slider("Minimum fit score", 0, 100, 0, step=1)
    known = [a["roster_count"] for a in agencies if a["roster_count"]]
    hi = max(known)
    roster_range = st.slider("Roster size (where published)", 0, hi, (0, hi))
    show_unknown = st.checkbox("Include agencies with a private / by-request roster", value=True)


# Read filter values with safe defaults if the expander was never opened
_min = locals().get("min_score", 0)
_range = locals().get("roster_range", None)
_unknown = locals().get("show_unknown", True)


def visible(a):
    if a["score"] < _min:
        return False
    rc = a["roster_count"]
    if rc is None:
        return _unknown
    if _range and not (_range[0] <= rc <= _range[1]):
        return False
    return True


shown = [a for a in agencies if visible(a)]
strong = [a for a in shown if a["score"] > 70]
other = [a for a in shown if a["score"] <= 70]


def render_card(a, dim=False):
    color = score_color(a["score"])
    dm = a["decision_maker"]
    dm_bit = f" · <b>{dm['name']}</b>" if dm["linkedin"] and dm["linkedin"] != "unknown" else ""
    b = a["score_breakdown"]
    st.markdown(
        f"""
        <div class="card {'dim' if dim else ''}">
          <div class="card-top">
            <div class="score" style="background:{color}">{a['score']}</div>
            <div class="head">
              <div class="name">{a['name']}</div>
              <div class="meta"><b>{a['hq_short']}</b> · {a['roster_display']}{dm_bit}</div>
            </div>
          </div>
          <div class="why">{hook(a)}</div>
          <div class="pills">
            <span class="pill">Roster <b>{b['roster_fit']}</b>/30</span>
            <span class="pill">Manual ops <b>{b['manual_ops']}</b>/25</span>
            <span class="pill">Managers <b>{b['multi_manager']}</b>/20</span>
            <span class="pill">Payments <b>{b['payment_complexity']}</b>/15</span>
            <span class="pill">Reach <b>{b['reachability']}</b>/10</span>
          </div>
          {f'<div class="flag">{a["flag"]}</div>' if a.get("flag") else ''}
        </div>
        """,
        unsafe_allow_html=True,
    )
    with st.expander("Details & draft email"):
        d = a
        dm = d["decision_maker"]
        if dm["linkedin"] and dm["linkedin"] != "unknown":
            dm_val = f"{dm['name']} — {dm['title']} · [LinkedIn]({dm['linkedin']})"
        else:
            dm_val = f"{dm['name']} — {dm['title']} (LinkedIn not public)"
        rows = [
            ("Website", f"[{clean(d['website'])}]({d['website']})"),
            ("HQ", d["hq"]),
            ("Roster", d["roster_display"]),
            ("Team / managers", d["employees"]),
            ("Brand inquiries", d["brand_inquiry"]),
            ("Named brand partners", d["brand_partners"]),
            ("Decision maker", dm_val),
        ]
        for k, v in rows:
            st.markdown(f"<div class='dline'><span class='k'>{k}:</span> {v}</div>", unsafe_allow_html=True)
        srcs = " · ".join(f"[{i+1}]({s})" for i, s in enumerate(d["sources"]))
        st.markdown(f"<div class='dline'><span class='k'>Sources:</span> {srcs}</div>", unsafe_allow_html=True)
        st.markdown("<div class='dline' style='margin-top:.5rem'><b>First-touch email</b></div>", unsafe_allow_html=True)
        st.code(d["email"], language=None)


if strong:
    st.markdown(f"<div class='section'>Strongest fits <span class='count'>{len(strong)}</span></div>", unsafe_allow_html=True)
    for a in strong:
        render_card(a)

if other:
    st.markdown(f"<div class='section'>Also researched <span class='count'>{len(other)}</span></div>", unsafe_allow_html=True)
    for a in other:
        render_card(a, dim=True)

if not shown:
    st.info("No agencies match the current filter.")

# ----------------------------------------------------------------------------
# Methodology
# ----------------------------------------------------------------------------
with st.expander("Methodology — rubric, weights, sourcing"):
    st.markdown(
        """
**What this is.** A prospect list for **July** (withjuly.com), which sells a CRM + media-kit +
payments platform to talent agencies and creator managers who currently run brand deals out of
spreadsheets, DMs, and PDF media kits. Every agency here is real and was confirmed from its live
website during research.

**How it was sourced.** Web search across creator-economy directories and trade press
(Tubefilter, Variety, Deadline, WWD) produced ~40 candidates. Each was opened and read on its own
live site to confirm it is a *management* agency — represents a roster, negotiates brand deals — not
a brand-side marketing shop, PR firm, or Hollywood agency. 30 passed; the 15 here are the strongest
ICP fits. Anything that couldn't be fetched cleanly, or turned out to be an OnlyFans / modeling /
coaching shop, was dropped rather than guessed.

**Scoring rubric (0–100).** Each score cites one observed fact.

| Weight | Signal | Scores highest when |
|--:|--|--|
| **30** | Roster size fit | 8–40 creators. Under 5 = low budget; over 60 = enterprise, scores lower |
| **25** | Manual-ops evidence | Single inbox, "email for rates", PDF kits, Linktree, no deal tracking |
| **20** | Multi-manager coordination | 2+ managers → handoffs, splits, commission tracking |
| **15** | Payment complexity | Agency–talent revenue splits, in-house legal/finance, high payout volume |
| **10** | Reachability | Named decision maker with a public LinkedIn |

**Honesty rules.** Unverifiable fields are labelled rather than estimated. Recent structural changes
are flagged inline (e.g., Spark was acquired Jan 2026; Parker is now a Propagate division). No one
was contacted — this is research output only.
        """
    )
