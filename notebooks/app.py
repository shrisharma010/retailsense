import streamlit as st
import pandas as pd
# import seaborn as sns
import matplotlib.pyplot as plt

import sys
sys.path.append(".")
from utils import calculate_revenue, classify_customer

st.set_page_config(page_title="RetailSense Analytics Dashboard", layout="wide")
st.title("🛒 RetailSense Analytics Dashboard")

# ── Load Data ────────────────────────────────────────────────────────
@st.cache_data
def load():
    customers = pd.read_csv("outputs/cleaned_customers.csv")
    orders    = pd.read_csv("data/orders.csv")
    products  = pd.read_csv("data/products.csv")
    products["price"] = pd.to_numeric(
        products["price"].astype(str).str.replace("₹","").str.strip(), errors="coerce")
    products["rating"].fillna(products["rating"].mean(), inplace=True)
    merged = orders.merge(customers, on="customer_id", how="inner")
    full   = merged.merge(products, on="product_id", how="inner")
    full["revenue"] = full.apply(
        lambda r: calculate_revenue(r["price"], r["quantity"], r["discount_pct"]), axis=1)
    return full, products

full_df, products_df = load()

# ── Sidebar ───────────────────────────────────────────────────────────
st.sidebar.header("Filters")
categories = ["All"] + list(full_df["category"].dropna().unique())
selected_cat = st.sidebar.selectbox("Category", categories)
min_rating   = st.sidebar.slider("Minimum Product Rating", 1.0, 5.0, 1.0, 0.1)

# Apply filters
filtered = full_df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["category"] == selected_cat]
filtered = filtered[filtered["rating"] >= min_rating]

# ── Section 1: Overview Metrics ──────────────────────────────────────
st.subheader("📊 Overview Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue",       f"₹{filtered['revenue'].sum():,.0f}")
col2.metric("Total Orders",        len(filtered))
col3.metric("Avg Product Rating",  f"{filtered['rating'].mean():.2f}")

st.divider()

# ── Section 2: Data Table ────────────────────────────────────────────
st.subheader("📋 Filtered Data (top 50 rows)")
cols = ["name","product_name","category","quantity","price","discount_pct","revenue","rating"]
st.dataframe(filtered[cols].head(50))

st.divider()

# ── Section 3: Charts ────────────────────────────────────────────────
st.subheader("📈 Charts")
c1, c2 = st.columns(2)

with c1:
    st.markdown("**Revenue by Age Group**")
    age_rev = filtered.groupby("age_group")["revenue"].sum().sort_values(ascending=False)
    fig1, ax1 = plt.subplots(figsize=(5, 3))
    ax1.bar(age_rev.index, age_rev.values, color="steelblue")
    ax1.set_xlabel("Age Group")
    ax1.set_ylabel("Revenue (₹)")
    st.pyplot(fig1)

with c2:
    st.markdown("**Price Distribution**")
    fig2, ax2 = plt.subplots(figsize=(5, 3))
    data = filtered if selected_cat == "All" else filtered[filtered["category"] == selected_cat]
    sns.boxplot(y=data["price"], ax=ax2, color="coral")
    ax2.set_ylabel("Price (₹)")
    st.pyplot(fig2)

st.divider()

# ── Section 4: Upload & Inspect ──────────────────────────────────────
st.subheader("📁 Upload & Inspect a CSV")
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])
if uploaded:
    df_upload = pd.read_csv(uploaded)
    st.write("First 10 rows:")
    st.dataframe(df_upload.head(10))
    st.write("Basic stats:")
    st.dataframe(df_upload.describe())