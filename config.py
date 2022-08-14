from credentials import PROJECT_SECRET_KEY


class Config:
    DEBUG = True
    DEVELOPMENT = True
    SECRET_KEY = PROJECT_SECRET_KEY
    FLASK_HTPASSWD_PATH = '/secret/.htpasswd'
    FLASK_SECRET = SECRET_KEY
    DATABASE = '/tmp/flstie.db'
    # DB_HOST = 'database'  # a docker link


class ProductionConfig(Config):
    DEVELOPMENT = False
    DEBUG = False
    # DB_HOST = 'my.production.database'  # not a docker link