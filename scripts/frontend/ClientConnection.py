"""
    Connection Handler used to interact with the server
"""
# import io
import tkinter

# import PIL.Image, PIL.ImageTk
import requests

from scripts import Warnings, Parameters, InputConstraints, Log, Constants, General
from scripts.backend.connection import API_Helper

"""
    Connection Variables
"""

# User variables
_user_id = None
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
    server_address: str
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
    url_values = ""
    for v in values.keys():
        url_values += "&" + str(v) + "=" + str(values[v])
    if len(url_values) > 0:
        url_values = "?" + url_values[1::]

    # Sends the get request if the server is online. Returns the boolean result
    if is_online:
        get_request = get_server_address() + url_extension + url_values
        Log.debug("Sending the get request: " + get_request)
        return process_response(requests.get(get_request), ovrd_ltst_msg=ovrd_ltst_msg)
    else:
        Log.warning("The server appears to be offline. Did not send the GET request to "
                    "'" + get_server_address() + url_extension + url_values + "'")
        return None


# def send_get_file_request(url_extension="", values={}):
#     is_online = is_server_online()
#
#     # Creates the variables
#     url_values = ""
#     for v in values.keys():
#         url_values += "&" + str(v) + "=" + str(values[v])
#     if len(url_values) > 0:
#         url_values = "?" + url_values[1::]
#
#     # Sends the get request if the server is online. Returns the boolean result
#     if is_online:
#         return requests.get(get_server_address() + url_extension + url_values)
#     else:
#         Log.warning("The server appears to be offline. Did not send the GET request to "
#                     "'" + get_server_address() + url_extension + url_values + "'")
#         return None


def send_post_request(url_extension="", file_to_send="", values={}, ovrd_ltst_msg=True):
    assert file_to_send is not None and len(file_to_send) != 0
    is_online = is_server_online()

    # Prepares and sends the file
    files = [(Constants.UPLOAD_KEY_WORD, (file_to_send, open(file_to_send, 'rb'), 'application/octet'))]

    # Compiles the url
    url_values = ""
    for k in values.keys():
        url_values += "&" + str(k) + "=" + str(values[k])
    if len(url_values) > 0:
        url_values = "?" + url_values[1::]

    # Sends the get request if the server is online. Returns the boolean result
    if is_online:
        return process_response(
            requests.post(get_server_address() + url_extension + url_values, files=files), ovrd_ltst_msg=ovrd_ltst_msg)
    else:
        Log.warning("The server appears to be offline. Did not send the POST request to "
                    "'" + get_server_address() + url_extension + url_values + "'")
        return None


def process_response(response, ovrd_ltst_msg=True):
    global latest_server_message, temp_message
    result = response.text
    Log.trace("The request result to process is: " + str(result))

    # Converts the string list to a list
    temp_message = None
    exec("temp_message = " + str(result), globals())
    assert temp_message is not None

    # Possibly overrides the latest server message
    if (ovrd_ltst_msg is True) and (temp_message[0] is not None):
        latest_server_message = str(temp_message[1])
        Log.debug("The new latest server message is: " + latest_server_message)

    if temp_message[0] is None:
        return temp_message[1]  # returns the values
    elif type(temp_message[0]) == bool:
        return temp_message[0]  # returns the boolean result
    else:
        Warnings.not_to_reach()
        return None


#
# def bytesIO_to_pil_image(bytesIO_stream) -> PIL.Image:
#     return PIL.Image.open(bytesIO_stream)
#
#
# def pil_image_to_photoImage(pil_image: PIL.Image) -> PIL.ImageTk:
#     return PIL.ImageTk.PhotoImage(pil_image)


"""
    User Management
"""


def log_in(user_name, password):
    global _user_id, _user_name, _password

    result = check_exists_user(user_name, password)

    if result is True:
        Log.info("Logged in as the user '" + user_name + "'.")
        _user_id = send_get_request("/account/get_user_id", {"user_name": user_name})
        _user_name = user_name
        _password = password
    return result


def log_out():
    global _user_name, _password
    Log.info("Logged out as the user '" + str(_user_name) + "'.")
    _user_id = None
    _user_name = None
    _password = None
    return True


def is_logged_in():
    global _user_id, _user_name, _password
    result = (_user_id is not None) and (_user_name is not None) and (_password is not None)
    Log.trace("Checking is the user is logged in. Returning: " + str(result))
    return result


def get_user_name():
    global _user_name
    # Log.trace("Fetched the user name '" + str(_user_name) + "'.")
    return _user_name


def get_user_id():
    global _user_id
    Log.trace("Fetched the user id '" + str(_user_id) + "'.")
    return _user_id


"""
    Account Management
"""


def get_all_user_names():
    Log.debug("Getting all user names from the database.")
    result = send_get_request("/fetch/all_user_names", ovrd_ltst_msg=False)
    Log.trace("Received the resulting user names: " + str(result))
    return result


def check_exists_user(user_name, password):
    Log.trace("Checking if the user named '" + user_name + "' exists with the password '" + password + "'.")
    result = send_get_request("/account/check_user", {"user_name": user_name, "password": password},
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

    result = send_get_request("/account/delete", {"user_name": user_name, "password": password})

    if result is True:
        Log.info("User named '" + user_name + "' with password '" + password + "' was successfully deleted.")
        return True
    else:
        Log.info("User named '" + user_name + "' with password '" + password + "' was not deleted.")
        return False


"""
    Entry Updating Management
"""


def update_dataset_entry(dataset_id, dataset_values):
    # Asserts that all send values are a part of the transfer list
    for k in dataset_values.keys():
        assert k in Constants.DATABASE_ENTRY_TRANSFER_DATA

    # Replaces the values
    for k in dataset_values.keys():
        dataset_values[k] = API_Helper.url_replacement_mapping(dataset_values.get(k))

    # Sends the information
    result = send_get_request("/update/dataset_entry", values={"id": dataset_id, "new_values": dataset_values})

    if result is True:
        Log.info("The dataset with the id '" + str(dataset_id) +
                 "' was successfully updated with the values: " + str(dataset_values))
        return True
    else:
        Log.info("The dataset with the id '" + str(dataset_id) +
                 "' failed to be updated with the values: " + str(dataset_values))
        return False


def update_model_entry(model_id, model_values):
    # Asserts that all send values are a part of the transfer list
    for k in model_values.keys():
        assert k in Constants.MODEL_ENTRY_TRANSFER_DATA

    # Replaces the values
    for k in model_values.keys():
        for r in Constants.URL_REPLACEMENT_MAP:
            model_values[k] = model_values.get(k).replace(r, Constants.URL_REPLACEMENT_MAP.get(r))

    # Sends the information
    result = send_get_request("/update/model_entry", values={"id": model_id, "new_values": model_values})

    if result is True:
        Log.info("The model with the id '" + model_id +
                 "' was successfully updated with the values: " + str(model_values))
        return True
    else:
        Log.info("The model with the id '" + model_id +
                 "' failed to be updated with the values: " + str(model_values))
        return False


"""
    Other Dataset Management
"""


# def duplicate_dataset_entry(dataset_id):
#     Log.info("Attempting to duplicate the dataset with the id '" + dataset_id + "'.")
#     result = send_get_request("/process/duplicate_dataset", {"id": dataset_id})
#
#     if result is True:
#         Log.info("The dataset with the id '" + dataset_id + "' was successfully duplicated.")
#     else:
#         Log.info("The dataset with the id '" + dataset_id + "' failed to duplicated.")
#     return result


def smooth_dataset(name, owner_id, date_created, access_perm_level, personal_rating, is_raw,
                   num_frames, frames_per_second,
                   dataset_id, frames_shift,
                   sensor_savagol_distance, sensor_savagol_degree,
                   angle_savagol_distance, angle_savagol_degree):
    Log.info("Attempting to smooth the dataset with the id '" + str(dataset_id) + "'. With: "
             + "\n              frames_shift=" + str(frames_shift)
             + "\n              sensor_savagol_distance=" + str(sensor_savagol_distance)
             + "\n              sensor_savagol_degree=" + str(sensor_savagol_degree)
             + "\n              angle_savagol_distance=" + str(angle_savagol_distance)
             + "\n              angle_savagol_degree=" + str(angle_savagol_degree))

    result = send_get_request("/process/smooth_dataset",
                              values={"name": name,
                                      "owner_id": owner_id,
                                      "date": date_created,
                                      "permission": access_perm_level,
                                      "rating": personal_rating,
                                      "is_raw": is_raw,
                                      "num_frames": num_frames,
                                      "FPS": frames_per_second,
                                      "parent_id": dataset_id,
                                      "frames_shift": frames_shift,
                                      "sensor_savagol_distance": sensor_savagol_distance,
                                      "sensor_savagol_degree": sensor_savagol_degree,
                                      "angle_savagol_distance": angle_savagol_distance,
                                      "angle_savagol_degree": angle_savagol_degree})
    if result is True:
        Log.info("The smoothing of dataset with id '" + str(dataset_id) + "' has begun.")
    else:
        Log.warning("The smoothing of dataset with id '" + str(dataset_id) + "' failed to begin.")


def merge_datasets(dataset_ids, dataset_name, dataset_owner_id, dataset_rating, dataset_fps):
    Log.info("Merging the datasets with ids: " + str(dataset_ids))

    result = send_get_request("/process/merge_datasets",
                              values={"dataset_ids": API_Helper.url_replacement_mapping(str(dataset_ids)),
                                      "name": API_Helper.url_replacement_mapping(dataset_name),
                                      "owner_id": dataset_owner_id,
                                      "rating": dataset_rating,
                                      "fps": dataset_fps})
    if result is True:
        Log.info("The datasets were successfully merged.")
        return True
    else:
        Log.info("The datasets were not successfully merged.")
        return False


"""
    Data Deletion Management
"""


def delete_dataset_entry(dataset_id):
    Log.info("Attempting to delete the dataset with the id '" + str(dataset_id) + "'.")
    result = send_get_request("/process/delete_dataset", {"id": dataset_id})
    if result is True:
        Log.info("The dataset with id '" + str(dataset_id) + "' was successfully deleted.")
        return True
    else:
        Log.warning("The dataset with id '" + str(dataset_id) + "' was not successfully deleted.")
        return False


"""
    File Transfer Management
"""


def upload_dataset(name, owner_id, date_created, access_perm_level, personal_rating, num_frames, frames_per_second):
    Log.info("Attempting to upload the dataset named '" + name + "'.")
    result = send_post_request(
        url_extension="/transfer/upload_dataset",
        file_to_send=Parameters.PROJECT_PATH + Constants.TEMP_DATASET_PATH + Constants.TEMP_SAVE_DATASET_NAME,
        values={"name": name,
                "owner_id": owner_id,
                "date": date_created,
                "permission": access_perm_level,
                "rating": personal_rating,
                "num_frames": num_frames,
                "FPS": frames_per_second})
    if result is True:
        Log.info("The dataset named '" + name + "' was successfully uploaded.")
        return True
    else:
        Log.info("The dataset named '" + name + "' failed to upload.")
        return False


"""
    Data Fetching Management
"""


def fetch_ordered_datasets(sort_by, direction, user_name):
    Log.info("Fetching ordered datasets list using the constraints: "
             "sort_by='" + sort_by + "', direction='" + direction + "', user_name='" + str(user_name) + "'.")

    result = send_get_request(
        url_extension="/fetch/sorted_datasets",
        values={"sort_by": sort_by,
                "direction": direction,
                "user_name": user_name},
        ovrd_ltst_msg=False)

    return result


def fetch_ordered_models(sort_by, direction, user_name):
    Log.info("Fetching ordered models list using the constraints: "
             "sort_by='" + sort_by + "', direction='" + direction + "', user_name='" + user_name + "'.")

    result = send_get_request(
        url_extension="/fetch/sorted_models",
        values={"sort_by": sort_by,
                "direction": direction,
                "user_name": user_name},
        ovrd_ltst_msg=False)

    return result


"""
    Image Fetching Management
"""


def fetch_dataset_finger_plot(dataset_id, finger, metric):
    Log.info("Fetching finger images for the dataset with id '" + str(dataset_id) + "'")

    result = send_get_request(
        url_extension="/transfer/get_dataset_finger_image",
        values={"dataset_id": dataset_id,
                "finger": finger,
                "metric": metric})

    return tkinter.PhotoImage(data=result)


def fetch_dataset_sensor_plot(dataset_id, sensor):
    Log.info("Fetching sensor images for the dataset with id '" + str(dataset_id) + "'")

    result = send_get_request(
        url_extension="/transfer/get_dataset_sensor_image",
        values={"dataset_id": dataset_id,
                "sensor": sensor})

    return tkinter.PhotoImage(data=result)
