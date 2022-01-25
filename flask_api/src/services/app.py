from email.policy import default
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from flask_login import LoginManager

# Init Flask.
app = Flask(__name__)

#  Config Variables to be used for Flask.
app.config.from_object("config.Config")

# Init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()
db.init_app(app)

# Flask-Login config.
# https://flask-login.readthedocs.io/en/latest/
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    # since the user_id is just the primary key of our user table, use it in
    #  the query for the user
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    photo = db.Column(db.String(100), nullable=True, default='default.jpg')
    password = db.Column(db.String, nullable=False)
    active = db.Column(db.Boolean(), default=True, nullable=False)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())

    def __init__(self, email, fullname, password):
        self.email = email
        self.fullname = fullname
        self.password = password


class Publication(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=True)
    description = db.Column(db.String(100), nullable=True)
    priority = db.Column(db.String(100), nullable=True)
    status = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    create_at = db.Column(db.DateTime, nullable=True, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True,
                           default=datetime.utcnow())

    def __init__(self, description):
        self.description = description
