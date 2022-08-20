import os

from flask import url_for
from flask_login import UserMixin


class UserLogin(UserMixin):
    def fromDB(self, user_id, database):
        self.__user = database.getUserByID(user_id)
        return self

    def login_user(self, user):
        self.__user = user
        return self

    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False

    def get_id(self):
        return self.__user['id']

    def get_name(self):
        return self.__user['name'] if self.__user else "No name found"

    def get_email(self):
        return self.__user['email'] if self.__user else "No email found"

    def get_avatar(self, app):
        img = None
        if self.__user:
            if not self.__user['avatar']:
                try:
                    default_file_path = ''.join((app.root_path, url_for('static', filename='images/default.png')))
                    with app.open_resource(default_file_path, 'rb') as file:
                        img = file.read()
                except FileNotFoundError as e:
                    print('No default avatar', e)
            else:
                img = self.__user['avatar']

        return img

    def verify_extension(self, filename) -> bool:
        extension = filename.rsplit('.', 1)[1]
        return True if extension in ('png', 'PNG') else False
