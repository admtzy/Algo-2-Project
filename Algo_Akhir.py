import psycopg2
import webbrowser
import os
from datetime import date
from tabulate import tabulate
import time
# import sort

# file_path = os.path.abspath("peta.html")
# webbrowser.open(f"file://{file_path}")
def connect_db():
    conn = psycopg2.connect(
    host="localhost",
    database="DBAlgo2",
    user="postgres",
    password="@Raditya14",
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
    clear_terminal()
    while True:
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	     	        MENU                 ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||                1. Register                    ||')
        print('||                2. Login                       ||')
        print('||                3. Keluar                      ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()

        if pilihan == "1":
            menu_register()

        elif pilihan == "2":
            menu_login()

        elif pilihan == "3":
            clear_terminal()
            print('\n' + '=' * 20 + ' ANDA KELUAR DARI APLIKASI ' + '=' * 20 + '\n')
            time.sleep(1)
            clear_terminal()
            break

        else:
            print("Pilihan tidak valid.")
            kembali()

def menu_register():
    clear_terminal()
    print('\n' + '=' * 20 + ' REGISTRASI AKUN ' + '=' * 20 + '\n')
    nama = input("Nama: ")
    no_hp = input("No HP: ")
    password = input("Password (max 8 karakter): ")
    register(nama, no_hp, password)

def register(nama, no_hp, password):
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM akun WHERE no_hp = %s", (no_hp,))
    no_hp2 = cur.fetchone()[0]
    
    if no_hp2 is not None:
        print("Registrasi gagal: Nomor HP sudah digunakan!!!")
        kembali()
        menu_register()
    
    try:
        if no_hp2 is None:
            print("Memuat Peta", end="")
            for i in range(5):
                print(".", end="", flush=True)
                time.sleep(0.5) 
            file_path = os.path.abspath("peta.html")
            webbrowser.open(f"file://{file_path}")
            lokasi=input("Masukkan Lokasi Anda : ")
            latitude,longitude=lokasi.split(',')
            
        else:
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
            input("Tekan Enter untuk kembali ke menu utama...")
            kembali()
            
    except psycopg2.IntegrityError:
        conn.rollback()
        input("Registrasi gagal: Nomor HP sudah digunakan atau data tidak valid.")
        kembali()
        
    except Exception as e:
        conn.rollback()
        input("Terjadi kesalahan:", e)
        kembali()
        
    finally:
        cur.close()
        conn.close()
        
def menu_login():
    clear_terminal()
    print('\n' + '=' * 20 + ' LOGIN ' + '=' * 20 + '\n')
    no_hp = input("No HP: ")
    password = input("Password: ")
    login(no_hp, password)
        
def login(no_hp, password):
    try:
        conn = connect_db()
        cur = conn.cursor()

        cur.execute("""
            SELECT id_akun, nama, status_akun FROM akun
            WHERE no_hp = %s AND password = %s;
        """, (no_hp, password))
        user = cur.fetchone()

        if user:
            id_akun= user[0]
            nama= user[1]
            status = user[2]
            
            if status == "0":
                menu_owner(nama)
                
            else : 
                menu_pembeli(id_akun,nama)
            
        else:
            input("Login gagal: Nomor HP atau password salah!!!")
            kembali()

    except Exception as e:
        print("Terjadi kesalahan saat login:", e)
        
    finally:
        cur.close()
        conn.close()

def menu_owner(nama):
    while True :
        clear_terminal()
        print('\n' + '=' * 20 + f' Halo {nama} selamat datang di Aplikasi Petani!!! ' + '=' * 20 + '\n')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	     	     MENU OWNER              ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||                1. Penjualan Hasil Tani        ||')
        print('||                2. Rute Pengiriman             ||')
        print('||                3. Pencatatan Transaksi        ||')
        print('||                4. Pengelolaan Stok            ||')
        print('||                5. Keluar                      ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()
        
        if pilihan == "1":
            penjualan_hasil_tani()
            
        elif pilihan == "2":
            rute_pengiriman()
            
        elif pilihan == "3":
            pencatatan_transaksi()
        
        elif pilihan == "4":
            pengelolaan_stok()
        
        elif pilihan == "5":
            print('\n' + '=' * 20 + ' TERIMA KASIH TELAH MENGGUNAKAN APLIKASI TANI ' + '=' * 20 + '\n')
            time.sleep(1)
            clear_terminal()
            break
        
        else:
            print("Pilihan tidak valid.")
            kembali()
        
def menu_pembeli(id_akun, nama):
    while True :
        clear_terminal()
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	     	    MENU PEMBELI             ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||                1. Beli Hasil Tani             ||')
        print('||                2. Keluar                      ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()
        
        if pilihan == "1":
            beli_hasil_tani(id_akun)
            
        elif pilihan == "2":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        
        else:
            print("Pilihan tidak valid.")

def beli_hasil_tani (id_akun):
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU BELI HASIL TANI ' + '=' * 20 + '\n')
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
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU PENJUALAN HASIL TANI ' + '=' * 20 + '\n')
    # Tambahkan logika untuk penjualan hasil tani

def rute_pengiriman():
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU RUTE PENGIRIMAN ' + '=' * 20 + '\n')
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
    clear_terminal()
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sayur")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def tampilkan_data(data):
    clear_terminal()
    print('\n' + '=' * 20 + ' DATA SAYUR ' + '=' * 20 + '\n')
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
        print("✅ Harga berhasil diperbarui!!!")
        
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal memperbarui harga: {e}")
    
    finally:
        cur.close()
        conn.close()


def pengelolaan_stok():
    data = ambil_semua_data()
    data_sorted = selection_sort_by_stok(data, jalan=True)
    while True:
        clear_terminal()
        tampilkan_data(data_sorted)
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	      MENU PENGELOLAAN STOK          ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||    1. Tampilkan Sayur Berdasar Stok           ||')
        print('||    2. Tampilkan Sayur Berdasarkan Urutan Nama ||')
        print('||    3. Cari Sayur dan Ganti Harga              ||')
        print('||    4. Kembali                                 ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()

        if pilihan == '1':
            data = ambil_semua_data()
            data_sorted = selection_sort_by_stok(data, jalan=True)
            clear_terminal()

        elif pilihan == '2':
            data = ambil_semua_data()
            data_sorted = selection_sort_by_nama(data, jalan1=True)
            clear_terminal()

        elif pilihan == '3':
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

            kembali()

        elif pilihan == '4':
            clear_terminal()
            break
        else:
            print("❌ Pilihan tidak valid. Silakan pilih 1, 2, 3, atau 4.")
            kembali()

def pencatatan_transaksi():
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU PENCATATAN TRANSAKSI ' + '=' * 20 + '\n')
    # Tambahkan logika untuk pencatatan transaksi
    
    
main()