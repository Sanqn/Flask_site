import datetime
import sqlite3


class FBbase:

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def menu(self):
        query = """SELECT * FROM mainmenu"""
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchall()
            if res: return res
        except Exception as E:
            print('Error {E}')
        return []

    def addpost(self, title_post, text_post):
        tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post = (title_post, text_post, tm)
        query = """INSERT INTO posts(id, title, text, time) VALUES(Null, ?, ?, ?);"""
        try:
            self.__cur.execute(query, post)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Error {e}')
            return False
        return True

    def get_post(self, id):
        query = f"SELECT * FROM posts WHERE id={id};"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False
