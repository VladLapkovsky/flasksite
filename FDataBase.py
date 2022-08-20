import math
import re
import sqlite3
import time
import typing

from flask import url_for, request, session
from flask_login import current_user
from werkzeug.security import check_password_hash


class SQLError(Exception):
    pass


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        if current_user.is_authenticated:
        # if session.get(COOKIE_LOGGED) and request.cookies.get('logged'):
            sql_query = 'SELECT * FROM mainmenu'
        else:
            sql_query = f"""SELECT * FROM mainmenu WHERE NOT url LIKE '{url_for("logout")}'"""

        execute_error, result = self._execute_sql_and_fetch_all(sql_query)

        return result if result is not None else []

    def addPost(self, post_title, post_content, post_url):
        if self._is_post_url_exists(post_url):
            msg = f'Post with {post_url} URL already exists'
            return False, msg

        base_path = url_for('static', filename='images_html')
        post_content = re.sub(
            r"(?P<tag><img\s+[^>]*src=)(?P<quote>[\"'])(?P<url>.+?)(?P=quote)>",
            "\\g<tag>" + base_path + "/\\g<url>>",
            post_content
        )

        sql_query = 'INSERT INTO posts VALUES(NULL, ?, ?, ?, ?)'
        post_adding_time = math.floor(time.time())
        is_added = False
        msg = ''

        execute_error, is_saved = self._execute_sql_and_save(sql_query, (
            post_title, post_content, post_url, post_adding_time,
        ))

        if execute_error is None and is_saved is True:
            is_added = True
        else:
            msg = f'Error occurred while adding post to DB: {execute_error}'
        return is_added, msg

    def getPost(self, post_url):
        sql_query = f"SELECT title, text FROM posts WHERE url LIKE '{post_url}' LIMIT 1"

        execute_error, result = self._execute_sql_and_fetch_one(sql_query)

        return result

    def getPostsAnnounce(self):
        sql_query = 'SELECT title, text, url FROM posts ORDER BY time DESC'

        execute_error, result = self._execute_sql_and_fetch_all(sql_query)

        return result if result is not None else []

    def add_user_with_email_check(self, username, email, hashed_password) -> typing.Tuple[bool, str]:
        if self._is_email_exists(email) is True:
            return False, 'User with this email already exists'

        return self.addUser(username, email, hashed_password)

    def addUser(self, username, email, hashed_password) -> typing.Tuple[bool, str]:
        error_msg = ''
        is_added = self._add_user_to_db(username, email, hashed_password)

        if is_added is False:
            error_msg = "User wasn't added, try again"

        return is_added, error_msg

    def getUserByID(self, user_id):
        sql_query = f"SELECT * FROM users WHERE id = {user_id} LIMIT 1"

        execute_error, user = self._execute_sql_and_fetch_one(sql_query)
        if execute_error is None and user is not None:
            return user
        return None

    def getUserByEmail(self, email) -> typing.Optional[sqlite3.Row]:
        return self._get_user_from_db_by_email(email)

    def updateUserAvatar(self, avatar, user_id):
        avatar_updated = False

        if not avatar:
            return avatar_updated

        binary_file = sqlite3.Binary(avatar)
        execute_error, is_saved = self._execute_sql_and_save(
            "UPDATE users SET avatar = ? WHERE id = ?",
            (binary_file, user_id)
        )
        if execute_error is None and is_saved is True:
            avatar_updated = True
        return avatar_updated

    def _is_email_exists(self, email):
        is_exists = False
        sql_query = f"SELECT COUNT() as `count` FROM users WHERE email LIKE '{email}'"

        execute_error, result = self._execute_sql_and_fetch_one(sql_query)

        if execute_error is None and result is not None and result['count'] > 0:
            is_exists = True
        return is_exists

    def _add_user_to_db(self, username, email, hashed_password) -> bool:
        is_added = False
        sql_query = 'INSERT INTO users VALUES(NULL, ?, ?, ?, NULL, ?)'
        tm = math.floor(time.time())

        execute_error, is_saved = self._execute_sql_and_save(sql_query, (username, email, hashed_password, tm))

        if execute_error is None and is_saved is True:
            is_added = True
        return is_added

    def _get_user_from_db_by_email(self, email):
        sql_query = f"SELECT * FROM users WHERE email LIKE '{email}' LIMIT 1"

        execute_error, result = self._execute_sql_and_fetch_one(sql_query)

        return result

    def _get_user_from_db_by_id(self, user_id):
        sql_query = f"SELECT * FROM users WHERE id = {user_id} LIMIT 1"

        execute_error, result = self._execute_sql_and_fetch_one(sql_query)

        return result

    def _is_post_url_exists(self, post_url):
        sql_query = f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{post_url}'"

        execute_error, result = self._execute_sql_and_fetch_one(sql_query)

        if execute_error is None and result is not None and result['count'] > 0:
            return True
        return False

    def _execute_sql_and_fetch_one(self, sql_query, *args):
        result = None

        execute_error = self._execute_sql_query(sql_query, *args)
        if execute_error is None:
            result = self._fetch_one_from_db()

        return execute_error, result
        # return self._fetch_one_from_db() if execute_error is None else execute_error

    def _execute_sql_and_fetch_all(self, sql_query, *args):
        result = None

        execute_error = self._execute_sql_query(sql_query, *args)

        if execute_error is None:
            result = self._fetch_all_from_db()
        return execute_error, result
        # return self._fetch_all_from_db() if execute_error is None else execute_error

    def _execute_sql_and_save(self, sql_query, *args):
        is_saved = False

        execute_error = self._execute_sql_query(sql_query, *args)

        if execute_error is None:
            is_saved = self._save_db()
        return execute_error, is_saved

    def _execute_sql_query(self, sql_query, *args):
        execute_error = None
        try:
            self.__cursor.execute(sql_query, *args)
        except Exception as e:
            # log.error
            execute_error = f'SQL query "{sql_query}" finished with error: {e}'
        return execute_error

    def _save_db(self):
        is_saved = True
        try:
            self.__db.commit()
        except Exception:
            # log.error...
            is_saved = False
        return is_saved

    def _fetch_one_from_db(self) -> typing.Optional[sqlite3.Row]:
        return self.__fetch_from_db('fetchone')

    def _fetch_all_from_db(self) -> typing.Optional[sqlite3.Row]:
        return self.__fetch_from_db('fetchall')

    def __fetch_from_db(self, fetch):
        sql_result = None
        try:
            sql_result = getattr(self.__cursor, fetch)()
        except Exception as e:
            # log.error
            # raise SQLError(f'"{fetch}()" from DB finished with error') from e
            print(f'"{fetch}()" from DB finished with error', e)
        return sql_result
