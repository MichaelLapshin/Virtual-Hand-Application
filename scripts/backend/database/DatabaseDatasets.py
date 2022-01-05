import os

from scripts import Warnings, Constants, Log, General, Parameters
from scripts.backend.database import Database
from scripts.backend.logic import DatasetPlotter
from scripts.logic import Worker


def get_all_datasets():
    Log.info("Retrieving all datasets.")
    Database.cursor.execute("SELECT * FROM Datasets")
    result = Database.cursor.fetchall()
    Log.debug("Retrieved: " + str(result))
    return result


def update_dataset_entry(dataset_id: int, new_values: dict):
    Log.info("Updating the dataset with id '" + str(dataset_id) + "' with the new values: " + str(new_values))
    try:
        Database.cursor.execute(
            "UPDATE Datasets SET " + General.dict_to_sql_update_features(new_values) + " WHERE ID=" + str(dataset_id))
        Database.connection.commit()
        Log.debug("Successfully updated and commit the changes to the dataset with id '" + str(dataset_id) + "'.")
        return True
    except:
        Log.debug("Was not successful in updating the values to the dataset with id '" + str(dataset_id) + "'.")
        return False


def create_new_dataset(name, owner_id, date_created, permission, rating, num_frames, fps,                       is_raw=True,
                       sensor_savagol_distance=0, sensor_savagol_degree=0,
                       angle_savagol_distance=0, angle_savagol_degree=0):
    """
    Creates a dataset entry
    :return: ID of the new dataset entry
    """

    # Prepares the data
    input_data = (name, owner_id, date_created, permission, rating, is_raw, num_frames, fps,
                  sensor_savagol_distance, sensor_savagol_degree,
                  angle_savagol_distance, angle_savagol_degree)
    Log.info("Inserting a dataset entry: " + str(input_data))

    # Create new dataset
    Database.cursor.execute("INSERT INTO Datasets VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", input_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastworid returns id for the cursor (cursor is shared)
    dataset_id = Database.cursor.lastrowid
    Log.debug("Created a dataset entry with the id '" + str(dataset_id) + "'")
    return dataset_id


def exists_dataset_by_id(dataset_id: int):
    Log.info("Checking if a dataset exists with the id '" + str(dataset_id) + "'.")
    Database.cursor.execute("SELECT * FROM Datasets WHERE ID='" + str(dataset_id) + "'")

    # Checks the number of datasets found with the given user name
    num_datasets = len(Database.cursor.fetchall())
    Log.debug("Found " + str(num_datasets) + " datasets with the id '" + str(dataset_id) + "'.")

    if num_datasets == 1:
        Log.info("Found the dataset with the name '" + str(dataset_id) + "'.")
        return True
    elif num_datasets == 0:
        Log.info("Did not find the dataset with the name '" + str(dataset_id) + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of datasets with the name '" + str(dataset_id) + "'.")
        Warnings.not_to_reach(popup=False)
        return True


def fetch_ordered_datasets(sort_by="Name", direction="ASC", user_id="NULL"):
    Log.info("Fetching a set of datasets for the user id:'" + str(user_id) +
             "'. Executing " + direction + " sorting on the column " + sort_by + ".")

    # Fetching the ordered data
    Database.cursor.execute(
        "SELECT " + General.list_to_sql_select_features(Constants.DATASET_ENTRY_TRANSFER_DATA)
        + " FROM Datasets WHERE ID_Owner=" + str(user_id) + " or "
        + "Permission<=" + str(Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC))
        + " ORDER BY " + sort_by + " " + direction)
    results = Database.cursor.fetchall()

    # Returning results
    Log.debug("Returning the results: " + str(results))
    return results


def delete_dataset(dataset_id: int):
    """
    Deletes the dataset. Soft deletes its presence in other objects which used it.
    :param dataset_id:
    :return: True, the dataset was deleted
    """
    Log.info("Deleting the dataset with id '" + str(dataset_id) + "'")

    # Delete the database file
    os.remove(Parameters.PROJECT_PATH + Constants.SERVER_DATASET_PATH + str(dataset_id) + Constants.DATASET_EXT)

    # Delete the finger images
    Database.cursor.execute("SELECT ID FROM DatasetFingerPlots WHERE ID_Dataset=" + str(dataset_id))
    finger_ids = Database.cursor.fetchall()

    for f in finger_ids:
        os.remove(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_FINGERS_PATH
                  + str(f[0]) + Constants.IMAGE_EXT)

    # Delete the sensor images
    Database.cursor.execute("SELECT ID FROM DatasetSensorPlots WHERE ID_Dataset=" + str(dataset_id))
    sensor_ids = Database.cursor.fetchall()

    for s in sensor_ids:
        os.remove(Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_DATASETS_SENSORS_PATH
                  + str(s[0]) + Constants.IMAGE_EXT)

    # Delete the database entries related to the dataset
    Database.cursor.execute("DELETE FROM Datasets WHERE ID=" + str(dataset_id))
    Database.cursor.execute("DELETE FROM DatasetDependencies WHERE ID_Dataset=" + str(dataset_id))
    Database.cursor.execute("DELETE FROM DatasetFingerPlots WHERE ID_Dataset=" + str(dataset_id))
    Database.cursor.execute("DELETE FROM DatasetSensorPlots WHERE ID_Dataset=" + str(dataset_id))

    # If it is a dependency for another dataset, then replace it with Constants.DATABASE_DELETED_ID
    Database.cursor.execute("UPDATE DatasetDependencies SET ID_Dependency=" + str(Constants.DATABASE_DELETED_ID)
                            + " WHERE ID_Dependency=" + str(dataset_id))
    Database.cursor.execute("UPDATE Models SET ID_Dataset=" + str(Constants.DATABASE_DELETED_ID)
                            + " WHERE ID_Dataset=" + str(dataset_id))

    # Saves the changes
    Database.connection.commit()
    return True
