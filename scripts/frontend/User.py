"""
[User.py]
@description: An interface for storing user data
@author: Michael Lapshin
"""

from scripts.frontend import ClientConnection

# User  constants
LOGIN_AS_MESSAGE = "Successfully logged in as: "
LOGIN_FAIL_MESSAGE = "Failed to log-in. The user name or password is incorrect."
LOGIN_CONNECTION_FAIL_MESSAGE = "Failed to log-in. Connection with the server was not established."

LOGOUT_MESSAGE = "Successfully logged out."

# User variables
_name = None
_password = None


def login(username, password):
    global _name, _password

    if True:
        _name = username
        _password = password
    else:
        pass


def logout():
    global _name, _password

    _name = None
    _password = None


def name():
    global _name

    if _name is None:
        return ""
    return _name


def is_connected():
    # pings the server and retrieves the username which the user is logged in as
    return "Michael"


def is_logged_in():
    global _name

    return is_connected() == _name
