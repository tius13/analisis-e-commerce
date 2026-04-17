import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# MENGATUR TAMPILAN HALAMAN
st.set_page_config(page_title="Dashboard E-Commerce Olist", page_icon="🛒", layout="wide")

# 2. MEMUAT DATA
@st.cache_data
def load_data():
    # Membaca file CSV yang ada di folder yang sama
    df = pd.read_csv("main_data.csv")
    df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])
    df["order_delivered_customer_date"] = pd.to_datetime(df["order_delivered_customer_date"])
    return df

main_df = load_data()

# MEMBUAT SIDEBAR 
with st.sidebar:
    st.header("Filter Waktu Transaksi")
    
    min_date = main_df["order_purchase_timestamp"].min()
    max_date = main_df["order_purchase_timestamp"].max()
    
    start_date, end_date = st.date_input(
        label='Pilih Rentang Waktu',
        min_value=min_date, max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data
filtered_df = main_df[(main_df["order_purchase_timestamp"] >= str(start_date)) & 
                      (main_df["order_purchase_timestamp"] <= str(end_date))]

# TAAMPILAN UTAMA
st.title("Dashboard Data Olist E-Commerce")
st.write("Gunakan menu di sebelah kiri untuk memfilter data berdasarkan tanggal pesanan.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Pesanan", value=f'{filtered_df["order_id"].nunique():,}')
with col2:
    st.metric("Total Pendapatan", value=f'R$ {filtered_df["price"].sum():,.0f}')
with col3:
    delivered = filtered_df[filtered_df['order_status'] == 'delivered'].copy()
    delivered['delivery_time'] = (delivered['order_delivered_customer_date'] - delivered['order_purchase_timestamp']).dt.days
    st.metric("Rata-rata Pengiriman", value=f"{delivered['delivery_time'].mean():.1f} Hari")

st.markdown("---")

# GRAFIK 1
st.subheader("1. Kategori Produk dengan Pendapatan Tertinggi")
revenue_by_category = filtered_df.groupby("product_category_name_english")['price'].sum().sort_values(ascending=False).head(10)
fig1, ax1 = plt.subplots(figsize=(12, 6))
sns.barplot(x=revenue_by_category.values, y=revenue_by_category.index, palette='viridis', ax=ax1)
ax1.set_xlabel('Total Pendapatan (BRL)')
ax1.set_ylabel('Kategori Produk')
st.pyplot(fig1)

st.markdown("---")

# GRAFIK 2
st.subheader("2. Wilayah dengan Waktu Pengiriman Terlama (Top 5)")
delivery_locations = delivered.groupby('customer_state')['delivery_time'].mean().sort_values(ascending=False).head(5)
fig2, ax2 = plt.subplots(figsize=(10, 6))
sns.barplot(x=delivery_locations.values, y=delivery_locations.index, palette='Reds_r', ax=ax2)
ax2.axvline(15, color='black', linestyle='--', label='Batas Wajar (15 Hari)')
ax2.set_xlabel('Rata-rata Waktu (Hari)')
ax2.set_ylabel('Negara Bagian')
ax2.legend()
st.pyplot(fig2)