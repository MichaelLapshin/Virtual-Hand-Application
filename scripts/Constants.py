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
UPLOAD_DATASET_KEY_WORD = "dataset"

# Dataset recording options
RECORDING_DEFAULT_FRAMES_PER_SECOND = 50
RECORDING_DEFAULT_SENSOR_ZEROING_DELAY = 10
RECORDING_DEFAULT_TRAINING_LENGTH = 30

# Client temporary directories paths
TEMP_DATASET_PATH = "AppData-Client\\temp-datasets\\"  # Makes sure the end the path with '\\'
TEMP_MODEL_PATH = "AppData-Client\\temp-models\\"  # Makes sure the end the path with '\\'
TEMP_SAVE_NAME = "temp_raw_dataset.hdf5"

# Training related constants
TRAIN_ZEROING_DELAY_S = 5
TRAIN_DATASET_PATH = "AppData-Server\\datasets\\"  # Makes sure the end the path with '\\'
TRAIN_MODEL_PATH = "AppData-Server\\models\\"  # Makes sure the end the path with '\\'

# Database constants
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "password"
DEFAULT_DATABASE_NAME = "database"
DATABASE_PATH = "AppData-Server\\databases\\"  # Makes sure the end the path with '\\'
