import psycopg2
import webview
import os
from datetime import date
from tabulate import tabulate
import time
from Rute import tampilkan_rute

def connect_db():
    conn = psycopg2.connect(
    host="localhost",
    database="Algo2",
    user="postgres",
    password="syadid1306",
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
        clear_terminal()
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
                
            html_path = os.path.abspath("Ambil_Koordinat.html")
            window = webview.create_window("Ambil Koordinat", f"file://{html_path}")
            webview.start(lambda: tampilkan_rute(window))
            clear_terminal()
            while True :
                try :
                        lokasi=input("\nMasukkan Lokasi Anda : ")
                        bagian = lokasi.split(',')
                        if bagian == "" :
                            raise ValueError
                        if len(bagian) != 2:
                            raise ValueError
                        break

                except ValueError :
                    clear_terminal()
            latitude = (bagian[0].strip())
            longitude =(bagian[1].strip())
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
        
    # except Exception as e:
    #     conn.rollback()
    #     input(f"Terjadi kesalahan: {e}")
    #     kembali()
        
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
            html_path = os.path.abspath("Rute_Pengiriman.html")
            window = webview.create_window("Rute Pengiriman", f"file://{html_path}")
            webview.start(lambda: tampilkan_rute(window))
            clear_terminal()
            
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

def beli_hasil_tani(id_akun):
    while True:
        try:
            clear_terminal()
            print('\n' + '=' * 20 + ' MENU BELI HASIL TANI ' + '=' * 20 + '\n')
            data = data_full()
            print(tabulate(data, headers=["ID", "Nama", "Stok", "Harga"], tablefmt="fancy_grid"))
            
            nama_sayur = str(input("Masukkan nama sayur (0 untuk kembali): ").strip())
            if nama_sayur == "0":
                return
            
            jumlah_beli = int(input("Masukkan jumlah beli: "))
            
            conn = connect_db()
            cur = conn.cursor()
            cur.execute("SELECT stok FROM sayur WHERE nama_sayur ILIKE %s", (nama_sayur,))
            result = cur.fetchone()
            cur.close()
            conn.close()

            if not result:
                input("⚠️ Sayur tidak ditemukan. Tekan Enter untuk ulang...")
                continue

            stok_tersedia = result[0]

            if jumlah_beli > stok_tersedia:
                input(f"⚠️ Jumlah melebihi stok tersedia ({stok_tersedia}). Tekan Enter untuk ulang...")
                continue
            break
        
        except ValueError:
            input("⚠️ Data yang dimasukkan salah... Tekan Enter untuk ulang...")
            continue

    
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
    print(tabulate(data,headers=["ID Request", "ID Akun", "ID Sayur", "Nama Sayur","Jumlah Beli", "Total Harga", "Status"],tablefmt="fancy_grid"))
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
        print(tabulate(data,headers=["ID Request", "ID Akun", "ID Sayur", "Nama Sayur","Jumlah Beli", "Total Harga", "Status"],tablefmt="fancy_grid"))
        pilihan = input("Masukkan id request yang ingin diproses (atau '0' untuk keluar): ").strip()
        
        if pilihan == '0':
            break
        
        else:
            if not pilihan.isdigit():
                print("\n⚠️ID request harus berupa angka!!!")
                time.sleep(1)
                continue
            
            pilihan = int(pilihan)
            if pilihan <= 0:
                print("\n⚠️ID request tidak valid!!!")
                time.sleep(1)
                continue
            
        conn = connect_db()
        cur = conn.cursor()

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
            
            id_sayur = request[2]
            jumlah_beli = request[4]
            
            cur.execute("SELECT stok FROM sayur WHERE id_sayur = %s", (id_sayur,))
            stok_skrg = cur.fetchone()
        
            if stok_skrg:
                stok_baru = stok_skrg[0] - jumlah_beli
                
                if stok_baru < 0:
                    print("\n⚠️ Stok tidak mencukupi untuk menyelesaikan request ini!")
                    
                else:
                    cur.execute("UPDATE sayur SET stok = %s WHERE id_sayur = %s", (stok_baru, id_sayur))
                    print(f"\n✅ Request ID {pilihan} berhasil diproses, stok diperbarui.")

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

def sort_data(data, berdasarkan='id'):
    n = len(data)
    indeks = {'id': 0, 'nama': 1, 'stok': 2}
    if berdasarkan not in indeks:
        print("Pilihan pengurutan tidak valid. Silakan pilih 'id', 'nama', atau 'stok'.")
        return data 
    kunci = indeks[berdasarkan]

    for i in range(n):
        index_min = i
        for j in range(i + 1, n):
            if berdasarkan == 'nama':
                if data[j][kunci].lower() < data[index_min][kunci].lower():
                    index_min = j
            else:
                if data[j][kunci] < data[index_min][kunci]:
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
        cur.execute("INSERT INTO sayur (nama_sayur, stok, harga_satuan) VALUES (%s, %s, %s)", (nama, stok, harga))
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

def pengelolaan_stok():
    awal = 0
    liss = 5

    while True:
        data = sort_data(data_full(), 'id')
        total = len(data)
        total_pages = (total + liss - 1) // liss

        clear_terminal()
        print("=== Data Sayur ===")
        start = awal * liss
        end = start + liss
        tampil = data[start:end]

        print(tabulate(tampil, headers=["ID", "Nama", "Stok", "Harga"], tablefmt="fancy_grid"))
        print(f"\nPage {awal + 1} dari {total_pages}")

        print('\n+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')
        print('|| ^^^ 	      MENU PENGELOLAAN STOK          ^^^ ||')
        print('||---------    Silahkan pilih menu      ---------||')
        print('||    1. Urut berdasarkan Stok                   ||')
        print('||    2. Urut berdasarkan Nama                   ||')
        print('||    3. Ganti Harga                             ||')
        print('||    4. Tambah Sayur                            ||')
        print('||    5. Hapus Sayur                             ||')
        print('||    6. Tambah Stok                             ||')
        print('||    7. Kembali                                 ||')
        print('||-----------------------------------------------||')
        print('||    n. Next Page | p. Prev Page | m. Pilih Menu||')
        print('+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+:+')

        opsi = input("Masukkan pilihan: ").strip().lower()

        if opsi == 'n' and awal < total_pages - 1:
            awal += 1
        elif opsi == 'p' and awal > 0:
            awal -= 1
        elif opsi == 'm':
            pilihan = input("\nMasukkan angka menu (1–7): ").strip()

            if pilihan == '1':
                data = sort_data(data, 'stok')
                awal = 0

            elif pilihan == '2':
                data = sort_data(data, 'nama')
                awal = 0

            elif pilihan == '3':
                data = sort_data(data, 'nama')
                target = input("\nMasukkan nama sayur: ").strip()
                index = cari_nama(data, target)
                if index != -1:
                    sayur = data[index]
                    harga_baru = input("Masukkan harga baru: ").strip()
                    if harga_baru.isdigit():
                        update_harga(sayur[0], int(harga_baru))
                    else:
                        print("❌ Harga tidak valid.")
                else:
                    print("❌ Sayur tidak ditemukan.")
                input("Tekan Enter untuk lanjut...")

            elif pilihan == '4':
                nama = input("Masukkan nama sayur: ").strip()
                stok = input("Masukkan stok: ").strip()
                harga = input("Masukkan harga satuan: ").strip()
                if stok.isdigit() and harga.isdigit():
                    tambah_sayur(nama, int(stok), int(harga))
                else:
                    print("❌ Input tidak valid.")
                input("Tekan Enter untuk lanjut...")

            elif pilihan == '5':
                id_del = input("Masukkan ID sayur yang ingin dihapus: ").strip()
                if id_del.isdigit():
                    hapus_sayur(int(id_del))
                else:
                    print("❌ ID tidak valid.")
                input("Tekan Enter untuk lanjut...")

            elif pilihan == '6':
                data = sort_data(data, 'nama')
                target = input("Masukkan nama sayur yang ingin ditambah stok: ").strip()
                index = cari_nama(data, target)
                if index != -1:
                    tambahan = input("Masukkan jumlah tambahan stok: ").strip()
                    if tambahan.isdigit():
                        tambah_stok(data[index][0], int(tambahan))
                    else:
                        print("❌ Jumlah tidak valid.")
                else:
                    print("❌ Sayur tidak ditemukan.")
                input("Tekan Enter untuk lanjut...")

            elif pilihan == '7':
                break

            else:
                print("❌ Pilihan tidak valid.")
                input("Tekan Enter untuk lanjut...")

        elif opsi == '7':
            break
        else:
            print("❌ Input tidak valid. Gunakan n, p, m, atau 1–7.")
            input("Tekan Enter untuk lanjut...")
            
main()