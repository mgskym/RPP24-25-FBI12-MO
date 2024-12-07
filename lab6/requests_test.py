import requests

IP_local = 'http://127.0.0.1:'

a = (requests.get(f'{IP_local}{5000}/health'))
print(a)