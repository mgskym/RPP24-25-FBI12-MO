import requests

IP_local = 'http://127.0.0.1:'

a = (requests.post(f'{IP_local}{5001}/set', json={"name": "Michael"}))
print(a)