"""
[ServerApp.py]
@description: In charge of the connections between client GUI and server database
@author: Michael Lapshin
"""

import flask
import flask_login

from Session import Session
from scripts import Logger, Question
from Database import Database
import os

# Questionnaire for the server setup


# Flask application + configurations
app = flask.Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(16)  # Random secret key

# Database
db = Database()

# Logger
logger = Logger("ServerApp", log_lvl=4)

if __name__ == '__main__':
    app.run()

@app.route('/')
def is_running_window():
    return "Virtual-Hand-Application Server is running."


@app.route('/login/create-user')
def create_user():
    user = flask.request.args['user']
    password = flask.request.args['password']

    Database.add_user(user=user, password=password)

    return "Created new user '" + user + "'."


@app.route('/user/login')
def login():
    user = flask.request.args['user']
    password = flask.request.args['password']

    if user is None or password is None:
        return "Add 'user=[username]' and 'password=password' to the URL."
    elif flask.session['is_logged_in']:
        return "You must log out before you can login. Currently logged in as '" + flask.session["user"] + "'"
    else:
        # Link session to user
        Session.login(flask.session, user, password)

        return "Logged in as '" + Session.get_name(flask.session) + "'."


@app.route("/user/logout")
def logout():
    if Session.is_logged_in(flask.session):
        Session.logout(flask.session)
        return "Signed-out as user '" + flask.session["user"] + "'."
    else:
        return "Cannot logout; not signed in as any user."

