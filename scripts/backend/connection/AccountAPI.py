import flask

from API_Helper import flarg
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseAccounts

account_api = flask.Blueprint('account_api', __name__)


@account_api.route('/create')  # TODO, Done
def create_user():
    user_name = flarg('user_name')
    password = flarg('password')

    create_status = DatabaseAccounts.add_user(user_name=user_name, password=password)

    if create_status is True:
        return "Created new user '" + user_name + "'."
    else:
        return "Could not create a new user '" + user_name + "'."


@account_api.route('/delete')  # TODO, Done
def delete_user():
    user_name = flarg('user_name')
    password = flarg('password')

    if flask.session['user_name'] == user_name:
        flask.session['is_logged_in'] = False

    delete_status = DatabaseAccounts.delete_user(user_name=user_name, password=password)

    if delete_status is True:
        return "Deleted the user '" + user_name + "'."
    else:
        return "Could not delete the user '" + user_name + "'."


@account_api.route('/logged_in')  # TODO, Done
def logged_in():
    user_name = flarg("user_name")
    password = flarg("password")

    if DatabaseAccounts.exists_user_by_name(user_name):
        flask.session['user_name'] = user_name
        flask.session['password'] = password
        flask.session['is_logged_in'] = True
        return "Logged in as the user '" + user_name + "'."
    else:
        return "User does not exist."


@account_api.route('/log_in')  # TODO, Done
def log_in():
    user_name = flarg('user')
    password = flarg('password')

    if user_name is None or password is None:
        return "The user name or password is null. Add 'user=[username]' and 'password=[password]' to the URL."
    elif flarg('is_logged_in'):
        return "You must log out before you can login. Currently logged in as '" + flarg("user") + "'"
    else:

        # Checks with the database if the user exists
        exists_status = DatabaseAccounts.exists_user_by_name(user_name)
        if exists_status is False:
            return "Could not log-in as the user '" + user_name + "'. User does not exist."

        # Checks if the user name and password match the database user
        login_status = DatabaseAccounts.check_user(user_name, password)
        if login_status is True:
            return "Successfully logged-in as the user '" + user_name + "'."
        else:
            return "Could not log-in as the user '" + user_name + "'. Incorrect password."


@account_api.route("/log_out")  # TODO, Done
def log_out():
    if flask.session["is_logged_in"] is True:
        flask.session["is_logged_in"] = False
        return "Successfully logged-out."
    else:
        return "Could not log-out. User was never logged-in."
