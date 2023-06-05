import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ttkbootstrap import Style
from turtle import title
from pywinauto import Application, Desktop
import time
from automation import run_epson_scan
from vch_temp_singkat import vch_txt


def submit_form():
    # Mendapatkan nilai input dari field
    nama_voucher = entry_nama_voucher.get()
    kode_voucher = entry_kode_voucher.get()
    harga = entry_harga.get()
    digipos = entry_digipos.get()
    user = entry_user.get()
    jumlah_voucher = entry_jumlah_voucher.get()
    waktu = datetime.now().strftime("%d-%m-%Y %H:%M")

    # Menampilkan nilai input
    print("Nama Voucher:", nama_voucher)
    print("Kode Voucher:", kode_voucher)
    print("Harga:", harga)
    print("Digipos:", digipos)
    print("Jumlah Voucher:", jumlah_voucher)
    print("User:", user)
    print("Waktu:", waktu)

    # Cek field yang belum diisi
    empty_fields = []
    if not nama_voucher:
        empty_fields.append("Nama Voucher")
    if not kode_voucher:
        empty_fields.append("Kode Voucher")
    if not harga:
        empty_fields.append("Harga")
    if not digipos:
        empty_fields.append("Digipos")
    if not user:
        empty_fields.append("User")
    if not jumlah_voucher:
        empty_fields.append("Jumlah Voucher")

    # Jika ada field yang belum diisi, tampilkan peringatan
    if empty_fields:
        empty_fields_text = ", ".join(empty_fields)
        messagebox.showerror("Peringatan", f"{empty_fields_text} belum diisi!")
        return

    # Menampilkan kotak dialog pesan konfirmasi
    confirm = messagebox.askyesno("Konfirmasi", "Apakah data sudah benar?")
    if confirm:
        # Panggil fungsi run_epson_scan di latar belakang
        kode_voucher = entry_kode_voucher.get()
        run_epson_scan(
            nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu
        )
        time.sleep(2)  # Tunggu sebentar agar Epson Scan dapat dijalankan

        # Mengosongkan field input
        entry_nama_voucher.delete(0, tk.END)
        entry_kode_voucher.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_digipos.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_jumlah_voucher.delete(0, tk.END)

    else:
        return


def validate_numeric_input(event):
    # Mendapatkan karakter yang diinputkan
    char = event.char

    # Memeriksa apakah karakter adalah angka atau backspace
    if not char.isdigit() and char != "\b":
        return "break"  # Membatalkan input karakter


def validate_fields():
    # Mendapatkan nilai input dari setiap field
    nama_voucher = entry_nama_voucher.get()
    kode_voucher = entry_kode_voucher.get()
    harga = entry_harga.get()
    digipos = entry_digipos.get()
    user = entry_user.get()
    jumlah_voucher = entry_jumlah_voucher.get()

    # Validasi field harga dan jumlah voucher hanya jika keduanya telah terisi
    if harga and jumlah_voucher:
        # Validasi input harga dan jumlah voucher
        if not harga.isdigit() or not jumlah_voucher.isdigit():
            return False

    # Kembalikan True jika semua field telah terisi dan validasi angka berhasil, False jika ada yang kosong atau tidak valid
    return all([nama_voucher, kode_voucher, harga, digipos, user, jumlah_voucher])

window = tk.Tk()
window.title("Form Voucher")
window.geometry("500x500")
window.resizable(False, False)

# Menerapkan tema menggunakan ttkbootstrap
style = Style(theme="journal")

# Membuat frame utama
frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

# Membuat label dan field untuk Nama Voucher
label_nama_voucher = tk.Label(frame, text="Nama Voucher")
label_nama_voucher.pack(anchor="w", padx=10, pady=5)
entry_nama_voucher = tk.Entry(frame, justify="right")
entry_nama_voucher.pack(anchor="e", padx=10, pady=5)

# Membuat label dan field untuk Kode Voucher
label_kode_voucher = tk.Label(frame, text="Kode Voucher")
label_kode_voucher.pack(anchor="w", padx=10, pady=5)
entry_kode_voucher = tk.Entry(frame, justify="right")
entry_kode_voucher.pack(anchor="e", padx=10, pady=5)

# Membuat label dan field untuk Harga
label_harga = tk.Label(frame, text="Harga")
label_harga.pack(anchor="w", padx=10, pady=5)
entry_harga = tk.Entry(frame, justify="right")
entry_harga.pack(anchor="e", padx=10, pady=5)

# Membuat label dan field untuk Digipos
label_digipos = tk.Label(frame, text="Digipos")
label_digipos.pack(anchor="w", padx=10, pady=5)
entry_digipos = tk.Entry(frame, justify="right")
entry_digipos.pack(anchor="e", padx=10, pady=5)

# Membuat label dan field untuk User
label_user = tk.Label(frame, text="User")
label_user.pack(anchor="w", padx=10, pady=5)
entry_user = tk.Entry(frame, justify="right")
entry_user.pack(anchor="e", padx=10, pady=5)

# Membuat label dan field untuk Jumlah Voucher
label_jumlah_voucher = tk.Label(frame, text="Jumlah Voucher")
label_jumlah_voucher.pack(anchor="w", padx=10, pady=5)
entry_jumlah_voucher = tk.Entry(frame, justify="right")
entry_jumlah_voucher.pack(anchor="e", padx=10, pady=5)

# Membuat tombol Simpan
button_simpan = tk.Button(frame, text="Simpan", command=submit_form)
button_simpan.pack(pady=20)

# Menjalankan event loop Tkinter
window.mainloop()
