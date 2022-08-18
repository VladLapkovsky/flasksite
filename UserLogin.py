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
        return self.__user['name']
