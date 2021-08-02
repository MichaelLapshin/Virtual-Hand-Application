import flask

from scripts import Warnings
from scripts.backend.database import Database
from scripts.backend.connection import Session

account_api = flask.Blueprint('account_api', __name__)


@account_api.route('/create-user')
def create_user():
    user = flask.request.args['user']
    password = flask.request.args['password']

    Database.add_user(user=user, password=password)

    return "Created new user '" + user + "'."


@account_api.route('/login')
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


@account_api.route("/logout")
def logout():
    if Session.is_logged_in(flask.session):
        Session.logout(flask.session)
        return "Signed-out as user '" + flask.session["user"] + "'."
    else:
        return "Cannot logout; not signed in as any user."
