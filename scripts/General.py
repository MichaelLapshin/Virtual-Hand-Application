import datetime

import numpy

from scripts import Log


def washed_colour_rgb(colour, percent):
    return (
        (int)(colour[0] + (255 - colour[0]) * (1 - percent)),
        (int)(colour[1] + (255 - colour[1]) * (1 - percent)),
        (int)(colour[2] + (255 - colour[2]) * (1 - percent)))


def washed_colour_hex(colour, percent):
    return '#%02x%02x%02x' % washed_colour_rgb(colour, percent)


def hex_to_rgb(hex_code):
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))


def get_current_slashed_date(hms=True):
    if hms is True:
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    else:
        return datetime.datetime.today().strftime('%Y-%m-%d')


def list_to_sql_select_features(a_list):
    new_string_list = str(a_list).lstrip("(").rstrip(")").replace("'", "")
    Log.info("Generated the new sql feature list: " + new_string_list)
    return new_string_list


def dict_to_sql_update_features(a_dict):
    new_string_dict = str(a_dict).lstrip("{").rstrip("}").replace(":", "=")
    Log.info("Generated the new sql feature dict: " + new_string_dict)
    return new_string_dict


def resizing_scale(width, height, space_width, space_height):
    # Calculates the scale
    scale = space_width / max(1, float(width))
    if int(scale * height) > space_height:
        scale = space_height / max(1, float(height))
    return scale


# Original lists which the post-processing will be based off of
def float_int_unknownArray2list(u_list):
    if type(u_list) == float or type(u_list) == int \
            or type(u_list) == numpy.int32 or type(u_list) == numpy.float64:
        return u_list
    elif type(u_list) != list:
        u_list = list(u_list)

    for i in range(0, len(u_list)):
        u_list[i] = float_int_unknownArray2list(u_list[i])

    return u_list
