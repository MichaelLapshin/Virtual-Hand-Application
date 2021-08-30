import datetime

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
    pass