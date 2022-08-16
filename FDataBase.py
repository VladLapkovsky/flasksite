import math
import re
import sqlite3
import time

from flask import url_for, request


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        # sql_query = 'SELECT * FROM mainmenu'

        is_logged = request.cookies.get('logged')
        if is_logged:
            sql_query = 'SELECT * FROM mainmenu'
        else:
            sql_query = 'SELECT * FROM mainmenu WHERE NOT `url` LIKE "/logout"'
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

    def _is_post_url_exists(self, post_url):
        count_sql_query = f"SELECT COUNT() as `count` FROM posts WHERE url LIKE '{post_url}'"
        self.__cursor.execute(count_sql_query)
        result = self.__cursor.fetchone()
        if result['count'] > 0:
            print(f'Post with {post_url} URL already exists')
            return True
        return False
