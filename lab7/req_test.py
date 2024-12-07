import requests

IP_local = 'http://127.0.0.1:'

a = (requests.delete(f'{IP_local}{5001}/delete/name'))
print(a)