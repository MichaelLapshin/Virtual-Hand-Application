import flask

from API_Helper import flarg, package
from scripts import Warnings, Log
from scripts.backend.database import Database, DatabaseAccounts

account_api = flask.Blueprint('account_api', __name__)


@account_api.route('/create')  # TODO, Done
def create_user():
    user_name = flarg('user_name')
    password = flarg('password')

    if DatabaseAccounts.exists_user_by_name(user_name) is False or \
            DatabaseAccounts.check_user(user_name=user_name, password=password) is False:

        create_status = DatabaseAccounts.add_user(user_name=user_name, password=password)

        if create_status is True:
            return package(True, "Created a new user named '" + user_name + "'.")
        else:
            return package(False, "Could not create the new user named '" + user_name + "'.")
    else:
        return package(False, "Could not create the new user named '" + user_name + "'. The user already exists.")


@account_api.route('/delete')  # TODO, Done
def delete_user():
    user_id = int(flarg('user_id'))
    Log.info("Deleting the user with id '" + str(user_id) + "'.")

    # if flask.session.get('user_name') == user_name:
    #     flask.session['is_logged_in'] = False

    exists_user = DatabaseAccounts.exists_user_by_id(user_id=user_id)
    delete_status = exists_user and DatabaseAccounts.delete_user(user_id=user_id)

    if delete_status is True:
        return package(True, "Deleted the user with id '" + str(user_id) + "'.")
    else:
        return package(False, "Could not delete the user with id '" + str(user_id) + "'.")


@account_api.route('/check_user')  # TODO, Done
def logged_in():
    user_name = flarg("user_name")
    password = flarg("password")

    if DatabaseAccounts.exists_user_by_name(user_name=user_name):
        if DatabaseAccounts.check_user(user_name=user_name, password=password):
            flask.session['user_name'] = user_name
            flask.session['password'] = password
            flask.session['is_logged_in'] = True
            return package(True, "The user '" + user_name + "' with the password '" + password + "' exists.")
        else:
            return package(False, "The inputted password for the user '" + user_name + "' is false.")
    else:
        return package(False, "User '" + user_name + "' does not exist.")


@account_api.route('/get_user_id')
def get_user_id():
    user_name = flarg("user_name")
    password = flarg("password")
    return package(None, DatabaseAccounts.get_user_id(user_name=user_name, password=password))


@account_api.route('/log_in')  # TODO, Done
def log_in():
    user_name = flarg('user')
    password = flarg('password')

    if user_name is None or password is None:
        return package(False,
                       "The user name or password is null. Add 'user=[username]' and 'password=[password]' to the URL.")
    elif flarg('is_logged_in'):
        return package(False, "You must log out before you can login. Currently logged in as '" + flarg("user") + "'")
    else:

        # Checks with the database if the user exists
        exists_status = DatabaseAccounts.exists_user_by_name(user_name=user_name, password=password)
        if exists_status is False:
            return package(False, "Could not log-in as the user '" + user_name + "'. User does not exist.")

        # Checks if the user name and password match the database user
        login_status = DatabaseAccounts.check_user(user_name, password)
        if login_status is True:
            return package(True, "Successfully logged-in as the user '" + user_name + "'.")
        else:
            return package(False, "Could not log-in as the user '" + user_name + "'. Incorrect password.")


@account_api.route("/log_out")  # TODO, Done
def log_out():
    if flask.session["is_logged_in"] is True:
        flask.session["is_logged_in"] = False
        return package(True, "Successfully logged-out.")
    else:
        return package(False, "Could not log-out. User was never logged-in.")
