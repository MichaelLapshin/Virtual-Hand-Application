from tkinter import messagebox


def warn(message):
    messagebox.showwarning(title="Warning!", message=message)


def error(message):
    messagebox.showerror(title="Error!", message=message)


"""
    General
"""


def assert_is_integer(value):
    if type(value) == int:
        return True

    if (type(value) == str) and ("." in value):
        return False

    try:
        int(value)
        return True
    except:
        return False


def assert_is_float(value):
    if type(value) == float:
        return True

    if (type(value) == str) and ("." not in value):
        return False

    try:
        float(value)
        return True
    except:
        return False


def assert_is_not_none(value_name, value):
    if value is None:
        warn("'" + str(value_name) + "' must be a non-null value.\nCurrent value: " + str(value))
        return False
    else:
        return True


"""
    String
"""


def assert_string_from_set(value_name, value, value_list):
    if value in value_list:
        return True
    else:
        warn("'" + str(value_name) + "' must one of the following strings: " + str(
            value_list) + ".\nCurrent value: " + str(value))
        return False


def assert_string_non_empty(value_name, value):
    if (value is None) or (value == ""):
        warn("'" + str(value_name) + "' must be a non-empty string.\nCurrent value: " + str(value))
        return False
    else:
        return True


"""
    Integer
"""


def assert_int_range_inclusive(value_name, value, min_int, max_int):
    if (value is not None) and assert_is_integer(value) and (min_int <= int(value) <= max_int):
        return True
    else:
        warn("'" + str(value_name) + "' must be an integer between " + str(min_int) + " and " + str(
            max_int) + " (inclusive).\nCurrent value: " + str(value))
        return False


def assert_int_non_negative(value_name, value, max_int=1000000000):
    if (value is not None) and assert_is_integer(value) and (0 <= int(value) <= max_int):
        return True
    else:
        warn("'" + str(value_name) + "' must be a non-negative integer (less than " + str(
            max_int) + ").\nCurrent value: " + str(value))
        return False


def assert_int_positive(value_name, value, max_int=1000000000):
    if (value is not None) and assert_is_integer(value) and (0 < int(value) <= max_int):
        return True
    else:
        warn("'" + str(value_name) + "' must be a positive integer (less than " + str(
            max_int) + ").\nCurrent value: " + str(value))
        return False


"""
    Float
     - Note: integers will be approved too
"""


def assert_float_range_inclusive(value_name, value, min_float, max_float):
    if (value is not None) and (assert_is_float(value) or assert_is_integer(value)) \
            and (min_float <= float(value) <= max_float):
        return True
    else:
        warn("'" + str(value_name) + "' must be an float between " + str(min_float) + " and " + str(
            max_float) + " (inclusive).\nCurrent value: " + str(value))
        return False


def assert_float_non_negative(value_name, value, max_float=1000000000):
    if (value is not None) and (assert_is_float(value) or assert_is_integer(value)) \
            and (0 <= float(value) <= max_float):
        return True
    else:
        warn("'" + str(value_name) + "' must be a non-negative float (less than " + str(
            max_float) + ").\nCurrent value: " + str(value))
        return False


def assert_float_positive(value_name, value, max_float=1000000000):
    if (value is not None) and (assert_is_float(value) or assert_is_integer(value)) \
            and (0 < float(value) <= max_float):
        return True
    else:
        warn("'" + str(value_name) + "' must be a positive float (less than " + str(
            max_float) + ").\nCurrent value: " + str(value))
        return False


"""
    Odd/even integers
"""


def assert_odd_integer(value_name, value):
    if (value is not None) and assert_is_integer(value) and (int(value) % 2 == 1):
        return True
    else:
        warn("'" + str(value_name) + "' must be an odd integer.\nCurrent value: " + str(value))
        return False


def assert_even_integer(value_name, value):
    if (value is not None) and assert_is_integer(value) and (int(value) % 2 == 0):
        return True
    else:
        warn("'" + str(value_name) + "' must be an even integer.\nCurrent value: " + str(value))
        return False


"""
    Size comparison
"""


def assert_int_less_than(value1_name, value1, value2_name, value2):
    if (value1 is not None) and assert_is_integer(value1) and \
            (value2 is not None) and assert_is_integer(value2) and \
            int(value1) < int(value2):
        return True
    else:
        warn("'" + str(value1_name) + "' must be an integer and less than the integer '" + str(value2_name) + "'."
             + "\nCurrent assertion: " + str(value1) + " < " + str(value2))
        return False


def assert_int_greater_than(value1_name, value1, value2_name, value2):
    if (value1 is not None) and assert_is_integer(value1) and \
            (value2 is not None) and assert_is_integer(value2) and \
            int(value1) > int(value2):
        return True
    else:
        warn("'" + str(value1_name) + "' must be an integer greater than the integer '" + str(value2_name) + "'."
             + "\nCurrent assertion: " + str(value1) + " > " + str(value2))
        return False
