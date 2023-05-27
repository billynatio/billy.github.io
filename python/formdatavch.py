import tkinter as tk
from tkinter import messagebox
from datetime import datetime

def submit_form():
    # Mendapatkan nilai input dari field
    nama_voucher = entry_nama_voucher.get()
    kode_voucher = entry_kode_voucher.get()
    harga = entry_harga.get()
    digipos = entry_digipos.get()
    user = entry_user.get()
    jumlah_voucher = entry_jumlah_voucher.get()
    
    # Validasi input tidak kosong
    if not nama_voucher or not kode_voucher or not harga or not digipos or not user or not jumlah_voucher:
        messagebox.showerror("Error", "Semua field harus diisi!")
        return

    # Validasi input harga dan jumlah voucher
    if not harga.isdigit() or not jumlah_voucher.isdigit():
        messagebox.showerror("Error", "Harga dan Jumlah Voucher harus berisi angka!")
        return

    # Konversi harga dan jumlah voucher ke tipe data integer
    harga = int(harga)
    jumlah_voucher = int(jumlah_voucher)

    # Menampilkan nilai input
    print("Nama Voucher:", nama_voucher)
    print("Kode Voucher:", kode_voucher)
    print("Harga:", harga)
    print("Digipos:", digipos)
    print("User:", user)
    print("Jumlah Voucher:", jumlah_voucher)

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
    else:
        return

def validate_numeric_input(event):
    # Mendapatkan karakter yang diinputkan
    char = event.char

    # Memeriksa apakah karakter adalah angka atau backspace
    if not char.isdigit() and char != '\b':
        return "break"  # Membatalkan input karakter

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
button_simpan = tk.Button(window, text="Simpan", command=submit_form)
button_simpan.grid(row=6, column=0, sticky="W")

# Menjalankan event loop Tkinter
window.mainloop()
