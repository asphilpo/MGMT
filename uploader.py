import os
import requests
import json


#SERVER STUFF
SERVER_URL = ""
AUTH_TOKEN = ""
#-------------------------------------


with open('secrets.json', 'r') as json_file:
    data = json.load(json_file)

REPORTS_DIR = data['REPORTS_DIR']
THUMB_DEPOT = data['THUMB_DEPOT_LOCAL']




def upload_directory(directory_path, filetype):
    if filetype not in ("image", "report"):
        raise ValueError("Invalid filetype. Must be 'image' or 'report'.")

    headers = {'Authorization': f'Bearer {AUTH_TOKEN}'}
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            try:
                with open(file_path, 'rb') as f:
                    files = {'file': f}
                    response = requests.post(SERVER_URL + filetype, files=files, headers=headers)
                    print(f"{filename}: {response.status_code} - {response.json()}")
            except Exception as e:
                print(f"Error uploading {filename}: {e}")




upload_directory(THUMB_DEPOT, "image")
upload_directory(REPORTS_DIR, "report")






