"""
[Parameters.py]
@description: A list of program-spanning constants that should not be changed by the user
@author: Michael Lapshin
"""

default_resolution = "1000x800"

# Server constants
SERVER_IP_ADDRESS = "localhost"

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

# Camera options
CAMERA_DEFAULT_RESOLUTION_X = 640
CAMERA_DEFAULT_RESOLUTION_Y = 480
CAMERA_DEFAULT_ZOOM_PERCENT = 100
CAMERA_DEFAULT_FIELD_OF_VIEW = 90
CAMERA_DEFAULT_FRAMES_PER_SECOND = 60

# Dataset recording options
RECORDING_DEFAULT_FRAMES_PER_SECOND = 50
RECORDING_DEFAULT_SENSOR_ZEROING_DELAY = 10
RECORDING_DEFAULT_TRAINING_LENGTH = 30

# Training related constants
TRAIN_ZEROING_DELAY_S = 5
TRAIN_BASE_RELATIVE_PATH = "C:\\Git\\Virtual-Hand-Application\\AppData-Client\\temp-datasets\\"  # Makes sure the end the path with '\\'
TRAIN_TEMP_SAVE_NAME = "temp_raw_dataset.hdf5"

# Database constants
DEFAULT_USER = "admin"
DEFAULT_PASSWORD = "password"
DEFAULT_DATABASE_NAME = "database"
DATABASE_ABSOLUTE_PATH = "C:\\Git\\Virtual-Hand-Application\\AppData-Server\\databases\\"  # Makes sure the end the path with '\\'
