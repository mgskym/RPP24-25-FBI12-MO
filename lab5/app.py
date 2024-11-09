from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, Blueprint, render_template, request, make_response, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from db import db
from db.models import user
from flask_login import login_user, login_required, current_user, logout_user

app = Flask(__name__)

app.secret_key = '123'
user_db = "postgres"
host_ip = "localhost"
host_port = "5432"
database_name = "rpp5_mo_db"
password = "postgres"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{user_db}:{password}@{host_ip}:{host_port}/{database_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_users(user_id):
    return users.query.get(int(user_id))


@app.route("/")
@app.route("/index")
@login_required
def start():
    return redirect("/main", code=302)


@app.route("/login", methods=['GET'])
def login_get():
    return render_template(
        'login.html'
    )


@app.route("/login", methods=['POST'])
def login_post():
    email_form = request.form.get('email')
    password_form = request.form.get('password')
    my_user = user.query.filter_by(email=email_form).first()

    if (email_form != '' and password_form != '') and my_user and check_password_hash(my_user.password, password_form):
        login_user(my_user, remember=False)
        return redirect("/index", code=302)
    else:
        errors = 'Пользователь не найден или не заполнены все обязательные поля'
        return render_template(
            'login.html',
            errors=errors
        )


@app.route("/signup", methods=['GET'])
def register_get():
    return render_template(
        'signup.html'
    )


@app.route("/signup", methods=['POST'])
def register_post():
    name_form = request.form.get('name')
    email_form = request.form.get('email')
    password_form = request.form.get('password')
    errors = "Не заполнены все обязательные поля"

    is_user_exists = user.query.filter_by(email=email_form).first()
    if is_user_exists:
        errors = 'Пользователь с такими данными уже существует'
        return render_template(
            'signup.html',
            errors=errors
        )
    else:
        if (name_form != '' and email_form != '' and password_form != ''):
            hashedPswd = generate_password_hash(password_form, method="pbkdf2")
            newUser = user(
                name = name_form,
                email = email_form,
                password = hashedPswd
            )
            db.session.add(newUser)
            db.session.commit()
            return redirect("/login", code=302)
        else:
            errors = 'Заполните все обязательные поля'
            return render_template(
                'signup.html',
                errors=errors
            )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/login")


@app.route("/main", methods=['POST', 'GET'])
@login_required
def main_page():
    return render_template(
        'index.html'
    )
