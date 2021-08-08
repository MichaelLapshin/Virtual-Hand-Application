"""
[Parameters.py]
@description: A list of program parameters which may be changed by the user
@author: Michael Lapshin
"""

PROJECT_PATH = "C:\\Git\\Virtual-Hand-Application\\"
_user_parameters_file_path = PROJECT_PATH + "scripts\\Parameters.txt"

# Logging parameters
LOG_LEVEL = 2

# Updating
UPDATE_DELAY_MS = 500
GUI_Scale = 1.2

# Colour
COLOUR_ALPHA = (91, 155, 213)
COLOUR_BRAVO = (146, 208, 80)

# Nice Colour Option
# COLOUR_ALPHA = (242, 91, 0)  # Orange
# COLOUR_BRAVO = (80, 90, 103)  # Grey

# Colour Gradients
ColourGrad_A = 0.10
ColourGrad_B = 0.20
ColourGrad_C = 0.4
ColourGrad_D = 0.5
ColourGrad_E = 0.60
ColourGrad_F = 0.70


def process_file_parameters():
    # Reads the constants files and evaluates the lines
    _input = open(_user_parameters_file_path, "r")

    for line in _input.readlines():
        exec(line, globals())
    _input.close()


def clear_file_parameters():
    _input = open(_user_parameters_file_path, "w")
    _input.close()


def add_file_parameters(item):
    _input = open(_user_parameters_file_path, "a")
    _input.write(item + "\n")
    _input.close()
