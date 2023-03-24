<p> <h3>Тестовое_задание_Python_(Juniour_Flask) (3)</h3>
Создайте виртуальное окружение и активируйте его.<br>
Установите все зависимости pip install -r requirements.txt<br>

<br>
Запустите сервер командой python3 app.py<br>
По умолчанию сервер будет прослушивать порт 5000.<br>
Изменить порт можно в файле constants.py.<br>
<br>
Сервер может обслужить следующие запросы:<br>
Вернуть список всеx загруженных файлов в формате JSON.<br>
    curl -X GET "http://localhost:5000/files/get/list" -o response.json<br>
    python3 script.py list<br>
<br>
Вернуть список всех файлов указанного расширения.<br>
    curl -X GET "http://localhost:5000/files/get/{extantion}" -o response.json<br>
    python3 script.py {extantion}<br>
<br>
Загрузить файл на сервер.<br>
    curl -X POST -H "key_1: value_1" -F 'file=@/path/to/example.txt' http://localhost:5000/files/create/<br>
    python3 script.py create<br>
<br>
Получить файл с сервера.<br>
    curl -OJ http://localhost:5000/files/get/txt/example<br>
    python3 script.py search<br>
<br>
Удалить файл с сервера.<br>
    curl -X DELETE http://localhost:5000/files/delete/example.txt<br>
    python3 script.py delete<br>
<br>
Или просто запустите скрипт и следуйте подсказкам.<br>
python3 script.py<br>
<br>
Пожалуйста, используйте в названиях файлов буквы латинского алфавита. <br>
</p>
