import tkinter

# Custom Entries constants
from scripts import General
from scripts.frontend import Constants, Parameters
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface

ENTRY_PADDING_X = 12
ENTRY_PADDING_Y = 8

"""
    Parent generic entry
"""


class Entry(tkinter.Entry, WidgetInterface):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=10, text=None):
        self._textvariable = tkinter.StringVar()

        tkinter.Entry.__init__(self, root,
                               textvariable=self._textvariable, width=width)
        self.grid(column=column, row=row,
                  columnspan=columnspan, rowspan=rowspan)
        self.anchor(tkinter.CENTER)

        if text is not None:
            self.insert(0, text)

    def get_entry(self):
        return self._textvariable

    def set_entry(self, value):
        self._textvariable.set(value=value)

    def disable(self):
        self.config(state=tkinter.DISABLED)

    def enable(self):
        self.config(state=tkinter.NORMAL)


"""
    Custom entry
"""


class NavigationEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)


class AccountEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)

        self.grid(padx=16, pady=16)

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_A))


class InfoEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)
        self.grid(sticky=tkinter.EW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)

class InfoEntryEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)
        self.grid(sticky=tkinter.EW)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)


class SearchEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)


class PlotEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)
        self.config(width=12)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
