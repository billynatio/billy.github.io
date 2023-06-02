from pywinauto import Application, Desktop
import time

def run_epson_scan(kode_voucher, waktu_sekarang):
    # Start the Epson Scan application
    app_epson = Application(backend="uia").start(r"C:\Windows\twain_32\escndv\escndv.exe")

    # Wait for the Epson Scan window to appear
    window_epson = app_epson.window(title="EPSON Scan")
    window_epson.wait("exists", timeout=10)  # Adjust the timeout as needed

    # Hide the Epson Scan window
    window_epson.set_visible(False)

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
    prefix_name = kode_voucher + "_" + waktu_sekarang.replace(" ", "_").replace(":", "-") + "/"
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