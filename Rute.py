import webview
import os
import time
import psycopg2

def connect_db():
    conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="syadid1306",
    port=5432
    )     
    return conn

def data_pengiriman():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("""select a.nama, l.latitude, l.longitude
                    from akun a
                    join lokasi l on (a.id_akun=l.id_akun)
                    join request_pembelian rp on (a.id_akun=rp.id_akun)
                    where rp.status = 'K'""")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

# Titik koordinat (nama: (lat, lon))


def ambil_titik_dari_db():
    data = data_pengiriman()  # [(nama1, lat1, lon1), ...]
    titik = {"OWNER": (-8.164744, 113.715277)}  # Titik owner selalu di awal
    titik.update({nama.strip(): (float(lat), float(lon)) for nama, lat, lon in data})
    return titik
# Hitung jarak antar dua koordinat (tanpa akar)
def hitung_jarak(a, b):
    dx = a[0] - b[0]
    dy = a[1] - b[1]
    return dx * dx + dy * dy

# Bangun graf secara otomatis dari titik
def buat_graf(titik):
    graf = {}
    semua_nama = list(titik.keys())
    for i in range(len(semua_nama)):
        nama_i = semua_nama[i]
        graf[nama_i] = []
        for j in range(len(semua_nama)):
            if i != j:
                nama_j = semua_nama[j]
                jarak = hitung_jarak(titik[nama_i], titik[nama_j])
                graf[nama_i].append((nama_j, jarak))
    return graf

# Algoritma Dijkstra tanpa sorted/min
def dijkstra(graf, titik_awal):
    jarak = {nama: None for nama in graf}
    jarak[titik_awal] = 0
    dikunjungi = []
    urutan = [titik_awal]

    while len(dikunjungi) < len(graf):
        titik_terdekat = None
        for nama in graf:
            if nama not in dikunjungi and jarak[nama] is not None:
                if titik_terdekat is None or jarak[nama] < jarak[titik_terdekat]:
                    titik_terdekat = nama

        if titik_terdekat is None:
            break

        for tetangga, bobot in graf[titik_terdekat]:
            total = jarak[titik_terdekat] + bobot
            if jarak[tetangga] is None or total < jarak[tetangga]:
                jarak[tetangga] = total
                if tetangga not in urutan:
                    urutan.append(tetangga)

        dikunjungi.append(titik_terdekat)

    return urutan


def tampilkan_rute(window):
    titik = ambil_titik_dari_db()
    graf = buat_graf(titik)
    titik_awal = list(titik.keys())[0]  # ambil salah satu titik sebagai awal
    rute_nama = dijkstra(graf, titik_awal)
    rute_koordinat = [titik[nama] for nama in rute_nama if nama in titik]
    rute_js = "[" + ",".join(f"[{lat},{lon}]" for lat, lon in rute_koordinat) + "]"
    js = f"tampilkanRute({rute_js})"
    time.sleep(2)
    window.evaluate_js(js)


print(ambil_titik_dari_db())