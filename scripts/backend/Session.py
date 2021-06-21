import flask
import sqlite3

class Session:
    db = sqlite3.connect("..\\..\\db.")

    @staticmethod
    def login(session, user, password):
        assert(user is not None and password is not None)
        session['user'] = user
        session['password'] = password
        session['is_logged_in'] = True

    @staticmethod
    def logout(session):
        assert(session['is_logged_in'] is True)
        session['is_logged_in'] = False

    @staticmethod
    def is_logged_in(session):
        return session["is_logged_in"]

    @staticmethod
    def get_name(session):
        return session['name']

    # @staticmethod
    # def get_name(session):