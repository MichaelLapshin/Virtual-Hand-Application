"""
[Log.py]
@description: A class used to log data of different priorities
"""
import datetime
import inspect

from scripts import Parameters

files_seen = []


def clear(file_name):
    file = open(Parameters.PROJECT_PATH + "logs\\" + file_name + ".log", 'w')
    print_on_lvl("Started the log '" + file_name + ".log'", 1000)
    file.close()


"""
    Log printing
"""


def print_on_lvl(text, lvl):
    if Parameters.LOG_LEVEL >= lvl:

        # Clears the logs
        file_path = inspect.getmodule(inspect.stack()[2][0]).__file__
        file_name = file_path[file_path.rfind("\\") + 1::].rstrip(".py")

        if file_name not in files_seen:
            files_seen.append(file_name)
            clear(file_name)

        # Starts the logs
        file = open(Parameters.PROJECT_PATH + "logs\\" + file_name + ".log", 'a')
        file.write(datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]") + text + "\n")
        file.close()


def trace(text):
    print_on_lvl("[TRACE] " + text, 0)


def debug(text):
    print_on_lvl("[DEBUG] " + text, 1)


def info(text):
    print_on_lvl("[INFO] " + text, 2)


def warning(text):
    print_on_lvl("[WARNING] " + text, 3)


def error(text):
    print_on_lvl("[ERROR] " + text, 4)


def critical(text):
    print_on_lvl("[CRITICAL] " + text, 5)


def blocker(text):
    print_on_lvl("[BLOCKER] " + text, 6)
