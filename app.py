import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

# Konfigurasi Halaman Streamlit
st.set_page_config(page_title="Dashboard Analisis Keuangan Multi-DBMS", layout="wide")

load_dotenv()

# Fungsi untuk mengambil data dari Cloud PostgreSQL (DBMS 1)
def get_data_postgresql():
    db_url = os.getenv("DATABASE_URL")
    if not db_url and "DATABASE_URL" in st.secrets:
        db_url = st.secrets["DATABASE_URL"]
    
    engine = create_engine(db_url)
    query = "SELECT * FROM transaksi_keuangan;"
    return pd.read_sql(query, engine)

# Fungsi untuk mengambil data dari SQLite Lokal (DBMS 2)
def get_data_sqlite():
    conn = sqlite3.connect("database/master_data.db")
    query = "SELECT * FROM master_kategori;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Judul Utama
st.title("💰 Dashboard Personal Finance & Budgeting")
st.caption("Integrasi Pipeline Data Multi-DBMS: Supabase (PostgreSQL) + Local SQLite")

try:
    # 1. Pipeline Data & Federation (Penggabungan di Python)
    df_transaksi = get_data_postgresql() # DBMS 1
    df_kategori = get_data_sqlite()     # DBMS 2
    
    # Penggabungan (Merge / Join)
    df_merged = pd.merge(df_transaksi, df_kategori, on="id_kategori", how="left")
    
    # Hitung Rekapitulasi Metrik
    total_pemasukan = df_merged[df_merged['tipe'] == 'Pemasukan']['jumlah'].sum()
    total_pengeluaran = df_merged[df_merged['tipe'] == 'Pengeluaran']['jumlah'].sum()
    sisa_saldo = total_pemasukan - total_pengeluaran

    # Display Metrics
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    col3.metric("Sisa Saldo Net", f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")

    # Visualisasi 1: Pengeluaran Per Kategori vs Alokasi Anggaran
    st.subheader("📊 Analisis Pengeluaran vs Batas Anggaran")
    df_pengeluaran = df_merged[df_merged['tipe'] == 'Pengeluaran'].groupby('nama_kategori').agg({
        'jumlah': 'sum',
        'alokasi_anggaran': 'first'
    }).reset_index()

    fig_bar = px.bar(
        df_pengeluaran, 
        x='nama_kategori', 
        y=['jumlah', 'alokasi_anggaran'],
        barmode='group',
        labels={'value': 'Jumlah (Rp)', 'nama_kategori': 'Kategori Pengeluaran', 'variable': 'Metrik'},
        title="Realisasi Pengeluaran vs Alokasi Anggaran (DBMS 1 + DBMS 2)"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Tabel Data Gabungan
    st.subheader("📋 Data Terintegrasi (Data Federation)")
    st.dataframe(df_merged[['id_transaksi', 'tanggal', 'keterangan', 'nama_kategori', 'tipe', 'jumlah', 'alokasi_anggaran']], use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")