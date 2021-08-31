import pathlib

import PIL

from scripts import Warnings, Constants, Log, General, Parameters
from scripts.backend.database import Database

"""
    All functions return the id of the dataset that was just created
"""


def create_dataset_sensor_image_entry(dataset_id, sensor_num, file=None):
    Log.info("Inserting a dataset sensor image entry: " + str((dataset_id, sensor_num)))

    # Create new dataset
    Database.cursor.execute("INSERT INTO DatasetSensorPlots VALUES (NULL, ?, ?)", (dataset_id, sensor_num))
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Create a dataset sensor image entry with the id '" + str(image_id) + "'")

    # Saves the file locally
    if file is not None:
        file.save(pathlib.Path(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH
                               + str(image_id) + Constants.IMAGE_EXT))
        file.close()
    else:
        Log.warning("A dataset sensor image entry with id '" + str(image_id) + "' is being saved without a file.")
    return True


def create_dataset_finger_image_entry(dataset_id, finger_num, metric, file=None):
    Log.info("Inserting a dataset finger image entry: " + str((dataset_id, finger_num, metric)))

    # Create new dataset
    Database.cursor.execute("INSERT INTO DatasetFingerPlots VALUES (NULL, ?, ?, ?)", (dataset_id, finger_num, metric))
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastrowid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Create a dataset finger image entry with the id '" + str(image_id) + "'")

    # Saves the file locally
    if file is not None:
        file.save(pathlib.Path(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH
                               + str(image_id) + Constants.IMAGE_EXT))
        file.close()
    else:
        Log.warning("A dataset finger image entry with id '" + str(image_id) + "' is being saved without a file.")
    return True


# Get finger images
def get_finger_image_id(dataset_id, finger_num, metric_num):
    Log.info("Getting the finger image id of the dataset with id '" + str(dataset_id) + "', finger num of '" +
             str(finger_num) + "', and metric '" + str(metric_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM DatasetFingerPlots WHERE ID_Dataset=" + str(dataset_id) +
                            " AND Finger=" + str(finger_num) + " AND Metric=" + str(metric_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) != 1:
        Log.error(
            "Using the inputs: " + str((dataset_id, finger_num, metric_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_finger_image_file_path(dataset_id, finger_num, metric_num):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH \
           + str(get_finger_image_id(dataset_id=dataset_id, finger_num=finger_num, metric_num=metric_num)) \
           + Constants.IMAGE_EXT


# Get sensor images
def get_sensor_image_id(dataset_id, sensor_num):
    Log.info("Getting the sensor image id of the dataset with id '" + str(dataset_id) + "' and sensor_num num of '" +
             str(sensor_num) + "'.")

    # Gets the id of the finger image
    Database.cursor.execute("SELECT ID FROM DatasetSensorPlots WHERE ID_Dataset=" + str(dataset_id) +
                            " AND Sensor=" + str(sensor_num))
    ids = Database.cursor.fetchall()

    Log.trace("Found the ids: " + str(ids))

    if len(ids) != 1:
        Log.error(
            "Using the inputs: " + str((dataset_id, sensor_num)) + ", found " + str(len(ids)) + " ids.")
        Warnings.not_to_reach(popup=False)
        return None
    else:
        Log.info("Found the finger image id '" + str(ids[0][0]) + "'")
        return int(ids[0][0])


def get_sensor_image_file_path(dataset_id, sensor_num):
    return Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH \
           + str(get_sensor_image_id(dataset_id=dataset_id, sensor_num=sensor_num)) + Constants.IMAGE_EXT
