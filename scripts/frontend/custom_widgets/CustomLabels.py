import tkinter

# Custom Labels constants
from scripts import General
from scripts.frontend import Constants

LABEL_PADDING_X = 12
LABEL_PADDING_Y = 8

"""
    Parent generic label
"""


class Label(tkinter.Label):

    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        tkinter.Label.__init__(self, root, text=text,
                               padx=padx, pady=pady)
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

        # Config
        self.anchor(tkinter.CENTER)
        self.config(bd=1, relief=tkinter.RIDGE)
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)


"""
    Custom label
"""


class NavigationLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)


class LoginLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        # Colour
        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour40))

        # Padding
        self.config(padx=12, pady=10)
        self.grid(padx=16, pady=16)


class InformationLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       text=text)

        # Colour
        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour40))

        # Grid
        self.grid(sticky=tkinter.NSEW)


class SearchLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour40))
        self.config(bd=1, relief=tkinter.RIDGE)
        self.grid(sticky=tkinter.NSEW)


class PlotLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
