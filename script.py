import requests
import json
from pathlib import Path
from constants import ALLOWED_EXTENSIONS, HTTP
from pprint import pprint

# Директория для хранения полученных ответов от сервера
RSESPONSES_DIR = Path.cwd()/"responses" 
RSESPONSES_DIR.mkdir(exist_ok=True)

# Имена файлов, в которые будут сохраняться ответы
FILE_NAME = 'response.json'
SERCH_FILE_NAME = 'search.txt'


while True:
    input_comand = input(
        'Нажмите Enter, чтобы увидеть все файл.\
        \nВедите тип файла, чтобы получит список всех загруженных файлов такого типа.\
        \nЕсли нужно загрузить файл, то введите up.\
        \nЧтобы удалить файл введите команду del.\
        \nЧто бы найти файл введите команду src.\
        \nКоманда: '
        )
    
    # Запрос всех доступных файлов
    if  input_comand == '':    
        response = requests.get(f'{HTTP}files/get/list').json()
        with open(RSESPONSES_DIR / FILE_NAME, 'w') as file:
                json.dump(response, file, indent=4, ensure_ascii=False)  

        print(f'Ответ сервера: ')
        pprint(response, width=10)
        print(f'Список файлов сохранен в {RSESPONSES_DIR}/{FILE_NAME}\n')
    
    # Если запрос на список файлов c конеретным расширением
    elif input_comand in ALLOWED_EXTENSIONS:
        # В запросе передаемрасширение файла
        response = requests.get(f'{HTTP}files/get/{input_comand}').json()
        with open(RSESPONSES_DIR / FILE_NAME, 'w') as file:
                json.dump(response, file, indent=4, ensure_ascii=False)  

        print(f'Ответ сервера: ')
        pprint(response, width=10)
        print(f'Список файлов сохранен в {RSESPONSES_DIR}/{FILE_NAME}\n')

    # Загрузить файл
    elif input_comand.lower() == 'up':

        file_input = input('Укажите путь к файлу: ')        
        #открываем файл
        try:
            with open(file_input, 'r') as file:
                # помещаем объект файла в словарь в качестве значения с ключом 'file'
                files = {
                     'file': file
                     }
                # передаем созданный словарь аргументу `files`
                response = requests.post(f'{HTTP}files/create', files=files)
                print(f'{response.text}\n')
        except :
             print("Файл не найден.\n")

    # Удалить файл
    elif input_comand.lower() == 'del':
        file_input = input('Введите имя файла, который хотите удалить: ')
        # В запросе передаем расширение и имя файла
        response = requests.post(f'{HTTP}files/delete/{file_input}')
        print(f'Ответ сервер: {response.text}\n')

    # Поиск файла
    elif input_comand.lower() == 'src':
        file_input = input('Введите имя файла, который хотите найти: ')
        file_name = file_input.rsplit(".")[0]
        extantion = file_input.rsplit(".")[1]
        response = requests.get(f'{HTTP}files/get/{extantion}/{file_name}')
        with open(f'{RSESPONSES_DIR}/{SERCH_FILE_NAME}', 'w') as file:
            file.write(response.text)
        
        print(f'Ответ сервера: {response.text}')
        print(f'Ответ сохранен в файле: {RSESPONSES_DIR}/{SERCH_FILE_NAME}\n')

    else:
         print('Неизвестная команда.\n')