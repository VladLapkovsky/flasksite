from credentials import PROJECT_SECRET_KEY


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = PROJECT_SECRET_KEY
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY

    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
