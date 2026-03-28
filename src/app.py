import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# Dashboard settings
st.set_page_config(page_title="PhonePe Pulse Data Viewer", page_icon="💸", layout="wide")

st.title("💸 PhonePe Pulse - Data Visualization Dashboard")
st.markdown("This dashboard provides business insights, geographical mapping, and payment trends from the PhonePe Pulse dataset.")

# Connect to Database
@st.cache_data
def load_data(query):
    conn = sqlite3.connect("phonepe_pulse.db")
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

st.sidebar.header("Filter Options")
year_filter = st.sidebar.selectbox("Select Year", options=[2018, 2019, 2020, 2021, 2022, 2023])
quarter_filter = st.sidebar.selectbox("Select Quarter", options=[1, 2, 3, 4])

# View Aggregated Transaction Data
st.subheader("1. Payment Category Trends (Aggregated Transactions)")

agg_trans_query = f"""
SELECT Transaction_type, SUM(Transaction_count) as Total_Count, SUM(Transaction_amount) as Total_Amount
FROM Aggregated_transaction
WHERE Year = {year_filter} AND Quarter = {quarter_filter}
GROUP BY Transaction_type
"""
df_agg_trans = load_data(agg_trans_query)

if not df_agg_trans.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig1 = px.pie(df_agg_trans, values='Total_Count', names='Transaction_type', title='Total Transaction Count by Category')
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = px.bar(df_agg_trans, x='Transaction_type', y='Total_Amount', title='Total Transaction Amount by Category', color='Transaction_type')
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("No data available for the selected Year and Quarter.")

# View Map Transaction Data (Top Districts)
st.subheader("2. Top 10 Districts by Transaction Amount")
map_trans_query = f"""
SELECT District, State, SUM(Transaction_amount) as Total_Amount
FROM Map_transaction
WHERE Year = {year_filter} AND Quarter = {quarter_filter}
GROUP BY District, State
ORDER BY Total_Amount DESC
LIMIT 10
"""
df_map_trans = load_data(map_trans_query)

if not df_map_trans.empty:
    fig3 = px.bar(df_map_trans, x='District', y='Total_Amount', color='State', title='Top 10 Districts by Ecosystem Size')
    st.plotly_chart(fig3, use_container_width=True)

# View Top User Brands
st.subheader("3. Registered Users by Device Brand")
agg_user_query = f"""
SELECT Brand, SUM(Count) as Total_Users
FROM Aggregated_user
WHERE Year = {year_filter} AND Quarter = {quarter_filter}
GROUP BY Brand
ORDER BY Total_Users DESC
LIMIT 10
"""
df_agg_user = load_data(agg_user_query)

if not df_agg_user.empty:
    fig4 = px.bar(df_agg_user, x='Total_Users', y='Brand', orientation='h', title='Top User Devices', color='Brand')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.markdown("Developed for the PhonePe Pulse Data Science Project. Uses local SQLite DB loaded from Pulse JSON files.")
