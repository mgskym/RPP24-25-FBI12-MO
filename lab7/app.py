from flask import Flask, request, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json


app = Flask(__name__)
limiter = Limiter(
    get_remote_address, app=app, default_limits=["100 per day"], storage_uri="memory://",
)


def read_json_data():
    try:
        with open('data.json', 'r') as file:
            return json.load(file)
    except:
        return {}


def write_data(data):
    with open('data.json', 'w') as file:
        json.dump(data, file, indent=4)


@app.route('/set', methods=['POST'])
@limiter.limit("10/minute", override_defaults=False)
def set_value():
    data = read_json_data()
    try:
        req = request.json
        if req['key'] and req['value']:
            data[req['key']] = req['value']
            write_data(data)
            return make_response('OK', 200)
        else:
            return make_response('No "key" and "value" in JSON.', 400)
    except:
        return make_response('Not JSON or file not exists.', 400)


@app.route('/get/<key>', methods=['GET'])
def get(key):
    data = read_json_data()
    if key in data:
        return make_response(f'{data[key]}', 200)
    else:
        return make_response('Key not found.', 400)


@app.route('/delete/<key>', methods=['DELETE'])
@limiter.limit("10/minute", override_defaults=False)
def delete(key):
    data = read_json_data()
    if key in data:
        del data[key]
        write_data(data)
        return make_response('Key deleted.', 200)
    else:
        return make_response('Key not found.', 400)


@app.route('/exists/<key>', methods=['GET'])
def exists(key):
    data = read_json_data()
    if key in data:
        return make_response('Key exists.', 200)
    else:
        return make_response('Key not exists.', 200)


if __name__ == '__main__':
    app.run(debug=True, port=5001)