# July — Talent Agency Prospect List

A cold-email artifact for a GTM application to [July](https://withjuly.com): 15 real
creator/talent-management agencies scored for fit with July's CRM + media-kit + payments platform,
each with a drafted first-touch email.

- Every agency was verified from its live website during research. Unverifiable fields are marked
  "unknown" / "n/d" rather than estimated. No agency, person, number, or URL is invented.
- Data lives in `agencies.json`, loaded with `@st.cache_data`.
- Mobile-first: expanders only (no wide tables), dark theme, Streamlit chrome removed.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy

Streamlit Community Cloud → point it at this repo, branch `main`, main file `app.py`.

Research output only. No outreach was sent.
