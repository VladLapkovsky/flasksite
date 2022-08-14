import math
import sqlite3
import time


class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        sql_query = 'SELECT * FROM mainmenu'
        try:
            self.__cursor.execute(sql_query)
            result = self.__cursor.fetchall()
            if result:
                return result
        except Exception as e:
            print('Error occurred while reading DB: ', e)
        return []

    def addPost(self, post_title, post_content):
        sql_query = 'INSERT INTO posts VALUES(NULL, ?, ?, ?)'
        post_adding_time = math.floor(time.time())
        result = False
        try:
            self.__cursor.execute(sql_query, (post_title, post_content, post_adding_time))
            self.__db.commit()
        except sqlite3.Error as e:
            print('sqlite3.Error occurred while adding post to DB: ', e)
        except Exception as e:
            print('Error occurred while adding post to DB: ', e)
        else:
            result = True
        return result

    def getPost(self, post_id):
        sql_query = 'SELECT title, text FROM posts WHERE id = ? LIMIT 1'
        try:
            self.__cursor.execute(sql_query, (post_id,))
            result = self.__cursor.fetchone()
            if result:
                return result
        except Exception as e:
            print('Error occurred while reading post from DB: ', e)
        return False, False


