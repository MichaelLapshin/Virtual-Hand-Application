"""
[Parameters.py]
@description: A list of program-spanning constants that should not be changed by the user
@author: Michael Lapshin
"""

default_resolution = "1000x800"

# Server constants

# GUI Spacing
LONG_SPACING = 20
STANDARD_SPACING = 5
SHORT_SPACING = 2

# Permissions
PERMISSION_ADMIN = "Admin"
PERMISSION_PRIVATE = "Private"
PERMISSION_PUBLIC = "Public"
PERMISSION_LEVELS = {PERMISSION_ADMIN: 2, PERMISSION_PRIVATE: 1, PERMISSION_PUBLIC: 0}

# Colours
COLOUR_GREEN = (146, 208, 80)
COLOUR_RED = (235, 0, 0)
COLOUR_GREY = (150, 150, 150)

# Camera options
CAMERA_DEFAULT_RESOLUTION_X = 640
CAMERA_DEFAULT_RESOLUTION_Y = 480
CAMERA_DEFAULT_ZOOM_PERCENT = 100
CAMERA_DEFAULT_FIELD_OF_VIEW = 90
CAMERA_DEFAULT_FRAMES_PER_SECOND = 60

# Uploading data constants
UPLOAD_KEY_WORD = "to_transfer"

# Dataset recording options
RECORDING_DEFAULT_FRAMES_PER_SECOND = 60
RECORDING_DEFAULT_SENSOR_ZEROING_DELAY = 10
RECORDING_DEFAULT_TRAINING_LENGTH = 30

# Client temporary directories paths
TEMP_DATASET_PATH = "AppData-Client\\temp-datasets\\"  # Makes sure the end the path with '\\'
TEMP_MODEL_PATH = "AppData-Client\\temp-models\\"  # Makes sure the end the path with '\\'
TEMP_SAVE_DATASET_NAME = "temp_raw_dataset.hdf5"
TEMP_SAVE_MODEL_NAME = "temp_model.mod"

# Server directory paths
SERVER_DATABASE_PATH = "AppData-Server\\databases\\"  # Makes sure the end the path with '\\'
SERVER_DATASET_PATH = "AppData-Server\\datasets\\"  # Makes sure the end the path with '\\'
SERVER_MODEL_PATH = "AppData-Server\\models\\"  # Makes sure the end the path with '\\'

# Data gathering related constants
TRAIN_ZEROING_DELAY_S = 5

# Model training
MODEL_ACT_FUNC_OPTIONS = ("selu", "linear", "relu", "elu", "sigmoid")

# Database constants
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "password"
DEFAULT_DATABASE_NAME = "database"

# Fetching data
DATABASE_DATA_TO_FETCH = ("ID", "Name", "ID_Owner", "Date_Created", "Permission", "FPS",
                          "Sensor_Savagol_Distance", "Sensor_Savagol_Degree",
                          "Angle_Savagol_Distance", "Angle_Savagol_Degree")
MODEL_DATA_TO_FETCH = ("ID", "Name", "ID_Owner", "Date_Created", "View_Domain", "ID_Dataset",
                       "Learning_Rate", "Batch_Size", "Num_Epochs", "Data_Time_Shift_s",
                       "Layer_Types", "Num_Layers", "Num_Nodes_Per_Layer")

# Database sorting parameter constants {"Displayed text", "Database feature name"}
DATABASES_SORT_BY_OPTIONS = {"ID Number": "ID",
                             "Name": "Name",
                             "Date created": "Date_Created",
                             "FPS": "FPS"}
MODELS_SORT_BY_OPTIONS = {"ID Number": "ID",
                          "Name": "Name",
                          "Date created": "Date_Created",
                          "Learning Rate": "Learning_Rate",
                          "Batch Size": "Batch_Size",
                          "# of Epochs": "Num_Epochs",
                          "# of Nodes per Layer": "Num_Nodes_Per_Layer",
                          "# of Layers": "Num_Layers"}
SORT_DIRECTION = {"Ascent": "ASC", "Descent": "DESC"}
