import json
import os
import pyfiglet
import webbrowser
import os
import time
import socket
import requests
from colorama import Fore, Style, init
from prettytable import PrettyTable
from datetime import datetime

produk_file = "produk.json"
rental_file = "rental.json"
deleted_produk_file = "deleted_produk.json"

HIJAU = "\033[92m"
PUTIH = "\033[0m" 



# Inisialisasi colorama untuk warna terminal
init(autoreset=True)

def print_logo():
    os.system("cls" if os.name == "nt" else "clear")  # Bersihkan layar terminal
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "⚡⚡ VULNXPERT - RENTAL TOOLS HACKER ⚡⚡\n")
    time.sleep(0.5)

    # Membuat tabel mewah
    table = PrettyTable()
    table.field_names = [Fore.LIGHTYELLOW_EX + "💀 VULNXPERT - RENTAL TOOLS HACKER 💀" + Fore.RESET]
    table.align["💀 VULNXPERT - RENTAL TOOLS HACKER 💀"] = "c"
    table.add_row([Fore.LIGHTGREEN_EX + "⚔️ HACK THE PLANET ⚔️" + Fore.RESET])
    table.add_row([Fore.YELLOW + "🌟 TOOLS PROFESSIONAL UNTUK PENTESTER 🌟" + Fore.RESET])
    table.add_row([Fore.LIGHTCYAN_EX + "🔥 GUNAKAN DENGAN BIJAK! 🔥" + Fore.RESET])
    
    print(Fore.LIGHTYELLOW_EX + table.get_string())

    time.sleep(0.5)

    # Efek loading dramatis
    print(Fore.LIGHTBLACK_EX + "\n[ LOADING SYSTEM... ]", end="")
    for _ in range(5):
        time.sleep(0.4)
        print(Fore.LIGHTYELLOW_EX + " ⚡", end="", flush=True)
    print("\n")

    # ASCII Tengkorak
    logo = Fore.LIGHTGREEN_EX + """
       ______
     .-        -.
    /            \\
   |              |
   |,  .-.  .-.  ,|
   | )(_o/  \o_)( |
   |/     /\     \|
   (_     ^^     _)
    \__|IIIIII|__/
     | \IIIIII/ |
     \          /
      `--------`⠀⠀
    """ + Fore.RESET

    print(logo)
    print(Fore.LIGHTYELLOW_EX + Style.BRIGHT + "\n🎉 SELAMAT MENYEWA DI VULNXPERT 🎉\n")

# Panggil fungsi untuk menampilkan logo
print_logo()


def database_menu():
    password = "dbadmin123"  # Password khusus untuk menu database
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        entered_password = input("\nMasukkan kata sandi database: ")
        if entered_password == password:
            print("\nAkses diterima. Selamat datang di Menu Database.")
            database_panel()
            return
        else:
            attempts += 1
            print(f"Kata sandi salah! Percobaan tersisa: {max_attempts - attempts}")
    
    print("\nAnda telah mencapai batas maksimal percobaan.")
    print("Kembali ke menu utama...")
    return

def database_panel():
    while True:
        print("\n--- Menu Database ---")
        print("1. Lihat seluruh data")
        print("2. Lihat riwayat perubahan database")
        print("3. Reset riwayat perubahan")
        print("4. Kelola Feedback")  # Tambahan Menu Kelola Feedback
        print("5. Kembali ke menu admin")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            show_all_data()
        elif choice == '2':
            show_history()
        elif choice == '3':
            reset_history()
        elif choice == '4':
            kelola_feedback()  # Menu baru untuk kelola feedback
        elif choice == '5':
            return  # Kembali ke menu admin
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


def kelola_feedback():
    while True:
        print("\n--- Kelola Feedback ---")
        print("1. Lihat Feedback")
        print("2. Hapus Feedback")
        print("3. Kembali ke Menu Database")
        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            lihat_feedback()
        elif choice == '2':
            hapus_feedback()
        elif choice == '3':
            return  # Kembali ke menu Database
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


def lihat_feedback():
    try:
        with open("feedback.json", "r") as file:
            feedbacks = file.readlines()
            if feedbacks:
                print("\n--- Daftar Feedback ---")
                for i, feedback in enumerate(feedbacks, start=1):
                    print(f"{i}. {feedback.strip()}")
            else:
                print("Belum ada feedback yang tersedia.")
    except FileNotFoundError:
        print("Belum ada feedback yang tersedia.")


import json

def hapus_feedback():
    try:
        with open("feedback.json", "r") as file:
            feedbacks = json.load(file)

        if not feedbacks:
            print("Belum ada feedback yang tersedia.")
            return

        print("\n--- Hapus Feedback ---")
        for i, feedback in enumerate(feedbacks, start=1):
            print(f"{i}. Nama: {feedback['nama']}, Waktu: {feedback['waktu']}, Feedback: {feedback['feedback']}")

        pilihan = input("Masukkan nomor feedback yang ingin dihapus (atau 0 untuk batal): ")

        if pilihan.isdigit():
            pilihan = int(pilihan)
            if 1 <= pilihan <= len(feedbacks):
                feedbacks.pop(pilihan - 1)
                with open("feedback.json", "w") as file:
                    json.dump(feedbacks, file, indent=4)

                print("Feedback berhasil dihapus!")
            elif pilihan == 0:
                print("Penghapusan dibatalkan.")
            else:
                print("Nomor tidak valid!")
        else:
            print("Masukkan angka yang valid!")

    except FileNotFoundError:
        print("Belum ada feedback yang tersedia.")
    except json.JSONDecodeError:
        print("Terjadi kesalahan dalam membaca file feedback.")


def show_all_data():
    print(Fore.YELLOW + Style.BRIGHT + "\n╔════════════════════════════════╗")
    print("║      📊 DATABASE RENTAL 📊      ║")
    print("╚════════════════════════════════╝")

    # Tampilkan Data Produk
    print(Fore.CYAN + "\n📌 Data Produk:")
    table_produk = PrettyTable(["ID", "Nama Produk", "Harga (Rp)", "Status"])
    table_produk.align["Nama Produk"] = "l"
    table_produk.align["Harga (Rp)"] = "r"

    for produk in produk_db:
        status_warna = Fore.GREEN + "✅ Tersedia" if produk['status'] == "Tersedia" else Fore.RED + "❌ Tidak Tersedia"
        table_produk.add_row([produk['id'], Fore.LIGHTYELLOW_EX + produk['nama'] + Fore.RESET, f"{produk['harga']:,}", status_warna])

    print(Fore.LIGHTBLACK_EX + table_produk.get_string())

    # Tampilkan Data Penyewaan
    print(Fore.MAGENTA + "\n📌 Data Penyewaan:")
    if rental_db:
        table_rental = PrettyTable(["Nama Pengguna", "Produk", "Durasi (hari)", "Total Harga", "Status"])
        for rental in rental_db:
            status_sewa = Fore.GREEN + "🟢 Aktif" if rental['status'] == "Aktif" else Fore.RED + "🔴 Selesai"
            table_rental.add_row([
                rental['nama_pengguna'],
                Fore.LIGHTYELLOW_EX + rental['nama_produk'] + Fore.RESET,
                rental['durasi_hari'],
                f"{rental['total_harga']:,}",
                status_sewa
            ])
        print(Fore.LIGHTBLACK_EX + table_rental.get_string())
    else:
        print(Fore.RED + "🚫 Tidak ada penyewaan aktif.")

    # Tampilkan Data Produk yang Dihapus
    print(Fore.RED + "\n📌 Data Produk yang Dihapus:")
    if deleted_produk_db:
        table_deleted = PrettyTable(["ID", "Nama Produk", "Harga (Rp)"])
        for deleted_produk in deleted_produk_db:
            table_deleted.add_row([deleted_produk['id'], Fore.LIGHTRED_EX + deleted_produk['nama'] + Fore.RESET, f"{deleted_produk['harga']:,}"])
        print(Fore.LIGHTBLACK_EX + table_deleted.get_string())
    else:
        print(Fore.YELLOW + "🚫 Tidak ada produk yang dihapus.")

    input(Fore.CYAN + "\n🔘 Tekan Enter untuk kembali ke menu database...")

# Tambahan fitur riwayat perubahan database
history = []

def add_to_history(action, data):
    history.append({"action": action, "data": data, "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")})

def show_history():
    print("\n--- Riwayat Perubahan Database ---")
    if not history:
        print("Belum ada riwayat perubahan.")
    else:
        for i, record in enumerate(history, 1):
            print(f"{i}. {record['timestamp']} | Aksi: {record['action']} | Data: {record['data']}")
    input("\nTekan Enter untuk kembali ke menu database...")

def reset_history():
    global history
    confirm = input("Apakah Anda yakin ingin menghapus semua riwayat perubahan? (Y/N): ").lower()
    if confirm == 'y':
        history.clear()
        print("Riwayat perubahan berhasil dihapus.")
    else:
        print("Riwayat perubahan tidak dihapus.")

def konfirmasi_sewa():
    menunggu_konfirmasi = [r for r in rental_db if r["status"] == "Menunggu Konfirmasi"]
    
    if not menunggu_konfirmasi:
        print("\nTidak ada penyewaan yang menunggu konfirmasi.")
        return
    
    print("\n--- Daftar Penyewaan Menunggu Konfirmasi ---")
    for i, sewa in enumerate(menunggu_konfirmasi, 1):
        print(f"{i}. Nama: {sewa['nama_pengguna']} | Produk: {sewa['nama_produk']} | Total: {sewa['total_harga']} | Waktu: {sewa['waktu_peminjaman']}")
    
    pilihan = int(input("\nPilih nomor penyewaan yang ingin dikonfirmasi (0 untuk batal): "))
    
    if pilihan == 0:
        print("Konfirmasi dibatalkan.")
        return
    
    sewa = menunggu_konfirmasi[pilihan - 1]
    produk = next(p for p in produk_db if p["id"] == sewa["id_produk"])
    
    sewa["status"] = "Belum Dikembalikan"
    produk["status"] = "Tidak Tersedia"
    
    print(f"Penyewaan produk '{sewa['nama_produk']}' oleh {sewa['nama_pengguna']} berhasil dikonfirmasi.")
    save_data()


def load_data():
    global produk_db, rental_db, deleted_produk_db
    if os.path.exists(produk_file):
        with open(produk_file, 'r') as f:
            produk_db = json.load(f)
    else:
        produk_db = [
            {"id": 1, "nama": "BurpSuite Enterprise", "harga": 500000, "status": "Tersedia"},
            {"id": 2, "nama": "Nessus", "harga": 45000, "status": "Tersedia"},
            {"id": 3, "nama": "Metasploit Pro", "harga": 600000, "status": "Tersedia"}
        ]

    if os.path.exists(rental_file):
        with open(rental_file, 'r') as f:
            rental_db = json.load(f)
    else:
        rental_db = []

    if os.path.exists(deleted_produk_file):
        with open(deleted_produk_file, 'r') as f:
            deleted_produk_db = json.load(f)
    else:
        deleted_produk_db = []

    return produk_db, rental_db, deleted_produk_db

def save_data():
    with open(produk_file, 'w') as f:
        json.dump(produk_db, f, indent=4)

    with open(rental_file, 'w') as f:
        json.dump(rental_db, f, indent=4)

def restore_deleted_produk():
    global produk_db, deleted_produk_db
    if deleted_produk_db:
        print("\n--- Daftar Produk yang Dihapus ---")
        for p in deleted_produk_db:
            print(f"ID: {p['id']} | Nama: {p['nama']} | Harga: {p['harga']}")
        
        restore = input("\nApakah Anda ingin mengembalikan produk yang dihapus? (Y/N): ").lower()
        if restore == 'y':
            for p in deleted_produk_db:
                produk_db.append(p)
            print(f"{len(deleted_produk_db)} produk berhasil dikembalikan.")
            deleted_produk_db.clear()
            save_data()
        else:
            print("Tidak ada produk yang dikembalikan.")

def ubah_produk():
    print_produk()
    id_produk = int(input("\nMasukkan ID produk yang ingin diubah: "))
    
    produk = next((p for p in produk_db if p["id"] == id_produk), None)
    
    if not produk:
        print("Produk tidak ditemukan!")
        return
    
    print("\nMau mengganti apa? ")
    print("1. Nama Produk")
    print("2. Harga Sewa per Hari")
    choice = input("Pilih (1/2): ")
    
    if choice == '1':
        produk["nama"] = input("Masukkan nama produk baru: ")
        print("Nama produk berhasil diubah.")
    elif choice == '2':
        produk["harga"] = int(input("Masukkan harga sewa baru per hari: "))
        print("Harga produk berhasil diubah.")
    else:
        print("Pilihan tidak valid.")
    
    save_data()

def tambah_produk():
    id_baru = len(produk_db) + 1
    nama = input("Masukkan nama produk baru: ")
    harga = int(input("Masukkan harga sewa per hari: "))
    
    produk_baru = {"id": id_baru, "nama": nama, "harga": harga, "status": "Tersedia"}
    produk_db.append(produk_baru)
    
    add_to_history("Tambah Produk", produk_baru)  
    print(f"Produk '{nama}' berhasil ditambahkan.")
    save_data()

def hapus_produk():
    print_produk()
    id_produk = int(input("\nMasukkan ID produk yang ingin dihapus: "))
    
    produk = next((p for p in produk_db if p["id"] == id_produk), None)
    
    if not produk:
        print("Produk tidak ditemukan!")
        return
    
    deleted_produk_db.append(produk)
    produk_db.remove(produk)
    
    add_to_history("Hapus Produk", produk)  # Catat ke riwayat perubahan
    print(f"Produk '{produk['nama']}' berhasil dihapus.")
    save_data()

def kelola_barang():
    while True:
        print("\n--- Menu Kelola Barang ---")
        print("1. Ubah Nama, Harga, dan ID Barang")
        print("2. Tambah Barang")
        print("3. Hapus Barang")
        print("4. Kembalikan Produk yang Dihapus")
        print("5. Kembali ke Menu Admin")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            ubah_produk()
        elif choice == '2':
            tambah_produk()
        elif choice == '3':
            hapus_produk()
        elif choice == '4':
            restore_deleted_produk()
        elif choice == '5':
            return  # Kembali ke menu admin
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

from datetime import datetime

def sewa_produk():
    print_produk()

    # Header penyewaan
    print(Fore.YELLOW + Style.BRIGHT + "\n╔════════════════════════════════╗")
    print("║  🚀  PROSES SEWA PRODUK   🚀  ║")
    print("╚════════════════════════════════╝")

    try:
        id_produk = int(input(Fore.CYAN + "\n🆔 Masukkan ID produk yang ingin disewa: " + Fore.RESET))

        produk = next((p for p in produk_db if p["id"] == id_produk and p["status"] == "Tersedia"), None)

        if not produk:
            print(Fore.RED + "❌ Produk tidak tersedia atau sudah disewa!")
            return

        hari_rental = int(input(Fore.CYAN + "📅 Masukkan durasi rental dalam hari: " + Fore.RESET))
        waktu_sekarang = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        total_harga = produk["harga"] * hari_rental
        print(Fore.GREEN + f"\n💰 Harga sewa per hari: Rp {produk['harga']:,}")
        print(Fore.GREEN + f"💵 Total sewa untuk {hari_rental} hari: Rp {total_harga:,}")

        nama_pengguna = input(Fore.CYAN + "👤 Masukkan nama pengguna: " + Fore.RESET)
        no_telepon = input(Fore.CYAN + "📞 Masukkan nomor telepon: " + Fore.RESET)

        # Tambahkan data penyewaan ke database
        rental_db.append({
            "id_produk": produk["id"],
            "nama_produk": produk["nama"],
            "harga_per_hari": produk["harga"],
            "durasi_hari": hari_rental,
            "total_harga": total_harga,
            "nama_pengguna": nama_pengguna,
            "no_telepon": no_telepon,
            "status": "Menunggu Konfirmasi",
            "waktu_peminjaman": waktu_sekarang
        })

        # Ubah status produk menjadi tidak tersedia
        produk["status"] = "Tidak Tersedia"

        print(Fore.GREEN + f"\n✅ Penyewaan produk '{produk['nama']}' berhasil diajukan.")
        print(Fore.YELLOW + "⏳ Menunggu konfirmasi admin...\n")

        # Simpan perubahan data
        save_data()

    except ValueError:
        print(Fore.RED + "⚠️  Input tidak valid! Harap masukkan angka yang benar.")

def admin_menu():
    password = "admin123"  
    attempts = 0
    max_attempts = 3

    while attempts < max_attempts:
        entered_password = input("\nMasukkan kata sandi admin: ")
        if entered_password == password:
            print("\nAkses diterima. Selamat datang di menu Admin.")
            admin_panel()
            return
        else:
            attempts += 1
            print(f"Kata sandi salah! Percobaan tersisa: {max_attempts - attempts}")

    print("\nAnda telah mencapai batas maksimal percobaan.")
    print("Kembali ke menu utama...")
    return 

def admin_panel():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Kelola barang rental")
        print("2. Lihat daftar barang")
        print("3. Konfirmasi penyewaan")
        print("4. Laporan pendapatan")
        print("5. Menu Database")
        print("6. Kembali ke menu utama")
        choice = input("Pilih menu (1/2/3/4/5/6): ")

        if choice == '1':
            kelola_barang()
        elif choice == '2':
            print_produk()
        elif choice == '3':
            konfirmasi_sewa()
        elif choice == '4':
            laporan_pendapatan()
        elif choice == '5':
            database_menu()
        elif choice == '6':
            return  # Kembali ke menu utama
        else:
            print("Pilihan tidak valid, silakan coba lagi.")



def user_menu():
    while True:
        print("\n--- Menu User ---")
        print("1. Lihat daftar produk")
        print("2. Sewa produk")
        print("3. Lihat riwayat penyewaan")
        print("4. Kembali ke menu utama")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            print_produk()
        elif choice == '2':
            sewa_produk()
        elif choice == '3':
            riwayat_penyewaan()
        elif choice == '4':
            return  # Kembali ke menu utama
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def print_produk():
    print("\n--- Daftar Produk ---")
    for produk in produk_db:
        print(f"ID: {produk['id']} | Nama: {produk['nama']} | Harga: {produk['harga']} | Status: {produk['status']}")

def riwayat_penyewaan():
    if rental_db:
        print("\n--- Riwayat Penyewaan ---")
        for sewa in rental_db:
            print(f"Nama: {sewa['nama_pengguna']} | Produk: {sewa['nama_produk']} | Durasi: {sewa['durasi_hari']} hari | Total Harga: {sewa['total_harga']}")
    else:
        print("\nTidak ada riwayat penyewaan.")

def laporan_pendapatan():
    total_pendapatan = sum(sewa["total_harga"] for sewa in rental_db if sewa["status"] == "Sudah Dikembalikan")
    print(f"\n--- Laporan Pendapatan ---")
    print(f"Total Pendapatan dari Penyewaan: Rp {total_pendapatan:,}")
    input("\nTekan Enter untuk kembali ke menu admin...")

import webbrowser

def main_menu():
    video_links = {
        "1": "https://youtu.be/QiNLNDSLuJY?si=X6c7nQQTDllpHxUB", 
        "2": "https://youtu.be/x87gbgQD4eg?si=SOpC1fIVGsBfo3cH",  
        "3": "https://youtu.be/xuYZNJCvHgQ?si=NtbvNZZCbAejNZFS"    
    }
    
    load_data()
    print_logo()
    
    while True:
        print("\n--- Menu Utama ---")
        print("1. Menu Admin")
        print("2. Menu User")
        print("3. Menu Database")
        print("4. Tentang Kami")
        print("5. Menu Feedback") 
        print("6. Tutorial YouTube")
        print("7. Simulasi Sederhana")
        print("8. Keluar")
        
        choice = input("Pilih menu (1/2/3/4/5/6/7): ")

        if choice == '1':
            admin_menu()
        elif choice == '2':
            user_menu()
        elif choice == '3':
            database_menu()
        elif choice == '4':
            tentang_kami()
        elif choice == '5':
            menu_feedback()
        elif choice == '6':  
            print("\n--- Tutorial YouTube ---")
            print("1. BELAJAR METASPLOIT")
            print("2. BELAJAR NESSUS")
            print("3. BELAJAR METASPLOIT PRO")
            
            pilih = input("Pilih: ")
            
            if pilih in video_links:
                print("Membuka video di YouTube...")
                webbrowser.open(video_links[pilih])  
            else:
                print("Pilihan tidak valid! Silakan pilih angka 1, 2, atau 3.")
        elif choice == '7':
            simulasi_sederhana()
        elif choice == '8':
            save_data()
            print("Terima kasih telah menggunakan aplikasi rental barang!")
            break
        else:
            print("Pilihan tidak valid, silakan coba lagi.")



def tampil_kontak():
    print("\n" + HIJAU + "="*50 + PUTIH)
    print("                    KONTAK")
    print(HIJAU + "="*50 + PUTIH)
    print("Email   : supportvu1n3xp3rt@gmail.com")
    print("Telepon : +62 895 1602 8710")
    print("Instagram : VulnXpert_Detective")
    print(HIJAU + "="*50 + PUTIH)


def tampil_lisensi():
    print("\n" + HIJAU + "="*50 + PUTIH)
    print("                   LISENSI")
    print(HIJAU + "="*50 + PUTIH)
    print("Sistem CLI Rental Pentesting Tools dilindungi oleh:")
    print("GNU General Public License v3.0")
    print("Semua hak cipta dilindungi undang-undang.")
    print(HIJAU + "="*50 + PUTIH)


def tampil_cara_menyewa():
    print("\n" + HIJAU + "="*50 + PUTIH)
    print("                 CARA MENYEWA")
    print(HIJAU + "="*50 + PUTIH)
    print("1. Daftarkan akun Anda melalui sistem CLI.")
    print("2. Login ke sistem menggunakan kredensial Anda.")
    print("3. Pilih alat pentesting yang ingin disewa.")
    print("4. Lakukan pembayaran sesuai dengan durasi penyewaan.")
    print("5. Unduh dan gunakan alat sesuai kebutuhan.")
    print(HIJAU + "="*50 + PUTIH)


def tentang_kami():
    print("\n" + HIJAU + "="*50 + PUTIH)
    print("                 TENTANG KAMI")
    print(HIJAU + "="*50 + PUTIH)
    print("SEKILAS TENTANG VULNXPERT")
    print(HIJAU + "-"*50 + PUTIH)
    print("Dalam era digital yang semakin maju, keamanan siber menjadi pilar utama")
    print("bagi organisasi yang ingin melindungi data dan infrastruktur mereka.")
    print("Namun, keterbatasan sumber daya seringkali menjadi hambatan.")
    print("Untuk menjawab tantangan ini, kami memperkenalkan:")
    print("  SISTEM CLI RENTAL PENTESTING TOOLS")
    print("Sebuah solusi revolusioner yang menggabungkan efisiensi, aksesibilitas,")
    print("dan keamanan dalam satu platform berbasis Command-Line Interface (CLI).")
    print(HIJAU + "-"*50 + PUTIH)


def menu_tentang_kami():
    while True:
        print("\n" + HIJAU + "="*50 + PUTIH)
        print("      MENU TENTANG KAMI")
        print(HIJAU + "="*50 + PUTIH)
        print("[1] Kontak")
        print("[2] Lisensi")
        print("[3] Cara Menyewa")
        print("[4] Kembali ke Menu Utama")
        print(HIJAU + "="*50 + PUTIH)

        pilihan = input("Pilih No: ")
        if pilihan == "1":
            tampil_kontak()
        elif pilihan == "2":
            tampil_lisensi()
        elif pilihan == "3":
            tampil_cara_menyewa()
        elif pilihan == "4":
            print("\nKembali ke Menu Utama...")
            break
        else:
            print("\nPilihan tidak Valid, Silahkan Masukkan pilihan yang Valid.")
            
        
feedback_file = "feedback.json"
def beri_feedback():
    feedback = input("\nSilakan tuliskan feedback atau saran Anda: ")
    nama_pengguna = input("Masukkan nama Anda (Opsional, tekan Enter jika ingin anonim): ")
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    data_feedback = {
        "nama": nama_pengguna if nama_pengguna else "Anonim",
        "waktu": waktu,
        "feedback": feedback
    }
    
    if os.path.exists(feedback_file):
        with open(feedback_file, 'r') as f:
            all_feedback = json.load(f)
    else:
        all_feedback = []

    all_feedback.append(data_feedback)

    with open(feedback_file, 'w') as f:
        json.dump(all_feedback, f, indent=4)

    print("\nTerima kasih atas feedback Anda!")
            
def lihat_feedback():
    if not os.path.exists(feedback_file):
        print("\nBelum ada feedback dari pengguna.")
        return

    with open(feedback_file, 'r') as f:
        all_feedback = json.load(f)

    print("\n--- Daftar Feedback Pengguna ---")
    if not all_feedback:
        print("Belum ada feedback yang tersimpan.")
    else:
        for i, fb in enumerate(all_feedback, 1):
            print(f"\n{i}. Waktu: {fb['waktu']}\n   Nama: {fb['nama']}\n   Feedback: {fb['feedback']}")

    input("\nTekan Enter untuk kembali ke menu...")

def menu_feedback():
    while True:
        print("\n--- Menu Feedback ---")
        print("1. Lihat Feedback")
        print("2. Kasih Feedback")
        print("3. Kembali ke Menu Utama")
        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            lihat_feedback()
        elif choice == '2':
            beri_feedback()
        elif choice == '3':
            return
        else:
            print("Pilihan tidak valid, silakan coba lagi.")
            
            # Efek Terminal
def loading_effect(text, delay=0.05):
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def terminal_effect():
    os.system("clear")
    print("\033[32m")  # Warna Hijau Matrix
    for _ in range(10):
        print("".join(random.choice("01█▓▒░") for _ in range(50)))
        time.sleep(0.05)
    print("\033[0m")  # Reset Warna

# Database Teka-Teki Acak
puzzles = [
    {"question": "Saya bisa mengunci dan membuka, tapi bukan kunci. Siapakah saya?", "answer": "password"},
    {"question": "Apa yang selalu ada tetapi tidak bisa disentuh?", "answer": "bayangan"},
    {"question": "Apa yang lebih kuat dari Tuhan, lebih jahat dari setan, dan jika dimakan bisa membunuh?", "answer": "tidak ada"},
    {"question": "Saya memiliki wajah tetapi tidak bisa berbicara. Apakah saya?", "answer": "jam"},
    {"question": "Jika aku memiliki 4 kaki di pagi hari, 2 kaki di siang hari, dan 3 kaki di malam hari, siapakah aku?", "answer": "manusia"},
]

# Fungsi Teka-Teki (Harus Dijawab untuk Lanjut)
def challenge():
    teka_teki = random.choice(puzzles)
    loading_effect("\n🧩 Sebelum lanjut, jawab tantangan ini!\n")
    
    user_answer = input(f"🧠 {teka_teki['question']}\n> ").strip().lower()
    if user_answer == teka_teki['answer']:
        print("✅ Jawaban BENAR! Lanjutkan misi!")
        return True
    else:
        print("❌ Jawaban SALAH! Coba lagi!")
        return False

# Simulasi Scan Port
def port_scan(target):
    terminal_effect()
    if not challenge():
        return

    loading_effect(f"\n🔍 Memulai port scanning pada {target}...\n")
    ports = [21, 22, 25, 53, 80, 443, 3306, 8080]
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((target, port))
        if result == 0:
            print(f"✅ Port {port} TERBUKA! 🚪")
        else:
            print(f"❌ Port {port} TERTUTUP.")
        sock.close()

    loading_effect("\n✅ Port scanning SELESAI!\n")

# Simulasi Web Enumeration
def web_enum(target):
    terminal_effect()
    if not challenge():
        return

    wordlist = ['admin', 'login', 'dashboard', 'config', 'backup', 'secret']
    loading_effect(f"\n🔎 Mencari direktori rahasia di {target}...\n")
    
    for path in wordlist:
        url = f"{target}/{path}"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"✅ DITEMUKAN: {url} 🟢")
            else:
                print(f"❌ {url} - Status {response.status_code}")
        except requests.exceptions.RequestException:
            print(f"⚠️ Tidak bisa mengakses {url}")

    loading_effect("\n🔍 Web Enumeration SELESAI!\n")

# Simulasi Brute Force Login
def brute_force():
    terminal_effect()
    if not challenge():
        return

    loading_effect("\n🔑 Simulasi Brute Force Login...\n")
    username = "admin"
    passwords = ["12345", "admin", "password", "letmein", "root"]

    for password in passwords:
        print(f"🔓 Mencoba login: {username} | {password} ...", end=" ", flush=True)
        time.sleep(1)
        if password == "root":
            print("✅ BERHASIL MASUK! 🔥")
            return
        else:
            print("❌ GAGAL.")

    loading_effect("\n❌ Brute Force GAGAL! Coba teknik lain!\n")

# Simulasi Eksploitasi Sistem
def exploit_system():
    terminal_effect()
    if not challenge():
        return

    loading_effect("\n💀 Menjalankan eksploitasi sistem...\n")
    
    if challenge():
        print("✅ Eksploitasi BERHASIL! Akses sistem diperoleh 🔓")
    else:
        print("❌ Eksploitasi GAGAL! Coba lagi! 🚫")
    
    loading_effect("\n🔥 Eksploitasi SELESAI!\n")

# Simulasi Post-Exploitation
def post_exploit():
    terminal_effect()
    if not challenge():
        return

    loading_effect("\n📂 Mengambil data rahasia...\n")
    
    files = ["database.db", "passwords.txt", "config.yaml", "secret_key.pem"]
    for file in files:
        print(f"📥 Mengunduh {file} ...")
        time.sleep(1)
    
    loading_effect("\n✅ Semua data telah DIAMBIL! 🔥\n")

# Menu Utama
def simulasi_sederhana():
    while True:
        os.system('clear')  
        print("\033[1;32m")  # Warna Hijau Terang
        print("=" * 50)
        print("   🏴‍☠️ DARK TERMINAL 2.0 - HACKER CHALLENGE 🏴‍☠️   ")
        print("=" * 50)
        print("1. Scan Port (Mirip Nmap) 🌐")
        print("2. Web Enumeration 🔎")
        print("3. Brute Force Login 🔑")
        print("4. Eksploitasi Sistem (HARUS Jawab Teka-Teki!) 💀")
        print("5. Post-Exploitation 📂")
        print("0. Keluar 🚪")
        print("=" * 50)
        print("\033[0m")  # Reset Warna
        pilihan = input("Pilih menu: ")

        if pilihan == '1':
            target = input("Masukkan IP target: ")
            port_scan(target)
        elif pilihan == '2':
            target = input("Masukkan URL target: ")
            web_enum(target)
        elif pilihan == '3':
            brute_force()
        elif pilihan == '4':
            exploit_system()
        elif pilihan == '5':
            post_exploit()
        elif pilihan == '0':
            loading_effect("\n🚀 Keluar dari sistem...")
            break
        else:
            print("\n❌ Pilihan tidak valid!")

        input("\n🔄 Tekan Enter untuk kembali ke menu...")



# Menjalankan program
if __name__ == "__main__":
    main_menu()