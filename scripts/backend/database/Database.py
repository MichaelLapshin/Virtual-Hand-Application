import sqlite3

from scripts import Warnings
from scripts.frontend import Constants

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
def connect(database_name):
    global cursor, connection

    assert connection is None

    connection = sqlite3.connect(Constants.DATABASE_ABSOLUTE_PATH + database_name)
    cursor = connection.cursor()


def create_new_tables():
    global cursor

    assert cursor is not None

    # Create Users table
    cursor.execute("""CREATE TABLE Users (
                        ID_Database        INTEGER PRIMARY KEY,
                        Name           TEXT,
                        Password       TEXT, 
                        Permission     INTEGER NOT NULL,
                        ID_Models      INTEGER, 
                        ID_Datasets    INTEGER)""")

    # Create Models Table
    cursor.execute("""CREATE TABLE Models (
                        ID_Self        INTEGER PRIMARY KEY,
                        Name           TEXT,
                        Date_Created   DATE,
                        View_Domain    INTEGER NOT NULL,
                        ID_Datasets    NOT NULL,
                        Batch_Size     INTEGER,
                        Num_Epochs     INTEGER,
                        Layer_Types    TEXT,
                        Num_Layers     INTEGER ,
                        Num_Nodes      INTEGER )""")

    # # Create Raw_datasets
    # self.cursor.execute("""CREATE TABLE RawDatasets (
    #                 ID_Self        INTEGER PRIMARY KEY,
    #                 Name           TEXT,
    #                 ID_Owner       INTEGER,
    #                 Date_Created   DATE,
    #                 FPS            INTEGER,
    #                 Num_Frames     INTEGER )""")

    # Create Datasets
    cursor.execute("""CREATE TABLE Datasets (
                        ID_Self        INTEGER PRIMARY KEY,
                        ID_Owner       INTEGER,
                        ID_Dataset     INTEGER,
                        Date_Created   DATE,
                        FPS_Old        INTEGER,
                        FPS_New        INTEGER,
                        Sensor_Savagol_Distance    INTEGER,
                        Sensor_Savagol_Degree      INTEGER,
                        Angle_Savagol_Distance     INTEGER,
                        Angle_Savagol_Degree       INTEGER)""")


def _get_table(table_name):
    global cursor

    # Database.cursor.execute("FROM . " + table_name + " GET *")
    Warnings.not_complete()
    cursor.execute("SELECT * FROM " + table_name)
    return


def _add_table_record(table_name, record_dictionary):
    global cursor

    Warnings.not_complete()
    sql_keys = ""
    for k in record_dictionary.getkeys():
        sql_keys += ":" + k + ","
    sql_keys.strip(",")

    cursor.execute("INSERT INTO " + table_name + "VALUES (" + sql_keys + ")", record_dictionary)


def _delete_table_record(table_name, oid):
    global cursor

    Warnings.not_complete()
    cursor.execute("DELETE from " + table_name + " WHERE oid=" + oid)


def _update_table_record(table_name, ):
    global cursor

    Warnings.not_complete()
    cursor.execute()


def get_graphs():
    global cursor, connection

    Warnings.not_complete()
    return _get_table("Graphs")


def save():
    global cursor

    Warnings.not_complete()
    cursor.commit()


def shutdown():
    global cursor, connection

    # Saves the changes
    cursor.commit()

    # Closes the connections
    cursor.close()
    connection.close()

    # Nullifies the objects
    cursor = None
    connection = None


def add_user(user_name, password):
    global cursor, connection

    cursor.execute()  # TODO, finish this function
    Warnings.not_complete()
