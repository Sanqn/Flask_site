from flask_login import UserMixin
from flask import Flask, redirect, url_for

class UserLogin(UserMixin):
    def fromDB(self, user_id, db):
        self.__user = db.getUser(user_id)
        return self

    def create(self, user):
        self.__user = user
        return self

    def get_id(self):
        if self.__user == False:
            return redirect(url_for('registration'))
        return str(self.__user['id'])

    def get_name(self):
        return self.__user['name'] if self.__user else 'No name'

    def get_email(self):
        return self.__user['email'] if self.__user else 'No email'

    def get_ava(self):
        return self.__user['avatar'] if self.__user else 'No email'
    # If we use UserMixin we can't use down mwthods
    # def is_authenticated(self):
    #     return True
    #
    # def is_active(self):
    #     return True
    #
    # def is_anonymous(self):
    #     return False
