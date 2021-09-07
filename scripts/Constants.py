"""
[Parameters.py]
@description: A list of program-spanning constants that should not be changed by the user
@author: Michael Lapshin
"""
import numpy as np

default_resolution = "1160x800"

# Server constants
ADMIN_USER_NAME = "Admin"
ADMIN_PASSWORD = "livelink"

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
TEMP_DATASET_IMAGE_PATH = "AppData-Client\\temp-images-datasets\\"  # Makes sure the end the path with '\\'
TEMP_MODEL_IMAGE_PATH = "AppData-Client\\temp-images-models\\"  # Makes sure the end the path with '\\'
TEMP_SAVE_DATASET_NAME = "temp_dataset.ds"

# Server directory paths
SERVER_DATABASE_PATH = "AppData-Server\\databases\\"  # Makes sure the end the path with '\\'

SERVER_DATASET_PATH = "AppData-Server\\datasets\\"  # Makes sure the end the path with '\\'
SERVER_IMAGES_DATASETS_FINGERS_PATH = "AppData-Server\\images-datasets-fingers\\"  # Makes sure the end the path with '\\'
SERVER_IMAGES_DATASETS_SENSORS_PATH = "AppData-Server\\images-datasets-sensors\\"  # Makes sure the end the path with '\\'

SERVER_MODEL_PATH = "AppData-Server\\models\\"  # Makes sure the end the path with '\\'
SERVER_IMAGES_MODELS_ERRORS_PATH = "AppData-Server\\images-models-errors\\"  # Makes sure the end the path with '\\'
SERVER_IMAGES_MODELS_PREDICTIONS_PATH = "AppData-Server\\images-models-predictions\\"  # Makes sure the end the path with '\\'

# Data gathering related constants
TRAIN_ZEROING_DELAY_S = 5

# Model training
MODEL_ACT_FUNC_OPTIONS = ("selu", "linear", "relu", "elu", "sigmoid")

# Database constants
DEFAULT_DATABASE_NAME = "database"
DATABASE_PUBLIC_ID = 0
DATABASE_DELETED_ID = -1
DATASET_EXT = ".ds"
MODEL_EXT = ".mod"
MODEL_DIR = "model_"

# Fetching data
URL_REPLACEMENT_MAP = {" ": "%", ":": "~"}
DATASET_ENTRY_TRANSFER_DATA = ("ID", "Name", "ID_Owner", "Date_Created", "Permission", "Rating",
                               "Is_Raw", "Num_Frames", "FPS",
                               "Sensor_Savagol_Distance", "Sensor_Savagol_Degree",
                               "Angle_Savagol_Distance", "Angle_Savagol_Degree")

MODEL_ENTRY_TRANSFER_DATA = ("ID", "Name", "ID_Owner", "Date_Created", "Permission", "Rating", "ID_Dataset",
                             "Frames_Shift", "Num_Training_Frames", "Learning_Rate", "Batch_Size", "Num_Epochs",
                             "Layer_Types", "Num_Layers", "Num_Nodes_Per_Layer")

# Database sorting parameter constants {"Displayed text", "Database feature name"}
DATABASES_SORT_BY_OPTIONS = {"ID Number": "ID",
                             "Name": "Name",
                             "Date created": "Date_Created",
                             "FPS": "FPS",
                             "Rating": "Rating",
                             "Is Raw": "Is_Raw"}
MODELS_SORT_BY_OPTIONS = {"ID Number": "ID",
                          "Name": "Name",
                          "Date created": "Date_Created",
                          "Rating": "Rating",
                          "Learning Rate": "Learning_Rate",
                          "Batch Size": "Batch_Size",
                          "# of Epochs": "Num_Epochs",
                          "# of Nodes per Layer": "Num_Nodes_Per_Layer",
                          "# of Layers": "Num_Layers"}
SORT_DIRECTION = {"Ascent": "ASC", "Descent": "DESC"}

# Database Information Display constants {"Database feature name", "Display text"}
DATASET_GENERAL_INFORMATION_OPTIONS = {"Name": "Name",
                                       "ID_Owner": "Owner",
                                       "Date_Created": "Date created",
                                       "Permission": "Access Permissions",
                                       "Rating": "Personal Rating",
                                       "Is_Raw": "Is Raw"}
DATASET_SMOOTHING_INFORMATION_OPTIONS = {"Num_Frames": "Number of Frames",
                                         "FPS": "Frames Per Second",
                                         "Sensor_Savagol_Distance": "Sensor Savagol Distance",
                                         "Sensor_Savagol_Degree": "Sensor Savagol Degree",
                                         "Angle_Savagol_Distance": "Angle Savagol Distance",
                                         "Angle_Savagol_Degree": "Angle Savagol Degree"}

# Model Information Display constants {"Model feature name", "Display text"}
MODEL_GENERAL_INFORMATION_OPTIONS = {"Name": "Name",
                                     "ID_Owner": "Owner",
                                     "Date_Created": "Date created",
                                     "Permission": "Access Permissions",
                                     None: "Average Training Loss (percentile)",
                                     "Rating": "Personal Rating",
                                     "ID_Dataset": "Training Dataset",
                                     "Frames_Shift": "Sensor-Angle Frame Shift", }
MODEL_TRAINING_INFORMATION_OPTIONS = {"Num_Training_Frames": "Training Frames",
                                      "Learning_Rate": "Learning Rate",
                                      "Batch_Size": "Batch Size",
                                      "Num_Epochs": "Number of Epochs",
                                      "Layer_Types": "Layer Type",
                                      "Num_Layers": "Number of Layers",
                                      "Num_Nodes_Per_Layer": "Number of Nodes per Layer"}

# Technical Constants
NUM_FINGERS = 5
NUM_LIMBS_PER_FINGER = 3
NUM_SENSORS = 5
NUM_FEATURES = NUM_FINGERS * NUM_LIMBS_PER_FINGER * 2 + NUM_SENSORS

eps = np.finfo(np.float32).eps.item()
DIGITS = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
BOOLEANS = {"False": 0, "True": 1}
MAX_RATING = 100

# Dataset Plot Type Conversions
FINGER_TYPE = ("Thumb", "Index", "Middle", "Ring", "Pinky")
LIMB_TYPE = ("Proximal", "Middle", "Distal")
METRIC = ("Position", "Velocity", "Acceleration")
IMAGE_EXT = ".png"
IMAGE_SAMPLING_ZOOM = 5
IMAGE_REQUEST_FREQ_S = 0.2
IMAGE_ATTEMPT_MAX_TIMES = 10
