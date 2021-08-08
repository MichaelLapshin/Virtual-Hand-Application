from tkinter import messagebox
import inspect

from scripts import Log

NOT_COMPLETE_MESSAGE = "This part of the program is not yet complete."
NOT_WORKING_MESSAGE = "This part of the program is not working."
NOT_TO_REACH_MESSAGE = "The code has entered a part of the code that should never be reached."

"""
    Warning messages to use
"""


def generic_warning(message, external_frame, popup):
    prepare_message = message + \
                      "\n    File:      " + str(external_frame[1][1]) + \
                      "\n    Function:  " + str(external_frame[1][3]) + \
                      "\n    Line #:    " + str(external_frame[1][2])

    # Print to different sources
    print(prepare_message)
    Log.warning(prepare_message)
    if popup:
        messagebox.showwarning(title="Warning!", message=prepare_message)

    return prepare_message


# Not complete warnings
def not_complete(popup=False):
    return generic_warning(NOT_COMPLETE_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)


# Not working warnings
def not_working(popup=True):
    return generic_warning(NOT_WORKING_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)


# Not to reach warnings
def not_to_reach(popup=True):
    return generic_warning(NOT_TO_REACH_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)
