import os


basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # Set the Variables to be used for Flask.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "strongKey")
    SWAGGER = {
        'title': 'Publication API',
        'uiversion': 3,
    }
