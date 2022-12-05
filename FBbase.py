import datetime
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash


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

    def addpost(self, title_post, url_post, text_post, image):
        tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        post = (title_post, text_post, url_post, image, tm)
        query = """INSERT INTO posts(id, title, text, url, image, time) VALUES(Null, ?, ?, ?, ?, ?);"""
        try:
            self.__cur.execute(query, post)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Error {e} ==================')
            return False
        return True

    def adduser(self, name, email, psw):
        tm = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        user = (name, email, psw, tm)
        query = """INSERT INTO users(id, name, email, psw, time) VALUES(Null, ?, ?, ?, ?);"""
        try:
            self.__cur.execute(query, user)
            self.__db.commit()
        except sqlite3.Error as e:
            print(f'Error {e} ==================')
            return False
        return True

    def check_user(self, email, pasw_user):
        query = f"SELECT name, psw FROM users WHERE email='{email}';"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if res == None:
                return False
            else:
                res = dict(res)
                check_psw = check_password_hash(res['psw'], pasw_user)
                if check_psw:
                    print(res['name'])
                    return res['name']
                else:
                    return False
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False

    def getUserbyEmail(self, email):
        query = f"SELECT * FROM users WHERE email='{email}';"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if not res:
                print('User not found')
                return False
            return res
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False

    def getUser(self, user_id):
        query = f"SELECT * FROM users WHERE id='{user_id}';"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if not res:
                print('User not found')
                return False
            return res
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False

    def get_post(self, url_post):
        query = f"SELECT * FROM posts WHERE url='{url_post}';"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchone()
            if res:
                return res
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False

    def get_all_post(self):
        query = "SELECT * FROM posts ORDER BY time DESC;"
        try:
            self.__cur.execute(query)
            res = self.__cur.fetchall()
            if res:
                return res
        except sqlite3.Error as e:
            print(f'Error {e}')
        return False
