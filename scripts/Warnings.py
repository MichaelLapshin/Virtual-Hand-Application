from tkinter import messagebox
import inspect

NOT_COMPLETE_MESSAGE = "Warning. This part of the program is not yet complete."
NOT_WORKING_MESSAGE = "Warning. This part of the program is not working."
NOT_TO_REACH_MESSAGE = "Warning. The code has entered a part of the code that should never be reached."

"""
    Warning messages to use
"""


def generic_warning(message, external_frame, popup):
    prepare_message = message + \
                      "\n    File:      " + str(external_frame[1][1]) + \
                      "\n    Function:  " + str(external_frame[1][3]) + \
                      "\n    Line #:    " + str(external_frame[1][2])
    print(prepare_message)
    if popup:
        messagebox.showwarning(prepare_message)
    return message


# Not complete warnings
def not_complete(popup=False):
    return generic_warning(NOT_COMPLETE_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)


# Not working warnings
def not_working(popup=True):
    return generic_warning(NOT_WORKING_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)


# Not to reach warnings
def not_to_reach(popup=True):
    return generic_warning(NOT_TO_REACH_MESSAGE, inspect.getouterframes(inspect.currentframe(), 2), popup)
