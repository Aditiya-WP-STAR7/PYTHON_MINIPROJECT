import json
import os
import pyfiglet
import webbrowser
import time
import requests
import random
import re
import random
import sqlite3
import os
import base64
import socket
import hashlib
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from prettytable import PrettyTable
from datetime import datetime
from colorama import Fore, Style, init
from prettytable import PrettyTable
from datetime import datetime

# **Konfigurasi Database JSON**
produk_file = "produk.json"
rental_file = "rental.json"
deleted_produk_file = "deleted_produk.json"

# **Konfigurasi Database SQLite**
DB_NAME = "rental.db"
PRODUK_FILE = "produk.json"
BACKUP_FILE = "backup_rental.sql"

# **Buat koneksi ke SQLite**
conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

# **Buat tabel rental jika belum ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS rental (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pengguna TEXT,
    nama_produk TEXT,
    durasi_hari INTEGER,
    total_harga INTEGER,
    waktu_peminjaman TEXT,
    status TEXT
)
""")


# **Inisialisasi Database SQLite**
conn = sqlite3.connect("rental.db")
cursor = conn.cursor()

# **Buat Tabel Produk Jika Belum Ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL,
    status TEXT NOT NULL
)
""")

# **Buat Tabel Rental Jika Belum Ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS rental (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama_pengguna TEXT NOT NULL,
    nama_produk TEXT NOT NULL,
    durasi_hari INTEGER NOT NULL,
    total_harga INTEGER NOT NULL,
    waktu_peminjaman TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

# **Buat Tabel Deleted Produk Jika Belum Ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS deleted_produk (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nama TEXT NOT NULL,
    harga INTEGER NOT NULL
)
""")

# **Buat Tabel Riwayat Perubahan Jika Belum Ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    data TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")

conn.commit()

conn.commit()

# **Buat Tabel Riwayat Perubahan Jika Belum Ada**
cursor.execute("""
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action TEXT NOT NULL,
    data TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
""")
conn.commit()



# **Backup Otomatis Sebelum Menyimpan Data**
def backup_rental_data():
    with open(BACKUP_FILE, "w") as f:
        for line in conn.iterdump():
            f.write(f"{line}\n")
    print("✅ Backup otomatis dibuat.")


#** SCREEN AWAL PEMBUKA**

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

def load_data():
    global produk_db, deleted_produk_db

    # Load Produk dari JSON
    if os.path.exists(produk_file):
        with open(produk_file, 'r') as f:
            produk_db = json.load(f)
    else:
        produk_db = [
            {"id": 1, "nama": "BurpSuite Enterprise", "harga": 500000, "status": "Tersedia"},
            {"id": 2, "nama": "Nessus", "harga": 45000, "status": "Tersedia"},
            {"id": 3, "nama": "Metasploit Pro", "harga": 600000, "status": "Tersedia"}
        ]

    # Load Produk yang Dihapus dari JSON
    if os.path.exists(deleted_produk_file):
        with open(deleted_produk_file, 'r') as f:
            deleted_produk_db = json.load(f)
    else:
        deleted_produk_db = []

    print("✅ Data produk & produk yang dihapus dimuat.")


def save_rental_data(nama_pengguna, nama_produk, durasi_hari, total_harga):
    backup_rental_data()  # Buat backup sebelum menyimpan

    cursor.execute("""
    INSERT INTO rental (nama_pengguna, nama_produk, durasi_hari, total_harga, waktu_peminjaman, status)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (nama_pengguna, nama_produk, durasi_hari, total_harga, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "Menunggu Konfirmasi"))
    
    conn.commit()
    print("✅ Data penyewaan disimpan ke SQLite.")


def save_data():
    with open(produk_file, 'w') as f:
        json.dump(produk_db, f, indent=4)

    with open(rental_file, 'w') as f:
        json.dump(rental_db, f, indent=4)

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
        print("1. TENTANG KAMI & CARA MENYEWA")
        print("2. MENU ADMIN")
        print("3. MENU USER")
        print("4. MENU FEEDBACK") 
        print("5. TUTORIAL YOUTUBE")
        print("6. SIMULASI SEDERHANA")
        print("7. CTF")
        print("0. KELUAR SISTEM")

        choice = input("Pilih menu (0/1/2/3/4/5/6/7): ")

        if choice == '1':
            tentang_kami()
            menu_tentang_kami()
        elif choice == '2':
            admin_menu()
        elif choice == '3':
            user_menu()
        elif choice == '4':
            menu_feedback()
        elif choice == '5':  
            print("\n--- Tutorial YouTube ---")
            print("1. BELAJAR METASPLOIT")
            print("2. BELAJAR NESSUS")
            print("3. BELAJAR BURP SUITE")

            pilih = input("Pilih: ")

            if pilih in video_links:
                print("Membuka video di YouTube...")
                webbrowser.open(video_links[pilih])  
            else:
                print("Pilihan tidak valid! Silakan pilih angka 1, 2, atau 3.")
        elif choice == '6':
            simulasi_sederhana()
        elif choice == '7':
            ctf()  # ← Perbaiki indentasi di sini!
        elif choice == '0':
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
    print("1. Masuk ke Menu User -> Sewa Produk")
    print("2. Isi Data yang Kami Perlukan dengan benar Khususnya No Telepon / WA yang bisa dihubungi.")
    print("3. Jika Data Salah Khususnya No Telepon/No WA Maka Konfirmasi Penyewaan Kami Batalkan.")
    print("4. Kami Akan Melakukan Konfirmasi Pembayaran Melalui WA dengan Pembayaran Paypal.")
    print("5. Akun dan Password akan Kami Kirimkan lewat WA.")
    print("6. Silahkan Anda Login di Software Akun yang Anda Sewa dengan Akun dan Password yang telah Kami Kirimkan.")
    print("7. Anda bebas Melakukan Apa saja Selama tidak Menentang Kebijakan.")
    print("8. Semua Pergerakan Kami Awasi. Seandainya Anda Menentang Kebijakan, Maka Kami berhak Menarik dan Melaporkan Anda.")
    print("9. Selama Penyewaan, Anda boleh Menanyakan Apapun terkait Tutorial Hacking dan Sebagainya.")
    print("10. Ketika Waktu Rental Selesai, Kami berhak Mengganti Akun dan Password.")
    print("11. Jika Ada Pertanyaan Silahkan WA ke Kami dengan Ketik WA.")
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
    
def menu_profil_penulis():
    while True:
        os.system("clear")  # Bersihkan layar (gunakan "cls" jika di Windows)
        print(Fore.LIGHTCYAN_EX + Style.BRIGHT + "\n📌 PROFIL PENULIS 📌\n")
        print(Fore.YELLOW + "=" * 50 + Fore.RESET)
        print(Fore.LIGHTGREEN_EX + "[1] Instagram" + Fore.RESET)
        print(Fore.LIGHTBLUE_EX + "[2] LinkedIn" + Fore.RESET)
        print(Fore.LIGHTMAGENTA_EX + "[3] TryHackMe" + Fore.RESET)
        print(Fore.LIGHTRED_EX + "[4] Threads" + Fore.RESET)
        print(Fore.LIGHTYELLOW_EX + "[5] Kaggle" + Fore.RESET)
        print(Fore.CYAN + "[0] Kembali ke Menu Sebelumnya" + Fore.RESET)
        print(Fore.YELLOW + "=" * 50 + Fore.RESET)

        pilihan = input("Pilih menu: ")

        links = {
            "1": "https://www.instagram.com/adit_widodoputra?igsh=MXRmc2ttemp0YWhweg==",
            "2": "https://www.linkedin.com/in/aditiya-widodo-putra-984047291?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app",
            "3": "https://tryhackme.com/p/AditiyaWP",
            "4": "https://www.threads.net/@adit_widodoputra",
            "5": "https://www.kaggle.com/aditiyawp"
        }

        if pilihan in links:
            print(Fore.GREEN + "\n🌍 Membuka halaman di browser...\n" + Fore.RESET)
            webbrowser.open(links[pilihan])
        elif pilihan == "0":
            break
        else:
            print(Fore.RED + "\n❌ Pilihan tidak valid! Coba lagi.\n" + Fore.RESET)
            time.sleep(1)




def menu_tentang_kami():
    while True:
        print("\n" + HIJAU + "="*50 + PUTIH)
        print("      MENU TENTANG KAMI")
        print(HIJAU + "="*50 + PUTIH)
        print("[1] Kontak")
        print("[2] Lisensi")
        print("[3] Cara Menyewa")
        print("[4] Profil Penulis")
        print("[WA] Kontak Langsung")
        print("[0] Kembali ke Menu Utama")
        print(HIJAU + "="*50 + PUTIH)

        pilihan = input("Pilih No: ")
        if pilihan == "1":
            tampil_kontak()
        elif pilihan == "2":
            tampil_lisensi()
        elif pilihan == "3":
            tampil_cara_menyewa()
        elif pilihan == "4":
            menu_profil_penulis() 
        elif pilihan == "WA":
            webbrowser.open(f"https://wa.me/+6289516028710")
        elif pilihan == "0":
            print("\nKembali ke Menu Utama...")
            break
        else:
            print("\nPilihan tidak Valid, Silahkan Masukkan pilihan yang Valid.")

PASSWORD_FILE = "admin_pass.enc"

# Kunci AES untuk enkripsi password
AES_KEY = b"16BYTES_AES_KEY!"  # Pastikan 16, 24, atau 32 byte

# =====================[ ENKRIPSI & DEKRIPSI AES ]=====================
def encrypt_password(password):
    cipher = AES.new(AES_KEY, AES.MODE_CBC)
    encrypted_data = cipher.encrypt(pad(password.encode(), AES.block_size))
    return base64.b64encode(cipher.iv + encrypted_data).decode()

def decrypt_password(encrypted_data):
    encrypted_data = base64.b64decode(encrypted_data)
    iv = encrypted_data[:AES.block_size]
    cipher = AES.new(AES_KEY, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(encrypted_data[AES.block_size:]), AES.block_size).decode()

# =====================[ SISTEM PASSWORD ADMIN ]=====================
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def save_admin_password():
    """Menyimpan password admin dengan enkripsi AES-256."""
    if not os.path.exists(PASSWORD_FILE):
        print(Fore.YELLOW + "\n🔐 Setup Password Admin Pertama Kali:")
        password = input(Fore.CYAN + "Masukkan password admin baru: " + Fore.RESET)
        confirm_password = input(Fore.CYAN + "Konfirmasi password: " + Fore.RESET)

        if password == confirm_password:
            encrypted_password = encrypt_password(password)
            with open(PASSWORD_FILE, "w") as f:
                f.write(encrypted_password)
            print(Fore.GREEN + "✅ Password admin berhasil disimpan!\n")
        else:
            print(Fore.RED + "❌ Password tidak cocok! Silakan coba lagi.")
            save_admin_password()

def verify_admin_password():
    """Verifikasi login admin dengan enkripsi dan hash SHA-256."""
    if not os.path.exists(PASSWORD_FILE):
        save_admin_password()

    with open(PASSWORD_FILE, "r") as f:
        encrypted_password = f.read()

    stored_password = decrypt_password(encrypted_password)
    entered_password = input(Fore.CYAN + "\nMasukkan password admin: " + Fore.RESET)

    if hash_password(entered_password) == hash_password(stored_password):
        print(Fore.GREEN + "✅ Akses diterima. Selamat datang di menu Admin.\n")
        return True  # Tambahkan return True agar admin_menu() bisa melanjutkan
    else:
        print(Fore.RED + "❌ Password salah! Akses ditolak.")
        return False  # Jika salah, pastikan mengembalikan False



# =====================[ MENU ADMIN ]=====================
def admin_menu():
    if verify_admin_password():  # Jika password benar, lanjut ke menu admin
        admin_panel()  # Panggil admin_panel() agar masuk ke menu admin
    else:
        print("❌ Gagal login sebagai admin. Kembali ke Menu Utama.")



def admin_panel():
    while True:
        print("\n--- Menu Admin ---")
        print("1. Kelola barang rental")
        print("2. Lihat daftar barang")
        print("3. Sorting daftar barang")  # Tambahkan sorting
        print("4. Konfirmasi penyewaan")
        print("5. Laporan pendapatan")
        print("6. Menu Database")
        print("7. Lihat Semua Transaksi")
        print("0. Kembali ke menu utama")
        choice = input("Pilih menu (0/1/2/3/4/5/6/7): ")

        if choice == '1':
            kelola_barang()
        elif choice == '2':
            print_produk()
        elif choice == '3':  
            sort_produk()  # Tambahkan fitur sorting produk
        elif choice == '4':
            konfirmasi_sewa()
        elif choice == '5':
            laporan_pendapatan()
        elif choice == '6':
            database_menu()
        elif choice == '7':
            lihat_semua_transaksi()
        elif choice == '0':
            return  # Kembali ke menu utama
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


def kelola_barang():
    while True:
        print("\n--- Menu Kelola Barang ---")
        print("1. Ubah Nama, Harga, dan ID Barang")
        print("2. Tambah Barang")
        print("3. Hapus Barang")
        print("4. Kembalikan Produk yang Dihapus")
        print("0. Kembali ke Menu Admin")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            ubah_produk()
        elif choice == '2':
            tambah_produk()
        elif choice == '3':
            hapus_produk()
        elif choice == '4':
            restore_deleted_produk()
        elif choice == '0':
            return  # Kembali ke menu admin
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

def ubah_produk():
    print("\n--- Daftar Produk ---")
    print("+----+-----------------------+------------+-------------------+")
    print("| ID |      Nama Produk      | Harga (Rp) |       Status      |")
    print("+----+-----------------------+------------+-------------------+")

    for produk in produk_db:
        status_icon = "✅ Tersedia" if produk["status"] == "Tersedia" else "❌ Tidak Tersedia"
        print(f"| {produk['id']:<2} | {produk['nama']:<21} | Rp {produk['harga']:<8,} | {status_icon:<18} |")

    print("+----+-----------------------+------------+-------------------+\n")

    # **Perbaikan Validasi Input**
    while True:
        id_produk_input = input("Masukkan ID produk yang ingin diubah (ketik 'batal' untuk kembali): ").strip()
        
        if id_produk_input.lower() == "batal":
            print("❌ Perubahan produk dibatalkan.")
            return

        if not id_produk_input.isdigit():
            print("⚠️ ID produk harus berupa angka! Coba lagi.")
            continue

        id_produk = int(id_produk_input)

        produk = next((p for p in produk_db if p["id"] == id_produk), None)
        if produk:
            break  # Produk ditemukan, lanjut ke proses edit
        else:
            print("❌ ID produk tidak ditemukan. Coba lagi.")

    print(f"\n📝 Ubah data produk: {produk['nama']}")
    
    nama_baru = input("Masukkan nama baru (kosongkan untuk tidak mengubah): ").strip()
    harga_baru = input("Masukkan harga baru (kosongkan untuk tidak mengubah): ").strip()

    if nama_baru:
        produk["nama"] = nama_baru
    if harga_baru:
        if harga_baru.isdigit():
            produk["harga"] = int(harga_baru)
        else:
            print("⚠️ Harga harus berupa angka! Perubahan harga dibatalkan.")

    save_data()
    print(f"✅ Produk berhasil diperbarui: {produk['nama']} - Rp {produk['harga']:,}")

def tambah_produk():
    """Menambahkan produk baru ke database."""
    print("\n🆕 Menambah Produk Baru")

    nama_produk = input("Masukkan nama produk baru: ").strip()
    if not nama_produk:
        print("❌ Nama produk tidak boleh kosong!")
        return

    while True:
        harga_input = input("Masukkan harga sewa per hari: ").strip()
        if harga_input.isdigit():
            harga = int(harga_input)
            break
        else:
            print("⚠️ Harga harus berupa angka!")

    # **Masukkan ke database SQLite**
    cursor.execute("INSERT INTO produk (nama, harga, status) VALUES (?, ?, ?)", (nama_produk, harga, "Tersedia"))
    conn.commit()
    
    print(f"✅ Produk '{nama_produk}' berhasil ditambahkan dengan harga Rp {harga:,}")
    input("\n🔘 Tekan Enter untuk kembali ke menu...")


def hapus_produk():
    """Menghapus produk dari daftar dan memindahkannya ke deleted_produk (SQLite & JSON)."""
    print("\n🗑️ Hapus Produk dari Daftar")

    # **Ambil Data dari SQLite**
    cursor.execute("SELECT id, nama, harga, status FROM produk")
    produk_list = cursor.fetchall()

    # **Jika SQLite kosong, ambil dari JSON**
    if not produk_list:
        produk_list = load_json_data(produk_file)

    # **Jika tetap kosong, tampilkan pesan**
    if not produk_list:
        print("🚫 Tidak ada produk yang bisa dihapus!")
        return

    # **Tampilkan Daftar Produk**
    table = PrettyTable(["ID", "Nama Produk", "Harga (Rp)", "Status"])
    for produk in produk_list:
        id_produk, nama, harga, status = produk if isinstance(produk, tuple) else (produk["id"], produk["nama"], produk["harga"], produk["status"])
        status_warna = "✅ Tersedia" if status == "Tersedia" else "❌ Tidak Tersedia"
        table.add_row([id_produk, nama, f"Rp {harga:,}", status_warna])
    
    print(table)

    # **Validasi Input ID Produk**
    while True:
        id_produk_input = input("Masukkan ID produk yang ingin dihapus (ketik 'batal' untuk kembali): ").strip()
        if id_produk_input.lower() == "batal":
            print("❌ Penghapusan dibatalkan.")
            return
        if id_produk_input.isdigit():
            id_produk = int(id_produk_input)
            break
        print("⚠️ ID produk harus berupa angka!")

    # **Cek di SQLite dulu**
    cursor.execute("SELECT * FROM produk WHERE id = ?", (id_produk,))
    produk = cursor.fetchone()

    if produk:
        # **Pindahkan ke `deleted_produk` di SQLite**
        cursor.execute("INSERT INTO deleted_produk (id, nama, harga) VALUES (?, ?, ?)", (produk[0], produk[1], produk[2]))
        cursor.execute("DELETE FROM produk WHERE id = ?", (id_produk,))
        conn.commit()
        print(f"✅ Produk '{produk[1]}' berhasil dihapus dan dipindahkan ke daftar produk yang dihapus.")
    else:
        # **Cek di JSON jika tidak ada di SQLite**
        produk_db = load_json_data(produk_file)
        deleted_produk_db = load_json_data(deleted_produk_file)

        produk_dihapus = None
        for p in produk_db:
            if p["id"] == id_produk:
                produk_dihapus = p
                break

        if produk_dihapus:
            produk_db.remove(produk_dihapus)
            deleted_produk_db.append(produk_dihapus)

            # **Simpan kembali ke JSON**
            with open(produk_file, "w") as f:
                json.dump(produk_db, f, indent=4)
            with open(deleted_produk_file, "w") as f:
                json.dump(deleted_produk_db, f, indent=4)

            print(f"✅ Produk '{produk_dihapus['nama']}' berhasil dihapus dari JSON dan dipindahkan ke daftar produk yang dihapus.")
        else:
            print("❌ Produk dengan ID tersebut tidak ditemukan!")

    input("\n🔘 Tekan Enter untuk kembali ke menu...")


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

def print_produk():
    print("\n--- Daftar Produk ---")
    table = PrettyTable(["ID", "Nama Produk", "Harga (Rp)", "Status"])
    for produk in produk_db:
        status_warna = Fore.GREEN + "✅ Tersedia" if produk['status'] == "Tersedia" else Fore.RED + "❌ Tidak Tersedia"
        table.add_row([produk['id'], produk['nama'], f"Rp {produk['harga']:,}", status_warna])

    print(table)
        
        
def sort_produk():
    global produk_db
    print("\n--- Sorting Daftar Produk ---")
    print("1. Harga Murah → Mahal")
    print("2. Harga Mahal → Murah")
    print("3. Nama A-Z")
    print("4. Nama Z-A")
    choice = input("Pilih metode sorting (1/2/3/4): ")

    if choice == '1':
        produk_db = sorted(produk_db, key=lambda x: x["harga"])
    elif choice == '2':
        produk_db = sorted(produk_db, key=lambda x: x["harga"], reverse=True)
    elif choice == '3':
        produk_db = sorted(produk_db, key=lambda x: x["nama"].lower())
    elif choice == '4':
        produk_db = sorted(produk_db, key=lambda x: x["nama"].lower(), reverse=True)
    else:
        print("Pilihan tidak valid, kembali ke menu.")

    print_produk()  # Tampilkan produk setelah sorting

def sort_rental():
    global rental_db
    print("\n--- Sorting Riwayat Penyewaan ---")
    print("1. Tanggal Terbaru → Terlama")
    print("2. Tanggal Terlama → Terbaru")
    print("3. Total Harga Murah → Mahal")
    print("4. Total Harga Mahal → Murah")
    choice = input("Pilih metode sorting (1/2/3/4): ")

    if choice in ["1", "2"]:
        # Pastikan semua entri memiliki 'waktu_peminjaman'
        rental_db = [r for r in rental_db if "waktu_peminjaman" in r]

        if choice == "1":
            rental_db = sorted(rental_db, key=lambda x: x["waktu_peminjaman"], reverse=True)
        elif choice == "2":
            rental_db = sorted(rental_db, key=lambda x: x["waktu_peminjaman"])
    
    elif choice == "3":
        rental_db = sorted(rental_db, key=lambda x: x.get("total_harga", 0))
    
    elif choice == "4":
        rental_db = sorted(rental_db, key=lambda x: x.get("total_harga", 0), reverse=True)

    else:
        print("❌ Pilihan tidak valid, kembali ke menu.")

    riwayat_penyewaan()  # Tampilkan hasil sorting

def konfirmasi_sewa():
    print("\n📌 --- Daftar Penyewaan Menunggu Konfirmasi --- 📌")

    try:
        # **Ambil Data dari SQLite**
        cursor.execute("SELECT id, nama_pengguna, nama_produk, durasi_hari FROM rental WHERE status = 'Menunggu Konfirmasi'")
        menunggu_konfirmasi = cursor.fetchall()

        if not menunggu_konfirmasi:
            print("\n✅ Tidak ada penyewaan yang menunggu konfirmasi.")
            input("\n🔙 Tekan Enter untuk kembali ke menu admin...")
            return

        # **Tampilkan Daftar Penyewaan**
        for i, (id_sewa, nama_pengguna, nama_produk, durasi_hari) in enumerate(menunggu_konfirmasi, 1):
            print(f"{i}. Nama: {nama_pengguna} | Produk: {nama_produk} | Durasi: {durasi_hari} hari")

        while True:
            try:
                pilihan = int(input("\nPilih nomor penyewaan yang ingin diproses (0 untuk kembali): "))

                if pilihan == 0:
                    print("🚫 Kembali ke menu Admin.")
                    return

                if 1 <= pilihan <= len(menunggu_konfirmasi):
                    id_sewa, nama_pengguna, nama_produk, durasi_hari = menunggu_konfirmasi[pilihan - 1]

                    print("\n📌 --- Konfirmasi Penyewaan --- 📌")
                    print(f"📌 Nama: {nama_pengguna}")
                    print(f"📦 Produk: {nama_produk}")
                    print(f"📆 Durasi: {durasi_hari} hari")
                    print("\n1. Terima Penyewaan")
                    print("2. Tolak Penyewaan")
                    print("0. Kembali")

                    tindakan = input("\nPilih tindakan (1/2/0): ")

                    if tindakan == "1":
                        # **Terima Penyewaan (Update Status di Database)**
                        cursor.execute("UPDATE rental SET status = 'Belum Dikembalikan' WHERE id = ?", (id_sewa,))
                        conn.commit()

                        # **Ubah status produk menjadi 'Tidak Tersedia'**
                        cursor.execute("UPDATE produk SET status = 'Tidak Tersedia' WHERE nama = ?", (nama_produk,))
                        conn.commit()

                        print(f"✅ Penyewaan '{nama_produk}' oleh {nama_pengguna} telah dikonfirmasi!")

                    elif tindakan == "2":
                        # **Hapus Penyewaan dari Database**
                        cursor.execute("DELETE FROM rental WHERE id = ?", (id_sewa,))
                        conn.commit()

                        # **Kembalikan status produk menjadi 'Tersedia'**
                        cursor.execute("UPDATE produk SET status = 'Tersedia' WHERE nama = ?", (nama_produk,))
                        conn.commit()

                        print(f"❌ Penyewaan '{nama_produk}' oleh {nama_pengguna} telah DITOLAK!")

                    elif tindakan == "0":
                        print("🚫 Tindakan dibatalkan.")
                        continue  # Kembali ke daftar penyewaan

                    else:
                        print("❌ Pilihan tidak valid!")

                else:
                    print("❌ Pilihan tidak valid!")

            except ValueError:
                print("❌ Input harus berupa angka!")

    except sqlite3.Error as e:
        print(f"❌ Terjadi kesalahan saat mengambil data: {e}")


def laporan_pendapatan():
    print("\n📜 --- Laporan Pendapatan --- 📜")

    try:
        # **Ambil Data dari SQLite**
        cursor.execute("SELECT nama_produk, total_harga, waktu_peminjaman FROM rental WHERE status = 'Sudah Dikembalikan'")
        transaksi = cursor.fetchall()

        if not transaksi:
            print("\n⚠️ Tidak ada data penyewaan yang tersedia!")
            input("\n🔙 Tekan Enter untuk kembali ke menu admin...")
            return

        # **Hitung Total Pendapatan**
        total_pendapatan = sum(row[1] for row in transaksi)

        # **Buat Tabel Transaksi**
        table = PrettyTable()
        table.field_names = ["No", "Nama Barang", "Total Harga (Rp)", "Tanggal"]

        transaksi_per_bulan = {}
        transaksi_list = []

        for idx, (barang, total_harga, tanggal) in enumerate(transaksi, start=1):
            table.add_row([idx, barang, f"Rp {total_harga:,}", tanggal])
            transaksi_list.append((barang, total_harga))

            bulan = tanggal[:7]  # Ambil tahun-bulan (YYYY-MM)
            transaksi_per_bulan[bulan] = transaksi_per_bulan.get(bulan, 0) + total_harga

        print(table)

        # **Grafik ASCII - Pendapatan per Bulan**
        if transaksi_per_bulan:
            print("\n📊 Grafik ASCII - Pendapatan per Bulan:")
            for bulan, pendapatan in sorted(transaksi_per_bulan.items()):
                bar = "█" * max(1, pendapatan // 100000)  
                print(f"🗓 {bulan}: {bar} Rp {pendapatan:,}")

        # **Grafik ASCII - Distribusi Pendapatan**
        if transaksi_list:
            total_all = sum(p[1] for p in transaksi_list)
            if total_all > 0:
                print("\n🍰 Grafik ASCII - Distribusi Pendapatan:")
                for barang, pendapatan in transaksi_list:
                    percentage = (pendapatan / total_all) * 100
                    bar = "■" * max(1, int(percentage // 2))  
                    print(f"{barang.ljust(15)} | {bar} {percentage:.1f}%")

        print(f"\n💰 Total Pendapatan dari Penyewaan: Rp {total_pendapatan:,}")
        input("\n🔙 Tekan Enter untuk kembali ke menu admin...")

    except sqlite3.Error as e:
        print(f"❌ Terjadi kesalahan saat mengambil data: {e}")



import webbrowser

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
        print("0. Kembali ke menu admin")
        choice = input("Pilih menu (1/2/3/4/5): ")

        if choice == '1':
            show_all_data()
        elif choice == '2':
            show_history()
        elif choice == '3':
            reset_history()
        elif choice == '4':
            kelola_feedback()  # Menu baru untuk kelola feedback
        elif choice == '0':
            return  # Kembali ke menu admin
        else:
            print("Pilihan tidak valid, silakan coba lagi.")

import sqlite3
from prettytable import PrettyTable
from colorama import Fore, Style
from datetime import datetime

def load_json_data(file_path):
    """Memuat data dari file JSON jika tersedia, jika tidak kembalikan list kosong."""
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def show_all_data():
    print(Fore.YELLOW + Style.BRIGHT + "\n╔════════════════════════════════╗")
    print("║      📊 DATABASE RENTAL 📊      ║")
    print("╚════════════════════════════════╝")

    try:
        # **Tampilkan Data Produk dari SQLite & JSON**
        print(Fore.CYAN + "\n📌 Data Produk:")
        cursor.execute("SELECT id, nama, harga, status FROM produk")
        produk_list = cursor.fetchall()

        if not produk_list:  # Jika SQLite kosong, ambil dari JSON
            produk_list = [(p["id"], p["nama"], p["harga"], p["status"]) for p in load_json_data(produk_file)]

        table_produk = PrettyTable(["ID", "Nama Produk", "Harga (Rp)", "Status"])
        table_produk.align["Nama Produk"] = "l"
        table_produk.align["Harga (Rp)"] = "r"

        if produk_list:
            for id_produk, nama_produk, harga, status in produk_list:
                status_warna = Fore.GREEN + "✅ Tersedia" if status == "Tersedia" else Fore.RED + "❌ Tidak Tersedia"
                table_produk.add_row([id_produk, Fore.LIGHTYELLOW_EX + nama_produk + Fore.RESET, f"{harga:,}", status_warna])
            print(Fore.LIGHTBLACK_EX + table_produk.get_string())
        else:
            print(Fore.RED + "🚫 Tidak ada data produk.")

        # **Tampilkan Data Penyewaan dari SQLite & JSON**
        print(Fore.MAGENTA + "\n📌 Data Penyewaan:")
        cursor.execute("SELECT nama_pengguna, nama_produk, durasi_hari, total_harga, status FROM rental")
        rental_list = cursor.fetchall()

        if not rental_list:  # Jika SQLite kosong, ambil dari JSON
            rental_list = [(r["nama_pengguna"], r["nama_produk"], r["durasi_hari"], r["total_harga"], r["status"]) for r in load_json_data(rental_file)]

        table_rental = PrettyTable(["Nama Pengguna", "Produk", "Durasi (hari)", "Total Harga", "Status"])

        if rental_list:
            for nama_pengguna, nama_produk, durasi_hari, total_harga, status in rental_list:
                status_sewa = Fore.GREEN + "🟢 Aktif" if status == "Belum Dikembalikan" else Fore.RED + "🔴 Selesai"
                table_rental.add_row([
                    nama_pengguna,
                    Fore.LIGHTYELLOW_EX + nama_produk + Fore.RESET,
                    durasi_hari,
                    f"{total_harga:,}",
                    status_sewa
                ])
            print(Fore.LIGHTBLACK_EX + table_rental.get_string())
        else:
            print(Fore.RED + "🚫 Tidak ada penyewaan aktif.")

        # **Tampilkan Data Produk yang Dihapus dari SQLite & JSON**
        print(Fore.RED + "\n📌 Data Produk yang Dihapus:")
        cursor.execute("SELECT id, nama, harga FROM deleted_produk")
        deleted_produk_list = cursor.fetchall()

        if not deleted_produk_list:  # Jika SQLite kosong, ambil dari JSON
            deleted_produk_list = [(d["id"], d["nama"], d["harga"]) for d in load_json_data(deleted_produk_file)]

        table_deleted = PrettyTable(["ID", "Nama Produk", "Harga (Rp)"])

        if deleted_produk_list:
            for id_produk, nama_produk, harga in deleted_produk_list:
                table_deleted.add_row([id_produk, Fore.LIGHTRED_EX + nama_produk + Fore.RESET, f"{harga:,}"])
            print(Fore.LIGHTBLACK_EX + table_deleted.get_string())
        else:
            print(Fore.YELLOW + "🚫 Tidak ada produk yang dihapus.")

        input(Fore.CYAN + "\n🔘 Tekan Enter untuk kembali ke menu database...")

    except sqlite3.Error as e:
        print(f"❌ Terjadi kesalahan saat mengambil data dari database: {e}")



def show_history():
    """Menampilkan riwayat perubahan database dari SQLite."""
    print("\n--- Riwayat Perubahan Database ---")

    cursor.execute("SELECT action, data, timestamp FROM history ORDER BY id DESC")
    history_list = cursor.fetchall()

    if not history_list:
        print("🚫 Tidak ada riwayat perubahan database.")
        return

    for idx, (action, data, timestamp) in enumerate(history_list, 1):
        print(f"{idx}. [{timestamp}] {action} -> {data}")

    input("\n🔙 Tekan Enter untuk kembali ke menu database...")

from datetime import datetime

def add_to_history(action, data):
    """Menyimpan riwayat perubahan ke database SQLite."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO history (action, data, timestamp) VALUES (?, ?, ?)", (action, str(data), timestamp))
    conn.commit()


def reset_history():
    """Menghapus semua riwayat perubahan dari database SQLite."""
    confirm = input("Apakah Anda yakin ingin menghapus semua riwayat perubahan? (Y/N): ").lower()
    
    if confirm == 'y':
        cursor.execute("DELETE FROM history")
        conn.commit()
        print("✅ Riwayat perubahan berhasil dihapus.")
    else:
        print("❌ Riwayat perubahan tidak dihapus.")

def kelola_feedback():
    while True:
        print("\n--- Kelola Feedback ---")
        print("1. Lihat Feedback")
        print("2. Hapus Feedback")
        print("0. Kembali ke Menu Database")
        choice = input("Pilih menu (1/2/3): ")

        if choice == '1':
            lihat_feedback()
        elif choice == '2':
            hapus_feedback()
        elif choice == '0':
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
        
        
def lihat_semua_transaksi():
    print("\n📜 DAFTAR SEMUA TRANSAKSI 📜")
    
    try:
        cursor.execute("SELECT * FROM rental")
        data = cursor.fetchall()

        if not data:
            print("🚫 Tidak ada transaksi penyewaan yang tercatat.")
            return

        print("+----+----------------+----------------------+-------+------------+-------------------+----------------------+")
        print("| ID | Nama Pengguna  | Produk              | Hari  | Total Harga | Waktu Peminjaman  | Status               |")
        print("+----+----------------+----------------------+-------+------------+-------------------+----------------------+")
        
        for row in data:
            print(f"| {row[0]:<2} | {row[1]:<14} | {row[2]:<20} | {row[3]:<5} | Rp {row[4]:<9,} | {row[5]:<16} | {row[6]:<20} |")

        print("+----+----------------+----------------------+-------+------------+-------------------+----------------------+")
    
    except sqlite3.Error as e:
        print(f"❌ Terjadi kesalahan saat mengambil data: {e}")





def user_menu():
    while True:
        print("\n--- Menu User ---")
        print("1. Lihat daftar produk")
        print("2. Sorting daftar produk")  # Tambahkan sorting
        print("3. Sewa produk")
        print("0. Kembali ke menu utama")
        choice = input("Pilih menu (0/1/2/3): ")

        if choice == '1':
            print_produk()
        elif choice == '2':
            sort_produk()  # Sorting produk
        elif choice == '3':
            sewa_produk()
        elif choice == '0':
            return  # Kembali ke menu utama
        else:
            print("Pilihan tidak valid, silakan coba lagi.")


from datetime import datetime

import re
from datetime import datetime
from colorama import Fore, Style

import hashlib
import random
import time
import re
import urllib.parse
import webbrowser

# Simpan history penyewaan per user
SEWA_HISTORY = {}
LIMIT_PER_MINUTE = 3  # Maksimal 3 penyewaan per menit

def save_data():
    print("💾 Data penyewaan disimpan.")  # Simulasi fungsi penyimpanan data

def sewa_produk():
    load_data()
    print("\n╔════════════════════════════════╗")
    print("║  🚀  PROSES SEWA PRODUK   🚀  ║")
    print("╚════════════════════════════════╝")
    
    
    # Input ID User (5 Digit)
    while True:
        id_user = input("🆔 Masukkan ID User (5 digit angka): ")
        if id_user.isdigit() and len(id_user) == 5:
            break
        print("⚠️ ID User harus 5 digit angka!")

    try:
        # Input ID Produk
        while True:
            id_produk_input = input("\n🆔 Masukkan ID produk yang ingin disewa (ketik 'batal' untuk keluar): ")
            if id_produk_input.lower() == "batal":
                print("❌ Penyewaan dibatalkan.\n")
                return
            if id_produk_input.isdigit():
                id_produk = int(id_produk_input)
                break
            print("⚠️  ID produk harus berupa angka!")

        # Cek ketersediaan produk
        produk = next((p for p in produk_db if p["id"] == id_produk and p["status"] == "Tersedia"), None)
        if not produk:
            print("❌ Produk tidak tersedia atau sudah disewa!")
            return

        # Input Durasi Rental
        while True:
            hari_rental_input = input("📅 Masukkan durasi rental dalam hari (ketik 'batal' untuk keluar): ")
            if hari_rental_input.lower() == "batal":
                print("❌ Penyewaan dibatalkan.\n")
                return
            if hari_rental_input.isdigit():
                hari_rental = int(hari_rental_input)
                break
            print("⚠️  Durasi rental harus berupa angka!")

        # Hitung total harga
        waktu_sekarang = time.time()
        total_harga = produk["harga"] * hari_rental
        print(f"\n💰 Harga sewa per hari: Rp {produk['harga']:,}")
        print(f"💵 Total sewa untuk {hari_rental} hari: Rp {total_harga:,}")

        # Input Nama Pengguna & Validasi
        while True:
            nama_pengguna = input("👤 Masukkan nama pengguna (ketik 'batal' untuk keluar): ")
            if nama_pengguna.lower() == "batal":
                print("❌ Penyewaan dibatalkan.\n")
                return
            if re.match(r"^[a-zA-Z\s]+$", nama_pengguna):
                break
            print("⚠️  Nama hanya boleh berisi huruf dan spasi!")

        # Input Nomor Telepon & Validasi
        while True:
            no_telepon = input("📞 Masukkan nomor telepon (+62xxxx): ")
            if no_telepon.lower() == "batal":
                print("❌ Penyewaan dibatalkan.\n")
                return
            if re.match(r"^\+62[0-9]{9,13}$", no_telepon):
                break
            print("⚠️  Nomor telepon harus diawali +62 dan memiliki 9-13 digit angka!")

        # 🔒 Rate Limiting: Batasi penyewaan per user
        if no_telepon in SEWA_HISTORY:
            recent_sewa = [t for t in SEWA_HISTORY[no_telepon] if t > waktu_sekarang - 60]
            if len(recent_sewa) >= LIMIT_PER_MINUTE:
                print("🚨 Anda sudah mencapai batas maksimal penyewaan per menit!")
                return
        SEWA_HISTORY.setdefault(no_telepon, []).append(waktu_sekarang)

        # 🔐 OTP dengan Hashing (SHA-256)
        otp = str(random.randint(100000, 999999))
        hashed_otp = hashlib.sha256(otp.encode()).hexdigest()

        print(f"\n🔐 OTP Anda (Gunakan untuk verifikasi): {otp}")  # Simulasi, seharusnya dikirim lewat WA/SMS
        otp_expiry = waktu_sekarang + 300  # OTP berlaku 5 menit
        otp_attempts = 3

        # Proses verifikasi OTP
        while otp_attempts > 0:
            otp_input = input("Masukkan kode OTP: ")
            hashed_input = hashlib.sha256(otp_input.encode()).hexdigest()

            if hashed_input == hashed_otp and time.time() <= otp_expiry:
                print("✅ Verifikasi OTP berhasil! Melanjutkan penyewaan...\n")
                break
            else:
                otp_attempts -= 1
                print(f"❌ OTP salah! Sisa percobaan: {otp_attempts}")
                if otp_attempts == 0 or time.time() > otp_expiry:
                    print("🚨 Terlalu banyak percobaan atau OTP kadaluarsa. Penyewaan dibatalkan!")
                    return

        # 🔽 Simpan penyewaan ke SQLite
        save_rental_data(nama_pengguna, produk["nama"], hari_rental, total_harga)

        # 🔄 Perbarui status produk di JSON
        for p in produk_db:
            if p["id"] == id_produk:
                p["status"] = "Tidak Tersedia"
                break
        save_data()  # Simpan perubahan ke `produk.json`

        print(f"\n✅ Penyewaan produk '{produk['nama']}' berhasil diajukan.")
        print("⏳ Menunggu konfirmasi admin...\n")

        # 🔗 Arahkan ke WhatsApp setelah verifikasi
        wa_message = f"Saya ingin Memesan {produk['nama']} selama {hari_rental} hari. Terima Kasih"
        wa_safe_message = urllib.parse.quote(wa_message)
        wa_link = f"https://wa.me/6289516028710?text={wa_safe_message}"
        webbrowser.open(wa_link)
        print("📲 Mengarahkan ke WhatsApp untuk konfirmasi...\n")

    except ValueError:
        print("⚠️  Input tidak valid! Harap masukkan angka yang benar.")

        

def menu_feedback():
    while True:
        print("\n" + "="*50)
        print("📢  MENU FEEDBACK")
        print("="*50)
        print("1. Lihat Feedback")
        print("2. Kasih Feedback")
        print("0. Kembali ke Menu Utama")
        print("="*50)

        choice = input("Pilih menu (1/2/3): ").strip()

        if choice == '1':
            lihat_feedback()
        elif choice == '2':
            beri_feedback()
        elif choice == '0':
            print("\n👋 Kembali ke menu utama...")
            time.sleep(1)
            return
        else:
            print("⚠️  Pilihan tidak valid, silakan coba lagi!")
            time.sleep(1)

init(autoreset=True)  # Inisialisasi colorama untuk warna terminal

feedback_file = "feedback.json"

def print_animated(text, delay=0.02):
    """Animasi teks muncul satu per satu"""
    for char in text:
        print(char, end="", flush=True)
        time.sleep(delay)
    print()

def beri_feedback():
    print("\n" + "="*50)
    print("💬 Silakan tuliskan feedback atau saran Anda")
    print("="*50)

    feedback = input("Masukkan feedback: ").strip()
    if not feedback:
        print("⚠️  Feedback tidak boleh kosong!")
        time.sleep(1)
        return

    nama_pengguna = input("Masukkan nama Anda (Opsional, Enter jika anonim): ").strip()
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

    print("\n✅ Terima kasih atas feedback Anda!")
    time.sleep(1.5)

def lihat_feedback():
    if not os.path.exists(feedback_file):
        print("\n🚫 Belum ada feedback dari pengguna.")
        time.sleep(1.5)
        return

    with open(feedback_file, 'r') as f:
        all_feedback = json.load(f)

    print("\n" + "="*50)
    print("📜 Daftar Feedback Pengguna")
    print("="*50)

    if not all_feedback:
        print("⚠️  Belum ada feedback yang tersimpan.")
    else:
        for i, fb in enumerate(all_feedback, 1):
            print(f"\n[{i}] {fb['waktu']}")
            print(f"Nama     : {fb['nama']}")
            print(f"Feedback : {fb['feedback']}")
            print("-"*50)

    input("\nTekan Enter untuk kembali ke menu...")


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
import socket
import struct
import sys
import time

def port_scan(target):
    print(f"\n🔍 Scanning {target}...")
    
    ports = [21, 22, 25, 53, 80, 443, 3306, 8080]
    
    # Ping Scan (-sn) tanpa Scapy
    try:
        socket.gethostbyname(target)
        print(f"✅ Host {target} is UP!")
    except socket.gaierror:
        print(f"❌ Host {target} is DOWN!")
        return
    
    # TCP Connect Scan (-sT)
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                print(f"✅ Port {port} (TCP) is OPEN!")
            sock.close()
        except Exception as e:
            print(f"Error scanning {port}: {e}")
    
    # UDP Scan (-sU) dengan socket
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(1)
            sock.sendto(b"\x00", (target, port))
            data, _ = sock.recvfrom(1024)
            print(f"✅ Port {port} (UDP) might be OPEN!")
        except socket.timeout:
            print(f"✅ Port {port} (UDP) might be OPEN! (No Response)")
        except Exception as e:
            print(f"❌ Port {port} (UDP) is CLOSED!")
    
    # Service & Version Detection (-sV)
    for port in ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((target, port))
            if result == 0:
                sock.send(b'\n')
                banner = sock.recv(1024)
                print(f"✅ Port {port} is OPEN! Service: {banner.strip().decode(errors='ignore')}")
            sock.close()
        except:
            print(f"❌ Port {port} is CLOSED or not responding.")
    
    print("✅ Port scanning SELESAI!")



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

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import get_random_bytes


from colorama import Fore, Style, init
from prettytable import PrettyTable
import hashlib
import random
import time
import base64

init(autoreset=True)  # Inisialisasi warna

# Efek loading
def loading_effect(text, delay=0.05):
    print(Fore.YELLOW + "\n[ SYSTEM LOADING... ]", end="")
    for _ in range(5):
        time.sleep(delay)
        print(Fore.LIGHTYELLOW_EX + " ⚡", end="", flush=True)
    print(Fore.GREEN + f"\n{text}\n")

# Animasi efek terminal ala Matrix
def terminal_effect():
    print(Fore.GREEN)
    for _ in range(10):
        print("".join(random.choice("01█▓▒░") for _ in range(50)))
        time.sleep(0.05)
    print(Style.RESET_ALL)

# Tampilan awal CTF yang lebih keren
def print_ctf_header():
    print(Fore.CYAN + Style.BRIGHT + """
╔════════════════════════════════════╗
║  🎯  WELCOME TO THE ULTIMATE CTF  🎯  ║
║   🚀 TEST YOUR HACKING SKILLS 🚀   ║
╚════════════════════════════════════╝
""" + Fore.RESET)

# Daftar challenge CTF
def ctf():
    while True:
        print_ctf_header()

        # Buat tabel dengan PrettyTable
        table = PrettyTable()
        table.field_names = [Fore.YELLOW + "🔰 NO", "🛠️  CHALLENGE", "🎯  CATEGORY" + Fore.RESET]
        table.add_row(["1", "Advanced Cryptography", "🔐 Cryptography"])
        table.add_row(["2", "Reverse Engineering", "🛠️  Reverse Engineering"])
        table.add_row(["3", "Binary Exploitation", "🏴‍☠️  Exploitation"])
        table.add_row(["4", "Web Exploitation", "🌐 Web Security"])
        table.add_row(["5", "Networking", "📡 Network Security"])
        table.add_row(["6", "Steganography", "🔎 Steganography"])
        table.add_row(["0", "Keluar", "❌ Exit"])
        
        print(table)  # Tampilkan tabel challenge

        choice = input(Fore.LIGHTCYAN_EX + "Masukkan pilihan: " + Fore.RESET)

        challenges = [
            cryptography_challenge,
            reverse_engineering_challenge,
            binary_exploitation_challenge,
            web_exploitation_challenge,
            networking_challenge,
            steganography_challenge
        ]

        if choice == "0":
            print(Fore.RED + "👋 Kembali ke menu utama...\n")
            break  # Keluar dari menu CTF

        try:
            challenge_index = int(choice) - 1
            if 0 <= challenge_index < len(challenges):
                loading_effect(f"⚡ Memulai {table.get_string(fields=['🛠️  CHALLENGE'])[challenge_index+1]}...")
                result = challenges[challenge_index]()  # Jalankan challenge
                if result is False:
                    continue  # Jika user memilih exit di dalam challenge
            else:
                print(Fore.RED + "❌ Pilihan tidak valid.")
        except ValueError:
            print(Fore.RED + "❌ Masukkan angka yang valid.")

# CHALLENGE 1: Advanced Cryptography
def cryptography_challenge():
    print(Fore.LIGHTCYAN_EX + "\n🔐 [Challenge: Advanced Cryptography] 🔐")

    # Simulasi Enkripsi AES + RSA
    hidden_message = "FLAG{ENCRYPTED_SECRET}"
    encrypted_message = base64.b64encode(hidden_message.encode()).decode()

    print(f"\n🔑 Encrypted Message (Base64): {Fore.YELLOW}{encrypted_message}{Fore.RESET}")

    while True:
        user_input = input(Fore.CYAN + "Masukkan flag yang benar (atau ketik 'exit' untuk kembali): " + Fore.RESET)
        if user_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif user_input == hidden_message:
            print(Fore.GREEN + "✅ Benar! Kamu berhasil menyelesaikan tantangan Advanced Cryptography!")
            return True
        else:
            print(Fore.RED + "❌ Salah! Coba lagi.")

# CHALLENGE 2: Reverse Engineering
def reverse_engineering_challenge():
    print(Fore.LIGHTMAGENTA_EX + "\n🛠️ [Challenge: Reverse Engineering] 🛠️")

    secret_number = random.randint(1000, 9999)
    hashed_number = hashlib.sha256(str(secret_number).encode()).hexdigest()

    print(f"\n🔢 SHA-256 Hash dari nomor rahasia: {Fore.YELLOW}{hashed_number}{Fore.RESET}")

    while True:
        user_input = input(Fore.CYAN + "Tebak nomor rahasia: " + Fore.RESET)
        if user_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif user_input == str(secret_number):
            print(Fore.GREEN + "✅ Benar! Kamu berhasil memecahkan Reverse Engineering!")
            return True
        else:
            print(Fore.RED + "❌ Salah! Coba lagi.")

# CHALLENGE 3: Binary Exploitation
def binary_exploitation_challenge():
    print(Fore.LIGHTRED_EX + "\n🏴‍☠️ [Challenge: Binary Exploitation] 🏴‍☠️")

    binary_flag = b"\x46\x4c\x41\x47\x7b\x42\x55\x46\x46\x45\x52\x5f\x4f\x56\x45\x52\x46\x4c\x4f\x57\x7d"
    decoded_flag = binary_flag.decode("utf-8", "ignore")

    print(f"\n🧩 Binary Data (hex): {Fore.YELLOW}{binary_flag.hex()}{Fore.RESET}")

    while True:
        user_input = input(Fore.CYAN + "Masukkan flag yang benar: " + Fore.RESET)
        if user_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif user_input == decoded_flag:
            print(Fore.GREEN + "✅ Benar! Kamu berhasil memecahkan Binary Exploitation!")
            return True
        else:
            print(Fore.RED + "❌ Salah! Coba lagi.")

# CHALLENGE 4: Web Exploitation
def web_exploitation_challenge():
    print(Fore.LIGHTBLUE_EX + "\n🌐 [Challenge: Web Exploitation] 🌐")

    hashed_password = hashlib.md5("FLAG{SQLi_INJECTION}".encode()).hexdigest()

    print(f"\n🔐 MD5 Hash password admin: {Fore.YELLOW}{hashed_password}{Fore.RESET}")

    while True:
        user_input = input(Fore.CYAN + "Masukkan password admin yang sebenarnya: " + Fore.RESET)
        if user_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif user_input == "FLAG{SQLi_INJECTION}":
            print(Fore.GREEN + "✅ Benar! Kamu berhasil melakukan SQL Injection!")
            return True
        else:
            print(Fore.RED + "❌ Salah! Coba lagi.")
            
            # CHALLENGE 5: Networking
import random
import hashlib
from colorama import Fore, init

init(autoreset=True)

def networking_challenge():
    print(Fore.LIGHTYELLOW_EX + "\n📡 [Challenge: Advanced Networking] 📡")
    
    # Tahap 1: Firewall Multi-Layer
    target_ips = ["192.168.1.1", "10.0.0.1", "172.16.0.1"]
    print(Fore.CYAN + "\n🔥 Firewall memiliki beberapa lapisan proteksi!")
    
    for ip in target_ips:
        while True:
            user_ip = input(Fore.CYAN + "Masukkan IP yang benar untuk menembus layer firewall: " + Fore.RESET)
            if user_ip.lower() == "exit":
                print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
                return False
            elif user_ip == ip:
                print(Fore.GREEN + "✅ Layer firewall berhasil ditembus!")
                break
            else:
                print(Fore.RED + "❌ Salah! Coba lagi.")
    
    # Tahap 2: Port Knocking
    correct_ports = [22, 443, 8080]
    print(Fore.CYAN + "\n🚪 Firewall memerlukan urutan port knocking untuk membuka akses!")
    user_ports = []
    
    for i in range(3):
        port = input(Fore.CYAN + f"Masukkan port ke-{i+1}: " + Fore.RESET)
        if port.isdigit():
            user_ports.append(int(port))
        else:
            print(Fore.RED + "⚠️ Harus berupa angka!")
            return False
    
    if user_ports == correct_ports:
        print(Fore.GREEN + "✅ Port knocking berhasil! Firewall terbuka.")
    else:
        print(Fore.RED + "❌ Port knocking gagal! Kembali ke awal.")
        return False
    
    # Tahap 3: Spoofing Traffic
    correct_hash = hashlib.sha256("spoofed_packet".encode()).hexdigest()
    print(Fore.CYAN + "\n📡 Firewall mendeteksi paket! Spoof paket yang benar!")
    
    while True:
        spoofed_input = input(Fore.CYAN + "Masukkan hash paket spoofing yang benar: " + Fore.RESET)
        if spoofed_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif spoofed_input == correct_hash:
            print(Fore.GREEN + "✅ Paket spoofing berhasil! Akses granted.")
            return True
        else:
            print(Fore.RED + "❌ Paket spoofing salah! Coba lagi.")


# CHALLENGE 6: Steganography
def steganography_challenge():
    print(Fore.LIGHTYELLOW_EX + "\n🔎 [Challenge: Steganography] 🔎")

    secret_message = "FLAG{HIDDEN_TEXT}"
    encoded_message = base64.b64encode(secret_message.encode()).decode()

    print(f"\n🖼️ Gambar berisi pesan rahasia dalam format Base64: {Fore.YELLOW}{encoded_message}{Fore.RESET}")

    while True:
        user_input = input(Fore.CYAN + "Masukkan flag yang tersembunyi (atau ketik 'exit' untuk kembali): " + Fore.RESET)
        if user_input.lower() == "exit":
            print(Fore.RED + "🔄 Kembali ke menu CTF...\n")
            return False
        elif user_input == secret_message:
            print(Fore.GREEN + "✅ Benar! Kamu berhasil menyelesaikan tantangan Steganography!")
            return True
        else:
            print(Fore.RED + "❌ Salah! Coba lagi.")

# Tambahkan tantangan lain jika diperlukan...

# Menjalankan program
if __name__ == "__main__":
    save_admin_password()
    main_menu()