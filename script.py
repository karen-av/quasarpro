import requests
import json
from pathlib import Path
from functions import requests_get_function
from constants import ALLOWED_EXTENSIONS


# Директория для хранения полученных json файлов
DATA_DIR = Path.cwd()/"responses" 
DATA_DIR.mkdir(exist_ok=True)
FILE_NAME = 'response.json'


while True:
    input_comand = input(
        'Нажмите Enter, чтобы увидеть все файл или введите тип файла,\
        \nчтобы получит список всех загруженных файлов такого типа.\
        \nЕсли нужно загрузить файл, то введите D: '
        )
    
    # Если запрос на список файлов
    if input_comand in ALLOWED_EXTENSIONS or input_comand == '':
        params = {
         'extantion': input_comand
         }

        # GET запрос
        response = requests_get_function(params)
        with open(DATA_DIR / FILE_NAME, 'w') as file:
                json.dump(response, file, indent=4, ensure_ascii=False)  

        print(response)
        print(f'Список файлов сохранен в {DATA_DIR}/{FILE_NAME}\n')

    elif input_comand.upper() == 'D':

        file_input = input('Укажите путь к файлу: ')        
        #открываем файл
        try:
            with open(file_input, 'r') as file:
                # помещаем объект файла в словарь 
                # в качестве значения с ключом 'file'
                files = {'file': file}
                # передаем созданный словарь аргументу `files`
                response = requests.post('http://127.0.0.1:5000//files/create', files=files)
                print(f'{response.text}\n')
        except Exception as _ex:
             print(f'[INFO] Exeptions while worcing with open:', _ex)


    



    
