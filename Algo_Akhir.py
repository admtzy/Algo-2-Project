
import psycopg2
import webbrowser
import os
from datetime import date
from tabulate import tabulate
import time
import sort

# file_path = os.path.abspath("peta.html")
# webbrowser.open(f"file://{file_path}")
def connect_db():
    conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="",
    port=5432
    )     
    return conn

def clear_terminal():
    os.system('cls')
    
def kembali ():
    
    inputan_kembali = input("Tekan Enter untuk kembali ke menu utama...")
    if inputan_kembali == "":
        clear_terminal()
    else:
        kembali()
        
def main():
    while True:
        print("\n=== MENU ===")
        print("1. Register")
        print("2. Login")
        print("3. Keluar")
        pilihan = input("Pilih menu (1/2/3): ")

        if pilihan == "1":
            os.system('cls')
            nama = input("Nama: ")
            no_hp = input("No HP: ")
            password = input("Password (max 8 karakter): ")
            # status_akun = input("Status akun (misalnya A): ")
            # latitude = float(input("Latitude: "))
            # longitude = float(input("Longitude: "))
            register(nama, no_hp, password)
            os.system('cls')

        elif pilihan == "2":
            no_hp = input("No HP: ")
            password = input("Password: ")
            login(no_hp, password)
            os.system('cls')

        elif pilihan == "3":
            print("Keluar dari program.")
            os.system('cls')
            break

        else:
            print("Pilihan tidak valid.")


def register(nama, no_hp, password):
    print("Memuat Peta", end="")
    for i in range(5):
        print(".", end="", flush=True)
        time.sleep(0.5) 
    file_path = os.path.abspath("peta.html")
    webbrowser.open(f"file://{file_path}")
    lokasi=input("Masukkan Lokasi Anda : ")
    latitude,longitude=lokasi.split(',')
    try:
        conn = connect_db()
        cur = conn.cursor()

        # Insert ke tabel akun
        cur.execute("""
            INSERT INTO akun (nama, no_hp, password, status_akun)
            VALUES (%s, %s, %s, %s) RETURNING id_akun;
        """, (nama, no_hp, password, "1"))
        id_akun = cur.fetchone()[0]

        # Insert ke tabel lokasi
        cur.execute("""
            INSERT INTO lokasi (latitude, longitude, id_akun)
            VALUES (%s, %s, %s);
        """, (latitude, longitude, id_akun))

        conn.commit()
        print("Registrasi berhasil!")
        inputan_kembali = input("Tekan Enter untuk kembali ke menu utama...")

    except psycopg2.IntegrityError:
        conn.rollback()
        inputan_kembali = input("Registrasi gagal: Nomor HP sudah digunakan atau data tidak valid.")
    except Exception as e:
        conn.rollback()
        inputan_kembali = input("Terjadi kesalahan:", e)
    finally:
        cur.close()
        conn.close()
        
def login(no_hp, password):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_akun, nama, status_akun FROM akun
            WHERE no_hp = %s AND password = %s;
        """, (no_hp, password))
        user = cur.fetchone()
        id_akun= user[0]
        nama= user[1]
        status = user[2]

        if user:
            if status == "0":
                menu_owner(nama)
            else : 
                menu_pembeli(id_akun,nama)
            clear_terminal()
        else:
            input("Login gagal: Nomor HP atau password salah.")
            kembali()

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
    finally:
        cur.close()
        conn.close()

def menu_owner(nama):
    while True :
        clear_terminal()
        print(f"halo {nama} selamat datang di aplikasi petani")
        print("=========================menu utama=========================")
        print("1. penjualan hasil tani")
        print("2. Rute pengiriman ")
        print("3.pencatatan transaksi")
        print("4. pengelolaan stock")
        print("5. Keluar")
        pilihan = input("Masukkan pilihan anda: ")
        if pilihan == "1":
            penjualan_hasil_tani()
        elif pilihan == "2":
            rute_pengiriman()
        elif pilihan == "3":
            pencatatan_transaksi()
        elif pilihan == "4":
            sort.menu()
        elif pilihan == "5":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        else:
            print("Pilihan tidak valid.")
        
def menu_pembeli(id_akun, nama):
    while True :
        clear_terminal()
        print(f"halo {nama} selamat datang di aplikasi petani")
        print("=========================menu utama=========================")
        print("1. Beli Hasil Tani")
        print("2. Keluar")
        pilihan = input("Masukkan pilihan anda: ")
        if pilihan == "1":
            beli_hasil_tani(id_akun)
        elif pilihan == "2":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        else:
            print("Pilihan tidak valid.")

def beli_hasil_tani (id_akun):
    print("Menu Beli Hasil Tani")
    nama_sayur = input("Masukkan nama sayur: ").strip()
    jumlah_beli = int(input("Masukkan jumlah beli: "))
    
    conn = connect_db()
    cur = conn.cursor()
    query = f"""
        SELECT id_sayur, harga_satuan
        FROM sayur
        WHERE nama_sayur ilike '{nama_sayur}'
    """
    cur.execute(query)

    data_sayur = cur.fetchone()

    if data_sayur is None:
        input("❌ Sayur tidak ditemukan dalam database.")
    else:
        id_sayur, harga_satuan = data_sayur
        total_harga = harga_satuan * jumlah_beli
        status = 'P'

        insert_query = f"""
            INSERT INTO request_pembelian (id_akun, id_sayur, nama_sayur, jumlah_beli, total_harga, status)
            VALUES ({id_akun}, {id_sayur}, '{nama_sayur}', {jumlah_beli}, {total_harga}, '{status}')
        """
        cur.execute(insert_query)
        conn.commit()
        input("✅ Request pembelian berhasil disimpan!")

    # max_budget = int(input("Masukkan budget maksimal: "))

 
def penjualan_hasil_tani():
    print("Menu Penjualan Hasil Tani")
    # Tambahkan logika untuk penjualan hasil tani

def rute_pengiriman():
    print("Menu Rute Pengiriman")
    # Tambahkan logika untuk rute pengiriman

def selection_sort_by_stok(data, jalan=True):
    n = len(data)
    for i in range(n):
        index_awal = i
        for j in range(i + 1, n):
            if jalan:
                if data[j][2] < data[index_awal][2]:
                    index_awal = j
            else:
                if data[j][2] > data[index_awal][2]:
                    index_awal = j
        data[i], data[index_awal] = data[index_awal], data[i]
    return data

def selection_sort_by_nama(data, jalan1=True):
    n = len(data)
    for i in range(n):
        idx_extreme = i
        for j in range(i + 1, n):
            nama_j = data[j][1].lower()
            nama_extreme = data[idx_extreme][1].lower()
            if jalan1:
                if nama_j < nama_extreme:
                    idx_extreme = j
            else:
                if nama_j > nama_extreme:
                    idx_extreme = j
        data[i], data[idx_extreme] = data[idx_extreme], data[i]
    return data

def binary_search_by_nama(data, target):
    target = target.lower()
    left = 0
    right = len(data) - 1

    while left <= right:
        mid = (left + right) // 2
        nama_mid = data[mid][1].lower()
        if nama_mid == target:
            return mid
        elif nama_mid < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

def ambil_semua_data():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sayur")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def tampilkan_data(data):
    print("\n Data Sayur:")
    print("-" * 50)
    for row in data:
        print(f"ID: {row[0]:<3} | Nama: {row[1]:<15} | Stok: {row[2]:<5} | Harga: Rp{row[3]:,.0f}")
    print("-" * 50)


def update_harga_satuan(id_sayur, harga_baru):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE sayur SET harga_satuan = %s WHERE id_sayur = %s", (harga_baru, id_sayur))
        conn.commit()
        print("✅ Harga berhasil diperbarui.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal memperbarui harga: {e}")
    finally:
        cur.close()
        conn.close()


def pengelolaan_stok():
    while True:
        print("\n==== Menu Pengelolaan Stok Hasil Tani ====")
        print("1. Tampilkan sayur berdasarkan stok ")
        print("2. Tampilkan sayur berdasarkan urutan nama")
        print("3. Cari sayur dan ganti harga ")
        print("4. Kembali")
        pilihan = input("Pilih menu (1/2/3/4): ").strip()

        if pilihan == '1':
            clear_terminal()
            data = ambil_semua_data()
            data_sorted = selection_sort_by_stok(data, jalan=True)
            tampilkan_data(data_sorted)
            input("\nTekan Enter untuk kembali...")
            clear_terminal()

        elif pilihan == '2':
            clear_terminal()
            data = ambil_semua_data()
            data_sorted = selection_sort_by_nama(data, jalan1=True)
            tampilkan_data(data_sorted)
            input("\nTekan Enter untuk kembali...")
            clear_terminal()

        elif pilihan == '3':
            clear_terminal()
            data = ambil_semua_data()
            data_sorted = selection_sort_by_nama(data, jalan1=True)
            tampilkan_data(data_sorted)

            target = input("\nMasukkan nama sayur yang ingin dicari: ").strip()
            index = binary_search_by_nama(data_sorted, target)

            if index != -1:
                sayur = data_sorted[index]
                print(f"\n✅ Ditemukan: ID: {sayur[0]}, Nama: {sayur[1]}, Stok: {sayur[2]}, Harga: Rp{sayur[3]:,.0f}")
                harga_baru = input("Masukkan harga baru: ").strip()
                if harga_baru.isdigit():
                    update_harga_satuan(sayur[0], int(harga_baru))
                else:
                    print("❌ Harga tidak valid.")
            else:
                print("❌ Sayur tidak ditemukan.")

            input("\nTekan Enter untuk kembali...")
            clear_terminal()

        elif pilihan == '4':
            clear_terminal()
            break
        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1, 2, 3, atau 4.")

def pencatatan_transaksi():
    print("Menu Pencatatan Transaksi")
    # Tambahkan logika untuk pencatatan transaksi
    
    
main()
