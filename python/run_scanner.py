import pyinsane.abstract as pyinsane
from datetime import datetime

def scan_and_save(scanner_name, save_path):
    # Membuka perangkat scanner
    scanner = pyinsane.Scanner(device=scanner_name)

    # Memulai pemindaian
    scanner.scan()

    # Menyimpan hasil pemindaian ke file
    filename = f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    save_file_path = save_path + filename
    scanner.save(path=save_file_path)

    return save_file_path

def main():
    # Mendapatkan daftar perangkat scanner yang tersedia
    devices = pyinsane.get_devices()
    
    if not devices:
        print("Tidak ditemukan perangkat scanner.")
        return
    
    # Menampilkan daftar perangkat scanner yang tersedia
    print("Perangkat scanner yang tersedia:")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device}")

    # Memilih perangkat scanner
    selected_device = devices[0]  # Ganti dengan indeks perangkat scanner yang ingin Anda gunakan

    # Menentukan lokasi penyimpanan file hasil pemindaian
    save_path = "C:/Users/Asus/Desktop/voucher yang discan/"  # Ganti dengan lokasi penyimpanan yang diinginkan

    # Memulai pemindaian dan menyimpan hasil pemindaian ke file
    save_file_path = scan_and_save(selected_device, save_path)

    print("File berhasil disimpan:", save_file_path)

if __name__ == "__main__":
    main()
