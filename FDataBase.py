import math
import re
import sqlite3
import time
import typing

from flask import url_for, request, session
from werkzeug.security import check_password_hash

from config import COOKIE_LOGGED


class SQLError(Exception):
    pass


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        if session.get(COOKIE_LOGGED) and request.cookies.get('logged'):
            sql_query = 'SELECT * FROM mainmenu'
        else:
            sql_query = f"""SELECT * FROM mainmenu WHERE NOT url LIKE '{url_for("logout")}'"""
        try:
            self.__cursor.execute(sql_query)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as e:
            print('Error occurred while reading DB: ', e)
        return []

    def addPost(self, post_title, post_content, post_url):
        if self._is_post_url_exists(post_url):
            return False

        base_path = url_for('static', filename='images_html')
        post_content = re.sub(
            r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
            "\\g<tag>" + base_path + "/\\g<url>>",
            post_content
        )
        sql_query = 'INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)'
        post_adding_time = math.floor(time.time())
        result = False
        try:
            self.__cursor.execute(sql_query, (post_title, post_content, post_url, post_adding_time))
            self.__db.commit()
        except sqlite3.Error as e:
            print('sqlite3.Error occurred while adding post to DB: ', e)
        except Exception as e:
            print('Error occurred while adding post to DB: ', e)
        else:
            result = True
        return result

    def getPost(self, post_url):
        sql_query = f"SELECT title, text FROM posts WHERE url LIKE '{post_url}' LIMIT 1"
        try:
            self.__cursor.execute(sql_query)
            result = self.__cursor.fetchone()
            if result:
                return result
        except Exception as e:
            print(f'Error occurred while getting post with URL {post_url} from DB: ', e)
        return False, False

    def getPostsAnnounce(self):
        sql_query = 'SELECT title, text, url FROM posts ORDER BY time DESC'
        try:
            self.__cursor.execute(sql_query)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as e:
            print('Error occurred while getting posts from DB: ', e)
        return []

    def addUser(self, username, email, hashed_password) -> typing.Tuple[bool, str]:
        try:
            if self._is_email_exists(email) is True:
                return False, 'User with this email already exists'
            self._add_user_to_db(username, email, hashed_password)
        except SQLError as error:
            return False, error.args[0]  # get Exception message

        return True, 'Registration succeed'

    def getUser(self, email, inputted_password) -> typing.Tuple[typing.Optional[sqlite3.Row], str]:
        try:
            if not self._is_email_exists(email):
                return None, "User with email doesn't exist"
            user = self._get_user_from_db(email)
            if not check_password_hash(user['password'], inputted_password):
                return None, "Wrong password"
        except SQLError as error:
            return None, error.args[0]  # get Exception message
        else:
            return user, ''

    def _is_email_exists(self, email):
        is_exists = False

        sql_query = f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'"
        try:
            self.__cursor.execute(sql_query)
            sql_result = self.__cursor.fetchone()
        except Exception as e:
            raise SQLError('Error occurred while selecting email from DB') from e
        else:
            if sql_result['count'] > 0:
                is_exists = True
        return is_exists

    def _add_user_to_db(self, username, email, hashed_password):
        sql_query = 'INSERT INTO users VALUES(NULL, ?, ?, ?, ?)'
        tm = math.floor(time.time())
        try:
            self.__cursor.execute(sql_query, (username, email, hashed_password, tm))
            self.__db.commit()
        except Exception as e:
            raise SQLError('User adding error') from e

    def _get_user_from_db(self, email):
        sql_query = f"SELECT * FROM users WHERE email LIKE '{email}' LIMIT 1"
        try:
            self.__cursor.execute(sql_query)
            sql_result = self.__cursor.fetchone()
        except Exception as e:
            raise SQLError('User getting from DB error') from e
        return sql_result

    def _is_post_url_exists(self, post_url):
        sql_query = f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{post_url}'"
        self.__cursor.execute(sql_query)
        result = self.__cursor.fetchone()
        if result['count'] > 0:
            print(f'Post with {post_url} URL already exists')
            return True
        return False
