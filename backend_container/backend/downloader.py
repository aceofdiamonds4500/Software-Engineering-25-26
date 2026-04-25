import os
import requests
import zipfile
import io
from pathlib import Path

#New Downloader For The Model
def download_model():

    script_dir = Path(__file__).resolve().parent
    target_dir = script_dir
    final_path = target_dir / "best"

    if os.path.exists("/app/backend/best"):
        print(f"Folder already exists at {final_path}")
        return

    if not os.access(target_dir, os.W_OK):
        print(f"ERROR: No write permission for {target_dir}")
        return

    print("Downloading model...")
    response = requests.get("https://downloads.dragonslair.cc/best.zip")

    if response.status_code == 200:
        print("Download Completed...")

        with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
            zip_ref.extractall(target_dir)
            print(f"Successfully extracted to {final_path}")

    else:
        print(f"Failed to download. HTTP Status Code: {response.status_code}")

def main():
    download_model()

main()