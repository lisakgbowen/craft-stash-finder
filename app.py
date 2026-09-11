
import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html
import re

st.set_page_config(
    page_title="Craft Stash Finder",
    page_icon="🎀",
    layout="wide",
)


# -----------------------------
# GRAPHIC ASSETS
# -----------------------------
BASE_DIR = Path(__file__).parent
ASSET_DIR = BASE_DIR / "assets"

def asset_data_uri(filename):
    """Return a local PNG as a browser-safe data URI."""
    path = ASSET_DIR / filename
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"

def asset_img(filename, css_class="", alt=""):
    uri = asset_data_uri(filename)
    if not uri:
        return ""
    return f'<img class="{css_class}" src="{uri}" alt="{html.escape(alt)}">'

# -----------------------------
# THEME / STYLING
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');

:root{
  --rose:#c74d7f;
  --rose-dark:#91345f;
  --pink:#f7c9dc;
  --blush:#fff1f6;
  --cream:#fffaf4;
  --sage:#dfe9dd;
  --gold:#c99148;
  --ink:#20324a;
  --muted:#796a73;
  --line:#ead7df;
}

.stApp {
  background:
    radial-gradient(circle at 4% 8%, rgba(247,201,220,.40) 0 85px, transparent 86px),
    radial-gradient(circle at 95% 6%, rgba(223,233,221,.55) 0 75px, transparent 76px),
    linear-gradient(180deg,#fffdfb 0%,#fff8fb 100%);
  color:var(--ink);
  font-family:'DM Sans', sans-serif;
}

.block-container {
  max-width: 1280px;
  padding-top: 1rem;
  padding-bottom: 3rem;
}

h1,h2,h3,h4 {
  font-family:'Playfair Display', serif;
  color:var(--ink);
}

/* Sidebar */
section[data-testid="stSidebar"] {
  background: linear-gradient(180deg,#fdebf3 0%,#fff7fb 100%);
  border-right:1px solid var(--line);
}
section[data-testid="stSidebar"] .stRadio > label{
  font-weight:700;
  color:var(--rose-dark);
}

/* Hero */
.hero{
  position:relative;
  overflow:hidden;
  background:
    linear-gradient(135deg,#fff8fb 0%,#ffeaf3 55%,#f9eee8 100%);
  border:1px solid #ebccd8;
  border-radius:26px;
  padding:34px 34px 30px;
  margin-bottom:18px;
  box-shadow:0 12px 28px rgba(173,86,125,.10);
}

}

}
.brandline{
  color:var(--rose-dark);
  font-family:'Playfair Display', serif;
  font-size:2.6rem;
  font-weight:700;
  text-align:center;
  margin:0;
}
.byline{
  text-align:center;
  font-size:1.05rem;
  color:#5f4a55;
  margin-top:2px;
}
.tagline{
  text-align:center;
  color:#8a6576;
  text-transform:uppercase;
  letter-spacing:.20em;
  font-size:.78rem;
  margin-top:8px;
  font-weight:600;
}

/* Metric cards */
div[data-testid="stMetric"]{
  background:rgba(255,255,255,.94);
  border:1px solid var(--line);
  padding:16px 18px;
  border-radius:18px;
  box-shadow:0 5px 14px rgba(173,86,125,.07);
}

/* Search section */
.panel{
  background:rgba(255,255,255,.94);
  border:1px solid var(--line);
  border-radius:20px;
  padding:18px 20px;
  box-shadow:0 6px 16px rgba(173,86,125,.06);
  margin:10px 0 16px;
}
.panel-title{
  font-family:'Playfair Display', serif;
  font-size:1.4rem;
  font-weight:700;
  color:var(--ink);
  margin-bottom:6px;
}

/* Result cards */
.result-card{
  background:#fff;
  border:1px solid var(--line);
  border-left:6px solid var(--rose);
  border-radius:18px;
  padding:16px 18px;
  margin:10px 0;
  box-shadow:0 6px 16px rgba(173,86,125,.06);
}
.result-title{
  font-family:'Playfair Display', serif;
  color:var(--rose-dark);
  font-size:1.12rem;
  font-weight:700;
  margin-bottom:7px;
}
.result-meta{
  color:#56454f;
  line-height:1.55;
}

/* Buttons */
.stButton > button{
  width:100%;
  border-radius:13px;
  border:1px solid #e3afc7;
  background:linear-gradient(180deg,#fff7fb 0%,#fde6f0 100%);
  color:var(--rose-dark);
  font-weight:700;
}
.stButton > button:hover{
  border-color:var(--rose);
  color:#6f244b;
  box-shadow:0 4px 12px rgba(199,77,127,.12);
}

/* Inputs */
div[data-baseweb="input"] > div,
div[data-baseweb="select"] > div{
  border-radius:13px !important;
}

/* Footer */
.footer{
  margin-top:28px;
  padding:18px 10px 8px;
  text-align:center;
  color:#8a6576;
  border-top:1px solid var(--line);
}
.footer .flourish{
  font-size:1.5rem;
  letter-spacing:10px;
  margin-bottom:5px;
}
.footer b{
  color:var(--rose-dark);
}

/* Real artwork from /assets */
.hero-art{
  width:100%;
  max-height:170px;
  object-fit:cover;
  object-position:center;
  display:block;
  border-radius:18px;
  margin:0 auto 10px;
}
.dragonfly-art{
  position:absolute;
  right:24px;
  bottom:12px;
  width:92px;
  max-height:70px;
  object-fit:contain;
  mix-blend-mode:multiply;
}
.sidebar-art{
  display:block;
  width:100%;
  max-width:220px;
  max-height:130px;
  object-fit:contain;
  margin:4px auto 10px;
}
.quick-art{
  display:block;
  width:100%;
  max-width:180px;
  height:95px;
  object-fit:contain;
  margin:0 auto 8px;
}
.quick-card{
  background:#fff;
  border:1px solid var(--line);
  border-radius:18px;
  padding:10px 10px 2px;
  min-height:112px;
  box-shadow:0 5px 14px rgba(173,86,125,.06);
  margin-bottom:6px;
  text-align:center;
}
.footer-divider{
  display:block;
  max-width:420px;
  width:70%;
  max-height:90px;
  object-fit:contain;
  margin:0 auto 4px;
}

/* Mobile improvements */
@media (max-width: 700px) {
  .block-container {
    padding-left: 0.8rem;
    padding-right: 0.8rem;
    padding-top: 0.5rem;
  }
  .hero {
    padding: 14px;
    border-radius: 18px;
  }
  .result-card {
    padding: 14px;
    overflow-wrap: anywhere;
  }
  .result-meta {
    font-size: 0.95rem;
  }
  .quick-card {
    min-height: 90px;
  }
  .quick-art {
    height: 72px;
  }
}


/* Force Streamlit text to remain readable on light cards, including mobile */
div[data-testid="stMetric"] label,
div[data-testid="stMetric"] [data-testid="stMetricLabel"],
div[data-testid="stMetric"] [data-testid="stMetricValue"],
div[data-testid="stMetric"] p,
.stTextInput label,
.stSelectbox label,
.stForm label,
.stCaptionContainer,
.stMarkdown,
.stMarkdown p {
  color: var(--ink) !important;
}

/* Input/select text and placeholders */
input,
div[data-baseweb="select"] *,
div[data-baseweb="input"] * {
  color: var(--ink) !important;
}

input::placeholder {
  color: #796a73 !important;
  opacity: 1 !important;
}

/* Keep button text readable */
.stButton > button,
.stFormSubmitButton > button {
  color: var(--rose-dark) !important;
}

/* Extra protection for small screens */
@media (max-width: 700px) {
  div[data-testid="stMetric"] label,
  div[data-testid="stMetric"] [data-testid="stMetricLabel"],
  div[data-testid="stMetric"] [data-testid="stMetricValue"],
  .stTextInput label,
  .stSelectbox label,
  .stForm label,
  .stCaptionContainer {
    color: #20324a !important;
    opacity: 1 !important;
  }
}


/* Keep Streamlit form controls light and readable on phones and in dark browser themes */
div[data-testid="stTextInput"] div[data-baseweb="input"],
div[data-testid="stTextInput"] div[data-baseweb="input"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] [role="combobox"] {
  background:#ffffff !important;
  background-color:#ffffff !important;
  color:#20324a !important;
  -webkit-text-fill-color:#20324a !important;
  opacity:1 !important;
}

div[data-testid="stTextInput"] input::placeholder {
  color:#796a73 !important;
  -webkit-text-fill-color:#796a73 !important;
  opacity:1 !important;
}

div[data-testid="stSelectbox"] div[data-baseweb="select"] *,
div[data-testid="stSelectbox"] [role="combobox"] *,
div[data-testid="stSelectbox"] svg {
  color:#20324a !important;
  fill:#20324a !important;
  -webkit-text-fill-color:#20324a !important;
}

/* Selectbox popup is rendered in a portal, so style it separately */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
li[role="option"] {
  background:#ffffff !important;
  background-color:#ffffff !important;
  color:#20324a !important;
  -webkit-text-fill-color:#20324a !important;
}
li[role="option"]:hover,
li[role="option"][aria-selected="true"] {
  background:#fff1f6 !important;
  color:#20324a !important;
}

/* Help mobile Safari/Chrome honor the intended light form-control palette */
.stApp {
  color-scheme: light;
}



/* Improve button contrast on mobile/desktop */
.stButton > button,
.stFormSubmitButton > button,
button[kind="primary"],
button[kind="secondary"] {
  background-color: #f2d6df !important;
  color: #20324a !important;
  border: 1px solid #c78fa4 !important;
  font-weight: 700 !important;
}

.stButton > button:hover,
.stFormSubmitButton > button:hover,
button[kind="primary"]:hover,
button[kind="secondary"]:hover {
  background-color: #e9c4d1 !important;
  color: #20324a !important;
  border-color: #b67990 !important;
}

/* Make warning/info/success messages readable on phone themes */
div[data-testid="stAlert"] *,
div[data-testid="stAlert"] p,
div[data-testid="stAlert"] span,
div[data-testid="stAlert"] div {
  color: #20324a !important;
  opacity: 1 !important;
}

/* Keep the warning box light with dark text */
div[data-testid="stAlert"] {
  color: #20324a !important;
}

/* Extra mobile protection */
@media (max-width: 700px) {
  .stButton > button,
  .stFormSubmitButton > button,
  button[kind="primary"],
  button[kind="secondary"] {
    background-color: #f2d6df !important;
    color: #20324a !important;
    -webkit-text-fill-color: #20324a !important;
  }

  div[data-testid="stAlert"] *,
  div[data-testid="stAlert"] p,
  div[data-testid="stAlert"] span,
  div[data-testid="stAlert"] div {
    color: #20324a !important;
    -webkit-text-fill-color: #20324a !important;
    opacity: 1 !important;
  }
}



/* Clickable dashboard summary cards */
button[data-testid="stBaseButton-secondary"]:has(p:first-child) {
  min-height: 96px;
}

/* The first three dashboard buttons inherit the app palette; ensure their
   multi-line labels remain readable and centered on phones too. */
div[data-testid="stColumn"] .stButton > button p {
  white-space: pre-line !important;
  text-align: center !important;
  line-height: 1.35 !important;
  color: #20324a !important;
  -webkit-text-fill-color: #20324a !important;
}

@media (max-width: 700px) {
  div[data-testid="stColumn"] .stButton > button {
    min-height: 88px !important;
    padding: 0.65rem 0.45rem !important;
  }
  div[data-testid="stColumn"] .stButton > button p {
    font-size: 0.93rem !important;
  }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# DATA
# -----------------------------
@st.cache_data
def load_inventory():
    path = Path(__file__).parent / "Craft_Stash_Finder_Inventory.csv"
    df = pd.read_csv(path).fillna("")
    expected = ["Area","Storage Unit","Shelf/Container","Category","Item","Theme/Design","Notes"]
    for c in expected:
        if c not in df.columns:
            df[c] = ""
    return df[expected]

df = load_inventory()


QUESTION_STOPWORDS = {
    "a","an","any","are","can","could","do","does","for","have","how","i","in",
    "is","it","me","my","of","please","put","should","the","there","to","where",
    "which","what","whats","what's","would","you","your","back","return","go"
}


# These words help rank close alternatives, but suggestions are ONLY returned
# when a matching item actually exists in the inventory.
ALTERNATIVE_TERMS = {
    "pumpkin": ["orange"],
    "scarlet": ["red"],
    "crimson": ["red"],
    "burgundy": ["red"],
    "navy": ["blue"],
    "aqua": ["blue", "teal"],
    "turquoise": ["teal", "blue"],
    "fuchsia": ["pink"],
    "magenta": ["pink"],
    "lavender": ["purple"],
    "violet": ["purple"],
    "ivory": ["cream", "white"],
    "beige": ["kraft", "tan", "brown"],
}

def inventory_text(row):
    return " ".join(str(row[c]) for c in df.columns).lower()

def find_alternatives(query, category="All", limit=3):
    """Find close, inventory-backed alternatives when an exact search has no match."""
    working = df.copy()
    if category != "All":
        working = working[working["Category"] == category]

    cleaned, _ = parse_inventory_question(query)
    terms = [t for t in cleaned.split() if t]
    if not terms:
        return working.iloc[0:0]

    # Recognize category/item-type words from the actual inventory itself.
    category_terms = set()
    for cat in df["Category"].astype(str):
        category_terms.update(re.findall(r"[a-z0-9]+", cat.lower()))

    # First narrow to rows that share the requested category/type when possible.
    type_terms = [t for t in terms if t in category_terms]
    candidates = working
    if type_terms:
        mask = []
        for _, row in candidates.iterrows():
            hay = inventory_text(row)
            mask.append(all(t in hay for t in type_terms))
        candidates = candidates[pd.Series(mask, index=candidates.index)]

    if len(candidates) == 0:
        return candidates

    scored = []
    for idx, row in candidates.iterrows():
        hay = inventory_text(row)
        score = 0

        # Reward requested words already shared with a candidate.
        for t in terms:
            if t in hay:
                score += 2

        # Strongly reward a known close descriptor, e.g. pumpkin -> orange.
        for t in terms:
            for alt in ALTERNATIVE_TERMS.get(t, []):
                if alt in hay:
                    score += 8

        # Prefer rows whose category/type matches the request.
        for t in type_terms:
            if t in hay:
                score += 3

        if score > 0:
            scored.append((score, idx))

    if not scored:
        return candidates.head(limit)

    scored.sort(key=lambda x: (-x[0], x[1]))
    best_score = scored[0][0]

    # If a strong synonym match exists, show only equally strong close options.
    strong = [(s, i) for s, i in scored if s >= best_score - 1]
    chosen = strong[:limit] if best_score >= 8 else scored[:limit]
    return df.loc[[idx for _, idx in chosen]]

def parse_inventory_question(query):
    """Turn a natural-language inventory question into useful search terms."""
    raw = (query or "").strip()
    lower = raw.lower()

    # Identify questions about returning an item to its designated home.
    return_intent = bool(re.search(
        r"\b(return|put\s+.*\bback|where\s+should\s+.*\bgo|where\s+do\s+i\s+put)\b",
        lower
    ))

    # Keep letters/numbers plus common item punctuation, then remove conversational filler.
    cleaned = re.sub(r"[^a-z0-9&+\-/' ]+", " ", lower)
    tokens = [t.strip("'") for t in cleaned.split()]
    meaningful = [t for t in tokens if t and t not in QUESTION_STOPWORDS]

    return " ".join(meaningful), return_intent

def run_search(query, category="All"):
    working = df.copy()
    if category != "All":
        working = working[working["Category"] == category]

    q, _ = parse_inventory_question(query)
    if not q:
        return working

    terms = [t for t in q.split() if t]
    mask = []
    for _, row in working.iterrows():
        hay = " ".join(str(row[c]) for c in working.columns).lower()
        # All meaningful item/location terms must be present somewhere in the row.
        mask.append(all(term in hay for term in terms))

    return working[pd.Series(mask, index=working.index)]

def show_card(row):
    loc = " → ".join([x for x in [row["Area"], row["Storage Unit"], row["Shelf/Container"]] if str(x).strip()])
    theme = row["Theme/Design"] if row["Theme/Design"] else "—"
    notes = row["Notes"] if row["Notes"] else "—"
    st.markdown(f"""
    <div class="result-card">
      <div class="result-title">🌸 {row['Item']}</div>
      <div class="result-meta">
        <b>Category:</b> {row['Category']}<br>
        <b>Theme/Design:</b> {theme}<br>
        <b>Location:</b> {loc if loc else 'Not listed'}<br>
        <b>Notes:</b> {notes}
      </div>
    </div>
    """, unsafe_allow_html=True)

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown(asset_img("sidebar_flower.png", "sidebar-art", "Floral and ribbon decoration"), unsafe_allow_html=True)
    st.markdown("## Craft Stash Finder")
    st.caption("by Handmade with Love and Crunchies by Lisa")
    page = st.radio(
        "Navigate",
        ["Find My Stash","Browse Inventory","Storage Map","About"],
        index=0
    )
    st.markdown("---")
    st.caption(f"📦 {len(df)} inventory items loaded")
    st.markdown(asset_img("sidebar_quote.png", "sidebar-art", "Craft stash motto"), unsafe_allow_html=True)
   
# -----------------------------
# HERO
# -----------------------------
st.markdown(f"""
<div class="hero">
  {asset_img("header.png", "hero-art", "Craft Stash Finder banner")}
 
</div>
""", unsafe_allow_html=True)

# -----------------------------
# PAGES
# -----------------------------
if page == "Find My Stash":
    # Clickable dashboard summary cards work on desktop and mobile.
    if "summary_view" not in st.session_state:
        st.session_state.summary_view = None

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            f"📦 Inventory Items\n\n{len(df)}",
            key="summary_inventory",
            use_container_width=True
        ):
            st.session_state.summary_view = (
                None if st.session_state.summary_view == "inventory" else "inventory"
            )

    with c2:
        if st.button(
            f"🏷️ Categories\n\n{df['Category'].nunique()}",
            key="summary_categories",
            use_container_width=True
        ):
            st.session_state.summary_view = (
                None if st.session_state.summary_view == "categories" else "categories"
            )

    with c3:
        if st.button(
            f"🗄️ Storage Units\n\n{df['Storage Unit'].nunique()}",
            key="summary_storage",
            use_container_width=True
        ):
            st.session_state.summary_view = (
                None if st.session_state.summary_view == "storage" else "storage"
            )

    # Expand the selected summary directly below the dashboard cards.
    if st.session_state.summary_view == "inventory":
        st.markdown("### 📦 All Inventory Items")
        st.caption(f"{len(df)} inventory entries")
        for _, row in df.sort_values(["Category", "Item"]).iterrows():
            show_card(row)

    elif st.session_state.summary_view == "categories":
        st.markdown("### 🏷️ Categories")
        category_counts = (
            df[df["Category"].astype(str).str.strip() != ""]
            .groupby("Category")
            .size()
            .sort_index()
        )
        for category_name, count in category_counts.items():
            with st.expander(f"{category_name} ({count})"):
                rows = df[df["Category"] == category_name].sort_values("Item")
                for _, row in rows.iterrows():
                    show_card(row)

    elif st.session_state.summary_view == "storage":
        st.markdown("### 🗄️ Storage Units")
        storage_values = sorted(
            [x for x in df["Storage Unit"].unique() if str(x).strip()]
        )
        for unit in storage_values:
            rows = df[df["Storage Unit"] == unit].sort_values(
                ["Area", "Shelf/Container", "Item"]
            )
            with st.expander(f"{unit} ({len(rows)})"):
                for _, row in rows.iterrows():
                    show_card(row)

    st.markdown('<div class="panel"><div class="panel-title">🔎 Search Your Craft Stash</div></div>', unsafe_allow_html=True)

    categories = ["All"] + sorted([x for x in df["Category"].unique() if str(x).strip()])

    # Search form. Results are deliberately rendered immediately below this
    # form after submission so phone users do not need JavaScript auto-scroll.
    with st.form("stash_search_form", clear_on_submit=False):
        query = st.text_input(
            "Search",
            placeholder="Ask: Where do I return my glue gun? Do I have pink ribbon?..."
        )
        category = st.selectbox("Category", categories)
        submitted = st.form_submit_button("🔎 Search", use_container_width=True)

    # Store an active search across Streamlit reruns. Quick-search buttons set
    # the same state and rerun once, which moves their results directly below
    # the form instead of leaving them below all the quick-search artwork.
    if submitted:
        st.session_state["active_stash_query"] = query
        st.session_state["active_stash_category"] = category

    active_query = st.session_state.get("active_stash_query", "")
    active_category = st.session_state.get("active_stash_category", category)

    if active_query:
        results = run_search(active_query, active_category)
        _, return_intent = parse_inventory_question(active_query)

        st.markdown("### Results")
        if len(results) == 0:
            alternatives = find_alternatives(active_query, active_category)

            # State clearly that the requested item was not found, then offer
            # only related items that truly exist in this inventory.
            cleaned_query, _ = parse_inventory_question(active_query)
            requested = cleaned_query if cleaned_query else active_query.strip()

            if len(alternatives) == 0:
                st.warning(f"I don't see **{requested}** in the current inventory, and I couldn't confirm a related alternative.")
            else:
                st.warning(f"I don't see **{requested}** in the current inventory.")
                st.markdown("#### You may already have a close alternative:")
                for _, row in alternatives.iterrows():
                    loc = " → ".join([
                        str(x) for x in [row["Area"], row["Storage Unit"], row["Shelf/Container"]]
                        if str(x).strip()
                    ])
                    note = f" — **{row['Notes']}**" if str(row["Notes"]).strip() else ""
                    st.info(f"**{row['Item']}** — {loc if loc else 'Location not listed'}{note}")
                    show_card(row)
        else:
            if return_intent:
                if len(results) == 1:
                    row = results.iloc[0]
                    loc = " → ".join([
                        str(x) for x in [row["Area"], row["Storage Unit"], row["Shelf/Container"]]
                        if str(x).strip()
                    ])
                    st.success(f"Put **{row['Item']}** back at: **{loc if loc else 'Location not listed'}**")
                else:
                    st.info("I found more than one possible match. Here are the designated locations for each one.")
                    for _, row in results.head(50).iterrows():
                        loc = " → ".join([
                            str(x) for x in [row["Area"], row["Storage Unit"], row["Shelf/Container"]]
                            if str(x).strip()
                        ])
                        st.markdown(f"**{row['Item']}** → {loc if loc else 'Location not listed'}")
            else:
                st.success(f"Found {len(results)} matching item{'s' if len(results)!=1 else ''}.")

            for _, row in results.head(50).iterrows():
                show_card(row)

        if st.button("← New search / show Quick Searches", key="clear_active_search"):
            st.session_state.pop("active_stash_query", None)
            st.session_state.pop("active_stash_category", None)
            st.rerun()

    else:
        st.caption("Quick searches")
        qcols = st.columns(5)
        quick = [
            ("Cardstock", "cat_cardstock.png"),
            ("Ribbon", "cat_ribbon.png"),
            ("Embellishments", "cat_embellishments.png"),
            ("Tools", "cat_tools.png"),
            ("Equipment", "cat_machines.png"),
        ]
        for col, (label, graphic) in zip(qcols, quick):
            with col:
                st.markdown(
                    f'<div class="quick-card">{asset_img(graphic, "quick-art", label)}</div>',
                    unsafe_allow_html=True
                )
                if st.button(label, key=f"quick_{label}"):
                    st.session_state["active_stash_query"] = label
                    st.session_state["active_stash_category"] = category
                    st.rerun()

        st.info("Enter a search above, or use a quick-search button.")

elif page == "Browse Inventory":
    st.markdown("## 📋 Browse Inventory")
    st.caption("Filter and browse everything currently in your stash.")

    c1,c2 = st.columns(2)
    cats = ["All"] + sorted([x for x in df["Category"].unique() if str(x).strip()])
    units = ["All"] + sorted([x for x in df["Storage Unit"].unique() if str(x).strip()])

    with c1:
        cat = st.selectbox("Category", cats, key="browse_cat")
    with c2:
        storage = st.selectbox("Storage Unit", units, key="browse_storage")

    filtered = df.copy()
    if cat != "All":
        filtered = filtered[filtered["Category"] == cat]
    if storage != "All":
        filtered = filtered[filtered["Storage Unit"] == storage]

    st.caption(f"Showing {len(filtered)} item{'s' if len(filtered) != 1 else ''}.")

    # Responsive cards keep every important field visible on phones. A wide
    # dataframe forces users to scroll sideways and can make columns look
    # missing on small screens.
    if len(filtered) == 0:
        st.info("No inventory items match these filters.")
    else:
        for _, row in filtered.iterrows():
            show_card(row)

elif page == "Storage Map":
    st.markdown("## 📦 Storage Map")
    st.caption("See what is stored in each cart, shelf, or container.")
    st.markdown(asset_img("cat_storage.png", "sidebar-art", "Craft storage"), unsafe_allow_html=True)

    units = [x for x in df["Storage Unit"].unique() if str(x).strip()]
    selected_unit = st.selectbox("Choose a storage unit", sorted(units))
    unit_df = df[df["Storage Unit"] == selected_unit].copy()
    shelves = [x for x in unit_df["Shelf/Container"].unique() if str(x).strip()]

    for shelf in sorted(shelves):
        with st.expander(f"🎀 {selected_unit} — {shelf}"):
            subset = unit_df[unit_df["Shelf/Container"] == shelf]
            for _,row in subset.iterrows():
                st.write(f"• **{row['Item']}** — {row['Category']}")

elif page == "About":
    ac1, ac2 = st.columns(2)
    with ac1:
        st.markdown(asset_img("jar.png", "sidebar-art", "Craft supply jar"), unsafe_allow_html=True)
    with ac2:
        st.markdown(asset_img("books.png", "sidebar-art", "Craft books"), unsafe_allow_html=True)
    st.markdown("## 💗 About Craft Stash Finder")
    st.write("""
    **Craft Stash Finder** helps answer a simple but expensive question:
    **“Do I already own this, and where did I put it?”**

    This interactive prototype searches a structured craft-room inventory and returns
    the item's category, theme/design, and exact storage location. If the inventory
    cannot confirm an item, the app says so rather than inventing an answer.
    """)

st.markdown(f"""
<div class="footer">
  {asset_img("bottom_divider.png", "footer-divider", "Floral ribbon divider")}
  <b>Handmade with Love and Crunchies by Lisa</b><br>
  Craft • Create • Be Happy
</div>
""", unsafe_allow_html=True)
