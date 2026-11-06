import os
import sqlite3
import pandas as pd
import plotly.express as px
import streamlit as st
from dotenv import load_dotenv
from sqlalchemy import create_engine

st.set_page_config(page_title="Dashboard Analisis Keuangan Multi-DBMS", layout="wide")

load_dotenv()

# Otomatisasi generate SQLite jika belum ada di cloud
def init_sqlite_db():
    os.makedirs("database", exist_ok=True)
    db_path = "database/master_data.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS master_kategori (
        id_kategori INTEGER PRIMARY KEY,
        nama_kategori TEXT NOT NULL,
        alokasi_anggaran REAL NOT NULL
    )
    ''')
    data = [
        (1, 'Gaji & Pendapatan', 0.0),
        (2, 'Makanan & Minuman', 1000000.0),
        (3, 'Tagihan & Langganan', 300000.0),
        (4, 'Akomodasi & Tempat Tinggal', 1000000.0),
        (5, 'Pendapatan Lain-lain', 0.0)
    ]
    cursor.executemany('INSERT OR REPLACE INTO master_kategori VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

# Inisialisasi SQLite saat app berjalan
init_sqlite_db()

def get_data_postgresql():
    db_url = os.getenv("DATABASE_URL")
    if not db_url and "DATABASE_URL" in st.secrets:
        db_url = st.secrets["DATABASE_URL"]
    
    engine = create_engine(db_url)
    query = "SELECT * FROM transaksi_keuangan;"
    return pd.read_sql(query, engine)

def get_data_sqlite():
    conn = sqlite3.connect("database/master_data.db")
    query = "SELECT * FROM master_kategori;"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

st.title("💰 Dashboard Personal Finance & Budgeting")
st.caption("Integrasi Pipeline Data Multi-DBMS: Supabase (PostgreSQL) + Local SQLite")

try:
    df_transaksi = get_data_postgresql()
    df_kategori = get_data_sqlite()
    
    df_merged = pd.merge(df_transaksi, df_kategori, on="id_kategori", how="left")
    
    total_pemasukan = df_merged[df_merged['tipe'] == 'Pemasukan']['jumlah'].sum()
    total_pengeluaran = df_merged[df_merged['tipe'] == 'Pengeluaran']['jumlah'].sum()
    sisa_saldo = total_pemasukan - total_pengeluaran

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pemasukan", f"Rp {total_pemasukan:,.0f}")
    col2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    col3.metric("Sisa Saldo Net", f"Rp {sisa_saldo:,.0f}")

    st.markdown("---")

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

    st.subheader("📋 Data Terintegrasi (Data Federation)")
    st.dataframe(df_merged[['id_transaksi', 'tanggal', 'keterangan', 'nama_kategori', 'tipe', 'jumlah', 'alokasi_anggaran']], use_container_width=True)

except Exception as e:
    st.error(f"Terjadi kesalahan saat memuat data: {e}")