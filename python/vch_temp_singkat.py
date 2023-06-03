from mimetypes import MimeTypes
import os
from pdb import run
import pydrive2
from Google import Create_Service
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.oauth2 import service_account

CLIENT_SECRET_FILE = ("credentials.json")
SCOPES = ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"]

# Layanan API
service_drive = Create_Service(CLIENT_SECRET_FILE, "drive", "v3", "https://www.googleapis.com/auth/drive")
service_doc = Create_Service(CLIENT_SECRET_FILE, "docs", "v1", ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/documents"])


def vch_txt(pdf_path: str, txt_path: str):
    try:
        # Membuat metadata file PDF
        file_metadata = {
            "name": os.path.basename(pdf_path),
            "parents": ["13-DRLgEBsHh5BEX2OQtq53wqdErut8YA"],
            "mimeType": "application/pdf",
        }

        # Unggah file PDF ke Google Drive
        media = MediaFileUpload(pdf_path, mimetype="application/pdf")
        pdf_file = (
            service_drive.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        pdf_file_id = pdf_file.get("id")

        # Membuat metadata file Google Docs
        gdoc_metadata = {
            "name": os.path.splitext(os.path.basename(pdf_path))[0],
            "mimeType": "application/vnd.google-apps.document",
            "parents": ["13-DRLgEBsHh5BEX2OQtq53wqdErut8YA"],
        }

        # Mengonversi file PDF menjadi Google Docs
        gdoc_file = (
            service_drive.files().copy(fileId=pdf_file_id, body=gdoc_metadata).execute()
        )
        gdoc_file_id = gdoc_file.get("id")

        # Unduh GDoc sebagai file teks
        txt_data = service_drive.files().export_media(fileId=gdoc_file_id, mimeType='text/plain').execute()

        with open(os.path.join(txt_path), 'wb') as f:
            f.write(txt_data)

        # Baca file teks
        with open(txt_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()

        # Saring data
        filtered_lines = []
        for line in lines:
            numbers = ''.join(filter(str.isdigit, line))
            if len(numbers) == 17:
                filtered_lines.append(numbers)

        # Simpan data yang telah difilter ke dalam file sementara
        temp_path = txt_path + ".temp"
        with open(temp_path, 'w', encoding='utf-8') as file:
            for line in filtered_lines:
                file.write(line + '\n')

        # Ganti file asli dengan file yang telah difilter
        os.remove(txt_path)
        os.rename(temp_path, txt_path)
        
        # Create the template using the filtered data
        template = "{}#{}#{}#{}#{}".format(
            "kodeproduk",
            "namavoucher",
            "#".join(filtered_lines),
            "harga",
            datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )

        # Save the template to a file
        with open("template.txt", "w", encoding="utf-8") as file:
            file.write(template)

        return gdoc_file_id

    except Exception as e:
        print("Terjadi kesalahan saat mengonversi PDF menjadi GDoc dan menyaring teks:", str(e))
        return None


# Konversi PDF menjadi GDoc dan saring teks
vch_txt()
