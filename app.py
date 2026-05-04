import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------------------
# PAGE CONFIG
# ---------------------------
st.set_page_config(page_title="Social Media Dashboard", layout="wide")

st.title("📊 Social Media Analytics Dashboard")

# ---------------------------
# LOAD & FIX CSV
# ---------------------------
try:
    df = pd.read_csv("clean_social_evolution.csv", header=None)

    # Fix wrong CSV structure
    df = df[0].str.split(",", expand=True)

    df.columns = df.iloc[0]
    df = df[1:]

    df.columns = df.columns.str.strip().str.lower()

except Exception as e:
    st.error(f"Error loading file: {e}")
    st.stop()

# ---------------------------
# REMOVE TIKTOK
# ---------------------------
if "platform" in df.columns:
    df = df[df["platform"].str.lower() != "tiktok"]

st.success("File Loaded Successfully ✅")

# ---------------------------
# CONVERT NUMERIC
# ---------------------------
for col in ["followers", "likes", "total_engagement"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.title("⚙️ Control Panel")

if "platform" in df.columns:
    platform = st.sidebar.multiselect("Platform", df["platform"].dropna().unique())
    if platform:
        df = df[df["platform"].isin(platform)]

if "location" in df.columns:
    location = st.sidebar.multiselect("Location", df["location"].dropna().unique())
    if location:
        df = df[df["location"].isin(location)]

if "sentiment_category" in df.columns:
    sentiment = st.sidebar.multiselect("Sentiment", df["sentiment_category"].dropna().unique())
    if sentiment:
        df = df[df["sentiment_category"].isin(sentiment)]

# ---------------------------
# KPI CARDS
# ---------------------------
col1, col2, col3, col4 = st.columns(4)

if "total_engagement" in df.columns:
    col1.metric("Total Engagement", f"{df['total_engagement'].sum():,.0f}")

if "post_id" in df.columns:
    col2.metric("Total Posts", f"{df['post_id'].count():,}")

if "likes" in df.columns:
    col3.metric("Avg Likes", f"{df['likes'].mean():.2f}")

if "followers" in df.columns:
    col4.metric("Followers", f"{df['followers'].sum():,.0f}")

# ---------------------------
# CHARTS
# ---------------------------
col1, col2, col3 = st.columns(3)

if "platform" in df.columns and "total_engagement" in df.columns:
    fig1 = px.bar(df, x="platform", y="total_engagement",
                  color="platform", title="Engagement by Platform")
    col1.plotly_chart(fig1, use_container_width=True)

if "sentiment_category" in df.columns:
    fig2 = px.pie(df, names="sentiment_category",
                  title="Sentiment Distribution")
    col2.plotly_chart(fig2, use_container_width=True)

if "location" in df.columns:
    fig3 = px.pie(df, names="location",
                  title="Posts by Location")
    col3.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# EXTRA CHARTS
# ---------------------------
col1, col2 = st.columns(2)

if "topic" in df.columns and "total_engagement" in df.columns:
    fig4 = px.bar(df, x="topic", y="total_engagement",
                  title="Top Topics", color="topic")
    col1.plotly_chart(fig4, use_container_width=True)

if "followers" in df.columns and "total_engagement" in df.columns:
    fig5 = px.scatter(df,
                      x="followers",
                      y="total_engagement",
                      color="platform",
                      title="Followers vs Engagement")
    col2.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# DATA TABLE
# ---------------------------
st.subheader("📄 Data Preview")
st.dataframe(df.head(50))