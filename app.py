from flask import Flask, redirect, render_template, flash, request
from config import Config
from pathlib import Path
import requests
from werkzeug.utils import secure_filename
import os
from functions import get_list_files, allowed_file
from constants import ALLOWED_EXTENSIONS

app = Flask(__name__)
app.config.from_object(Config)

# Директория для сохранения загруженных файлов
DATA_DIR = Path.cwd()/"uploads" 
DATA_DIR.mkdir(exist_ok=True)


# Главная
@app.route('/')
def index():
    return render_template('index.html')


# Список всех загруженных файлов
@app.route('/files/get/', methods=['GET'])
def files():
    # Список для сохранения названий файлов
    files_list = []
    
    # тип файла из get запроса
    query = request.args.get('extantion')
    
    # Функция вернет список всех загруженных файлов
    files_list = get_list_files(DATA_DIR)
    
    # Если есть запрос на конкретное расширение файла 
    if query != '':
        files_list_filter = []
        for file in files_list: 
            # Получаем расширение файла через поиск индекса последнего входжения элемента и среза
            ext = file[file.rfind('.') + 1:]
            if ext == query:
                # Удалаяем файл с несоответсвующим расшинеринием
                files_list_filter.append(file)
            # Возвращаем словарь
            return {'files': files_list_filter}

    # Возвращаем словарь
    return {'files': files_list}


# Принимаем файл 
@app.route('/files/create/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        #Принимаем файл из запроса
        file = request.files['file']

        # Если файл не загружен
        if file.filename == '':
            return 'No selected file'
        
        # Безопасное сохраниение имени файла
        filename = secure_filename(file.filename)

        #Проверяем допустимо ли расширение загружаемого файла и проверяем на наличие дубликатов
        if allowed_file(filename) and filename not in get_list_files(DATA_DIR):
            # Сохранение файла в директорию
            file.save(os.path.join(DATA_DIR, filename))
            return 'Файл успешно загружен и сохранен!'

        return "Недопустимый формат файла или файл c таким именем загружен"


if __name__ == ('__main__'):
    app.run(debug=True, host='0.0.0.0', port=5000)

