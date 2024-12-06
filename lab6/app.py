import sys
from flask import Flask, request, make_response
sys.path.append('..')


app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    res_body = {
        "message": "OK"
    }
    return make_response(res_body, 200)

@app.route('/process', methods=['GET'])
def process():
    res_body = {
        "instance_id": 3
    }
    return make_response(res_body, 200)


if __name__ == '__main__':
    app.run(port=5003)