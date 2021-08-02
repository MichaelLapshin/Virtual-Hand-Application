import flask
import sqlite3

from scripts.frontend import Constants

db = sqlite3.connect(Constants.DATABASE_ABSOLUTE_PATH)


def login(session, user, password):
    assert (user is not None and password is not None)
    session['user'] = user
    session['password'] = password
    session['is_logged_in'] = True


def logout(session):
    assert (session['is_logged_in'] is True)
    session['is_logged_in'] = False


def is_logged_in(session):
    return session["is_logged_in"]


def get_name(session):
    return session['name']

# @staticmethod
# def get_name(session):
