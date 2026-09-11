
import streamlit as st
import pandas as pd
from pathlib import Path
import base64
import html

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
.hero::before{
  content:"🌸";
  position:absolute;
  left:18px;
  top:10px;
  font-size:3.1rem;
  opacity:.9;
}
.hero::after{
  content:"🎀  🌿  🌸";
  position:absolute;
  right:26px;
  top:18px;
  font-size:2rem;
  opacity:.9;
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

def run_search(query, category="All"):
    working = df.copy()
    if category != "All":
        working = working[working["Category"] == category]
    q = (query or "").strip().lower()
    if not q:
        return working
    terms = [t for t in q.replace(","," ").split() if t]
    mask = []
    for _, row in working.iterrows():
        hay = " ".join(str(row[c]) for c in working.columns).lower()
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
    st.markdown("🌸 **Find it. Use it. Don't buy it twice.**")

# -----------------------------
# HERO
# -----------------------------
st.markdown(f"""
<div class="hero">
  {asset_img("header.png", "hero-art", "Craft Stash Finder banner")}
  {asset_img("dragonfly.png", "dragonfly-art", "Dragonfly")}
</div>
""", unsafe_allow_html=True)

# -----------------------------
# PAGES
# -----------------------------
if page == "Find My Stash":
    c1,c2,c3 = st.columns(3)
    c1.metric("Inventory Items", len(df))
    c2.metric("Categories", df["Category"].nunique())
    c3.metric("Storage Units", df["Storage Unit"].nunique())

    st.markdown('<div class="panel"><div class="panel-title">🔎 Search Your Craft Stash</div></div>', unsafe_allow_html=True)

    query = st.text_input(
        "Search",
        placeholder="Try: pink ribbon, brass brads, floral cardstock, glue gun..."
    )

    categories = ["All"] + sorted([x for x in df["Category"].unique() if str(x).strip()])
    category = st.selectbox("Category", categories)

    st.caption("Quick searches")
    qcols = st.columns(5)
    quick = [
        ("Cardstock", "cat_cardstock.png"),
        ("Ribbon", "cat_ribbon.png"),
        ("Embellishments", "cat_embellishments.png"),
        ("Tools", "cat_tools.png"),
        ("Equipment", "cat_machines.png"),
    ]
    selected_quick = None
    for col, (label, graphic) in zip(qcols, quick):
        with col:
            st.markdown(
                f'<div class="quick-card">{asset_img(graphic, "quick-art", label)}</div>',
                unsafe_allow_html=True
            )
            if st.button(label, key=f"quick_{label}"):
                selected_quick = label

    effective_query = selected_quick if selected_quick else query
    results = run_search(effective_query, category)

    if effective_query:
        st.markdown("### Results")
        if len(results) == 0:
            st.warning("I couldn't confirm a match in the current inventory. Try a broader term or check whether the item has been inventoried yet.")
        else:
            st.success(f"Found {len(results)} matching item{'s' if len(results)!=1 else ''}.")
            for _,row in results.head(50).iterrows():
                show_card(row)
    else:
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

    st.dataframe(filtered, use_container_width=True, hide_index=True)

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
