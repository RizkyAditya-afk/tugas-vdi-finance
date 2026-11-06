import sqlite3

conn = sqlite3.connect('database/master_data.db')
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
print("Database SQLite berhasil dibuat dan diisi data!")