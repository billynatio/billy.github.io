from mimetypes import MimeTypes
import os
from pdb import run
import pydrive2
from Google import Create_Service
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

CLIENT_SECRET_FILE = ("credentials.json")
SCOPES = ["https://www.googleapis.com/auth/drive",
          "https://www.googleapis.com/auth/documents",]

# service api
service_drive = Create_Service(CLIENT_SECRET_FILE, "drive", "v3", "https://www.googleapis.com/auth/drive")
service_doc = Create_Service(CLIENT_SECRET_FILE,"docs", "v1",["https://www.googleapis.com/auth/drive","https://www.googleapis.com/auth/documents"],)


def vch_txt(pdf_path: str, txt_path: str, nama_voucher, kode_voucher, harga, digipos, jumlah_voucher, waktu):
    print("-Sedang mendapatkan file txt")
    try:
        # Create PDF file metadata
        file_metadata = {
            "name": os.path.basename(pdf_path),
            "parents": ["13-DRLgEBsHh5BEX2OQtq53wqdErut8YA"],
            "mimeType": "application/pdf"
        }

        # Upload PDF file to Google Drive
        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        pdf_file = service_drive.files().create(body=file_metadata, media_body=media, fields="id").execute()
        pdf_file_id = pdf_file.get("id")

        # Create Google Docs file metadata
        gdoc_metadata = {
            "name": os.path.splitext(os.path.basename(pdf_path))[0],
            "mimeType": "application/vnd.google-apps.document",
            "parents": ["13-DRLgEBsHh5BEX2OQtq53wqdErut8YA"]
        }

        # Convert PDF file to Google Docs
        gdoc_file = service_drive.files().copy(fileId=pdf_file_id, body=gdoc_metadata).execute()
        gdoc_file_id = gdoc_file.get("id")

        # Export GDoc as plain text file
        txt_data = service_drive.files().export_media(fileId=gdoc_file_id, mimeType="text/plain").execute()

        with open(os.path.join(txt_path), "wb") as f:
            f.write(txt_data)

        # Read the text file
        with open(txt_path, "r", encoding="utf-8") as file:
            lines = file.readlines()

        # Filter data
        filtered_lines = []
        for line in lines:
            numbers = "".join(filter(str.isdigit, line))
            if len(numbers) == 17:
                filtered_lines.append(numbers)
            
        
        # Format data
        print("- Memasukkan format data!")
        formatted_lines = []
        for line in filtered_lines:
            formatted_line = "{}#{}#{}#{}#{}\n".format(
                kode_voucher, nama_voucher, line, harga, waktu)
            formatted_lines.append(formatted_line)

        # Write formatted lines to temporary file
        temp_path = txt_path + ".temp"
        with open(temp_path, 'w', encoding='utf-8') as file:
            for formatted_line in formatted_lines:
                file.write(formatted_line)

        # Replace the original file with the filtered file
        os.remove(txt_path)
        os.rename(temp_path, txt_path)
        print("- Proses selesai!")


    except Exception as e:
        print("Terjadi kesalahan saat mengonversi PDF menjadi GDoc dan menyaring teks:", str(e))


