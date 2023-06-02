import os
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from pywinauto import Application, Desktop
import time

vch_folder_path = r"C:\Users\cahayabaru\Desktop\voucher scan\automation"

def run_epson_scan(kode_voucher, waktu_sekarang):
    try:
        # Mulai aplikasi Epson Scan
        app_epson = Application(backend="uia").start(r"C:\Windows\twain_32\escndv\escndv.exe")

        # Tunggu hingga jendela Epson Scan muncul
        window_epson = app_epson.window(title="EPSON Scan")
        window_epson.wait("exists", timeout=10)

        # Sembunyikan jendela Epson Scan
        window_epson.set_visible(False)
        print("Epson sudah dibuka")

        # Klik tombol "Customize"
        button_customize = window_epson.child_window(title="Customize...", control_type="Button")
        button_customize.click()
        print("Customize sudah dibuka")

        # Tunggu hingga dialog "Customize" muncul
        window_customize = window_epson.window(title="Customize")
        window_customize.wait("exists", timeout=10)

        # Klik tombol "File Save Settings" dalam dialog "Customize"
        button_file_save_settings = window_customize.child_window(auto_id="1080", control_type="Button")
        button_file_save_settings.click()

        # Tunggu hingga dialog "Save Settings" muncul
        window_save_settings = window_epson.window(title="File Save Settings")
        window_save_settings.wait("exists", timeout=10)

        # Tetapkan nama awalan sebagai kode voucher dan waktu saat ini
        prefix_name = kode_voucher + " " + waktu_sekarang.strftime("%d_%m_%Y %H-%M") + " "
        edit_prefix = window_save_settings.child_window(auto_id="1202", control_type="Edit")
        edit_prefix.set_text(prefix_name)

        # Tetapkan nomor awal sebagai "888"
        edit_start_number = window_save_settings.child_window(title="Start Number:", control_type="Edit")
        edit_start_number.set_text("888")

        # Dapatkan nama file
        file_path = os.path.join(vch_folder_path, prefix_name + "888.pdf")

        # Klik tombol "OK" dalam dialog "Save Settings"
        button_ok_save_settings = window_save_settings.child_window(title="OK", control_type="Button")
        button_ok_save_settings.click()

        # Klik tombol "OK" dalam dialog "Customize"
        button_ok_customize = window_customize.child_window(title="OK", control_type="Button")
        button_ok_customize.click()

        # Klik tombol "Scan" dalam jendela Epson Scan
        button_scan = window_epson.child_window(title="Scan", control_type="Button")
        button_scan.click()

        # Tunggu hingga pemindaian selesai
        window_epson.wait_not("exists", timeout=60)

        # Periksa apakah file yang dipindai ada
        if os.path.exists(file_path):
            # Ubah nama path file tanpa "888" dan dengan ekstensi ".pdf"
            vch_path = file_path.replace(" 888", ".pdf")
            os.rename(file_path, vch_path)
            return vch_path
        else:
            return None

    except Exception as e:
        print("Kesalahan saat menjalankan Epson Scan:", str(e))
        return None

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

        # Panggil fungsi run_epson_scan di latar belakang
        kode_voucher = entry_kode_voucher.get()
        waktu_sekarang = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        run_epson_scan(kode_voucher, waktu_sekarang)
        time.sleep(2)  # Tunggu sebentar agar Epson Scan dapat dijalankan

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
label_nama_voucher.grid(row=0, column=0, padx=10, pady=5)
entry_nama_voucher = tk.Entry(window)
entry_nama_voucher.grid(row=0, column=1, padx=10, pady=5)

# Membuat label dan field untuk Kode Voucher
label_kode_voucher = tk.Label(window, text="Kode Voucher:")
label_kode_voucher.grid(row=1, column=0, padx=10, pady=5)
entry_kode_voucher = tk.Entry(window)
entry_kode_voucher.grid(row=1, column=1, padx=10, pady=5)

# Membuat label dan field untuk Harga
label_harga = tk.Label(window, text="Harga:")
label_harga.grid(row=2, column=0, padx=10, pady=5)
entry_harga = tk.Entry(window)
entry_harga.grid(row=2, column=1, padx=10, pady=5)

# Membuat label dan field untuk Digipos
label_digipos = tk.Label(window, text="Digipos:")
label_digipos.grid(row=3, column=0, padx=10, pady=5)
entry_digipos = tk.Entry(window)
entry_digipos.grid(row=3, column=1, padx=10, pady=5)

# Membuat label dan field untuk User
label_user = tk.Label(window, text="User:")
label_user.grid(row=4, column=0, padx=10, pady=5)
entry_user = tk.Entry(window)
entry_user.grid(row=4, column=1, padx=10, pady=5)

# Membuat label dan field untuk Jumlah Voucher
label_jumlah_voucher = tk.Label(window, text="Jumlah Voucher:")
label_jumlah_voucher.grid(row=5, column=0, padx=10, pady=5)
entry_jumlah_voucher = tk.Entry(window)
entry_jumlah_voucher.grid(row=5, column=1, padx=10, pady=5)

# Membuat tombol Submit
button_submit = tk.Button(window, text="Submit", command=submit_form)
button_submit.grid(row=6, column=0, columnspan=2, padx=10, pady=5)

# Menambahkan event handler untuk membatasi input karakter pada field harga dan jumlah voucher
entry_harga.bind("<KeyPress>", validate_numeric_input)
entry_jumlah_voucher.bind("<KeyPress>", validate_numeric_input)

# Menambahkan event handler untuk memvalidasi field sebelum submit
window.bind("<Return>", lambda event: validate_fields() and submit_form())

# Menjalankan event loop window Tkinter
window.mainloop()
