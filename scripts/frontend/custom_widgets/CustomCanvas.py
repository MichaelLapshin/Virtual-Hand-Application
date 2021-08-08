import tkinter

from scripts import General, Parameters
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class Canvas(tkinter.Canvas, WidgetInterface):

    def __init__(self, root, column, row, columnspan=1, rowspan=1):
        tkinter.Canvas.__init__(self, root)

        self.anchor(tkinter.CENTER)
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.grid(sticky=tkinter.NSEW)

    def update_content(self):
        super().update_colour()

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
