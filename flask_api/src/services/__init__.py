from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify
from datetime import datetime

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)


class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    photo = db.Column(db.String(100), nullable=True)
    password = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())

    def __init__(self, email):
        self.email = email


class Publication(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    create_at = db.Column(db.String(100), nullable=True)
    password = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())

    def __init__(self, email):
        self.email = email


@app.route("/")
def hello_world():
    return jsonify(hello="world")
