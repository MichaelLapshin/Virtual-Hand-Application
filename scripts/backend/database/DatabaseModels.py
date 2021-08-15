from scripts import Warnings, Log, Constants, General
from scripts.backend.database import Database


def get_all_models():
    Log.debug("Retrieving all models.")
    Database.cursor.execute("SELECT * FROM Models")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result


def fetch_ordered_models(sort_by="Name", direction="ASC", user_id=None):
    Log.info("Fetching a set of models for the user id:'" + str(user_id) +
             "'. Executing " + direction + " sorting on the column " + sort_by + ".")

    # Fetching the ordered data
    Database.cursor.execute(
        "SELECT " + General.list_to_sql_select_features(Constants.MODEL_DATA_TO_FETCH)
        + " FROM Models WHERE ID_Owner = " + str(user_id) + " or "
        + "Permission <= " + str(Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC))
        + " ORDER BY " + sort_by + " " + direction)
    results = Database.cursor.fetchall()

    # Returning results
    Log.debug("Returning the results: " + str(results))
    return results
