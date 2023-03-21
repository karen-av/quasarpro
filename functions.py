import json
import requests

def requests_get_function(params):
    x = requests.get(f'http://127.0.0.1:5000/files/get', params = params).json()
    print(type(x))
    return x