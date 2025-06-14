import psycopg2
import webbrowser
import os
from datetime import date
from tabulate import tabulate
import time

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
    
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("SELECT * FROM akun WHERE no_hp = %s", (no_hp,))
    no_hp2 = cur.fetchone()
    
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
            lokasi=input("\nMasukkan Lokasi Anda : ")
            latitude,longitude=lokasi.split(',')
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
            clear_terminal()
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
        print('\n' + '=' * 20 + f' Halo {nama} selamat datang di Aplikasi Petani!!! ' + '=' * 20 + '\n')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	     	    MENU PEMBELI             ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||                1. Beli Hasil Tani             ||')
        print('||                2. Riwayat Pembelian           ||')
        print('||                3. Keluar                      ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()
        
        if pilihan == "1":
            beli_hasil_tani(id_akun)
            
        elif pilihan == "2":
            riwayat_pembelian(id_akun)
            
        elif pilihan == "3":
            print("Terima kasih telah menggunakan aplikasi ini.")
            clear_terminal()
            break
        
        else:
            print("Pilihan tidak valid.")

def beli_hasil_tani (id_akun):
    while True :
        try :
            clear_terminal()
            print('\n' + '=' * 20 + ' MENU BELI HASIL TANI ' + '=' * 20 + '\n')
            data=data_full()
            print(tabulate(data,headers=["ID", "Nama", "Stok", "Harga"],tablefmt="psql"))
            nama_sayur = str(input("Masukkan nama sayur (0 untuk kembali): ").strip())
            jumlah_beli = int(input("Masukkan jumlah beli: "))
            break
        except ValueError :
            input("Data yang dimasukkan salah...")
            continue
    if nama_sayur == "0" :
        return
    conn = connect_db()
    cur = conn.cursor()
    query = f"""
        SELECT id_sayur, harga_satuan
        FROM sayur
        WHERE nama_sayur ilike '{nama_sayur}'
    """
    cur.execute(query)
    data_sayur = cur.fetchone()
    
    try:
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

    except Exception as e:
        input(f"❌ Terjadi kesalahan: {e}")

        clear_terminal()
        
    finally:
        cur.close()
        conn.close()

def riwayat_pembelian(id_akun):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM request_pembelian where id_akun = {id_akun}")
    data = cur.fetchall()
    cur.close()
    conn.close()

    clear_terminal()
    print('\n' + '=' * 20 + ' RIWAYAT PEMBELIAN ' + '=' * 20 + '\n')
    print(tabulate(data,headers=["ID Request", "ID Akun", "ID Sayur", "Nama Sayur","Jumlah Beli", "Total Harga", "Status"],tablefmt="psql"))
    input("Tekan Enter Untuk Kembali...")
    # Tambahkan logika untuk menampilkan riwayat pembelian
 
def penjualan_hasil_tani():

    while True:
        conn = connect_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM request_pembelian where status != 'S'")
        data = cur.fetchall()
        cur.close()
        conn.close()

        clear_terminal()
        print('\n' + '=' * 20 + ' MENU PENJUALAN HASIL TANI ' + '=' * 20 + '\n')
        # data_full()
        print(tabulate(data,headers=["ID Request", "ID Akun", "ID Sayur", "Nama Sayur","Jumlah Beli", "Total Harga", "Status"],tablefmt="fancy_grid"))
        # print(tabulate(data, headers=colnames, tablefmt="psql"))
        pilihan = input("Masukkan id request yang ingin diproses (atau '0' untuk keluar): ").strip()
        if pilihan == '0':
            break
        
        conn = connect_db()
        cur = conn.cursor()

        # Periksa apakah ID request valid
        cur.execute("SELECT * FROM request_pembelian WHERE id_request = %s", (pilihan,))
        request = cur.fetchone()

        if not request:
            print(f"\n[!] ID request {pilihan} tidak ditemukan.")
            input("Tekan Enter untuk lanjut...")
            cur.close()
            conn.close()
            continue

        status_input = input("Masukkan status untuk request ini (K = Kirim / T = Tolak / S = Selesai): ").strip().upper()

        if status_input not in ['K', 'T', 'S']:
            print("\n⚠️Status tidak valid!!!")
            kembali()
            cur.close()
            conn.close()
            continue

        elif status_input == 'S':
            cur.execute(
                "UPDATE request_pembelian SET status = 'S' WHERE id_request = %s", (pilihan,)
            )
            cur.execute(
                "INSERT INTO transaksi (id_request, tanggal) VALUES (%s, %s)",
                (pilihan, date.today())
            )
            print(f"\n✅Request ID {pilihan} berhasil diproses dan dimasukkan ke transaksi.")
            
        elif status_input == 'K':
            cur.execute(
                "UPDATE request_pembelian SET status = 'K' WHERE id_request = %s", (pilihan,)
            )
            print(f"\n✅Request ID {pilihan} sedang dikirim!!!")

        conn.commit()
        cur.close()
        conn.close()
        input("Tekan Enter untuk lanjut...")
    clear_terminal()

def pencatatan_transaksi():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM request_pembelian where status = 'S' ")
    data = cur.fetchall()
    cur.close()
    conn.close()
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU PENCATATAN TRANSAKSI ' + '=' * 20 + '\n')
    print(tabulate(data,headers=["ID Request", "ID Akun", "ID Sayur", "Nama Sayur","Jumlah Beli", "Total Harga", "Status"],tablefmt="fancy_grid"))
    
    input("Tekan Enter Untuk Kembali")
    
def rute_pengiriman():
    clear_terminal()
    print('\n' + '=' * 20 + ' MENU RUTE PENGIRIMAN ' + '=' * 20 + '\n')
    # Tambahkan logika untuk rute pengiriman

def sort_stock(data):
    n = len(data)
    for i in range(n):
        indek_min = i
        for j in range(i + 1, n):
            if data[j][2] < data[indek_min][2]:
                indek_min = j
        data[i], data[indek_min] = data[indek_min], data[i]
    return data

def sort_id(data):
    n = len(data)
    for i in range(n):
        indek_min = i
        for j in range(i + 1, n):
            if data[j][0] < data[indek_min][0]:
                indek_min = j
        data[i], data[indek_min] = data[indek_min], data[i]
    return data

def sort_nama(data):
    n = len(data)
    for i in range(n):
        index_min = i
        for j in range(i + 1, n):
            if data[j][1].lower() < data[index_min][1].lower():
                index_min = j
        data[i], data[index_min] = data[index_min], data[i]
    return data

def cari_nama(data, target):
    target = target.lower()
    kiri, kanan = 0, len(data) - 1
    while kiri <= kanan:
        tengah = (kiri + kanan) // 2
        if data[tengah][1].lower() == target:
            return tengah
        elif data[tengah][1].lower() < target:
            kiri = tengah + 1
        else:
            kanan = tengah - 1
    return -1

def data_full():
    conn = connect_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM sayur")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

def tambah_sayur(nama, stok, harga):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("INSERT INTO sayur (nama, stok, harga_satuan) VALUES (%s, %s, %s)", (nama, stok, harga))
        conn.commit()
        print("✅ Sayur berhasil ditambahkan.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal menambahkan sayur: {e}")
    finally:
        cur.close()
        conn.close()

def hapus_sayur(id_sayur):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM sayur WHERE id_sayur = %s", (id_sayur,))
        conn.commit()
        print("✅ Sayur berhasil dihapus.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal menghapus sayur: {e}")
    finally:
        cur.close()
        conn.close()

def update_harga(id_sayur, harga_baru):
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

def tambah_stok(id_sayur, tambahan):
    conn = connect_db()
    cur = conn.cursor()
    try:
        cur.execute("UPDATE sayur SET stok = stok + %s WHERE id_sayur = %s", (tambahan, id_sayur))
        conn.commit()
        print("✅ Stok berhasil ditambahkan.")
    except Exception as e:
        conn.rollback()
        print(f"❌ Gagal menambahkan stok: {e}")
    finally:
        cur.close()
        conn.close()

def min_5(data):
    per_page = 5
    total = len(data)
    pages = (total + per_page - 1) // per_page
    current = 0
    while True:
        clear_terminal()
        print(tabulate(data[current * per_page: (current + 1) * per_page], headers=["ID", "Nama", "Stok", "Harga"], tablefmt="fancy_grid"))
        print(f"\nPage {current + 1} of {pages}")
        print("\n1. Next Page | 2. Prev Page | 0. Exit View")
        cmd = input("Pilih opsi: ")
        if cmd == "1" and current < pages - 1:
            current += 1
        elif cmd == "2" and current > 0:
            current -= 1
        elif cmd == "0":
            break

def pengelolaan_stok():
    data = data_full()
    while True:
        clear_terminal()
        min_5(data)
        # data_full(data_sorted)
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	      MENU PENGELOLAAN STOK          ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||    1. Tampilkan Sayur Berdasar Stok           ||')
        print('||    2. Tampilkan Sayur Berdasarkan Urutan Nama ||')
        print('||    3. Cari Sayur dan Ganti Harga              ||')
        print('||    4. Tambah Sayur                            ||')
        print('||    5. Hapus Sayur                             ||')
        print('||    6. Tambah Stock                            ||')
        print('||    7. Kembali                                 ||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        pilihan = input('Silahkan pilih menu: ').strip()

        if pilihan == '1':
            data = sort_stock(data)
            min_5(data)

        elif pilihan == '2':
            data = sort_nama(data)
            min_5(data)

        elif pilihan == '3':
            data = sort_nama(data)
            min_5(data)
            target = input("\nMasukkan nama sayur: ").strip()
            index = cari_nama(data, target)
            if index != -1:
                sayur = data[index]
                harga_baru = input("Masukkan harga baru: ").strip()
                if harga_baru.isdigit():
                    update_harga(sayur[0], int(harga_baru))
                    data = sort_id (data_full())
                else:
                    print("❌ Harga tidak valid.")
            else:
                print("❌ Sayur tidak ditemukan.")

        elif pilihan == '4':
            nama = input("Masukkan nama sayur: ").strip()
            stok = input("Masukkan stok: ").strip()
            harga = input("Masukkan harga satuan: ").strip()
            if stok.isdigit() and harga.isdigit():
                tambah_sayur(nama, int(stok), int(harga))
                data = sort_id (data_full())
            else:
                print("❌ Input stok atau harga tidak valid.")

        elif pilihan == '5':
            clear_terminal()
            data = sort_id(data_full())
            min_5(data)
            id_del = input("\nMasukkan ID sayur yang ingin dihapus: ").strip()
            if id_del.isdigit():
                id_del = int(id_del)
                say = None
                for item in data:
                    if item[0] == id_del:
                        say = item
                        break
                if say:
                    print("\n✅ Sayur yang akan dihapus:")
                    konfirmasi = input("Yakin ingin menghapus? (y/n): ").strip().lower()
                    if konfirmasi == 'y':
                        hapus_sayur(id_del)
                    else:
                        print("❌ Dibatalkan.")
                else:
                    print("❌ ID tidak ditemukan.")
            else:
                print("❌ ID tidak valid.")

        elif pilihan == '6':
            clear_terminal()
            data = sort_id(data_full())
            min_5(data)
            id_sayur = input("\nMasukkan ID sayur yang ingin ditambah stok: ").strip()
            if id_sayur.isdigit():
                id_sayur = int(id_sayur)
                say1 = None
                for item in data:
                    if item[0] == id_sayur:
                        say1 = item
                        break
                if say1:
                    print("\n✅ Sayur yang dipilih:")
                    print(tabulate([say1], headers=["ID", "Nama", "Stok", "Harga"], tablefmt="fancy_grid"))
                    tambahan = input("Masukkan jumlah stok tambahan: ").strip()
                    if tambahan.isdigit():
                        tambah_stok(id_sayur, int(tambahan))
                        data = sort_id(data_full())
                        kembali()
                    else:
                        print("❌ Jumlah stok tidak valid.")
                else:
                    print("❌ ID tidak ditemukan.")
            else:
                print("❌ ID tidak valid.")

        elif pilihan == '7':
            break
        else:
            print("❌ Pilihan tidak valid.")


    
    
main()