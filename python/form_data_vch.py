import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from pyinsane2 import Scanner
from pyPDF2 import PdfWriter


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

        messagebox.showinfo("Konfirmasi", "Data berhasil disimpan!")

        # # Menjalankan pemindaian
        # scanner = Scanner()
        # devices = scanner.scan_devices()
        # if len(devices) > 0:
        #     device = devices[0]
        #     with device:
        #         image = device.scan()
        #         filename = f"{nama_voucher}_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        #         save_path = os.path.join("C:\\Users\\Asus\\Desktop\\voucher_yang_discan", filename)
        #         image.save(save_path, 'PDF')
        #         print("File berhasil disimpan:", save_path)
        # else:
        #     print("Tidak ada pemindai yang ditemukan.")
    else:
        return


def validate_numeric_input(event):
    # Mendapatkan karakter yang diinputkan
    char = event.char

    # Memeriksa apakah karakter adalah angka atau backspace
    if not char.isdigit() and char != '\b':
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
button_simpan = tk.Button(window, text="Simpan", command=lambda: validate_fields() and submit_form())
button_simpan.grid(row=6, column=0, sticky="W")

# Menjalankan event loop Tkinter
window.mainloop()
