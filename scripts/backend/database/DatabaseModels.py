import os, shutil

from scripts import Log, Constants, General, Parameters, Warnings
from scripts.backend.database import Database
from scripts.logic import Worker


def get_all_models():
    Log.debug("Retrieving all models.")
    Database.cursor.execute("SELECT * FROM Models")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result


def update_model_entry(model_id: int, new_values: dict):
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


def create_new_model(name: str, owner_id: int, date_created: str, permission: int, rating: int,
                     dataset_id: int, frames_shift: int,
                     num_training_frames: int, learning_rate: float,
                     batch_size: int, num_epochs: int,
                     layer_type: str, num_layers: int, num_nodes_per_layer: int):
    # Prepares the data
    input_data = (name, owner_id, date_created, permission, rating, dataset_id, frames_shift, num_training_frames,
                  learning_rate, batch_size, num_epochs, layer_type, num_layers, num_nodes_per_layer)
    Log.info("Inserting a model entry: " + str(input_data))

    # Create new dataset
    Database.cursor.execute("INSERT INTO Models VALUES (NULL, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", input_data)
    Database.connection.commit()

    # Obtains the ID of the new dataset
    # TODO, Warning: can cause problem with multiple users since lastworid returns id for the cursor (cursor is shared)
    model_id = Database.cursor.lastrowid
    Log.debug("Create a model entry with the id '" + str(model_id) + "'")

    return model_id


def exists_dataset_by_id(model_id: int):
    Log.info("Checking if a model exists with the id '" + str(model_id) + "'.")
    Database.cursor.execute("SELECT * FROM Models WHERE ID='" + str(model_id) + "'")

    # Checks the number of datasets found with the given user name
    num_models = len(Database.cursor.fetchall())
    Log.debug("Found " + str(num_models) + " models with the id '" + str(model_id) + "'.")

    if num_models == 1:
        Log.info("Found the model with the name '" + str(model_id) + "'.")
        return True
    elif num_models == 0:
        Log.info("Did not find the model with the name '" + str(model_id) + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of models with the name '" + str(model_id) + "'.")
        Warnings.not_to_reach(popup=False)
        return True


def fetch_ordered_models(sort_by="Name", direction="ASC", user_id="NULL"):
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


def delete_model(model_id: int):
    """
    Deletes the model. Soft deletes its presence in other objects which used it.
    :param model_id:
    :return: True, the model was deleted
    """
    Log.info("Deleting the model with id '" + str(model_id) + "'")

    # Delete the model directories and files
    shutil.rmtree(Parameters.PROJECT_PATH + Constants.SERVER_MODEL_PATH + Constants.MODEL_DIR + str(model_id))

    # Delete the errors images
    Database.cursor.execute("SELECT ID FROM ModelErrorPlots WHERE ID_Model=" + str(model_id))
    error_ids = Database.cursor.fetchall()
    for e in error_ids:
        os.remove(
            Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_ERRORS_PATH + str(e[0]) + Constants.IMAGE_EXT)

    # Delete the errors images
    Database.cursor.execute("SELECT ID FROM ModelPredictionPlots WHERE ID_Model=" + str(model_id))
    prediction_ids = Database.cursor.fetchall()
    for p in prediction_ids:
        os.remove(
            Parameters.PROJECT_PATH + Constants.SERVER_IMAGES_MODELS_PREDICTIONS_PATH + str(p[0]) + Constants.IMAGE_EXT)

    # Delete the database entries related to the dataset
    Database.cursor.execute("DELETE FROM Models WHERE ID=" + str(model_id))
    Database.cursor.execute("DELETE FROM ModelErrorPlots WHERE ID_Model=" + str(model_id))
    Database.cursor.execute("DELETE FROM ModelPredictionPlots WHERE ID_Model=" + str(model_id))

    # Saves the changes
    Database.connection.commit()
    return True
