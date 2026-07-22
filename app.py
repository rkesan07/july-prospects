import json
from pathlib import Path
from statistics import median

import streamlit as st

st.set_page_config(
    page_title="July · Talent Agency Prospect List",
    page_icon=None,
    layout="centered",
)

# --- kill Streamlit chrome so it reads as a tool, not a Streamlit demo ---
st.markdown(
    """
    <style>
      #MainMenu {visibility: hidden;}
      footer {visibility: hidden;}
      header {visibility: hidden;}
      .stDeployButton {display: none;}
      div[data-testid="stToolbar"] {display: none;}
      /* tighten mobile spacing */
      .block-container {padding-top: 2.2rem; padding-bottom: 3rem; max-width: 780px;}
      .agency-line {margin: 0.15rem 0; font-size: 0.93rem; line-height: 1.4;}
      .agency-label {color: #9a9aa5;}
      .flag-note {color: #e0a44a; font-size: 0.9rem;}
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

# --- header ---
st.markdown("### July — talent-agency prospect list")
st.caption(
    "30 real creator/talent-management agencies sourced, narrowed to the 15 strongest fits for "
    "July's CRM + media-kit + payments platform. Every field was verified from the agency's live "
    "site this session. Built by Rishi Kesan as a cold-email artifact — research only, no outreach sent."
)

# --- metric tiles ---
scores = [a["score"] for a in agencies]
m1, m2, m3 = st.columns(3)
m1.metric("Agencies scored", len(agencies))
m2.metric("Median score", int(median(scores)))
m3.metric("Above 70", sum(1 for s in scores if s > 70))

st.divider()

# --- filters (top of page, not sidebar) ---
st.markdown("**Filters**")
min_score = st.slider("Minimum fit score", 0, 100, 0, step=1)

known_counts = [a["roster_count"] for a in agencies if a["roster_count"] is not None]
lo, hi = min(known_counts), max(known_counts)
roster_range = st.slider(
    "Roster size (known counts)", 0, hi, (0, hi), step=1,
    help="Agencies that don't publish a roster count are always shown.",
)
show_unknown = st.checkbox("Include agencies with undisclosed roster size", value=True)


def passes(agency):
    if agency["score"] < min_score:
        return False
    rc = agency["roster_count"]
    if rc is None:
        return show_unknown
    return roster_range[0] <= rc <= roster_range[1]


visible = [a for a in agencies if passes(a)]
st.caption(f"Showing {len(visible)} of {len(agencies)} agencies")
st.divider()


def line(label, value):
    st.markdown(
        f"<div class='agency-line'><span class='agency-label'>{label}:</span> {value}</div>",
        unsafe_allow_html=True,
    )


for a in visible:
    title = f"{a['score']} · {a['name']} · {a['hq_short']} · {a['roster_display']}"
    with st.expander(title):
        st.markdown(f"**Why this score.** {a['reasoning']}")

        b = a["score_breakdown"]
        st.markdown(
            f"<div class='agency-line'><span class='agency-label'>Score:</span> "
            f"roster {b['roster_fit']}/30 · ops {b['manual_ops']}/25 · "
            f"managers {b['multi_manager']}/20 · payments {b['payment_complexity']}/15 · "
            f"reach {b['reachability']}/10</div>",
            unsafe_allow_html=True,
        )

        st.markdown("&nbsp;", unsafe_allow_html=True)
        line("Website", f"[{a['website'].replace('https://', '').replace('http://', '')}]({a['website']})")
        line("HQ", a["hq"])
        line("Roster", a["roster_display"])
        line("Team / managers", a["employees"])
        line("Brand inquiries", a["brand_inquiry"])
        line("Named brand partners", a["brand_partners"])

        dm = a["decision_maker"]
        if dm["linkedin"] and dm["linkedin"] != "unknown":
            dm_val = f"{dm['name']} — {dm['title']} ([LinkedIn]({dm['linkedin']}))"
        else:
            dm_val = f"{dm['name']} — {dm['title']} (LinkedIn: unknown)"
        line("Decision maker", dm_val)

        if a.get("flag"):
            st.markdown(f"<div class='flag-note'>Note: {a['flag']}</div>", unsafe_allow_html=True)

        st.markdown("**Sources**")
        for src in a["sources"]:
            st.markdown(
                f"<div class='agency-line'>- [{src.replace('https://', '').replace('http://', '')[:60]}]({src})</div>",
                unsafe_allow_html=True,
            )

        st.markdown("**First-touch email**")
        st.code(a["email"], language=None)

st.divider()

with st.expander("Methodology — rubric, weights, sourcing"):
    st.markdown(
        """
**What this is.** A prospect list for July (withjuly.com), which sells a CRM + media-kit +
payments platform to talent agencies and creator managers who currently run brand deals out of
spreadsheets, DMs, and PDF media kits. The goal was a verifiable artifact: every agency is real and
was confirmed from its live website during research.

**How I sourced.** Web search across creator-economy directories, trade press (Tubefilter, Variety,
Deadline, WWD), and agency listicles produced ~40 candidates. Each was opened and read on its own
live site to confirm it is a *management* agency (represents a roster, negotiates brand deals) — not
a brand-side marketing shop, PR firm, or Hollywood agency. 30 passed; the 15 here are the strongest
ICP fits. Agencies I couldn't fetch cleanly, or that turned out to be OnlyFans/modeling/coaching
shops, were dropped rather than guessed.

**Scoring rubric (0–100).** Each score cites one observed fact.

- **Roster size fit — 30 pts.** 8–40 creators scores highest. Under 5 = likely low budget.
  Over 60 = likely custom/enterprise needs, so it scores lower.
- **Manual-ops evidence — 25 pts.** PDF media kits, "email for rates," single inbox, Google Forms,
  Linktree, no visible deal tracking. More friction = higher score.
- **Multi-manager coordination — 20 pts.** 2+ managers on staff means deal handoffs, splits, and
  commission tracking are already painful.
- **Payment complexity — 15 pts.** Evidence of agency–talent revenue splits, in-house legal/finance,
  or high payout volume.
- **Reachability — 10 pts.** A named decision maker with a public LinkedIn.

**Honesty rules applied.** Any field that couldn't be verified is marked "n/d" / "unknown" rather
than estimated. Recent acquisitions or structural caveats are flagged inline (e.g., Spark Talent
Group was acquired in Jan 2026; Parker is now a Propagate division). No one was contacted — this is
research output only.
        """
    )
