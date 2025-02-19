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

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
import webbrowser
import random
import hashlib
import time
import urllib.parse


class MainScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'

        self.add_widget(Label(text="VULN XPERT", font_size=40, bold=True, size_hint_y=None, height=60))
        self.add_widget(Label(text="\n💀 RENTAL TOOLS HACKER 💀\n⚔️ HACK THE PLANET ⚔️\n🌟 TOOLS PROFESSIONAL UNTUK PENTESTER 🌟",
                              font_size=35, halign='center', size_hint_y=None, height=120))
        self.add_widget(Image(source='skull.jpg', size_hint=(1, 0.1)))

        # Perbaikan: Memindahkan daftar tombol ke dalam __init__
        buttons = [
            ("TENTANG KAMI & CARA MENYEWA", self.tentang_kami),
            ("MENU ADMIN", self.admin_menu),
            ("MENU USER", self.user_menu),
            ("MENU FEEDBACK", self.menu_feedback),
            ("TUTORIAL", self.video_tutorial),
            ("SIMULASI SEDERHANA", self.simulasi_sederhana),
            ("CTF", self.ctf)
        ]

        for text, func in buttons:
            btn = Button(text=text, font_size=24, size_hint_y=None, height=80)
            btn.bind(on_press=lambda instance, f=func: f())  # Bind fungsi ke tombol
            self.add_widget(btn)


def user_menu(self):
    """Menu User"""
    self.clear_widgets()
    self.add_widget(Label(text="👤 MENU USER", font_size=30, bold=True))

    options = [
        ("Lihat Daftar Produk", self.lihat_produk),
        ("Sorting Daftar Produk", self.sort_produk),
        ("Sewa Produk", self.form_sewa)
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def lihat_produk(self):
    """Menampilkan daftar produk yang tersedia"""
    self.clear_widgets()
    self.add_widget(Label(text="📦 DAFTAR PRODUK", font_size=30, bold=True))

    cursor.execute("SELECT nama, harga, status FROM produk")
    produk_list = cursor.fetchall()

    for nama, harga, status in produk_list:
        status_label = "✅ Tersedia" if status == "Tersedia" else "❌ Tidak Tersedia"
        self.add_widget(Label(text=f"{nama} - Rp {harga:,} - {status_label}", font_size=18))

    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def sort_produk(self):
    """Sorting produk berdasarkan harga"""
    self.clear_widgets()
    self.add_widget(Label(text="📊 SORTING PRODUK", font_size=30, bold=True))

    options = [
        ("Harga Termurah", lambda: self.sort_produk_by("ASC")),
        ("Harga Termahal", lambda: self.sort_produk_by("DESC"))
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def sort_produk_by(self, order):
    """Melakukan sorting produk berdasarkan harga"""
    self.clear_widgets()
    self.add_widget(Label(text="📊 HASIL SORTING PRODUK", font_size=30, bold=True))

    cursor.execute(f"SELECT nama, harga, status FROM produk ORDER BY harga {order}")
    produk_list = cursor.fetchall()

    for nama, harga, status in produk_list:
        status_label = "✅ Tersedia" if status == "Tersedia" else "❌ Tidak Tersedia"
        self.add_widget(Label(text=f"{nama} - Rp {harga:,} - {status_label}", font_size=18))

    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def pilih_produk(self):
    """Menampilkan daftar produk yang bisa dipilih untuk disewa"""
    self.clear_widgets()
    self.add_widget(Label(text="🛒 PILIH PENTEST TOOLS", font_size=30, bold=True))

    cursor.execute("SELECT id, nama, harga FROM produk WHERE status='Tersedia'")
    produk_list = cursor.fetchall()

    if not produk_list:
        self.add_widget(Label(text="❌ Tidak ada produk tersedia", font_size=20))

    self.produk_terpilih = None  # Inisialisasi variabel untuk menyimpan pilihan

    for id_barang, nama, harga in produk_list:
        btn = Button(text=f"{nama} - Rp {harga:,}/hari", font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, id=id_barang, n=nama, h=harga: self.set_produk_terpilih(id, n, h))
        self.add_widget(btn)

    # Tombol Lanjut (default dalam keadaan nonaktif)
    self.btn_lanjut = Button(text="Pilih Barang Sebelum Lanjut", font_size=18, size_hint_y=None, height=60, disabled=True)
    self.btn_lanjut.bind(on_press=self.form_data_diri)
    self.add_widget(self.btn_lanjut)

    # Tombol Kembali
    btn_back = Button(text="Pergi ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=self.user_menu)
    self.add_widget(btn_back)

def set_produk_terpilih(self, id_barang, nama, harga):
    """Menyimpan produk yang dipilih dan mengaktifkan tombol lanjut"""
    self.produk_terpilih = {"id": id_barang, "nama": nama, "harga": harga}
    self.btn_lanjut.text = f"✅ {nama} Dipilih - Lanjut"
    self.btn_lanjut.disabled = False

def form_data_diri(self, instance):
    """Halaman 2: Form untuk mengisi data diri sebelum menyewa"""
    if not self.produk_terpilih:
        return  # Pastikan produk telah dipilih

    self.clear_widgets()
    self.add_widget(Label(text="📋 FORM DATA DIRI", font_size=30, bold=True))

    self.id_user = TextInput(hint_text="Masukkan ID User", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.id_user)

    self.username = TextInput(hint_text="Masukkan Username", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.username)

    self.no_wa = TextInput(hint_text="Masukkan No WA (628xxx)", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.no_wa)

    self.durasi = TextInput(hint_text="Durasi Sewa (hari)", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.durasi)

    # Tombol Sewa
    btn_sewa = Button(text="Sewa Pentest Tools", font_size=20, size_hint_y=None, height=80)
    btn_sewa.bind(on_press=self.kirim_whatsapp)
    self.add_widget(btn_sewa)

    # Tombol kembali
    btn_back = Button(text="Pergi ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

import webbrowser
import urllib.parse

def kirim_whatsapp(self, instance):
    """Mengirim permintaan sewa melalui WhatsApp"""
    if not self.produk_terpilih:
        return  # Pastikan produk dipilih

    id_user = self.id_user.text.strip()
    username = self.username.text.strip()
    no_wa = self.no_wa.text.strip()
    durasi = self.durasi.text.strip()

    # Validasi Input
    if not id_user or not username or not no_wa or not durasi:
        print("⚠️ Semua data harus diisi!")
        return

    nama_produk = self.produk_terpilih["nama"]

    # Format pesan WhatsApp
    pesan = f"Saya ingin menyewa \"{nama_produk}\" dengan durasi \"{durasi} hari\". Terima kasih."
    link_wa = f"https://wa.me/{no_wa}?text={urllib.parse.quote(pesan)}"
    
    webbrowser.open(link_wa)  # Buka WhatsApp dengan pesan otomatis
    print("📲 Mengarahkan ke WhatsApp untuk konfirmasi...\n")

def simulasi_sederhana(self):
    """Menu Simulasi Sederhana"""
    self.clear_widgets()
    self.add_widget(Label(text="🔍 SIMULASI SEDERHANA", font_size=30, bold=True))

    options = [
        ("Scan Port", self.dummy_function),
        ("Web Enumeration", self.dummy_function),
        ("Brute Force Login", self.dummy_function)
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def ctf(self):
    """Tampilan menu CTF (Capture The Flag)"""
    self.clear_widgets()
    self.add_widget(Label(text="🏴‍☠️ CTF CHALLENGE", font_size=30, bold=True))

    options = [
        ("Advanced Cryptography", self.dummy_function),
        ("Reverse Engineering", self.dummy_function),
        ("Binary Exploitation", self.dummy_function),
        ("Web Exploitation", self.dummy_function),
        ("Networking", self.dummy_function),
        ("Steganography", self.dummy_function)
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def video_tutorial(self):
    """Menu Tutorial YouTube"""
    self.clear_widgets()
    self.add_widget(Label(text="📺 PILIH TUTORIAL:", font_size=30, bold=True))

    video_links = {
        "1": "https://youtu.be/QiNLNDSLuJY?si=X6c7nQQTDllpHxUB",
        "2": "https://youtu.be/x87gbgQD4eg?si=SOpC1fIVGsBfo3cH",
        "3": "https://youtu.be/xuYZNJCvHgQ?si=NtbvNZZCbAejNZFS"
    }

    options = [
        ("BELAJAR METASPLOIT", lambda: webbrowser.open(video_links["1"])),
        ("BELAJAR NMAP", lambda: webbrowser.open(video_links["2"])),
        ("BELAJAR BURP SUITE", lambda: webbrowser.open(video_links["3"]))
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def tentang_kami(self):
    """Menampilkan menu Tentang Kami & Cara Menyewa"""
    self.clear_widgets()
    self.add_widget(Label(text="📜 TENTANG KAMI & CARA MENYEWA", font_size=30, bold=True))

    # Tombol-Tombol Navigasi
    options = [
        ("Tentang Kami", self.show_tentang_kami),
        ("Cara Menyewa", self.show_cara_menyewa),
        ("Profil Penulis", self.show_profil_penulis),
        ("Kontak WhatsApp", self.kontak_whatsapp)
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def show_tentang_kami(self):
    """Menampilkan informasi tentang layanan"""
    self.clear_widgets()
    self.add_widget(Label(text="📜 TENTANG KAMI", font_size=30, bold=True))
    self.add_widget(Label(text="Kami menyediakan layanan rental tools hacking profesional.", font_size=18))
    
    # Tombol Kembali
    btn_back = Button(text="Kembali", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.tentang_kami())
    self.add_widget(btn_back)

def show_cara_menyewa(self):
    """Menampilkan cara menyewa tools"""
    self.clear_widgets()
    self.add_widget(Label(text="📜 CARA MENYEWA", font_size=30, bold=True))
    self.add_widget(Label(text="1. Pilih tools yang ingin disewa\n2. Lakukan pembayaran\n3. Verifikasi melalui admin\n4. Tools siap digunakan!", font_size=18))

    # Tombol Kembali
    btn_back = Button(text="Kembali", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.tentang_kami())
    self.add_widget(btn_back)

def show_profil_penulis(self):
    """Menampilkan profil penulis aplikasi"""
    self.clear_widgets()
    self.add_widget(Label(text="👤 PROFIL PENULIS", font_size=30, bold=True))
    self.add_widget(Label(text="Penulis: John Doe\nPakar Cybersecurity & Developer Python", font_size=18))

    # Tombol Kembali
    btn_back = Button(text="Kembali", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.tentang_kami())
    self.add_widget(btn_back)

def kontak_whatsapp(self):
    """Membuka WhatsApp untuk komunikasi langsung"""
    webbrowser.open("https://wa.me/6289516028710")  # Ganti dengan nomor WhatsApp yang benar

def menu_feedback(self):
    """Tampilan Menu Feedback"""
    self.clear_widgets()
    self.add_widget(Label(text="📢 MENU FEEDBACK", font_size=30, bold=True))

    options = [
        ("Lihat Feedback", self.dummy_function),
        ("Beri Feedback", self.dummy_function)
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def admin_menu(self):
    """Tampilan GUI Menu Admin"""
    self.clear_widgets()
    self.add_widget(Label(text="🔧 MENU ADMIN", font_size=30, bold=True))

    options = [
        ("Kelola Barang Rental", self.kelola_barang_gui),
        ("Lihat Daftar Barang", self.lihat_produk),
        ("Sorting Daftar Barang", self.sort_produk),
        ("Konfirmasi Penyewaan", self.dummy_function),  # Placeholder untuk fitur konfirmasi
        ("Laporan Pendapatan", self.dummy_function),  # Placeholder untuk laporan pendapatan
        ("Menu Database", self.dummy_function),  # Placeholder untuk pengelolaan database
        ("Lihat Semua Transaksi", self.dummy_function)  # Placeholder untuk melihat transaksi
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def kelola_barang_gui(self):
    """Menu GUI untuk Kelola Barang"""
    self.clear_widgets()
    self.add_widget(Label(text="📦 KELOLA BARANG", font_size=30, bold=True))

    options = [
        ("Ubah Nama, Harga, dan ID Barang", self.dummy_function),  # Placeholder untuk ubah produk
        ("Tambah Barang", self.dummy_function),  # Placeholder untuk tambah produk
        ("Hapus Barang", self.dummy_function),  # Placeholder untuk hapus produk
        ("Kembalikan Produk yang Dihapus", self.dummy_function)  # Placeholder untuk restore produk
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu Admin", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.admin_menu())
    self.add_widget(btn_back)

def lihat_produk(self):
    """Menampilkan daftar produk yang tersedia"""
    self.clear_widgets()
    self.add_widget(Label(text="📦 DAFTAR PRODUK", font_size=30, bold=True))

    cursor.execute("SELECT nama, harga, status FROM produk")
    produk_list = cursor.fetchall()

    if not produk_list:
        self.add_widget(Label(text="❌ Tidak ada produk tersedia", font_size=20))
    else:
        for nama, harga, status in produk_list:
            status_label = "✅ Tersedia" if status == "Tersedia" else "❌ Tidak Tersedia"
            self.add_widget(Label(text=f"{nama} - Rp {harga:,} - {status_label}", font_size=18))

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def sort_produk(self):
    """Menampilkan menu untuk sorting produk berdasarkan harga"""
    self.clear_widgets()
    self.add_widget(Label(text="📊 SORTING PRODUK", font_size=30, bold=True))

    options = [
        ("Harga Termurah", lambda: self.sort_produk_by("ASC")),
        ("Harga Termahal", lambda: self.sort_produk_by("DESC"))
    ]

    for text, func in options:
        btn = Button(text=text, font_size=18, size_hint_y=None, height=60)
        btn.bind(on_press=lambda instance, f=func: f())  
        self.add_widget(btn)

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def sort_produk_by(self, order):
    """Melakukan sorting produk berdasarkan harga"""
    self.clear_widgets()
    self.add_widget(Label(text="📊 HASIL SORTING PRODUK", font_size=30, bold=True))

    cursor.execute(f"SELECT nama, harga, status FROM produk ORDER BY harga {order}")
    produk_list = cursor.fetchall()

    if not produk_list:
        self.add_widget(Label(text="❌ Tidak ada produk tersedia", font_size=20))
    else:
        for nama, harga, status in produk_list:
            status_label = "✅ Tersedia" if status == "Tersedia" else "❌ Tidak Tersedia"
            self.add_widget(Label(text=f"{nama} - Rp {harga:,} - {status_label}", font_size=18))

    # Tombol Kembali
    btn_back = Button(text="Kembali ke Menu User", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.user_menu())
    self.add_widget(btn_back)

def form_sewa(self):
    """Tampilan Form Penyewaan GUI"""
    self.clear_widgets()
    self.add_widget(Label(text="📌 FORM SEWA PENTEST TOOLS", font_size=30, bold=True))

    # Input ID Barang
    self.id_barang = TextInput(hint_text="Masukkan ID Barang", font_size=18, size_hint_y=None, height=60)
    self.id_barang.bind(text=self.update_nama_harga)
    self.add_widget(self.id_barang)

    # Nama Barang (Otomatis)
    self.nama_barang = Label(text="Nama Pentest Tools: -", font_size=18)
    self.add_widget(self.nama_barang)

    # Harga Sewa per Hari (Otomatis)
    self.harga_sewa = Label(text="Harga Sewa Per Hari: -", font_size=18)
    self.add_widget(self.harga_sewa)

    # Input Berapa Hari
    self.hari_sewa = TextInput(hint_text="Masukkan Jumlah Hari", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.hari_sewa)

    # Input ID User
    self.id_user = TextInput(hint_text="Masukkan ID User (5 Digit)", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.id_user)

    # Input Username
    self.username = TextInput(hint_text="Masukkan Username", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.username)

    # Input Nomor WhatsApp
    self.nomor_wa = TextInput(hint_text="Masukkan Nomor WhatsApp (+62xxx)", font_size=18, size_hint_y=None, height=60)
    self.add_widget(self.nomor_wa)

    # Tombol untuk menyewa
    btn_sewa = Button(text="Sewa Pentest Tools", font_size=20, size_hint_y=None, height=80)
    btn_sewa.bind(on_press=self.proses_sewa)
    self.add_widget(btn_sewa)

    # Tombol kembali
    btn_back = Button(text="Kembali ke Menu Utama", font_size=18, size_hint_y=None, height=60)
    btn_back.bind(on_press=lambda instance: self.main_menu())
    self.add_widget(btn_back)

def update_nama_harga(self, instance, value):
    """Update Nama dan Harga dari ID Barang yang dimasukkan"""
    if value.isdigit():
        id_barang = int(value)

        # Ambil data produk dari database
        cursor.execute("SELECT nama, harga FROM produk WHERE id=? AND status='Tersedia'", (id_barang,))
        produk = cursor.fetchone()

        if produk:
            nama, harga = produk
            self.nama_barang.text = f"Nama Pentest Tools: {nama}"
            self.harga_sewa.text = f"Harga Sewa Per Hari: Rp {harga:,}"
        else:
            self.nama_barang.text = "Nama Pentest Tools: Tidak Ditemukan"
            self.harga_sewa.text = "Harga Sewa Per Hari: -"

import random
import hashlib
import urllib.parse
import webbrowser

def proses_sewa(self, instance):
    """Proses Penyewaan"""
    id_barang = self.id_barang.text.strip()
    hari_sewa = self.hari_sewa.text.strip()
    id_user = self.id_user.text.strip()
    username = self.username.text.strip()
    nomor_wa = self.nomor_wa.text.strip()

    # Validasi Input
    if not (id_barang.isdigit() and hari_sewa.isdigit() and id_user.isdigit() and username and nomor_wa):
        print("⚠️ Semua data harus diisi dengan benar!")
        return

    id_barang = int(id_barang)
    hari_sewa = int(hari_sewa)

    # Ambil produk dari database
    cursor.execute("SELECT nama, harga FROM produk WHERE id=? AND status='Tersedia'", (id_barang,))
    produk = cursor.fetchone()

    if not produk:
        print("❌ Produk tidak tersedia atau sudah disewa!")
        return

    nama_produk, harga_per_hari = produk
    total_harga = harga_per_hari * hari_sewa

    # OTP Verification
    otp = str(random.randint(100000, 999999))
    hashed_otp = hashlib.sha256(otp.encode()).hexdigest()
    print(f"🔐 OTP Anda: {otp}")  # Simulasi OTP

    otp_attempts = 3
    while otp_attempts > 0:
        otp_input = input("Masukkan kode OTP: ")
        hashed_input = hashlib.sha256(otp_input.encode()).hexdigest()

        if hashed_input == hashed_otp:
            print("✅ Verifikasi OTP berhasil!")
            break
        else:
            otp_attempts -= 1
            print(f"❌ OTP salah! Sisa percobaan: {otp_attempts}")
            if otp_attempts == 0:
                print("🚨 Terlalu banyak percobaan. Penyewaan dibatalkan!")
                return

    # Simpan ke Database
    waktu_peminjaman = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO rental (nama_pengguna, nama_produk, durasi_hari, total_harga, waktu_peminjaman, status) VALUES (?, ?, ?, ?, ?, ?)",
                   (username, nama_produk, hari_sewa, total_harga, waktu_peminjaman, "Disewa"))
    conn.commit()

    # Update Status Produk
    cursor.execute("UPDATE produk SET status='Tidak Tersedia' WHERE id=?", (id_barang,))
    conn.commit()

    # Kirim ke WhatsApp
    wa_message = f"Saya ingin menyewa {nama_produk} selama {hari_sewa} hari. Terima Kasih."
    wa_safe_message = urllib.parse.quote(wa_message)
    wa_link = f"https://wa.me/{nomor_wa}?text={wa_safe_message}"
    webbrowser.open(wa_link)

    print("📲 Mengarahkan ke WhatsApp untuk konfirmasi...\n")

def dummy_function(self):
    """Fungsi sementara untuk fitur yang belum diimplementasikan"""
    print("⚠️ Fitur ini belum tersedia. Sedang dalam pengembangan...")

class RentalApp(App):
    def build(self):
        return MainScreen()

if __name__ == "__main__":
    RentalApp().run()
