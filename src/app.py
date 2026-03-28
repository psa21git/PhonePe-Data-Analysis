import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# ─── Page Config ───
st.set_page_config(page_title="PhonePe Pulse Dashboard", page_icon="💸", layout="wide")

# ─── Database Connection ───
DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "phonepe_pulse.db")

@st.cache_data
def load_table(table_name):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df

# Load all 9 tables
df_agg_trans = load_table("Aggregated_transaction")
df_agg_user  = load_table("Aggregated_user")
df_agg_ins   = load_table("Aggregated_insurance")
df_map_trans = load_table("Map_transaction")
df_map_user  = load_table("Map_user")
df_map_ins   = load_table("Map_insurance")
df_top_trans = load_table("Top_transaction")
df_top_user  = load_table("Top_user")
df_top_ins   = load_table("Top_insurance")

# ─── Sidebar Filters ───
st.sidebar.title("🔍 Filters")
years = sorted(df_agg_trans["Year"].unique())
selected_year = st.sidebar.selectbox("Year", years, index=len(years)-1)
selected_quarter = st.sidebar.selectbox("Quarter", [1, 2, 3, 4])

states = sorted(df_map_trans["State"].unique())
selected_state = st.sidebar.selectbox("State (for drill-down)", ["All India"] + states)

# ─── Header ───
st.title("💸 PhonePe Pulse — Interactive Data Dashboard")
st.markdown(f"**Showing data for:** `{selected_year} Q{selected_quarter}`")
st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 1: TOP-LEVEL KPI CARDS
# ════════════════════════════════════════════════
st.header("📊 Key Performance Indicators")

filt_agg = df_agg_trans[(df_agg_trans["Year"] == selected_year) & (df_agg_trans["Quarter"] == selected_quarter)]
filt_map_user = df_map_user[(df_map_user["Year"] == selected_year) & (df_map_user["Quarter"] == selected_quarter)]
filt_ins = df_agg_ins[(df_agg_ins["Year"] == selected_year) & (df_agg_ins["Quarter"] == selected_quarter)]

total_trans_count = filt_agg["Transaction_count"].sum()
total_trans_amount = filt_agg["Transaction_amount"].sum()
total_users = filt_map_user["RegisteredUsers"].sum()
total_app_opens = filt_map_user["AppOpens"].sum()
total_ins_count = filt_ins["Transaction_count"].sum() if not filt_ins.empty else 0
total_ins_amount = filt_ins["Transaction_amount"].sum() if not filt_ins.empty else 0

kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
kpi1.metric("Total Transactions", f"{total_trans_count/1e6:,.1f}M")
kpi2.metric("Transaction Value", f"₹{total_trans_amount/1e9:,.1f}B")
kpi3.metric("Registered Users", f"{total_users/1e6:,.1f}M")
kpi4.metric("App Opens", f"{total_app_opens/1e6:,.1f}M")
kpi5.metric("Insurance Policies", f"{total_ins_count/1e3:,.1f}K")
kpi6.metric("Insurance Value", f"₹{total_ins_amount/1e6:,.1f}M")

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 2: TRANSACTION CATEGORY BREAKDOWN
# ════════════════════════════════════════════════
st.header("1️⃣ Payment Category Analysis")
st.caption("Source: Aggregated_transaction")

cat_data = filt_agg.groupby("Transaction_type").agg(
    Total_Count=("Transaction_count", "sum"),
    Total_Amount=("Transaction_amount", "sum")
).reset_index()

if not cat_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.pie(cat_data, values="Total_Count", names="Transaction_type",
                     title="Transaction Count Share by Category",
                     color_discrete_sequence=px.colors.qualitative.Set2,
                     hole=0.4)
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.bar(cat_data.sort_values("Total_Amount", ascending=True),
                     x="Total_Amount", y="Transaction_type", orientation="h",
                     title="Transaction Amount by Category (₹)",
                     color="Transaction_type",
                     color_discrete_sequence=px.colors.qualitative.Pastel)
        fig.update_layout(showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("No transaction data for this period.")

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 3: YEAR-OVER-YEAR GROWTH TRENDS
# ════════════════════════════════════════════════
st.header("2️⃣ Year-over-Year Growth Trends")
st.caption("Source: Aggregated_transaction + Aggregated_insurance")

yearly = df_agg_trans.groupby("Year").agg(
    Count=("Transaction_count", "sum"),
    Amount=("Transaction_amount", "sum")
).reset_index()

col1, col2 = st.columns(2)
with col1:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=yearly["Year"], y=yearly["Amount"]/1e12,
                         name="Amount (₹ Trillions)", marker_color="steelblue"))
    fig.add_trace(go.Scatter(x=yearly["Year"], y=yearly["Count"]/1e9,
                             name="Count (Billions)", yaxis="y2",
                             line=dict(color="crimson", width=3), mode="lines+markers"))
    fig.update_layout(
        title="Transaction Growth — Amount & Count",
        yaxis=dict(title="Amount (₹ Trillions)"),
        yaxis2=dict(title="Count (Billions)", overlaying="y", side="right"),
        legend=dict(x=0, y=1.15, orientation="h")
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    yearly_ins = df_agg_ins.groupby("Year").agg(
        Count=("Transaction_count", "sum"),
        Amount=("Transaction_amount", "sum")
    ).reset_index()
    if not yearly_ins.empty:
        fig = px.area(yearly_ins, x="Year", y="Amount",
                      title="Insurance Value Growth Over Years (₹)",
                      color_discrete_sequence=["mediumseagreen"])
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 4: QUARTERLY TRENDS
# ════════════════════════════════════════════════
st.header("3️⃣ Quarterly Transaction Trends")
st.caption("Source: Aggregated_transaction")

quarterly = df_agg_trans.groupby(["Year", "Quarter"]).agg(
    Amount=("Transaction_amount", "sum")
).reset_index()
quarterly["YQ"] = quarterly["Year"].astype(str) + "-Q" + quarterly["Quarter"].astype(str)

fig = px.line(quarterly, x="YQ", y="Amount", title="Transaction Amount by Quarter",
              markers=True, color_discrete_sequence=["darkorange"])
fig.update_layout(xaxis_tickangle=-45)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 5: TOP STATES BY TRANSACTIONS
# ════════════════════════════════════════════════
st.header("4️⃣ Top 10 States — Transactions")
st.caption("Source: Map_transaction")

filt_map_trans = df_map_trans[(df_map_trans["Year"] == selected_year) & (df_map_trans["Quarter"] == selected_quarter)]
state_trans = filt_map_trans.groupby("State").agg(
    Total_Count=("Transaction_count", "sum"),
    Total_Amount=("Transaction_amount", "sum")
).reset_index()

col1, col2 = st.columns(2)
with col1:
    top10_amt = state_trans.nlargest(10, "Total_Amount")
    fig = px.bar(top10_amt, x="Total_Amount", y="State", orientation="h",
                 title="Top 10 States by Transaction Amount",
                 color="Total_Amount", color_continuous_scale="Oranges")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

with col2:
    top10_cnt = state_trans.nlargest(10, "Total_Count")
    fig = px.bar(top10_cnt, x="Total_Count", y="State", orientation="h",
                 title="Top 10 States by Transaction Count",
                 color="Total_Count", color_continuous_scale="Blues")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 6: STATE GROWTH COMPARISON
# ════════════════════════════════════════════════
st.header("5️⃣ State Growth Comparison (Top 5)")
st.caption("Source: Map_transaction")

top5_states = (df_map_trans.groupby("State")["Transaction_amount"].sum()
               .nlargest(5).index.tolist())
state_yearly = (df_map_trans[df_map_trans["State"].isin(top5_states)]
                .groupby(["State", "Year"])["Transaction_amount"].sum().reset_index())

fig = px.line(state_yearly, x="Year", y="Transaction_amount", color="State",
              title="Year-wise Growth of Top 5 States",
              markers=True, color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 7: DEVICE BRAND ANALYSIS
# ════════════════════════════════════════════════
st.header("6️⃣ Device Brand Market Share")
st.caption("Source: Aggregated_user")

filt_user = df_agg_user[(df_agg_user["Year"] == selected_year) & (df_agg_user["Quarter"] == selected_quarter)]
brand_data = filt_user.groupby("Brand")["Count"].sum().reset_index().sort_values("Count", ascending=False).head(10)

if not brand_data.empty:
    col1, col2 = st.columns(2)
    with col1:
        fig = px.bar(brand_data, x="Count", y="Brand", orientation="h",
                     title="Top 10 Device Brands by Users",
                     color="Brand", color_discrete_sequence=px.colors.qualitative.Vivid)
        fig.update_layout(showlegend=False, yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        fig = px.pie(brand_data, values="Count", names="Brand",
                     title="Device Brand Market Share",
                     color_discrete_sequence=px.colors.qualitative.Pastel, hole=0.35)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 8: USER ENGAGEMENT — REGISTERED VS APP OPENS
# ════════════════════════════════════════════════
st.header("7️⃣ User Engagement — Registered Users vs App Opens")
st.caption("Source: Map_user")

state_user = filt_map_user.groupby("State").agg(
    Users=("RegisteredUsers", "sum"),
    Opens=("AppOpens", "sum")
).reset_index()

if not state_user.empty:
    fig = px.scatter(state_user, x="Users", y="Opens", hover_name="State",
                     size="Users", color="Opens",
                     title="State-level: Registered Users vs App Opens",
                     color_continuous_scale="YlOrRd",
                     labels={"Users": "Registered Users", "Opens": "App Opens"})
    fig.update_traces(marker=dict(line=dict(width=1, color="black")))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 9: DISTRICT DRILL-DOWN
# ════════════════════════════════════════════════
st.header("8️⃣ District-Level Drill-Down")
st.caption("Source: Map_transaction + Map_user")

if selected_state != "All India":
    dist_trans = filt_map_trans[filt_map_trans["State"] == selected_state]
    dist_data = dist_trans.groupby("District").agg(
        Count=("Transaction_count", "sum"),
        Amount=("Transaction_amount", "sum")
    ).reset_index().sort_values("Amount", ascending=False).head(15)

    if not dist_data.empty:
        fig = px.bar(dist_data, x="Amount", y="District", orientation="h",
                     title=f"Top Districts in {selected_state.replace('-', ' ').title()}",
                     color="Amount", color_continuous_scale="Tealgrn")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

    # District user engagement
    dist_user = filt_map_user[filt_map_user["State"] == selected_state]
    dist_user_agg = dist_user.groupby("District").agg(
        Users=("RegisteredUsers", "sum"),
        Opens=("AppOpens", "sum")
    ).reset_index().sort_values("Users", ascending=False).head(15)

    if not dist_user_agg.empty:
        fig = px.bar(dist_user_agg, x="District", y=["Users", "Opens"],
                     title=f"Users vs App Opens — Districts in {selected_state.replace('-', ' ').title()}",
                     barmode="group", color_discrete_sequence=["steelblue", "darkorange"])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
else:
    st.info("👈 Select a specific state from the sidebar to see district-level data.")

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 10: TOP PINCODES
# ════════════════════════════════════════════════
st.header("9️⃣ Top Pincodes — Transaction Hotspots")
st.caption("Source: Top_transaction + Top_user")

filt_top_trans = df_top_trans[(df_top_trans["Year"] == selected_year) & (df_top_trans["Quarter"] == selected_quarter)]
top_pins = filt_top_trans.groupby(["State", "Pincode"]).agg(
    Amount=("Transaction_amount", "sum"),
    Count=("Transaction_count", "sum")
).reset_index().nlargest(15, "Amount")
top_pins["Label"] = top_pins["State"].str.replace("-", " ").str.title() + " – " + top_pins["Pincode"].astype(str)

if not top_pins.empty:
    fig = px.bar(top_pins, x="Amount", y="Label", orientation="h",
                 title="Top 15 Pincodes by Transaction Amount",
                 color="Amount", color_continuous_scale="Sunset")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 11: INSURANCE ANALYSIS
# ════════════════════════════════════════════════
st.header("🔟 Insurance Segment Analysis")
st.caption("Source: Aggregated_insurance + Map_insurance")

col1, col2 = st.columns(2)

with col1:
    filt_map_ins = df_map_ins[(df_map_ins["Year"] == selected_year) & (df_map_ins["Quarter"] == selected_quarter)]
    state_ins = filt_map_ins.groupby("State").agg(
        Count=("Transaction_count", "sum"),
        Amount=("Transaction_amount", "sum")
    ).reset_index().nlargest(10, "Count")
    if not state_ins.empty:
        fig = px.bar(state_ins, x="Count", y="State", orientation="h",
                     title="Top 10 States — Insurance Policies Sold",
                     color="Count", color_continuous_scale="Greens")
        fig.update_layout(yaxis=dict(autorange="reversed"))
        st.plotly_chart(fig, use_container_width=True)

with col2:
    ins_quarterly = df_agg_ins.groupby(["Year", "Quarter"]).agg(
        Amount=("Transaction_amount", "sum")
    ).reset_index()
    ins_quarterly["YQ"] = ins_quarterly["Year"].astype(str) + "-Q" + ins_quarterly["Quarter"].astype(str)
    if not ins_quarterly.empty:
        fig = px.area(ins_quarterly, x="YQ", y="Amount",
                      title="Insurance Premium Growth Over Time",
                      color_discrete_sequence=["mediumseagreen"])
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 12: AVERAGE TRANSACTION VALUE BY STATE
# ════════════════════════════════════════════════
st.header("1️⃣1️⃣ Average Transaction Value by State")
st.caption("Source: Map_transaction")

if not state_trans.empty:
    state_trans["Avg_Value"] = state_trans["Total_Amount"] / (state_trans["Total_Count"] + 1)
    top_avg = state_trans.nlargest(15, "Avg_Value")
    fig = px.bar(top_avg, x="Avg_Value", y="State", orientation="h",
                 title="Top 15 States — Highest Average Transaction Value (₹)",
                 color="Avg_Value", color_continuous_scale="Purples")
    fig.update_layout(yaxis=dict(autorange="reversed"))
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ════════════════════════════════════════════════
# SECTION 13: PAYMENT VS INSURANCE CORRELATION
# ════════════════════════════════════════════════
st.header("1️⃣2️⃣ Payment vs Insurance — State Correlation")
st.caption("Source: Map_transaction + Map_insurance")

pay_state = filt_map_trans.groupby("State")["Transaction_amount"].sum().reset_index()
pay_state.columns = ["State", "Payment_Amount"]
ins_state = filt_map_ins.groupby("State")["Transaction_amount"].sum().reset_index() if not filt_map_ins.empty else pd.DataFrame(columns=["State", "Transaction_amount"])
ins_state.columns = ["State", "Insurance_Amount"]
merged = pay_state.merge(ins_state, on="State", how="inner")

if len(merged) > 3:
    fig = px.scatter(merged, x="Payment_Amount", y="Insurance_Amount",
                     hover_name="State", size="Payment_Amount",
                     title="Do high-payment states also buy more insurance?",
                     color_discrete_sequence=["teal"],
                     labels={"Payment_Amount": "Payment Transaction Amount (₹)",
                             "Insurance_Amount": "Insurance Amount (₹)"})
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ═══════════════════
# FOOTER
# ═══════════════════
st.markdown("""
<div style="text-align:center; color:gray; padding:20px;">
    <p>Built with ❤️ using Streamlit & Plotly | Data: PhonePe Pulse Open Dataset</p>
    <p>9 SQL Tables • 90,000+ rows • 2018–2024</p>
</div>
""", unsafe_allow_html=True)
