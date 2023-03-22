"""https://pypi.org/project/pytest/"""
"""https://pytest-docs-ru.readthedocs.io/ru/latest/getting-started.html#installation"""

from functions import get_list_files, allowed_file
from app import UPLOAD_FOLDER
from constants import ALLOWED_EXTENSIONS, HTTP
import requests



class TestClass:

    # Функция должна возвращать сисок
    def test_get_list_files(self):
        assert type(get_list_files(UPLOAD_FOLDER)) == type(list())

    
    # Расширение файла должно быть из списка разрешенных
    def test_allowed_file(self):
        for extensions in ALLOWED_EXTENSIONS:
            assert allowed_file('.' + extensions) == True


    # Проверка пути /
    def test_route_index(self):
        response = requests.get(HTTP)
        assert response.status_code == 200

        # 405 Method Not Allowed
        response = requests.post(HTTP)
        assert response.status_code == 405


    # Проверка пути files/get/list
    def test_route_files_list(self):
        response = requests.get(f'{HTTP}files/get/list')
        assert response.status_code == 200

        # 405 Method Not Allowed
        response = requests.post(f'{HTTP}files/get/list')
        assert response.status_code == 405


    # Проверка пути /files/get/{extantion}
    def test_route_files(self):
        response = requests.get(f'{HTTP}files/get/txt')
        assert response.status_code == 200
        
        # 405 Method Not Allowed
        response = requests.post(f'{HTTP}files/get/txt')
        assert response.status_code == 405

         # Ожидаем получить dict
        response = requests.get(f'{HTTP}files/get/txt').json()
        assert type(response) == type({})
        
        # 404 Not Found 
        response = requests.post(f'{HTTP}files/get')
        assert response.status_code == 404

        # 404 Not Found 
        response = requests.get(f'{HTTP}files/get')
        assert response.status_code == 404
    

    # Проверка пути /files/create/
    def test_route_upload_file(self):
        files = {
                'file': ''
                }
        response = requests.post(f'{HTTP}files/create/', files=files)
        assert response.status_code == 200

        # 405 Method Not Allowed
        response = requests.get(f'{HTTP}files/create/')
        assert response.status_code == 405


    # Проверка пути files/delete 
    def test_route_delete(self):
        response = requests.post(f'{HTTP}files/delete/txt')
        assert response.status_code == 200

        # 404 Not Found 
        response = requests.post(f'{HTTP}files/delete/')
        assert response.status_code == 404

        # 404 Not Found 
        response = requests.get(f'{HTTP}files/delete/')
        assert response.status_code == 404

    
    # Проверка пути /files/get/search
    def test_route_search(self):
        response = requests.get(f'{HTTP}/files/get/txt/filename')
        assert response.status_code == 200

        # 405 Method Not Allowed
        response = requests.post(f'{HTTP}/files/get/txt/filename')
        assert response.status_code == 405


    