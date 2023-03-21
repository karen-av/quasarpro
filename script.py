import requests
import json
from pathlib import Path

# Путить к директории для хранения полученных json файлов
DATA_DIR = Path.cwd()/"responses" 
DATA_DIR.mkdir(exist_ok=True)
FILE_NAME = 'response.json'


response = requests.get('http://127.0.0.1:5000/files/get/list').json()
with open(DATA_DIR / FILE_NAME, 'w') as file:
        json.dump(response, file, indent=4, ensure_ascii=False)  
print(response)