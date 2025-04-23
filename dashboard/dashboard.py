import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')


# Load data
all_df = pd.read_csv("all_data.csv")
all_df["dteday"] = pd.to_datetime(all_df["dteday"])

# Sidebar - filter rentang tanggal
st.sidebar.image("https://i.imgur.com/5RHR6Ku.png", width=100)  # logo placeholder
st.sidebar.title("Rentang Waktu")
start_date = st.sidebar.date_input("Dari", all_df["dteday"].min())
end_date = st.sidebar.date_input("Sampai", all_df["dteday"].max())

# Filter data sesuai rentang
filtered_df = all_df[(all_df["dteday"] >= pd.to_datetime(start_date)) & 
                     (all_df["dteday"] <= pd.to_datetime(end_date))]

# Header
st.title("🚲 Dicoding Collection Dashboard")
st.subheader("Daily Orders")

# Stat Box
total_orders = filtered_df["cnt_day"].sum()
total_revenue = total_orders * 1.05  # asumsikan 1.05 AUD per peminjaman
st.metric("Total Orders", f"{total_orders}")
st.metric("Total Revenue", f"AUD{total_revenue:,.2f}")

# Line Chart: Tren harian
daily_df = filtered_df.groupby("dteday")["cnt_day"].sum().reset_index()
fig, ax = plt.subplots()
ax.plot(daily_df["dteday"], daily_df["cnt_day"], color='skyblue')
ax.set_title("Tren Harian Peminjaman Sepeda")
ax.set_xlabel("Tanggal")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

# Heatmap jam vs hari
st.subheader("Pola Jam Sibuk (Heatmap)")
pivot_df = filtered_df.pivot_table(index="weekday", columns="hr", values="cnt_hour", aggfunc="mean")
fig2, ax2 = plt.subplots(figsize=(10,4))
sns.heatmap(pivot_df, cmap="YlGnBu", ax=ax2)
ax2.set_title("Heatmap Rata-rata Peminjaman (Hari vs Jam)")
st.pyplot(fig2)

# Tabel Data
st.subheader("Data Tabel")
st.dataframe(filtered_df[["dteday", "hr", "cnt_hour", "casual_hour", "registered_hour"]])
