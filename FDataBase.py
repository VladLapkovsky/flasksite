class FDataBase:
    def __init__(self, db):
        self.__db = db
        self.__cursor = db.cursor()

    def getMenu(self):
        sql_query = '''SELECT * FROM mainmenu'''
        result = []
        try:
            self.__cursor.execute(sql_query)
            result = self.__cursor.fetchall()
        except Exception as e:
            print('Error occurred while reading DB: ', e)
        return result
