"""https://pypi.org/project/pytest/"""
"""https://pytest-docs-ru.readthedocs.io/ru/latest/getting-started.html#installation"""

from functions import requests_get_function


class TestClass:
    # Функця должна воврацать словарь
    def test_requests_get_function(self):
        params = {}
        assert type(requests_get_function(params)) == type(params)

