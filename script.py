import requests
import json
from pathlib import Path
from functions import requests_get_function
from constants import ALLOWED_EXTENSIONS, HTTP


# Директория для хранения полученных json файлов
RSESPONSES_DIR = Path.cwd()/"responses" 
RSESPONSES_DIR.mkdir(exist_ok=True)
FILE_NAME = 'response.json'


while True:
    input_comand = input(
        'Нажмите Enter, чтобы увидеть все файл.\
        \nВедите тип файла, чтобы получит список всех загруженных файлов такого типа.\
        \nЕсли нужно загрузить файл, то введите up.\
        \nЧтобы удалить файл введите команду del.\
        \nЧто бы найти файл введите команду ser.\
        \nКоманда: '
        )
    
    # Если запрос на список файлов
    if input_comand in ALLOWED_EXTENSIONS or input_comand == '':
        params = {
         'extantion': input_comand
         }

        # GET запрос
        response = requests_get_function(params)
        with open(RSESPONSES_DIR / FILE_NAME, 'w') as file:
                json.dump(response, file, indent=4, ensure_ascii=False)  

        print(f'Ответ сервера: {response}')
        print(f'Список файлов сохранен в {RSESPONSES_DIR}/{FILE_NAME}\n')

    # Загрузить файл
    elif input_comand.lower() == 'up':

        file_input = input('Укажите путь к файлу: ')        
        #открываем файл
        try:
            with open(file_input, 'r') as file:
                # помещаем объект файла в словарь 
                # в качестве значения с ключом 'file'
                files = {'file': file}
                # передаем созданный словарь аргументу `files`
                response = requests.post(f'{HTTP}files/create', files=files)
                print(f'{response.text}\n')
        except Exception as _ex:
             print(f'[INFO] Exeptions while worcing with open:', _ex)

    # Удалить файл
    elif input_comand.lower() == 'del':
        file_input = input('Введите имя файла, который хотите удалить: ')
        data = {
         'filename': file_input
         }
        response = requests.post(f'{HTTP}files/delete/', data=data)
        print(f'Ответ сервер: {response.text}\n')


    elif input_comand.lower() == 'ser':
        file_input = input('Введите имя файла, который хотите найти: ')
        params = {
         'q': file_input
         }
        response = requests.get(f'{HTTP}files/get/search', params=params)
        print(f'Ответ сервера: \n{response.text}\n')
