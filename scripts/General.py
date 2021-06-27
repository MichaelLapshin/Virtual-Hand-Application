import tkinter


def washed_colour_rgb(colour, percent):
    return (
        (int)(colour[0] + (255 - colour[0]) * (1 - percent)),
        (int)(colour[1] + (255 - colour[1]) * (1 - percent)),
        (int)(colour[2] + (255 - colour[2]) * (1 - percent)))


def washed_colour_hex(colour, percent):
    return '#%02x%02x%02x' % washed_colour_rgb(colour, percent)
