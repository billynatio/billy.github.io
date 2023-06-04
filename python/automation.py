from pywinauto import Application, Desktop, keyboard
import time
import os
from vch_temp_singkat import vch_txt
import pywinauto.findwindows as findwindows

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

         # Pilih radio button "Others" dalam dialog "File Save Settings"
        radio_others = window_save_settings.child_window(auto_id="1186", control_type="RadioButton")
        radio_others.set_focus()
        radio_others.click_input()

        # Tunggu hingga dialog "Browse For Folder" muncul
        button_browse = window_save_settings.child_window(auto_id="1002", control_type="Button")
        button_browse.click()
        window_browse_folder = window_epson.window(title="Browse For Folder")
        window_browse_folder.wait("exists", timeout=10)
        
        # Cari dialog "Browse For Folder" berdasarkan teks judulnya
        dlg_browse = findwindows.find_windows(title="Browse For Folder")[0]
        dlg_browse = app_epson.window(handle=dlg_browse)

        # Klik tree item "This PC"
        this_pc_item = dlg_browse.child_window(control_type="TreeItem", depth=1)
        this_pc_item.click_input()

        # Klik tree item "Desktop"
        desktop_item = this_pc_item.child_window(title="Desktop", control_type="TreeItem")
        desktop_item.click_input()

        # Klik tree item "voucher_scan"
        voucher_scan_item = desktop_item.child_window(title="voucher_scan", control_type="TreeItem")
        voucher_scan_item.click_input()

        # Klik tree item "automation"
        automation_item = voucher_scan_item.child_window(title="automation", control_type="TreeItem")
        automation_item.click_input()

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
            print("-Mengubah nama file")
            # Jalankan fungsi vch_txt untuk mengonversi PDF menjadi Google Docs dan menyaring teks
            vch_txt(pdf_path, txt_path, nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu)  # Replace 'txt_path' with the desired output text path
            return pdf_path
        else:
            return None

    except Exception as e:
        print("Kesalahan saat menjalankan Epson Scan:", str(e))
        return None