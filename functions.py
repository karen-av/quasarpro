import json
import requests
from pathlib import Path
from constants import ALLOWED_EXTENSIONS, HTTP


# Запрос get к серверу 
def requests_get_function(params):
    return requests.get(f'{HTTP}files/get', params = params).json()


# Список всех сохраненных файлов
# https://docs.python.org/3/library/pathlib.html#Path.rglob
def get_list_files(DATA_DIR):
    return [x.name for x in Path(DATA_DIR).iterdir()]
       

# Проверяем расширение файла при загрузке
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS