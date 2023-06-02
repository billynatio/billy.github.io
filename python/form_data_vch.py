import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from turtle import title
from pywinauto import Application, Desktop
import time


def submit_form():
    # Mendapatkan nilai input dari field
    nama_voucher = entry_nama_voucher.get()
    kode_voucher = entry_kode_voucher.get()
    harga = entry_harga.get()
    digipos = entry_digipos.get()
    user = entry_user.get()
    jumlah_voucher = entry_jumlah_voucher.get()

    # Menampilkan nilai input
    print("Nama Voucher:", nama_voucher)
    print("Kode Voucher:", kode_voucher)
    print("Harga:", harga)
    print("Digipos:", digipos)
    print("Jumlah Voucher:", jumlah_voucher)
    print("User:", user)

    # Mendapatkan waktu sekarang
    waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    print("Waktu:", waktu_sekarang)

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
        # Mengosongkan field input
        entry_nama_voucher.delete(0, tk.END)
        entry_kode_voucher.delete(0, tk.END)
        entry_harga.delete(0, tk.END)
        entry_digipos.delete(0, tk.END)
        entry_user.delete(0, tk.END)
        entry_jumlah_voucher.delete(0, tk.END)

        # Start the Epson Scan application
        app_epson = Application(backend="uia").start(r"C:\Windows\twain_32\escndv\escndv.exe")

        # Wait for the Epson Scan window to appear
        window_epson = app_epson.window(title="EPSON Scan")
        window_epson.wait("exists", timeout=10)  # Adjust the timeout as needed

        # Activate the Epson Scan window
        window_epson.set_focus()

        # Click the "Customize" button
        button_customize = window_epson.child_window(title="Customize...", control_type="Button")
        button_customize.click()

        # Wait for the "Customize" dialog to appear
        window_customize = window_epson.window(title="Customize")
        window_customize.wait("exists", timeout=10)  # Adjust the timeout as needed

        # Click the "File Save Settings" button in the "Customize" dialog
        button_file_save_settings = window_customize.child_window(auto_id="1080", control_type="Button")
        button_file_save_settings.click()

        # Wait for the "Save Settings" dialog to appear
        window_save_settings = window_epson.window(title="File Save Settings")
        window_save_settings.wait("exists", timeout=10)  # Adjust the timeout as needed

        # Set the prefix name to the code voucher and current time
        prefix_name = kode_voucher + "_" + waktu_sekarang.replace(" ", "_").replace(":", "-") +"/"
        edit_prefix = window_save_settings.child_window(auto_id="1202", control_type="Edit")
        edit_prefix.set_text(prefix_name)


        # Set the start number to "888"
        edit_start_number = window_save_settings.child_window(title="Start Number:", control_type="Edit")
        edit_start_number.set_text("888")

        # Click the "OK" button in the "Save Settings" dialog
        button_ok_save_settings = window_save_settings.child_window(title="OK", control_type="Button")
        button_ok_save_settings.click()

        # Click the "OK" button in the "Customize" dialog
        button_ok_customize = window_customize.child_window(title="OK", control_type="Button")
        button_ok_customize.click()

        # Click the "Scan" button in the Epson Scan window
        button_scan = window_epson.child_window(title="Scan", control_type="Button")
        button_scan.click()

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


# Membuat window Tkinter
window = tk.Tk()
window.title("Form Voucher")

# Membuat label dan field untuk Nama Voucher
label_nama_voucher = tk.Label(window, text="Nama Voucher:")
label_nama_voucher.grid(row=0, column=0, sticky="W")
entry_nama_voucher = tk.Entry(window)
entry_nama_voucher.grid(row=0, column=1)

# Membuat label dan field untuk Kode Voucher
label_kode_voucher = tk.Label(window, text="Kode Voucher:")
label_kode_voucher.grid(row=1, column=0, sticky="W")
entry_kode_voucher = tk.Entry(window)
entry_kode_voucher.grid(row=1, column=1)

# Membuat label dan field untuk Harga
label_harga = tk.Label(window, text="Harga:")
label_harga.grid(row=2, column=0, sticky="W")
entry_harga = tk.Entry(window)
entry_harga.grid(row=2, column=1)
entry_harga.bind("<KeyPress>", validate_numeric_input)

# Membuat label dan field untuk Jumlah_voucher
label_jumlah_voucher = tk.Label(window, text="Jumlah Voucher:")
label_jumlah_voucher.grid(row=3, column=0, sticky="W")
entry_jumlah_voucher = tk.Entry(window)
entry_jumlah_voucher.grid(row=3, column=1)
entry_jumlah_voucher.bind("<KeyPress>", validate_numeric_input)

# Membuat label dan field untuk Digipos
label_digipos = tk.Label(window, text="Digipos:")
label_digipos.grid(row=4, column=0, sticky="W")
entry_digipos = tk.Entry(window)
entry_digipos.grid(row=4, column=1)

# Membuat label dan field untuk User
label_user = tk.Label(window, text="User:")
label_user.grid(row=5, column=0, sticky="W")
entry_user = tk.Entry(window)
entry_user.grid(row=5, column=1)

# Mendapatkan waktu sekarang
waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Membuat label untuk waktu sekarang di sudut kanan bawah
label_waktu = tk.Label(window, text=waktu_sekarang)
label_waktu.grid(row=7, column=1, sticky="SE")

# Membuat tombol Simpan
button_simpan = tk.Button(
    window, text="Simpan", command=lambda: validate_fields() and submit_form()
)
button_simpan.grid(row=6, column=0, sticky="W")

# Menjalankan event loop Tkinter
window.mainloop()
