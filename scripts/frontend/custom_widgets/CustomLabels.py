import tkinter
import tkinter.font

# Custom Labels constants
from scripts import General
from scripts.frontend import Constants, Parameters
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

"""
    Parent generic label
"""


class Label(tkinter.Label, WidgetInterface):

    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        tkinter.Label.__init__(self, root, text=text,
                               padx=padx, pady=pady)
        self.grid(column=column, row=row)
        self.grid(columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

        # Config
        self.anchor(tkinter.CENTER)
        self.config(bd=1, relief=tkinter.RIDGE)
        self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_C))

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


class AccountLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)

        # Padding
        self.config(padx=12, pady=10)
        self.grid(padx=16, pady=16)



class InformationLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       text=text)
        # Grid
        self.grid(sticky=tkinter.NSEW)

    def update_colour(self):
        super().update_colour()
        # Colour
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))


class SearchLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.config(bd=1, relief=tkinter.RIDGE)
        self.grid(sticky=tkinter.NSEW)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))


class PlotLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)


class TitleLabel(Label):
    TITLE_FONT_SIZE = 16

    def __init__(self, root, column, row, columnspan=1, rowspan=1,
                 padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)

        # Title configurations
        self.config(font=tkinter.font.Font(size=TitleLabel.TITLE_FONT_SIZE))
        self.config(padx=Constants.LONG_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(padx=Constants.LONG_SPACING, pady=Constants.STANDARD_SPACING)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

