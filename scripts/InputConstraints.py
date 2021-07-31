from tkinter import messagebox


def warn(message):
    messagebox.showwarning(title="Warning!", message=message)


"""
    Integer
"""


def assert_int_range_inclusive(input_name, input, min_int, max_int):
    assert type(input) is int

    if (input is not None) and (min_int <= input <= max_int):
        return True
    else:
        warn("'" + str(input_name) + "' must be an integer between " + str(min_int) + " and " + str(
            max_int) + " (inclusive). Current input: " + str(input))
        return False


def assert_int_non_negative(input_name, input, max_int=1000000000):
    assert type(input) is int

    if (input is not None) and (0 <= input <= max_int):
        return True
    else:
        warn("'" + str(input_name) + "' must be a non-negative integer (less than " + str(
            max_int) + "). Current input: " + str(input))
        return False


def assert_int_positive(input_name, input, max_int=1000000000):
    assert type(input) is int

    if (input is not None) and (0 < input <= max_int):
        return True
    else:
        warn("'" + str(input_name) + "' must be a positive integer (less than " + str(
            max_int) + "). Current input: " + str(input))
        return False


"""
    Double
"""


def assert_float_range_inclusive(input_name, input, min_float, max_float):
    assert type(input) is float

    if (input is not None) and (min_float <= input <= max_float):
        return True
    else:
        warn("'" + str(input_name) + "' must be an float between " + str(min_float) + " and " + str(
            max_float) + " (inclusive). Current input: " + str(input))
        return False


def assert_float_non_negative(input_name, input, max_float=1000000000):
    assert type(input) is float

    if (input is not None) and (0 <= input <= max_float):
        return True
    else:
        warn("'" + str(input_name) + "' must be a non-negative float (less than " + str(
            max_float) + "). Current input: " + str(input))
        return False


def assert_float_positive(input_name, input, max_float=1000000000):
    assert type(input) is float

    if (input is not None) and (0 < input <= max_float):
        return True
    else:
        warn("'" + str(input_name) + "' must be a positive float (less than " + str(
            max_float) + "). Current input: " + str(input))
        return False
