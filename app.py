import streamlit as st
import pandas as pd
import plotly.express as px
# Load Dataset
df = pd.read_csv("Sales Data.csv")
# Dashboard Heading
st.set_page_config(page_title="Sales Dashboard", layout="wide")

st.title("Electronics Store Sales Dashboard")
st.subheader("Sales Data Analysis - 2019")

st.write("Original Data Shape:", df.shape)
st.write(df.head())
# Data Cleaning

# Drop Unnamed Column
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Remove Missing Values
df = df.dropna()

# Remove Duplicate Rows
df = df.drop_duplicates()

# Convert Order Date
df["Order Date"] = pd.to_datetime(
    df["Order Date"], errors="coerce"
)

df = df.dropna(subset=["Order Date"])

st.write("Cleaned Data Shape:", df.shape)
# Create New Columns

df["Sales"] = df["Quantity Ordered"] * df["Price Each"]

df["Month"] = df["Order Date"].dt.month_name()

df["Hour"] = df["Order Date"].dt.hour

df["City"] = df["Purchase Address"].apply(
    lambda x: x.split(",")[1].strip() +
    " (" + x.split(",")[2].split(" ")[1] + ")"
)
# Sidebar Filters

st.sidebar.header("Filters")

# Month Filter
month_list = ["All"] + sorted(df["Month"].unique().tolist())
selected_month = st.sidebar.selectbox("Select Month", month_list)

# City Filter
city_list = ["All"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", city_list)

# Product Filter
product_list = ["All"] + sorted(df["Product"].unique().tolist())
selected_product = st.sidebar.selectbox("Select Product", product_list)

# Apply Filters
filtered_df = df.copy()

if selected_month != "All":
    filtered_df = filtered_df[filtered_df["Month"] == selected_month]

if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]

if selected_product != "All":
    filtered_df = filtered_df[filtered_df["Product"] == selected_product]
    # Check Empty Data

if filtered_df.empty:
    st.warning("No data found. Please change filters.")

else:

    # Calculate Total Sales
    total_sales = filtered_df["Sales"].sum()

    # Calculate Number of Orders
    total_orders = len(filtered_df)

    # Calculate Items Sold
    items_sold = filtered_df["Quantity Ordered"].sum()

    # Calculate Average Order Value
    avg_order = total_sales / total_orders

    # Display Four Metrics
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Number of Orders", total_orders)
    col3.metric("Items Sold", items_sold)
    col4.metric("Average Order Value", f"${avg_order:,.2f}")
        # Dashboard Charts

    st.header("Sales Analysis")

    # Quantity Ordered
    fig1 = px.histogram(
        filtered_df,
        x="Quantity Ordered",
        title="Quantity Ordered Distribution"
    )
    st.plotly_chart(fig1, use_container_width=True)

    # Price Each
    fig2 = px.histogram(
        filtered_df,
        x="Price Each",
        title="Price Each Distribution"
    )
    st.plotly_chart(fig2, use_container_width=True)

    # Sales
    fig3 = px.histogram(
        filtered_df,
        x="Sales",
        title="Sales Distribution"
    )
    st.plotly_chart(fig3, use_container_width=True)
        # Product Graph
    fig4 = px.histogram(
        filtered_df,
        x="Product",
        title="Product Sales Count"
    )
    st.plotly_chart(fig4, use_container_width=True)

    # City Graph
    fig5 = px.histogram(
        filtered_df,
        x="City",
        title="Orders by City"
    )
    st.plotly_chart(fig5, use_container_width=True)

    # Month Graph
    fig6 = px.histogram(
        filtered_df,
        x="Month",
        title="Orders by Month"
    )
    st.plotly_chart(fig6, use_container_width=True)

    # Hour Graph
    fig7 = px.histogram(
        filtered_df,
        x="Hour",
        title="Orders by Hour"
    )
    st.plotly_chart(fig7, use_container_width=True)
        # Average Sales by City
    st.header("Bivariate Analysis")

    city_sales = filtered_df.groupby("City")["Sales"].mean().reset_index()

    fig8 = px.bar(
        city_sales,
        x="City",
        y="Sales",
        title="Average Sales per Order by City",
        labels={"Sales": "Average Sales"}
    )
    st.plotly_chart(fig8, use_container_width=True)
        # Quantity by Product

    product_qty = filtered_df.groupby("Product")["Quantity Ordered"].sum().reset_index()

    fig9 = px.bar(
        product_qty,
        x="Product",
        y="Quantity Ordered",
        title="Quantity Ordered by Product"
    )
    st.plotly_chart(fig9, use_container_width=True)
        # Total Sales by Month

    month_sales = filtered_df.groupby("Month")["Sales"].sum().reset_index()

    fig10 = px.bar(
        month_sales,
        x="Month",
        y="Sales",
        title="Total Sales by Month"
    )
    st.plotly_chart(fig10, use_container_width=True)
        # Total Sales by Hour

    hour_sales = filtered_df.groupby("Hour")["Sales"].sum().reset_index()

    fig11 = px.line(
        hour_sales,
        x="Hour",
        y="Sales",
        title="Total Sales by Hour"
    )
    st.plotly_chart(fig11, use_container_width=True)

    # Price vs Quantity

    fig12 = px.scatter(
        filtered_df,
        x="Price Each",
        y="Quantity Ordered",
        title="Price vs Quantity"
    )
    st.plotly_chart(fig12, use_container_width=True)
        # Research Question 1

    st.header("Research Questions")

    filtered_df["Day"] = filtered_df["Order Date"].dt.day_name()

    day_sales = filtered_df.groupby("Day")["Sales"].sum().reset_index()

    fig13 = px.bar(
        day_sales,
        x="Day",
        y="Sales",
        title="Sales by Day of the Week",
        labels={"Sales": "Total Sales"}
    )

    st.plotly_chart(fig13, use_container_width=True)

    st.write("This graph shows which day of the week generates the highest sales.")
        # Research Question 2

    product_average = filtered_df.groupby("Product")["Quantity Ordered"].mean().reset_index()

    fig14 = px.bar(
        product_average,
        x="Product",
        y="Quantity Ordered",
        title="Average Quantity per Product",
        labels={"Quantity Ordered": "Average Quantity"}
    )

    st.plotly_chart(fig14, use_container_width=True)

    st.write("This graph shows which product has the highest average quantity per order.")