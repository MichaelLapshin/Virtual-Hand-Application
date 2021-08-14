from scripts import Warnings, Constants, Log
from scripts.backend.database import Database


def get_all_datasets():
    Log.debug("Retrieving all datasets.")
    Database.cursor.execute("SELECT * FROM Datasets")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result


def create_new_dataset(name, owner_id, date, permission, fps):
    Log.info("Inserting a dataset entry: " + str((name, owner_id, date, permission, fps, 0, 0, 0, 0)))
    Database.cursor.execute("INSERT INTO Datasets VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                            (name, owner_id, date, permission, fps, 0, 0, 0, 0))
    Database.connection.commit()
    Warnings.not_complete()
    return True


def exists_dataset_by_name(dataset_name):
    Log.info("Checking if a dataset exists with the name '" + dataset_name + "'.")
    Database.cursor.execute("SELECT * FROM Datasets WHERE Name='" + dataset_name + "'")

    # Checks the number of datasets found with the given user name
    num_datasets = len(Database.cursor.fetchall())
    Log.debug("Found " + str(num_datasets) + " datasets with the name '" + dataset_name + "'.")

    if num_datasets == 1:
        Log.info("Found the dataset with the name '" + dataset_name + "'.")
        return True
    elif num_datasets == 0:
        Log.info("Did not find the dataset with the name '" + dataset_name + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of datasets with the name '" + dataset_name + "'.")
        Warnings.not_to_reach()
        return True


def fetch_ordered_datasets(sort_by="Name", direction="ASC", user_id=None):
    Log.info("Fetching a set of datasets for the user id:'" + user_id +
             "'. Executing " + direction + " sorting on the column " + sort_by + ".")

    # Fetching the ordered data
    Database.cursor.execute("SELECT * FROM Datasets WHERE ID_Owner = " + str(user_id) + " or "
                            + "Permission <=" + str(Constants.PERMISSION_LEVELS[Constants.PERMISSION_PUBLIC])
                            + " ORDER BY " + sort_by + " " + direction)
    results = Database.cursor.fetchall()

    # Returning results
    Log.debug("Returning the results: " + str(results))
    return results


def get_graphs():
    Warnings.not_complete()
    return None
