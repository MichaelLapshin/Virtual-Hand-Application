"""
[Parameters.py]
@description: A list of program-spanning constants that should not be changed by the user
@author: Michael Lapshin
"""

default_resolution = "1000x800"

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

# Camera options
CAMERA_DEFAULT_RESOLUTION_X = 640
CAMERA_DEFAULT_RESOLUTION_Y = 480
CAMERA_DEFAULT_ZOOM_PERCENT = 100
CAMERA_DEFAULT_FIELD_OF_VIEW = 90
CAMERA_DEFAULT_FRAMES_PER_SECOND = 30
