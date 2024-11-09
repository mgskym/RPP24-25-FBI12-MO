from flask_login import UserMixin
from . import db

class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(30), nullable=False)
    name = db.Column(db.String(30))
    password = db.Column(db.String(102), nullable=False)

    def __repr__(self):
        return f"id:{self.id}, , email:{self.email}, name:{self.name}"