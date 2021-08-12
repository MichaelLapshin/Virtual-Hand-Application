"""
[Parameters.py]
@description: A list of program parameters which may be changed by the user
@author: Michael Lapshin
"""

PROJECT_PATH = "C:\\Git\\Virtual-Hand-Application\\"
_user_parameters_file_path = PROJECT_PATH + "scripts\\Parameters.txt"

# Server Parameters
SERVER_IP_ADDRESS = "http://localhost"
SERVER_PORT = "5000"

# Logging parameters
LOG_LEVEL = 1

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


def optimize_file_parameters():
    # Reads the constants files and evaluates the lines
    _input = open(_user_parameters_file_path, "r")

    # Obtains parameters
    unique_parameters = {}
    for line in _input.readlines():
        if line.find("=") != -1:
            unique_parameters[line[:line.index("="):]] = line[line.index("=") + 1::]
    _input.close()

    # Puts in the unique parameters back into the file
    _output = open(_user_parameters_file_path, "w")
    for k in unique_parameters.keys():
        _output.write(k + "=" + unique_parameters[k])
    _output.close()


def clear_file_parameters():
    _output = open(_user_parameters_file_path, "w")
    _output.close()


def add_file_parameters(item):
    _output = open(_user_parameters_file_path, "a")
    _output.write(item + "\n")
    _output.close()
