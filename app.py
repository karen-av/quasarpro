from flask import Flask, redirect, render_template, flash, request
from config import Config
from pathlib import Path
import requests

app = Flask(__name__)
app.config.from_object(Config)

# Директория для сохранения загруженных файлов
DATA_DIR = Path.cwd()/"download_folder" 
DATA_DIR.mkdir(exist_ok=True)


# Главная
@app.route('/')
def index():
    return render_template('index.html')


# Список всех загруженных файлов
@app.route('/files/get', methods=['GET'])
def files():
    # Список для сохранения названий файлов
    files_list = []
    
    # тип файла из get запроса
    query = request.args.get('extantion')
    
    if query == 'all' or query == '':
        # https://docs.python.org/3/library/pathlib.html#Path.rglob
        for x in Path(DATA_DIR).iterdir(): 
            files_list.append(x.name)

    else:
        for x in Path(DATA_DIR).iterdir(): 
            # Получаем расширение файла через поиск индекса точки и среза
            if x.name[x.name.find(".") + 1:] == query:
                files_list.append(x.name)

    # Словарь для возарвта json
    
    return {'files': files_list}





if __name__ == ('__main__'):
    app.run(debug=True, host='0.0.0.0', port=5000)

