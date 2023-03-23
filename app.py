from flask import Flask, request, send_file, jsonify
from config import Config
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join 
import os
from functions import get_list_files, allowed_file
from constants import PORT
import filecmp


app = Flask(__name__)
app.config.from_object(Config)


# Директория для сохранения загруженных файлов
UPLOAD_FOLDER = Path.cwd()/"uploads" 
UPLOAD_FOLDER.mkdir(exist_ok=True)


# Список всех доступных файлов
@app.route('/files/get/list', methods=['GET'])
def files_all():
    # Функция вернет список всех загруженных файлов
    files_list = get_list_files(UPLOAD_FOLDER)

    # Возвращаем json
    return jsonify({'files': files_list})


# Возвращает список файлов с указанным расширением
@app.route('/files/get/<extantion>', methods=['GET'])
def files(extantion):
    # тип файла из get запроса
    query = extantion
    
    # Функция вернет список всех загруженных файлов
    files_list = get_list_files(UPLOAD_FOLDER)
    
    # Итоговый список
    files_list_filter = []

    # Ищем все файлы нужного расширения
    for file in files_list: 
        # Получаем расширение файла через поиск индекса последнего входжения элемента и среза
        ext = file[file.rfind('.') + 1:]
        # если расширение файла совпадает с запросом
        if ext == query:
            # Добавляем файл с несоответсвующим расшинеринием
            files_list_filter.append(file)

    # Возвращаем json
    return jsonify({'files': files_list_filter})


# Принимает загрузку файла и сохраняет его на сервере, проверяя на наличие 
# дубликатов.
@app.route('/files/create/', methods=['POST'])
def create():
    if request.method == 'POST':
        #Принимаем файл из запроса
        file = request.files['file']

        # Если файл не загружен
        if file.filename == '':
            return 'Сервер не получил файл для загрузки.'

        # Безопасное сохраниение имени файла
        filename = secure_filename(file.filename)

        # Список ранее загруженных файлов
        files_list = get_list_files(UPLOAD_FOLDER)

        # Проверяем на наличие дубликатов
        if filename in files_list:
            return "Файл с таким именем уже существует."
        
        # Проверяем допустимо ли расширение загружаемого файла
        if allowed_file(filename) is False:
            return "Недопустимый формат файла."

        # Сохранение файла в директорию
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # Сравнивает содержимое с существующими файлами 
        for file in files_list:
            # Безопасное соединение базовый каталог и имя файла и проверяем 
            # содержимое файлов на уникальность
            # https://docs.python.org/3/library/filecmp.html
            if filecmp.cmp(
                safe_join(UPLOAD_FOLDER, file), 
                safe_join(UPLOAD_FOLDER, filename), 
                shallow=False
                ):
                # Если находим файл с там же содержиым, то удаляем полученный файл
                os.remove(safe_join(UPLOAD_FOLDER, filename))
                return (f"Файл с таким содержимым был загружен ранее. \
                        Имя файла {file}")
                
        return 'Файл успешно загружен.'


# Удаляет указанный файл с сервера.
@app.route('/files/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    if request.method == 'DELETE':
        # Ицем имя полученного файла в списке всех файлов, который вернула функция
        if filename in get_list_files(UPLOAD_FOLDER):
            # Безопасное соединение базовый каталог и имя файла
            safe_path = safe_join(UPLOAD_FOLDER, filename)

            # Удаляем файл
            os.remove(safe_path)
            return "Файл удален."
        
        return 'Файл не найден.'


# Возвращает запрошенный файл.
@app.route('/files/get/<extantion>/<file_name>', methods=['GET'])
def search(extantion, file_name):
    # Получаем имя файла из полученного запроса
    filename = file_name + '.' + extantion

    # Безопасное сохраниение имени файла
    filename = secure_filename(filename)

    try:
        # Безопасное соединение базовый каталог и имя файла
        #https://werkzeug.palletsprojects.com/en/2.2.x/utils/#werkzeug.security.safe_join
        safe_path = safe_join(UPLOAD_FOLDER, filename)

        # Если файл есть, то вернем еге. Иначе вернем ошибку
        # https://flask.palletsprojects.com/en/2.2.x/api/
        return send_file(safe_path, as_attachment=True)
    
    except:
        return "Файл не найден.", 404
            

if __name__ == ('__main__'):
    app.run(debug=True, host='0.0.0.0', port=PORT)

