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

    def __init__(self, root, column, row, columnspan=1, rowspan=1, textvariable=None, width=5, text=None):
        tkinter.Entry.__init__(self, root,
                               textvariable=textvariable, width=width)
        self.grid(column=column, row=row,
                  columnspan=columnspan, rowspan=rowspan)
        self.anchor(tkinter.CENTER)

        if text is not None:
            self.insert(0, text)

    def disable(self):
        self.config(state=tkinter.DISABLED)

    def enable(self):
        self.config(state=tkinter.NORMAL)

"""
    Custom entry
"""


class NavigationEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, textvariable=None, width=5, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text, textvariable=textvariable)


class AccountEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, textvariable=None, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text, textvariable=textvariable)

        self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour10))
        self.grid(padx=16, pady=16)

class InformationEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, textvariable=None, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text, textvariable=textvariable)


class SearchEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, textvariable=None, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text, textvariable=textvariable)


class PlotEntry(Entry):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, width=5, textvariable=None, text=None):
        Entry.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       width=width, text=text, textvariable=textvariable)
