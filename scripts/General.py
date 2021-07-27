import datetime

def washed_colour_rgb(colour, percent):
    return (
        (int)(colour[0] + (255 - colour[0]) * (1 - percent)),
        (int)(colour[1] + (255 - colour[1]) * (1 - percent)),
        (int)(colour[2] + (255 - colour[2]) * (1 - percent)))


def washed_colour_hex(colour, percent):
    return '#%02x%02x%02x' % washed_colour_rgb(colour, percent)


def hex_to_rgb(hex_code):
    return tuple(int(hex_code[i:i + 2], 16) for i in (0, 2, 4))

def get_current_slashed_date():
    return datetime.datetime.today().strftime('%d-%m-%Y')