from mimetypes import MimeTypes
import os
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

# lokasi hasil scan voucher
pdf_path = r"C:\Users\Asus\Downloads\img251.pdf"
# lokasi export txt file
txt_path = r"C:\Users\Asus\Downloads\img251.txt"
# Lokasi txt file sudah difilter
filtered_text_path = r"C:\Users\Asus\Downloads\img251.pdf"

# Fungsi untuk mengonversi file PDF menjadi Google Docs (GDoc)
def convert_pdf_to_txt(pdf_path: str, parents: list = None):
    # Membuat metadata file PDF
    file_metadata = {
        "name": os.path.basename(pdf_path),
        "parents": ["13-DRLgEBsHh5BEX2OQtq53wqdErut8YA"],
        "mimeType": "application/pdf",
    }

    # Upload file PDF ke Google Drive
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
    
    # download gdoc menjadi txt
    txt_data=service_drive.files().export_media(
        fileId=gdoc_file_id, 
        mimeType= 'text/plain').execute()
    
    
    with open(os.path.join(txt_path), 'wb') as f:
        f.write(txt_data)
        f.close()
    return gdoc_file_id


def filter_text(txt_path: str):
    # Membaca file teks
    with open(txt_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Memfilter data
    filtered_lines = []
    for line in lines:
        numbers = ''.join(filter(str.isdigit, line))
        if len(numbers) == 17:
            filtered_lines.append(numbers)

    # Menyimpan data yang telah difilter ke dalam file sementara
    temp_path = txt_path + ".temp"
    with open(temp_path, 'w', encoding='utf-8') as file:
        for line in filtered_lines:
            file.write(line + '\n')

    # Mengganti file asli dengan file yang telah difilter
    os.remove(txt_path)
    os.rename(temp_path, txt_path)

# Konversi PDF menjadi GDoc
convert_pdf_to_txt(pdf_path, txt_path)
# filter file txt
filter_text(txt_path)
