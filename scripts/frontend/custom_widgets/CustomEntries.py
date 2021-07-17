import tkinter

# Custom Entries constants
from scripts import General
from scripts.frontend import Constants

ENTRY_PADDING_X = 12
ENTRY_PADDING_Y = 8

"""
    Parent generic entry
"""


class Entry(tkinter.Entry):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
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

        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour10))
        self.grid(padx=16, pady=16)

class InformationEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text)


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


