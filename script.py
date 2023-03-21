import requests
import json
from pathlib import Path
from functions import requests_get_function


# Директория для хранения полученных json файлов
DATA_DIR = Path.cwd()/"responses_files" 
DATA_DIR.mkdir(exist_ok=True)
FILE_NAME = 'response.json'


while True:
    input_comand = input('Нажмите Enter, чтобы увидеть все файл или введите тип файла: ')
    params = {
         'extantion': 'all'
         }
    
    if len(input_comand) != 0:
        params['extantion'] = input_comand

    # GET запрос
    response = requests_get_function(params)
    with open(DATA_DIR / FILE_NAME, 'w') as file:
            json.dump(response, file, indent=4, ensure_ascii=False)  
    
    print(response)
    print(f'Список файлов сохранен в {DATA_DIR}/{FILE_NAME}')



    
