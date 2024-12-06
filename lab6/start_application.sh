#!/bin/bash

start_flask_app() {
    local ip=$1
    local port=$2

    source venv/Scripts/activate

    FLASK_APP=app.py FLASK_RUN_HOST=$ip FLASK_RUN_PORT=$port flask run &

    local pid=$!
    echo "Flask-приложение запущено с PID $pid на $ip:$port."
}

start_flask_app "$1" "$2"