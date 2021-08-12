"""
    Connection Handler used to interact with the server
"""
import requests

from scripts import Warnings, Parameters, InputConstraints, Log

Warnings.not_complete()

"""
    Connection Variables
"""

# User variables
_user_name = None
_password = None

latest_server_message = ""

"""
    General
"""


def get_server_address():
    return Parameters.SERVER_IP_ADDRESS + ":" + Parameters.SERVER_PORT


def is_server_online(ip_address=None, port=None):
    # Compiles the server address
    server_address = None
    if (ip_address is not None) and (port is not None):
        server_address = ip_address + ":" + port
    else:
        server_address = get_server_address()
    assert server_address is not None

    # Attempts to reach the server
    try:
        Log.debug("Checking if the server '" + server_address + "' is online.")
        result = process_response(requests.get(server_address + "/is_online"), ovrd_ltst_msg=False)
        Log.debug("The server '" + server_address + "' was reached.")
        return result
    except:
        Log.debug("The server '" + server_address + "' was not reached.")
        return False


def send_get_request(url_extension="", values={}, ovrd_ltst_msg=True):
    is_online = is_server_online()

    # Creates the variables
    values_ext = ""
    for v in values.keys():
        values_ext += "&" + str(v) + "=" + str(values[v])
    if len(values_ext) != 0:
        values_ext = values_ext[1::]
        values_ext = "?" + values_ext

    # Sends the get request if the server is online. Returns the boolean result
    if is_online:
        return process_response(requests.get(get_server_address() + url_extension + values_ext),
                                ovrd_ltst_msg=ovrd_ltst_msg)
    else:
        Log.warning("The server appears to be offline. Did not send the get request "
                    "'" + get_server_address() + url_extension + values_ext + "'")
        return None


def process_response(response, ovrd_ltst_msg=True):
    global latest_server_message, temp_message
    result = response.text

    # Converts the string list to a list
    temp_message = None
    exec("temp_message = " + result, globals())
    assert temp_message is not None

    # Possibly overrides the latest server message
    if ovrd_ltst_msg is True:
        latest_server_message = temp_message
        Log.debug("The new latest server message is: " + str(latest_server_message))

    return temp_message[0]  # returns the boolean result


"""
    User Management
    
"""


def log_in(user_name, password):
    global _user_name, _password

    result = check_exists_user(user_name, password)

    if result is True:
        Log.info("Logged in as the user '" + user_name + "'.")
        _user_name = user_name
        _password = password
    return result


def log_out():
    global _user_name, _password
    Log.info("Logged out as the user '" + str(_user_name) + "'.")
    _user_name = None
    _password = None
    return True


def is_logged_in():
    global _user_name, _password
    result = (_user_name is not None) and (_password is not None)
    Log.trace("Checking is the user is logged in. Returning: " + str(result))
    return result


def get_user_name():
    global _user_name
    Log.trace("Fetched the user name '" + str(_user_name) + "'.")
    return _user_name


"""
    Account Management
"""


def check_exists_user(user_name, password):
    Log.trace("Checking if the user named '" + user_name + "' exists with the password '" + password + "'.")
    result = send_get_request("/account/exists_user", {"user_name": user_name, "password": password},
                              ovrd_ltst_msg=False)
    if result is True:
        Log.trace("The user exists.")
    else:
        Log.trace("The user does not exist.")
    return result


def create_user(user_name, password):
    Log.info("Attempting to create a new user '" + user_name + "' with password '" + password + "'.")

    is_created = send_get_request("/account/create", {"user_name": user_name, "password": password})

    if is_created is True:
        Log.info("User named '" + user_name + "' with password '" + password + "' was successfully created.")
        return True
    else:
        Log.info("User named '" + user_name + "' with password '" + password + "' failed to be created.")
        return False


def delete_user(user_name, password):
    Log.info("Attempting to delete the user named '" + user_name + "' with password '" + password + "'.")

    is_created = send_get_request("/account/delete", {"user_name": user_name, "password": password})

    if is_created is True:
        Log.info("User named '" + user_name + "' with password '" + password + "' was successfully deleted.")
        return True
    else:
        Log.info("User named '" + user_name + "' with password '" + password + "' was not deleted.")
        return False


"""
    File Transfer Management
"""


def upload_dataset(self, dataset_name):
    Warnings.not_complete()
