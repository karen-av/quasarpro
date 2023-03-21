"""https://pypi.org/project/pytest/"""
"""https://pytest-docs-ru.readthedocs.io/ru/latest/getting-started.html#installation"""

from functions import requests_get_function, get_list_files, allowed_file
from app import DATA_DIR
from constants import ALLOWED_EXTENSIONS



class TestClass:

    # Функця должна воврацать словарь
    def test_requests_get_function(self):
        params = {}
        assert type(requests_get_function(params)) == type(params)


    # Функция должна возвращать сисок
    def test_get_list_files(self):
        assert type(get_list_files(DATA_DIR)) == type(list())

    
    # Расширение файла должно быть из списка разрешенных
    def test_allowed_file(self):
        for extensions in ALLOWED_EXTENSIONS:
            assert allowed_file('.' + extensions) == True
