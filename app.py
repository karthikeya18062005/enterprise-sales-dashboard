import streamlit as st
import snowflake.connector
import pandas as pd

st.set_page_config(page_title="Enterprise Sales Dashboard", layout="wide")

# -------------------------
# Snowflake Connection
# -------------------------
conn = snowflake.connector.connect(
    user=st.secrets["user"],
    password=st.secrets["password"],
    account=st.secrets["account"],
    warehouse="STREAMLIT_WH",
    database="ENTERPRISE_DB",
    schema="GOLD"
)

def run_query(query):
    return pd.read_sql(query, conn)

st.title("🚀 Enterprise Sales Intelligence Dashboard")

# =====================================================
# EXECUTIVE OVERVIEW
# =====================================================

st.header("📊 Executive Overview")

summary = run_query("SELECT * FROM VW_EXEC_SUMMARY")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Revenue", f"${summary['TOTAL_REVENUE'][0]:,.0f}")
col2.metric("Total Orders", int(summary['TOTAL_ORDERS'][0]))
col3.metric("Avg Order Value", f"${summary['AVG_ORDER_VALUE'][0]:,.2f}")
col4.metric("Total Customers", int(summary['TOTAL_CUSTOMERS'][0]))

st.divider()

# =====================================================
# REVENUE ANALYTICS
# =====================================================

st.header("🌍 Revenue Analytics")

df_region = run_query("SELECT * FROM VW_REVENUE_BY_REGION")
st.subheader("Revenue by Region")
st.bar_chart(df_region.set_index("REGION")["TOTAL_REVENUE"])

df_month = run_query("SELECT * FROM VW_MONTHLY_TREND")
st.subheader("Monthly Trend")
st.line_chart(df_month.set_index("MONTH")["TOTAL_REVENUE"])

df_year = run_query("SELECT * FROM VW_YEARLY_TREND")
st.subheader("Yearly Trend")
st.bar_chart(df_year.set_index("YEAR")["TOTAL_REVENUE"])

st.divider()

# =====================================================
# CUSTOMER INSIGHTS
# =====================================================

st.header("👥 Customer Insights")

df_top = run_query("SELECT * FROM VW_TOP_CUSTOMERS")
st.subheader("Top Customers")
st.dataframe(df_top)

df_weak = run_query("SELECT * FROM VW_WEAK_CUSTOMERS")
st.subheader("Weak Customers")
st.dataframe(df_weak)

df_segment = run_query("SELECT * FROM VW_SEGMENT_REVENUE_SHARE")
st.subheader("Revenue Share by Segment")
st.bar_chart(df_segment.set_index("SEGMENT")["REVENUE_PERCENT"])

st.divider()

# =====================================================
# PRODUCT INSIGHTS
# =====================================================

st.header("📦 Product Insights")

df_category = run_query("SELECT * FROM VW_REVENUE_BY_CATEGORY")
st.subheader("Revenue by Category")
st.bar_chart(df_category.set_index("CATEGORY")["TOTAL_REVENUE"])

df_top_cat = run_query("SELECT * FROM VW_TOP_CATEGORY")
st.subheader("Most Profitable Category")
st.dataframe(df_top_cat)
