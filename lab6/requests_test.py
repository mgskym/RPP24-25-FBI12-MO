import requests

IP_local = 'http://127.0.0.1:'

a = (requests.get(f'{IP_local}{5009}/health')).json()['message']
print(a)