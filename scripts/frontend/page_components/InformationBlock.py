import tkinter
import tkinter.font

from scripts import General
from scripts.frontend import Constants
from scripts.frontend.custom_widgets.CustomLabels import InformationLabel
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

TITLE_FONT_SIZE = 8


class Frame(tkinter.Frame, WidgetInterface):

    def __init__(self, root, num_columns, num_rows,
                 frame_colour, label_colour,
                 title=None, column=0, row=0, columnspan=1, rowspan=1):

        # Asserts dimensions
        assert num_columns > 0 and num_rows > 0
        self.num_columns = num_columns
        self.num_rows = num_rows

        # Saves the colour
        self.frame_colour = frame_colour
        self.label_colour = label_colour

        # Creates self frame
        tkinter.Frame.__init__(self, root, relief=tkinter.RIDGE, bd=1)

        self.grid(column=column, row=row,
                  columnspan=columnspan, rowspan=rowspan,
                  padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING,
                  sticky=tkinter.NSEW)

        # Configure weights
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Creates title bar
        if title is not None:
            self.titlebar = InformationLabel(self, text=title, column=0, row=0)
            self.titlebar.config(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
            self.titlebar.config(font=TITLE_FONT_SIZE)
            self.titlebar.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

        # Dynamic number of columns
        self.info_frame = tkinter.Frame(self, relief=tkinter.RIDGE)
        self.info_frame.grid(column=0, row=1)
        self.info_frame.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.info_frame.grid(sticky=tkinter.NSEW)

        # Configure info frame weights
        for x in range(0, num_columns):
            self.info_frame.columnconfigure(x, weight=1)

        # Creates the info spaces
        self.info_spaces = []  # spaces[x, y] = position
        for y in range(0, num_rows):
            self.info_spaces.append([])
            for x in range(0, num_columns):
                widget = InformationLabel(self.info_frame, column=x, row=y)
                # widget.config(bg=General.washed_colour_hex(label_colour, Constants.ColourGrad_C))
                self.info_spaces[y].append(widget)

    def update_colour(self):
        super().update_colour()
        self.titlebar.update_colour()
        for y in range(0, len(self.info_spaces)):
            for x in range(0, len(self.info_spaces[y])):
                self.info_spaces[y][x].update_colour()

        self.config(bg=General.washed_colour_hex(self.frame_colour, Constants.ColourGrad_B))
        self.info_frame.config(bg=General.washed_colour_hex(self.frame_colour, Constants.ColourGrad_B))
        self.titlebar.config(bg=General.washed_colour_hex(self.label_colour, Constants.ColourGrad_D))

    def set_frame_colour(self, colour):
        self.frame_colour = colour

    def set_label_colour(self, colour):
        self.label_colour = colour

    # Functionality Methods
    def assert_within_grid(self, column, row):
        assert column >= 0 and row >= 0
        assert column < self.num_columns and row < self.num_rows

    def set_info(self, column, row, text):
        self.assert_within_grid(column, row)
        self.info_spaces[row][column].config(text=text)

    def set_font(self, column, row, font_size):
        self.assert_within_grid(column, row)
        font = tkinter.font.Font(size=12)
        self.info_spaces[row][column].config(font=font)

    def add_info(self, column, row, text):
        self.assert_within_grid(column, row)

        if self.info_spaces[row][column]["text"] is not None:
            self.info_spaces[row][column].config(text=str(self.info_spaces[row][column]["text"]) + str(text))
        else:
            self.info_spaces[row][column].config(text=str(text))
