from credentials import PROJECT_SECRET_KEY

APP_DATABASE = None
# COOKIE_LOGGED = 'emailLogged'


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = PROJECT_SECRET_KEY
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    DATABASE = None
    DATABASE_PATH = '/home/vladlapkovsky/Desktop/DjangoProjects/flasksite/flsite.db'
    MAX_CONTENT_LENGTH = 1024 * 1024  # 1 Mb

    # DB_HOST = 'database'  # a docker link
    # PERMANENT_SESSION_LIFETIME = 10  # session life time if user doesn't do anything


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    # DB_HOST = 'my.production.database'  # not a docker link
