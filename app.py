from flask import Flask, redirect, render_template, flash
from config import Config
from pathlib import Path
import requests

app = Flask(__name__)
app.config.from_object(Config)

DATA_DIR = Path.cwd()/"files" 
DATA_DIR.mkdir(exist_ok=True)

# Для отображени в виде HTML установить True
# Для работы scriot.py установите False
WEB_SITE_MODE = False


# Главная
@app.route('/')
def index():
    return render_template('index.html')


# Список всех загруженных файлов
@app.route('/files/get/list')
def files():
    files_list = []
    # https://docs.python.org/3/library/pathlib.html#Path.rglob
    for x in Path(DATA_DIR).iterdir(): 
        files_list.append(x.name)
    dict_files = {}
    dict_files['files'] = files_list
    if WEB_SITE_MODE:
        return render_template('index.html', files_list=files_list)
    return dict_files


if __name__ == ('__main__'):
    app.run(debug=True, host='0.0.0.0', port=5000)

