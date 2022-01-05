from scripts import Warnings, Log, Constants
from scripts.backend.database import Database

"""
    All database functions return a boolean value as for whether the operation or check was successful or not
"""


def get_user_name_list():
    Log.debug("Retrieving all user names.")
    Database.cursor.execute("SELECT Name FROM Users")
    temp_result = Database.cursor.fetchall()

    # Compiles the list of user names
    result = []
    for r in temp_result:
        result.append(r[0])

    Log.trace("Retrieved: " + str(result))
    return result


def get_all_account():
    Log.debug("Retrieving all user accounts.")
    Database.cursor.execute("SELECT * FROM Users")
    result = Database.cursor.fetchall()
    Log.trace("Retrieved: " + str(result))
    return result


def get_user_id(user_name: str, password: str) -> int:
    Log.debug("Getting the ID of a user named '" + user_name + "'.")
    Database.cursor.execute("SELECT ID FROM Users WHERE Name='" + user_name + "' and Password='" + password + "'")

    fetched_data = Database.cursor.fetchall()

    if len(fetched_data) <= 0:
        return -1

    # Obtain the user ID
    id = int(fetched_data[0][0])
    Log.info(
        "Retrieved the ID '" + str(id) + "' for the user named '" + user_name + "' with password '" + password + "'")
    return id


def get_user_name(user_id: int) -> str:
    Log.debug("Getting the name of a user with id '" + str(user_id) + "'.")
    Database.cursor.execute("SELECT Name FROM Users WHERE ID=" + str(user_id))

    fetched_data = Database.cursor.fetchall()

    if len(fetched_data) <= 0:
        return -1

    # Obtain the user name
    name = fetched_data[0][0]
    Log.info("Retrieved the name '" + name + "' for the user with id '" + str(user_id) + "'")
    return name


def exists_user_by_id(user_id: int):
    Log.info("Checking if a user exists with the ID '" + str(user_id) + "'.")
    Database.cursor.execute("SELECT ID FROM Users WHERE ID=" + str(user_id))

    # Checks the number of users found with the given user ID
    result = Database.cursor.fetchall()
    num_users = len(result)
    Log.debug("Found " + str(num_users) + " users with the ID '" + str(user_id) + "'.")

    if num_users == 1:
        Log.info("Found the user with the ID '" + str(user_id) + "'.")
        return True
    elif num_users == 0:
        Log.info("Did not find the user with the ID '" + str(user_id) + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of the user with the ID '" + str(user_id) + "'.")
        Warnings.not_to_reach()
        return True


def exists_user_by_name(user_name: str):
    Log.info("Checking if a user exists with the name '" + user_name + "'.")
    Database.cursor.execute("SELECT * FROM Users WHERE Name='" + user_name + "'")

    # Checks the number of users found with the given user name
    num_users = len(Database.cursor.fetchall())
    Log.debug("Found " + str(num_users) + " users with the name '" + user_name + "'.")

    if num_users == 1:
        Log.info("Found the user with the name '" + user_name + "'.")
        return True
    elif num_users == 0:
        Log.info("Did not find the user with the name '" + user_name + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of the user with the name '" + user_name + "'.")
        Warnings.not_to_reach()
        return True


def check_user(user_name, password):
    Log.info("Checking if the user exists with the name '" + user_name + "' and password '" + password + "'.")

    assert exists_user_by_name(user_name=user_name) is True

    Database.cursor.execute("SELECT ID FROM Users WHERE Name='" + user_name + "' and Password='" + password + "'")

    # Checks the number of users found with the given username/password
    num_users = len(Database.cursor.fetchall())
    Log.debug("Found " + str(num_users) + " users matching the credentials.")
    if num_users == 1:
        Log.info("A user matching the credentials has been found.")
        return True
    elif num_users == 0:
        Log.info("A user matching the credentials has not been found.")
        return False
    else:
        Log.warning("Multiple users matching the credentials have been found.")
        Warnings.not_to_reach(popup=False)
        return True


def add_user(user_name, password, permission=Constants.PERMISSION_LEVELS.get(Constants.PERMISSION_PUBLIC)):
    """
    Creates and adds a new user to the database.
    :param user_name: name
    :param password: password
    :param permission: 0=basic user, 1=admin user
    :return: whether a user has been successfully committed to the database or not
    """

    Log.info("Adding a new user to the database with the credentials: Name='" + user_name +
             "', Password='" + password + "', Permission='" + str(permission) + "'")

    assert permission in Constants.PERMISSION_LEVELS.values()
    assert exists_user_by_name(user_name) is False

    # Creates a user
    Database.cursor.execute("INSERT INTO Users VALUES (NULL, ?,?,?)", (user_name, password, permission))
    Database.connection.commit()

    Log.debug("The insertion of the new user entry has been committed to the database.")

    if exists_user_by_name(user_name) is True:
        Log.info("The user has been successfully created.")
        return True
    else:
        Log.info("The user has not been successfully created.")
        return False


def delete_user(user_id):
    """
    Deletes the user. Soft deletes all owned objects
    :param user_id: user with user_id to delete
    """

    Log.debug("Deleting the user with id '" + str(user_id) + "' from the database.")

    assert exists_user_by_id(user_id=user_id) is True

    # Deletes the user
    Database.cursor.execute("DELETE FROM Users WHERE ID=" + str(user_id))

    # Soft deletes all objects with owner id (replace with Constants.DATABASE_DELETED_ID)
    Database.cursor.execute("UPDATE Datasets SET ID_Owner=" + str(Constants.DATABASE_DELETED_ID)
                            + " WHERE ID_Owner=" + str(user_id))
    Database.cursor.execute("UPDATE Models SET ID_Owner=" + str(Constants.DATABASE_DELETED_ID)
                            + " WHERE ID_Owner=" + str(user_id))

    # Saves the changes
    Database.connection.commit()

    Log.info("Deleted the user with id '" + str(user_id) + "'.")
    return True
