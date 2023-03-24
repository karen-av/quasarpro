import requests
import json
from pathlib import Path
from constants import ALLOWED_EXTENSIONS, HTTP
from pprint import pprint
import sys
import tkinter
from tkinter.filedialog import askopenfilename

# Директория для хранения полученных ответов от сервера
RSESPONSES_DIR = Path.cwd()/"responses" 
RSESPONSES_DIR.mkdir(exist_ok=True)

# Имена файлов, в которые будут сохраняться списки файло с сервера
FILE_NAME = 'response.json'

# Обработка полученных от пользователя команд
def comands_handler(input_comand):
     # Запрос имен всех файлов, сохраненных на сервере
    if  input_comand == 'list':    
        # get запрос
        response = requests.get(f'{HTTP}files/get/list').json()
        # Сохраняем результат в json
        with open(RSESPONSES_DIR / FILE_NAME, 'w') as file:
            json.dump(response, file, indent=4, ensure_ascii=False)  
        
        pprint(response, width=10)
        print(f'Cохранено в {FILE_NAME}')
    
    # Если запрос на список файлов c конеретным расширением
    elif input_comand in ALLOWED_EXTENSIONS:
        # В get запросе передаем расширение файла
        response = requests.get(f'{HTTP}files/get/{input_comand}').json()
        # Сохраняем результат в json
        with open(RSESPONSES_DIR / FILE_NAME, 'w') as file:
            json.dump(response, file, indent=4, ensure_ascii=False) 

        pprint(response, width=10)
        print(f'Cохранено в {FILE_NAME}')

    # Создать файл на серверен файл
    elif input_comand == 'create':
       # Принмаем файл у пользователя через диалоговое окно 
        # https://docs.python.org/3/library/tkinter.html#a-hello-world-program
        widget = tkinter.Tk()    
        widget.withdraw()
        filename = askopenfilename()
        
        # Проверяем выбрал ли пользователь файл
        if not filename:
            print('Файл не выбран.')
            exit()

        # Метаданные
        headers = {'key_1': 'value_1'}

         #открываем принятый файл
        with open(filename, 'rb') as file:
            # Помещаем объект файла в словарь в качестве значения с ключом 'file'
            files = {'file': file}

            # Передаем созданные словарь с файлом через post запрос
            response = requests.post(f'{HTTP}files/create/', files=files, headers=headers)
            print(response.text)
       
    # Удалить файл
    elif input_comand == 'delete':
        # Принимаем имя файла
        file_input = input('Имя файла: ')

        # В delete запросе передаем имя файла
        response = requests.delete(f'{HTTP}files/delete/{file_input}')

        print(response.text)
    
    # Найти файл
    elif input_comand.lower() == 'search':
        # Принимаем имя файла
        file_input = input('Имя файла: ')

        # Разделяем имя файла и расширение
        extantion = '.' in file_input and \
            file_input.rsplit('.', 1)[1].lower()
        filename_without_extantion = '.' in file_input and \
        file_input.rsplit('.', 1)[0].lower()

        # Если нет имени файла или расширения
        if not extantion or not filename_without_extantion:
            print('Файл не найден.')
            return True
            
        # get запрос на поиск файла
        response = requests.get(
            f'{HTTP}/files/get/{extantion}/{filename_without_extantion}'
            )
        
        # Если сервер вернул файл, сохраняем его 
        if response.status_code == 200:
            with open(f'{RSESPONSES_DIR}/{file_input}', 'wb') as file:
                file.write(response.content)
                print('Файл найден и сохранен.')
        # Если сервер не вернул файл, возвращаем сообщение об ошибке от сервера 
        else:
            print(response.text)
            
    # Прочие случаи
    else:
        print('Неизвестная команда.')

def main():
    # Два аргумента командной строки
    if len(sys.argv) == 2:
        comands_handler(sys.argv[1].lower())

    # Один аргумент командной строки
    elif len(sys.argv) == 1:
            while True:
                # Принимаем команду
                input_comand = input(\
                    '\nlist - Вернуть список всеx загруженных файлов в формате JSON.\
                    \n{extantion} - Вернуть список всех файлов указанного расширения.\
                    \ncreate - Загрузить файл на сервер.\
                    \nsearch - Получить файл с сервера.\
                    \ndelete - Удалить с сервера файл exemple.txt\
                    \nВведите команду: ')
                
                # Передаем input функции управления командами
                comands_handler(input_comand.lower())

    # Более двух аргументов командной строки
    else:
        print('Слишком много аргументов.')

if __name__ == ("__main__"):
    main()