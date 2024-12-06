import sys
import time
from flask import Flask, request, make_response, render_template, redirect
import requests
import threading
import random
import os
import subprocess

sys.path.append('..')


balancer = Flask(__name__)

IP_local = 'http://127.0.0.1:'
app_ports = [5001, 5002, 5003]
active_instances = []

def health_instances():
    while True:
        global active_instances
        global app_ports
        ids = []
        for i in range(0, len(app_ports)):
            try:
                health = requests.get(f'{IP_local}{app_ports[i]}/health').json()["message"]
                if health == 'OK':
                    ids.append(i+1)
            except:
                print(f'Instance {i+1} is not avaliable.')
        active_instances = ids
        print(active_instances)
        print(app_ports)
        time.sleep(5)


@balancer.route('/health', methods=['GET'])
def health():
    res_body = {
        "active_instances": active_instances
    }
    return make_response(res_body, 200)


@balancer.route('/process', methods=['GET'])
def process():
    if active_instances:
        selected_id = random.choice(active_instances)
        response = requests.get(f'{IP_local}{app_ports[selected_id-1]}/process').json()['instance_id']
        res_body = {
            "message": response
        }
    else:
        res_body = {
            "message": "Error"
        }
    return make_response(res_body, 200)


@balancer.route('/', methods=['GET'])
def manager():
    return render_template(
        'index.html',
        active_instances = active_instances 
    )


@balancer.route('/add_instance', methods=['GET'])
def add_instance_page():
    return render_template(
        'add.html'
    )

@balancer.route('/add_instance', methods=['POST'])
def add_instance():
    global app_ports
    ip = request.form.get('ip')
    port = request.form.get('port')
    app_ports.append(int(port))

    script_path = "./start_application.sh"
    # subprocess.call([script_path, ip, port], shell=True)
    os.system(f"bash {script_path} {ip} {port}")

    return redirect('/', code=301)


@balancer.route('/remove_instance', methods=['GET'])
def remove_instance_page():
    global active_instances
    instances = active_instances
    return render_template(
        'remove.html',
        instances = instances
    )


@balancer.route('/remove_instance', methods=['POST'])
def remove_instance():
    global app_ports
    id = request.form.get('id')
    app_ports.pop(int(id) - 1)
    return redirect('/', code=301)


@balancer.route('/<path:path>', methods=['GET'])
def path():
    if active_instances:
        selected_id = random.choice(active_instances)
        request = requests.get(f'{IP_local}{app_ports[selected_id-1]}/{path}')
    else:
        res_body = {
            "message": request
        }
    return make_response(res_body, 200)


if __name__ == '__main__':
    threading.Thread(target=health_instances, daemon=True).start()
    balancer.run(port=5004, debug=True)