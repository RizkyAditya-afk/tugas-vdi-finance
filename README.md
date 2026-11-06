# Multi-DBMS Data Pipeline & Web Visualization: Personal Finance App

## Identitas Mahasiswa
* **Nama:** Rizky Aditya
* **NIM:** 230660121116
* **Program Studi:** Informatika
* **Mata Kuliah:** Visualisasi Data dan Informasi

---

## Tautan Utama Penugasan
1. **URL Live Web Application:** [Isi Link Streamlit Cloud Setelah Deployment]
2. **URL Repositori GitHub:** [Isi Link Repositori GitHub Kamu]
3. **URL Sumber Data Original:** https://www.kaggle.com/datasets/kratidataset/financial-crime-analysis
4. **URL Referensi Kode/Proyek:** https://github.com/streamlit/streamlit-example-app

---

## Ringkasan Arsitektur & Data Pipeline

### 1. Arsitektur Multi-DBMS
* **DBMS 1 (Relational Cloud):** Supabase (PostgreSQL Cloud) digunakan untuk menyimpan data transaksi keuangan real-time (`transaksi_keuangan`).
* **DBMS 2 (Local Embedded):** SQLite3 Lokal digunakan untuk menyimpan data master kategori pengeluaran dan limit anggaran (`master_kategori`).

### 2. Alur Integrasi (Data Pipeline)
1. Aplikasi melakukan query ke **DBMS 1 (Supabase PostgreSQL)** menggunakan SQLAlchemy untuk mengambil log transaksi.
2. Aplikasi melakukan query ke **DBMS 2 (SQLite)** menggunakan `sqlite3` untuk mengambil referensi master kategori.
3. Kedua set data digabungkan di tingkat aplikasi (Python) menggunakan `pandas.merge()` dengan kunci `id_kategori`.
4. Visualisasi interaktif dibangun menggunakan Plotly Express dan disajikan via Streamlit.