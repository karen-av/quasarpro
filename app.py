from flask import Flask, render_template, request, send_file, jsonify, send_from_directory
from config import Config
from pathlib import Path
from werkzeug.utils import secure_filename
from werkzeug.security import safe_join 
import os
from functions import get_list_files, allowed_file
from constants import ALLOWED_EXTENSIONS, PORT
import filecmp


app = Flask(__name__)
app.config.from_object(Config)

# Директория для сохранения загруженных файлов
UPLOAD_FOLDER = Path.cwd()/"uploads" 
UPLOAD_FOLDER.mkdir(exist_ok=True)


# Главная
@app.route('/')
def index():
    return render_template('index.html')


# Список всех доступных файлов
@app.route('/files/get/list', methods=['GET'])
def files_all():
    # Функция вернет список всех загруженных файлов
    files_list = get_list_files(UPLOAD_FOLDER)

    # Возвращаем json
    return jsonify({'files': files_list})


# Возвращает список файлов с указанным расширением
@app.route('/files/get/<extantion>')
def files_1(extantion):
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
        if ext == query:
            # Удалаяем файл с несоответсвующим расшинеринием
            files_list_filter.append(file)

    # Возвращаем json
    return jsonify({'files': files_list_filter})


# Принимает загрузку файла и сохраняет его на сервере, проверяя на наличие дубликатов.
@app.route('/files/create/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #Принимаем файл из запроса
        file = request.files['file']
        print(file)

        # Если файл не загружен
        if file.filename == '':
            return 'Нет файла'

        # Безопасное сохраниение имени файла
        filename = secure_filename(file.filename)

        # Список ранее загруженных файлов
        files_list = get_list_files(UPLOAD_FOLDER)

        # Проверяем на наличие дубликатов
        if filename in files_list:
            return "Файл с таким именем уже существует."
        
        #Проверяем допустимо ли расширение загружаемого файла
        if allowed_file(filename) is False:
            return "Недопустимый формат файла."

        # Сохранение файла в директорию
        file.save(os.path.join(UPLOAD_FOLDER, filename))

        # https://docs.python.org/3/library/filecmp.html
        # Сравнивает содержимое с существующими файлами 
        for file in files_list:
            # Безопасное соединение базовый каталог и имя файла
            if filecmp.cmp(safe_join(UPLOAD_FOLDER, file), safe_join(UPLOAD_FOLDER, filename), shallow=False):
                os.remove(safe_join(UPLOAD_FOLDER, filename))
                return (f"Файл с таким содержимым был загруже ранее. Имя файла {file}")
                
        return 'Файл успешно загружен и сохранен!'


# Удаляет указанный файл с сервера.
@app.route('/files/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if request.method == 'POST':

        # Если файл существует, то удаляем его
        if filename in get_list_files(UPLOAD_FOLDER):
            # Безопасное соединение базовый каталог и имя файла
            safe_path = safe_join(UPLOAD_FOLDER, filename)
            os.remove(safe_path)
            return "Файл удален."
        
        return 'Файл не найден.'


# Возвращает выбранный файл.
@app.route('/files/get/<extantion>/<file_name>', methods=['GET'])
def search(extantion, file_name):
    filename = file_name + '.' + extantion

    # Безопасное соединение базовый каталог и имя файла
    #https://werkzeug.palletsprojects.com/en/2.2.x/utils/#werkzeug.security.safe_join
    safe_path = safe_join(UPLOAD_FOLDER, filename)

    try:
        # https://flask.palletsprojects.com/en/2.2.x/api/
        return send_file(safe_path, as_attachment=True)
    except:
        return "Файл не найден."


if __name__ == ('__main__'):
    app.run(debug=True, host='0.0.0.0', port=PORT)

