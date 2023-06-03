from pywinauto import Application, Desktop
import time
import os
from vch_temp_singkat import vch_txt

def run_epson_scan(nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu):
    vch_folder_path = r"C:\Users\cahayabaru\Desktop\voucher_scan\automation"
    try:
        # Mulai aplikasi Epson Scan
        app_epson = Application(backend="uia").start(r"C:\Windows\twain_32\escndv\escndv.exe")

        # Tunggu hingga jendela Epson Scan muncul
        window_epson = app_epson.window(title="EPSON Scan")
        window_epson.wait("exists", timeout=10)
        print("-Membuka epson scanner!")

        # Klik tombol "Customize"
        button_customize = window_epson.child_window(title="Customize...", control_type="Button")
        button_customize.click()

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
        prefix_name = kode_voucher + " " + waktu.replace(" ", "_").replace(":", "-") + " "
        edit_prefix = window_save_settings.child_window(auto_id="1202", control_type="Edit")
        edit_prefix.set_text(prefix_name)

        # Tetapkan nomor awal sebagai "888"
        edit_start_number = window_save_settings.child_window(title="Start Number:", control_type="Edit")
        edit_start_number.set_text("888")

        # Klik tombol "OK" dalam dialog "Save Settings"
        button_ok_save_settings = window_save_settings.child_window(title="OK", control_type="Button")
        button_ok_save_settings.click()

        # Klik tombol "OK" dalam dialog "Customize"
        button_ok_customize = window_customize.child_window(title="OK", control_type="Button")
        button_ok_customize.click()

        # Klik tombol "Scan" dalam jendela Epson Scan
        button_scan = window_epson.child_window(title="Scan", control_type="Button")
        button_scan.click()
        print("-Proses scanning sedang berjalan")

        # Tunggu hingga pemindaian selesai
        window_epson.wait_not("exists", timeout=60)

        # Dapatkan nama file
        file_path = os.path.join(vch_folder_path, prefix_name + "888.pdf")
        # Buat nama file baru
        pdf_path = os.path.join(vch_folder_path, prefix_name + ".pdf")
        # Buat nama file teks dengan ekstensi .txt
        txt_path = os.path.splitext(pdf_path)[0] + ".txt"
        
        

        # Periksa apakah file yang dipindai ada
        if os.path.exists(file_path):
            # Ubah nama path file tanpa "888" dan dengan ekstensi ".pdf"
            os.rename(file_path, pdf_path)
            print("-Berhasil mengubah nama file")
            # Jalankan fungsi vch_txt untuk mengonversi PDF menjadi Google Docs dan menyaring teks
            vch_txt(pdf_path, txt_path, nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu)  # Replace 'txt_path' with the desired output text path
            return pdf_path
        else:
            return None

    except Exception as e:
        print("Kesalahan saat menjalankan Epson Scan:", str(e))
        return None