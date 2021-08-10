"""
[User.py]
@description: An interface for storing user data
@author: Michael Lapshin
"""
import requests

from scripts import Warnings, Constants, Parameters
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

    Warnings.not_complete()
    logged_in = requests.get(url=Constants.SERVER_IP_ADDRESS + "?user_name=" + _name + "&password=" + _password)
    if True:
        _name = username
        _password = password
    else:
        Warnings.not_complete()
        pass


def logout():
    global _name, _password

    _name = None
    _password = None

    Warnings.not_complete()


def get_name():
    global _name

    if _name is None:
        return ""
    return _name


def is_connected():
    # pings the server and retrieves the username which the user is logged in as
    Warnings.not_complete()
    return "Michael"


def is_logged_in():
    global _name

    return requests.get(url=Constants.SERVER_IP_ADDRESS)
