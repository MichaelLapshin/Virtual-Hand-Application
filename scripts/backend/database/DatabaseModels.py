from scripts import Warnings, Log, Constants, General
from scripts.backend.database import Database
from scripts.backend.logic.Worker import model_worker


def get_all_models():
    Log.debug("Retrieving all models.")
    Database.cursor.execute("SELECT * FROM Models")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result

def update_model_entry(model_id, new_values):
    Log.info("Updating the model with id '" + str(model_id) + "' with the new values: " + str(new_values))
    try:
        Database.cursor.execute(
            "UPDATE Models SET " + General.dict_to_sql_update_features(new_values) + " WHERE ID=" + str(model_id))
        Database.connection.commit()
        Log.debug("Successfully updated and commit the changes to the model with id '" + str(model_id) + "'.")
        return True
    except:
        Log.debug("Was not successful in updating the values to the model with id '" + str(model_id) + "'.")
        return False



def fetch_ordered_models(sort_by="Name", direction="ASC", user_id=None):
    Log.info("Fetching a set of models for the user id:'" + str(user_id) +
             "'. Executing " + direction + " sorting on the column " + sort_by + ".")

    # Fetching the ordered data
    Database.cursor.execute(
        "SELECT " + General.list_to_sql_select_features(Constants.MODEL_ENTRY_TRANSFER_DATA)
        + " FROM Models WHERE ID_Owner = " + str(user_id) + " or "
        + "Permission <= " + str(Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC))
        + " ORDER BY " + sort_by + " " + direction)
    results = Database.cursor.fetchall()

    # Returning results
    Log.debug("Returning the results: " + str(results))
    return results
