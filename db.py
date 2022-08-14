import sqlite3


def connect_db(app):
    connection = sqlite3.connect(app.config['DATABASE'])
    connection.row_factory = sqlite3.Row
    return connection


def create_db(app, sql_file_path):
    db = connect_db(app)
    with app.open_resource(sql_file_path, mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()
