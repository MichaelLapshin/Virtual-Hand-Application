from tkinter import messagebox

NOT_COMPLETE_MESSAGE = "Warning. This part of the program is not yet complete."
NOT_WORKING_MESSAGE = "Warning. This part of the program is not working."
NOT_TO_REACH_MESSAGE = "Warning. The code has entered a part of the code that should never be reached."

"""
    Warning messages to use
"""


def generic_warning(message, popup=False):
    print(message)
    if popup:
        messagebox.showwarning(message)
    return message


# Not complete warnings
def not_complete():
    return generic_warning(NOT_COMPLETE_MESSAGE)


def not_complete(popup):
    return generic_warning(NOT_COMPLETE_MESSAGE, popup)


# Not working warnings
def not_working():
    return generic_warning(NOT_WORKING_MESSAGE)


def not_working(popup):
    return generic_warning(NOT_WORKING_MESSAGE)


# Not to reach warnings
def not_to_reach():
    return generic_warning(NOT_TO_REACH_MESSAGE)


def not_to_reach(popup):
    return generic_warning(NOT_TO_REACH_MESSAGE)
