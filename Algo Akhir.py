import psycopg2
import webbrowser
import os

# file_path = os.path.abspath("peta.html")
# webbrowser.open(f"file://{file_path}")

def connectdb():
    conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="syadid1306",
    port=5432
    )
    return conn

conn=connectdb()
cur = conn.cursor()

# Eksekusi query SQL
cur.execute("SELECT * FROM akun;")

# Ambil hasil
rows = cur.fetchall()
for row in rows:
    print(row)

# Tutup koneksi
cur.close()
conn.close()
