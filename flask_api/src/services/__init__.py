# from .main import main as main_blueprint
# from .auth import auth as auth_blueprint
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

app.config.from_object("config.Config")

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy(app)

# # blueprint for auth routes in our app
# app.register_blueprint(auth_blueprint)

# # blueprint for non-auth parts of app
# app.register_blueprint(main_blueprint)


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
    password = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())

    def __init__(self, email):
        self.email = email
