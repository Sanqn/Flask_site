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
