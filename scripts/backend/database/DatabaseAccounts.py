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


def get_user_id(user_name):
    Log.debug("Getting the ID of a user named '" + user_name + "'.")
    Database.cursor.execute("SELECT ID FROM Users WHERE Name='" + user_name + "'")

    # Obtain the user ID
    id = int(Database.cursor.fetchone()[0])
    Log.info("Retrieved the ID '" + str(id) + "' for the user named '" + user_name + "'")
    return id


def exists_user_by_id(user_id):
    Log.info("Checking if a user exists with the ID '" + user_id + "'.")
    Database.cursor.execute("SELECT ID FROM Users WHERE rowid=" + str(user_id))

    # Checks the number of users found with the given user ID
    result = Database.cursor.fetchall()
    num_users = len(result)
    Log.debug("Found " + str(num_users) + " users with the ID '" + user_id + "'.")

    if num_users == 1:
        Log.info("Found the user with the ID '" + user_id + "'.")
        return True
    elif num_users == 0:
        Log.info("Did not find the user with the ID '" + user_id + "'.")
        return False
    else:
        Log.warning("Found multiple occurrences of the user with the ID '" + user_id + "'.")
        Warnings.not_to_reach()
        return True


def exists_user_by_name(user_name):
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
        Warnings.not_to_reach()
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

    assert (permission == 0) or (permission == 1)
    assert exists_user_by_name(user_name) is False

    # Creates a user
    Database.cursor.execute("INSERT INTO Users VALUES (NULL, ?,?,?,?,?)", (user_name, password, permission, None, None))
    Database.connection.commit()

    Log.debug("The insertion of the new user entry has been committed to the database.")

    if exists_user_by_name(user_name) is True:
        Log.info("The user has been successfully created.")
        return True
    else:
        Log.info("The user has not been successfully created.")
        return False


def delete_user(user_name, password):
    """
    Deletes the user. Transfers all possessions to the Admin user.
    :param user_name: the user
    :param password: the password
    """

    Log.debug("Deleting the user '" + user_name + "' from the database. Using the password '" + password + "'.")

    assert check_user(user_name=user_name, password=password) is True

    # Deletes the user
    Database.cursor.execute("DELETE FROM Users WHERE Name='" + user_name + "' and Password='" + password + "'")
    Database.connection.commit()

    Log.info("Deleted the user '" + user_name + "'.")
