import pathlib

import PIL

from scripts import Warnings, Constants, Log, General, Parameters
from scripts.backend.database import Database

"""
    All functions return the id of the dataset that was just created
"""

"""
    Datasets
"""


def create_dataset_sensor_image_entry(dataset_id: int, sensor_num: int):
    info_data = (dataset_id, sensor_num)
    Log.info("Inserting a dataset sensor image entry: " + str(info_data))

    # Create new dataset
    Database.cursor.execute("INSERT INTO DatasetSensorPlots VALUES (NULL, ?, ?)", info_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Created a dataset sensor image entry with the id '" + str(image_id) + "'")

    return image_id


def create_dataset_finger_image_entry(dataset_id: int, finger_num: int, metric: int):
    info_data = (dataset_id, finger_num, metric)
    Log.info("Inserting a dataset finger image entry: " + str(info_data))

    # Create new dataset
    Database.cursor.execute("INSERT INTO DatasetFingerPlots VALUES (NULL, ?, ?, ?)", info_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Created a dataset finger image entry with the id '" + str(image_id) + "'")

    return image_id


# Get finger images
def get_dataset_finger_image_id(dataset_id: int, finger_num: int, metric_num: int):
    Log.info("Getting the finger image id of the dataset with id '" + str(dataset_id) + "', finger num of '" +
             str(finger_num) + "', and metric '" + str(metric_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM DatasetFingerPlots WHERE ID_Dataset=" + str(dataset_id) +
                            " AND Finger=" + str(finger_num) + " AND Metric=" + str(metric_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) == 0:
        return None
    elif len(ids) > 1:
        Log.error(
            "Using the inputs: " + str((dataset_id, finger_num, metric_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_dataset_finger_image_file_path(dataset_id: int, finger_num: int, metric_num: int):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH \
           + str(get_dataset_finger_image_id(dataset_id=dataset_id, finger_num=finger_num, metric_num=metric_num)) \
           + Constants.IMAGE_EXT


# Get sensor images
def get_sensor_image_id(dataset_id: int, sensor_num: int):
    Log.info("Getting the sensor image id of the dataset with id '" + str(dataset_id) + "' and sensor_num num of '" +
             str(sensor_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM DatasetSensorPlots WHERE ID_Dataset=" + str(dataset_id) +
                            " AND Sensor=" + str(sensor_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) == 0:
        return None
    elif len(ids) > 1:
        Log.error(
            "Using the inputs: " + str((dataset_id, sensor_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_sensor_image_file_path(dataset_id: int, sensor_num: int):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH \
           + str(get_sensor_image_id(dataset_id=dataset_id, sensor_num=sensor_num)) + Constants.IMAGE_EXT


"""
    Models
"""


def create_model_error_image_entry(model_id: int, finger_index: int, limb_index: int):
    info_data = (model_id, finger_index, limb_index)
    Log.info("Inserting a model error image entry: " + str((model_id, finger_index, limb_index)))

    # Create new dataset
    Database.cursor.execute("INSERT INTO ModelErrorPlots VALUES (NULL, ?, ?, ?)", info_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Created a model error image entry with the id '" + str(image_id) + "'")

    return image_id


def create_model_prediction_image_entry(model_id: int, finger_index: int, limb_index: int):
    info_data = (model_id, finger_index, limb_index)
    Log.info("Inserting a model prediction image entry: " + str((model_id, finger_index, limb_index)))

    # Create new dataset
    Database.cursor.execute("INSERT INTO ModelPredictionPlots VALUES (NULL, ?, ?, ?)", info_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Created a model prediction image entry with the id '" + str(image_id) + "'")

    return image_id


# Get prediction images
def get_model_prediction_image_id(model_id: int, finger_num: int, limb_num: int):
    Log.info("Getting the prediction image id of the model with id '" + str(model_id) + "', finger num of '" +
             str(finger_num) + "', and limb_num '" + str(limb_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM ModelPredictionPlots WHERE ID_Model=" + str(model_id) +
                            " AND Finger=" + str(finger_num) + " AND Limb=" + str(limb_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) == 0:
        return None
    elif len(ids) > 1:
        Log.error(
            "Using the inputs: " + str((model_id, finger_num, limb_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_model_prediction_image_file_path(model_id: int, finger_num: int, limb_num: int):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_PREDICTIONS_PATH \
           + str(get_model_prediction_image_id(model_id=model_id, finger_num=finger_num, limb_num=limb_num)) \
           + Constants.IMAGE_EXT


# Get error images
def get_model_error_image_id(model_id: int, finger_num: int, limb_num: int):
    Log.info("Getting the error image id of the model with id '" + str(model_id) + "', finger num of '" +
             str(finger_num) + "', and limb_num '" + str(limb_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM ModelErrorPlots WHERE ID_Model=" + str(model_id) +
                            " AND Finger=" + str(finger_num) + " AND Limb=" + str(limb_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) == 0:
        return None
    elif len(ids) > 1:
        Log.error(
            "Using the inputs: " + str((model_id, finger_num, limb_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_model_error_image_file_path(model_id: int, finger_num: int, limb_num: int):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_ERRORS_PATH \
           + str(get_model_error_image_id(model_id=model_id, finger_num=finger_num, limb_num=limb_num)) \
           + Constants.IMAGE_EXT
