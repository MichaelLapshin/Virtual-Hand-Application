from scripts import Warnings, Log
from scripts.backend.database import Database


def get_all_models():
    Log.debug("Retrieving all models.")
    Database.cursor.execute("SELECT * FROM Models")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result
