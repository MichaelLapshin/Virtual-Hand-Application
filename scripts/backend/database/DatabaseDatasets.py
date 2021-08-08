from scripts import Warnings, Constants, Log
from scripts.backend.database import Database


def create_new_dataset(name, owner_id, date, permission, fps):
    Log.info("Inserting a dataset entry: " + str((name, owner_id, date, permission, fps, 0, 0, 0, 0)))
    Database.cursor.execute("INSERT INTO Datasets VALUES (?, ?, ?, ?, ?)",
                            (name, owner_id, date, permission, fps, 0, 0, 0, 0))

    Warnings.not_complete()
    return True


def exists_dataset_by_name(name):
    Log.debug("Checking if the dataset with the name '" + name + "' exists.")
    Warnings.not_complete()


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
