import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
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
        run_epson_scan(nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu)
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


# Membuat window Tkinter
window = tk.Tk()
window.title("Form Voucher")
window.configure(bg="#F8F8F8")  # Warna latar belakang

# Membuat label dan field untuk Nama Voucher
label_nama_voucher = tk.Label(window, text="Nama Voucher:", bg="#F8F8F8")  # Warna latar belakang
label_nama_voucher.grid(row=0, column=0, sticky="W")
entry_nama_voucher = tk.Entry(window)
entry_nama_voucher.grid(row=0, column=1)

# Membuat label dan field untuk Kode Voucher
label_kode_voucher = tk.Label(window, text="Kode Voucher:", bg="#F8F8F8")  # Warna latar belakang
label_kode_voucher.grid(row=1, column=0, sticky="W")
entry_kode_voucher = tk.Entry(window)
entry_kode_voucher.grid(row=1, column=1)

# Membuat label dan field untuk Harga
label_harga = tk.Label(window, text="Harga:", bg="#F8F8F8")  # Warna latar belakang
label_harga.grid(row=2, column=0, sticky="W")
entry_harga = tk.Entry(window)
entry_harga.grid(row=2, column=1)
entry_harga.bind("<KeyPress>", validate_numeric_input)

# Membuat label dan field untuk Jumlah Voucher
label_jumlah_voucher = tk.Label(window, text="Jumlah Voucher:", bg="#F8F8F8")  # Warna latar belakang
label_jumlah_voucher.grid(row=3, column=0, sticky="W")
entry_jumlah_voucher = tk.Entry(window)
entry_jumlah_voucher.grid(row=3, column=1)
entry_jumlah_voucher.bind("<KeyPress>", validate_numeric_input)

# Membuat label dan field untuk Digipos
label_digipos = tk.Label(window, text="Digipos:", bg="#F8F8F8")  # Warna latar belakang
label_digipos.grid(row=4, column=0, sticky="W")
entry_digipos = tk.Entry(window)
entry_digipos.grid(row=4, column=1)

# Membuat label dan field untuk User
label_user = tk.Label(window, text="User:", bg="#F8F8F8")  # Warna latar belakang
label_user.grid(row=5, column=0, sticky="W")
entry_user = tk.Entry(window)
entry_user.grid(row=5, column=1)

# Mendapatkan waktu sekarang
waktu = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

# Membuat label untuk waktu sekarang di sudut kanan bawah
label_waktu = tk.Label(window, text=waktu, bg="#F8F8F8", font=("Helvetica", 10, "italic"))
label_waktu.grid(row=6, column=1, sticky="E")

# Membuat tombol Submit dengan gaya yang lebih modern
submit_button = tk.Button(window, text="Submit", command=submit_form, bg="#4CAF50", fg="#FFFFFF", padx=10, pady=5,
                          font=("Helvetica", 12, "bold"), relief="groove", activebackground="#45A049")
submit_button.grid(row=7, column=1, pady=10)

# Memposisikan window di tengah layar
window.update_idletasks()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Memanggil fungsi validate_fields saat tombol Submit ditekan
window.bind("<Return>", lambda event: submit_form() if validate_fields() else None)

# Menjalankan main loop aplikasi
window.mainloop()