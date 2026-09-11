
import streamlit as st
import pandas as pd
from pathlib import Path

st.set_page_config(
    page_title="Craft Stash Finder",
    page_icon="🎀",
    layout="wide",
)

# ---------- Styling ----------
st.markdown("""
<style>
:root {
    --pink: #d95f9f;
    --deep-pink: #b54784;
    --soft-pink: #fff1f7;
    --blush: #f8d7e8;
    --cream: #fffaf5;
    --text: #3d2b36;
    --muted: #7a6570;
    --border: #ecd3df;
}

.stApp {
    background: linear-gradient(180deg, #fffafd 0%, #fff8fb 100%);
    color: var(--text);
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1250px;
}

h1, h2, h3 {
    color: var(--text);
}

.hero {
    background: linear-gradient(135deg, #ffe4f0 0%, #fff7fb 55%, #f8e7f0 100%);
    border: 1px solid var(--border);
    border-radius: 22px;
    padding: 28px 30px;
    margin-bottom: 20px;
    box-shadow: 0 7px 22px rgba(181, 71, 132, 0.08);
}
.hero-title {
    font-size: 2.2rem;
    font-weight: 800;
    margin: 0;
    color: #8f3569;
}
.hero-sub {
    font-size: 1.03rem;
    color: var(--muted);
    margin-top: 6px;
}
.tagline {
    display: inline-block;
    background: white;
    color: #9a3e72;
    border: 1px solid #edbfd6;
    border-radius: 999px;
    padding: 6px 12px;
    margin-top: 12px;
    font-weight: 600;
}

.result-card {
    background: #ffffff;
    border: 1px solid var(--border);
    border-left: 6px solid var(--pink);
    border-radius: 16px;
    padding: 16px 18px;
    margin: 10px 0;
    box-shadow: 0 4px 14px rgba(181, 71, 132, 0.06);
}
.result-title {
    font-size: 1.12rem;
    font-weight: 750;
    color: #87345f;
    margin-bottom: 6px;
}
.result-meta {
    color: #5f4a55;
    line-height: 1.55;
}
.small-muted {
    color: var(--muted);
    font-size: 0.9rem;
}

div[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid var(--border);
    padding: 12px;
    border-radius: 14px;
}

section[data-testid="stSidebar"] {
    background: #fff2f8;
    border-right: 1px solid var(--border);
}

.stButton > button {
    border-radius: 12px;
    border: 1px solid #e6b8d0;
    background: #fff7fb;
    color: #8f3569;
    font-weight: 650;
}
.stButton > button:hover {
    border-color: #d95f9f;
    color: #6f2450;
}
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
@st.cache_data
def load_inventory():
    path = Path(__file__).parent / "Craft_Stash_Finder_Inventory.csv"
    df = pd.read_csv(path).fillna("")
    # Normalize expected columns
    expected = ["Area", "Storage Unit", "Shelf/Container", "Category", "Item", "Theme/Design", "Notes"]
    for col in expected:
        if col not in df.columns:
            df[col] = ""
    return df[expected]

df = load_inventory()

# ---------- Helpers ----------
def searchable_text(row):
    return " ".join(str(row[c]) for c in df.columns).lower()

def run_search(query, category="All"):
    working = df.copy()
    if category != "All":
        working = working[working["Category"] == category]

    q = (query or "").strip().lower()
    if not q:
        return working

    terms = [t for t in q.replace(",", " ").split() if t]
    mask = []
    for _, row in working.iterrows():
        hay = " ".join(str(row[c]) for c in working.columns).lower()
        mask.append(all(term in hay for term in terms))
    return working[pd.Series(mask, index=working.index)]

def show_card(row):
    location_parts = [row["Area"], row["Storage Unit"], row["Shelf/Container"]]
    location = " → ".join([x for x in location_parts if str(x).strip()])
    theme = row["Theme/Design"] if row["Theme/Design"] else "—"
    notes = row["Notes"] if row["Notes"] else "—"

    st.markdown(
        f"""
        <div class="result-card">
            <div class="result-title">✨ {row['Item']}</div>
            <div class="result-meta">
                <b>Category:</b> {row['Category']}<br>
                <b>Theme/Design:</b> {theme}<br>
                <b>Location:</b> {location if location else 'Not listed'}<br>
                <b>Notes:</b> {notes}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------- Sidebar ----------
with st.sidebar:
    st.markdown("## 🎀 Craft Stash Finder")
    st.caption("Find it. Use it. Don’t buy it twice.")
    page = st.radio(
        "Navigate",
        ["Find My Stash", "Browse Inventory", "Storage Map", "About"],
        index=0
    )
    st.markdown("---")
    st.caption("Inventory source")
    st.write(f"**{len(df)} items** loaded from your CSV")

# ---------- Main ----------
if page == "Find My Stash":
    st.markdown("""
    <div class="hero">
        <div class="hero-title">Craft Stash Finder</div>
        <div class="hero-sub">Search your real craft inventory by item, color, theme, category, cart, shelf, or container.</div>
        <div class="tagline">Find it. Use it. Don’t buy it twice.</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    c1.metric("Inventory items", len(df))
    c2.metric("Categories", df["Category"].nunique())
    c3.metric("Storage units", df["Storage Unit"].nunique())

    st.markdown("### 🔎 What are you looking for?")
    query = st.text_input(
        "Search your stash",
        placeholder="Try: pink ribbon, brass brads, floral cardstock, glue gun..."
    )

    categories = ["All"] + sorted([x for x in df["Category"].unique() if str(x).strip()])
    category = st.selectbox("Optional category filter", categories)

    # Quick searches
    st.caption("Quick searches")
    qcols = st.columns(5)
    quick = ["Cardstock", "Ribbon", "Embellishments", "Tools", "Equipment"]
    selected_quick = None
    for col, label in zip(qcols, quick):
        if col.button(label, use_container_width=True):
            selected_quick = label

    effective_query = selected_quick if selected_quick else query
    results = run_search(effective_query, category)

    if effective_query:
        st.markdown(f"### Results")
        if len(results) == 0:
            st.warning(
                "I couldn't confirm a match in the current inventory. "
                "Try a broader word, another color/theme, or check whether the item has been inventoried yet."
            )
        else:
            st.success(f"Found {len(results)} matching item{'s' if len(results) != 1 else ''}.")
            for _, row in results.head(50).iterrows():
                show_card(row)
            if len(results) > 50:
                st.info(f"Showing the first 50 of {len(results)} matches.")
    else:
        st.info("Enter a search above, or use one of the quick-search buttons.")

elif page == "Browse Inventory":
    st.markdown("## 📋 Browse Inventory")
    st.caption("Filter and browse everything currently in Craft Stash Finder.")

    c1, c2 = st.columns(2)
    category_values = ["All"] + sorted([x for x in df["Category"].unique() if str(x).strip()])
    storage_values = ["All"] + sorted([x for x in df["Storage Unit"].unique() if str(x).strip()])

    with c1:
        cat = st.selectbox("Category", category_values, key="browse_cat")
    with c2:
        storage = st.selectbox("Storage Unit", storage_values, key="browse_storage")

    filtered = df.copy()
    if cat != "All":
        filtered = filtered[filtered["Category"] == cat]
    if storage != "All":
        filtered = filtered[filtered["Storage Unit"] == storage]

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Area": st.column_config.TextColumn(width="small"),
            "Storage Unit": st.column_config.TextColumn(width="medium"),
            "Shelf/Container": st.column_config.TextColumn(width="medium"),
            "Category": st.column_config.TextColumn(width="medium"),
            "Item": st.column_config.TextColumn(width="large"),
            "Theme/Design": st.column_config.TextColumn(width="medium"),
            "Notes": st.column_config.TextColumn(width="large"),
        }
    )

elif page == "Storage Map":
    st.markdown("## 📦 Storage Map")
    st.caption("See what is stored in each location.")

    units = [x for x in df["Storage Unit"].unique() if str(x).strip()]
    selected_unit = st.selectbox("Choose a storage unit", sorted(units))

    unit_df = df[df["Storage Unit"] == selected_unit].copy()
    shelves = [x for x in unit_df["Shelf/Container"].unique() if str(x).strip()]

    for shelf in sorted(shelves):
        with st.expander(f"📍 {selected_unit} — {shelf}", expanded=False):
            subset = unit_df[unit_df["Shelf/Container"] == shelf]
            for _, row in subset.iterrows():
                st.write(f"• **{row['Item']}** — {row['Category']}")

elif page == "About":
    st.markdown("## 💗 About Craft Stash Finder")
    st.write(
        """
        **Craft Stash Finder** is a searchable inventory prototype designed to answer a very practical question:
        **“Do I already own this, and where did I put it?”**

        The app uses a structured craft-room inventory as its source of truth. Search results are grounded in that
        inventory rather than generated from guesses. If an item is not found, the app says it cannot confirm the item
        instead of pretending it exists.

        This Streamlit version is a visual, interactive front end for the same inventory concept tested in NotebookLM.
        """
    )
