import sqlite3

from scripts import Warnings, Constants, Log, Parameters

"""
Tables:
- Users
    + ID_Self: id
    + Name: name
    + Password: password
    + Permission: permission level (0 = basic user, 1 = admin)
    + ID_Models: access to which models
    + ID_Datasets: access to which datasets
- Models
    ~ General Information:
        + Name: name
        + ID_Self: id #
        + ID_Owner: id # of owner
        + Date_Created: date created
        + View_Domain: viewing permissions level (0 = everyone owns it, 1 = others can view, 2 = owner and admin)
        + ID_Datasets: datasets used to train it
    ~ Model Information:
        + Training_Frames: total training frames
        + Batch_Size: batch
        + Num_Epoch: epoch
        + Layer_Types: layer types
        + Num_Layers: number of layers
        + Num_Nodes: nodes per layer
- RawDatasets 
    + Name: name
    + ID_Self: id #
    + ID_Owner: id # of owner
    + Date_Created: date created
    + FPS: frame rate
    + Num_Frames: number of frames
- Datasets
    ~ General Information:
        + Name: name
        + ID_Self: id #
        + ID_Owner: id # of owner
        + ID_Dataset: id # of original dataset
        + Date_Created: date created
    ~ Modifications
        + FPS_Old: old frame rate
        + FPS_New: new frame rate
        + Sensor_Savagol_Distance: sensors savagol smoothing distance (milliseconds range)
        + Sensor_Savagol_Degree: sensors savagol smoothing degree (radians)
        + Angle_Savagol_Distance: angles savagol smoothing distance (milliseconds range)
        + Angle_Savagol_Degree: angles savagol smoothing degree (radians)
- Graphs
    + ID_Group: 
        + ID_Self: personal ID number
    + ID_Owner: owner ID number
    + Name: name
    + 
"""

connection = None
cursor = None


# Loads or spawn in a new Database
def connect(database_name=Constants.DEFAULT_DATABASE_NAME):
    global cursor, connection

    assert connection is None

    try:
        connection = sqlite3.connect(Parameters.PROJECT_PATH + Constants.DATABASE_PATH + database_name,
                                     check_same_thread=False)
        cursor = connection.cursor()
    except:
        return False
    return True


def disconnect():
    global cursor, connection

    # Closes the connections
    cursor.close()
    connection.close()

    # Nullifies the objects
    cursor = None
    connection = None


def create_users_table():
    global cursor
    # Create Users table
    cursor.execute("""CREATE TABLE Users (
                            ID             INTEGER PRIMARY KEY,
                            Name           TEXT UNIQUE NOT NULL,
                            Password       TEXT NOT NULL, 
                            Permission     INTEGER NOT NULL,
                            ID_Models      INTEGER, 
                            ID_Datasets    INTEGER)""")


def create_datasets_table():
    global cursor
    # Create Datasets
    cursor.execute("""CREATE TABLE Datasets (
                            ID             INTEGER PRIMARY KEY,
                            Name           TEXT UNIQUE NOT NULL,
                            ID_Owner       INTEGER NOT NULL REFERENCES Users(ID) ON UPDATE CASCADE,
                            Date_Created   DATE,
                            Permission     INTEGER NOT NULL,
                            FPS            INTEGER NOT NULL,
                            Sensor_Savagol_Distance    REAL,
                            Sensor_Savagol_Degree      REAL,
                            Angle_Savagol_Distance     REAL,
                            Angle_Savagol_Degree       REAL)""")


def create_dataset_dependency_table():
    global cursor
    # Create Datasets
    cursor.execute("""CREATE TABLE DatasetDependency (
                                ID_Dataset      INTEGER NOT NULL REFERENCES Datasets(ID) ON UPDATE CASCADE,
                                ID_Dependency   INTEGER NOT NULL REFERENCES Datasets(ID) ON UPDATE CASCADE)""")


def create_models_table():
    global cursor
    # Create Models Table
    cursor.execute("""CREATE TABLE Models (
                            ID             INTEGER PRIMARY KEY,
                            Name           TEXT NOT NULL,
                            ID_Owner       INTEGER NOT NULL REFERENCES Users(ID) ON UPDATE CASCADE,
                            Date_Created   DATE,
                            View_Domain    INTEGER NOT NULL,
                            ID_Dataset     INTEGER NOT NULL REFERENCES Datasets(ID) ON UPDATE CASCADE,
                            Batch_Size     INTEGER NOT NULL,
                            Num_Epochs     INTEGER NOT NULL,
                            Layer_Types    TEXT NOT NULL,
                            Num_Layers     INTEGER NOT NULL,
                            Num_Nodes      INTEGER NOT NULL)""")


def create_all_new_tables(replace=False):
    global cursor

    assert cursor is not None

    Log.info("Creating database tables...")

    # Creating the new tables
    _create_table_check(table_name="Users", create_tables_function=create_users_table, replace=replace)
    _create_table_check(table_name="Datasets", create_tables_function=create_datasets_table, replace=replace)
    _create_table_check(table_name="DatasetDependency", create_tables_function=create_dataset_dependency_table,
                        replace=replace)
    _create_table_check(table_name="Models", create_tables_function=create_models_table, replace=replace)


def _create_table_check(table_name, create_tables_function, replace):
    global cursor, connection

    # Checks for the user table
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='" + table_name + "'")
    exists_user = cursor.fetchone() is not None

    Log.info("The '" + table_name + "' table exists: " + str(exists_user))

    # Logic for creating the tables
    if exists_user is True:
        if replace is True:
            # Drop the table
            cursor.execute("DROP TABLE IF EXISTS " + table_name)

            # Create new table
            create_tables_function()
            connection.commit()

            # Create new table
            Log.info("Replaced the '" + table_name + "' table")
    else:
        create_tables_function()
        Log.info("Created the '" + table_name + "' table")


def _get_table(table_name):
    global cursor

    # Database.cursor.execute("FROM . " + table_name + " GET *")
    Warnings.not_complete()
    cursor.execute("SELECT * FROM " + table_name)
    return


def _add_table_record(table_name, record_dictionary):
    global cursor, connection

    Warnings.not_complete()
    sql_keys = ""
    for k in record_dictionary.getkeys():
        sql_keys += ":" + k + ","
    sql_keys.strip(",")

    cursor.execute("INSERT INTO " + table_name + "VALUES (" + sql_keys + ")", record_dictionary)
    connection.commit()


def _delete_table_record(table_name, oid):
    global cursor, connection

    Warnings.not_complete()
    cursor.execute("DELETE from " + table_name + " WHERE oid=" + oid)
    connection.commit()


def _update_table_record(table_name, ):
    global cursor, connection

    Warnings.not_complete()
    cursor.execute()
    connection.commit()
