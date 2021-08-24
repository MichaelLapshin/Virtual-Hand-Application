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
    # TODO, Warning: can cause problem with multiple users since lastworid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Create a dataset sensor image entry with the id '" + str(image_id) + "'")

    # Saves the file locally
    if file is not None:
        file.save(fp=Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH
                     + str(image_id) + Constants.IMAGE_EXT)
    else:
        Log.warning("A dataset sensor image entry with id '" + str(image_id) + "' is being saved without a file.")
    return True


def create_dataset_finger_image_entry(dataset_id, finger_num, metric, file=None):
    Log.info("Inserting a dataset finger image entry: " + str((dataset_id, finger_num, metric)))

    # Create new dataset
    Database.cursor.execute("INSERT INTO DatasetFingerPlots VALUES (NULL, ?, ?, ?)", (dataset_id, finger_num, metric))
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastworid returns id for the cursor (cursor is shared)
    image_id = Database.cursor.lastrowid
    Log.debug("Create a dataset finger image entry with the id '" + str(image_id) + "'")

    # Saves the file locally
    if file is not None:
        file.save(fp=Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH
                     + str(image_id) + Constants.IMAGE_EXT)
    else:
        Log.warning("A dataset finger image entry with id '" + str(image_id) + "' is being saved without a file.")
    return True
