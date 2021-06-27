import tkinter

# Custom Labels constants
LABEL_PADDING_X = 12
LABEL_PADDING_Y = 8

"""
    Parent generic label
"""


class Label(tkinter.Label):

    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None):
        tkinter.Label.__init__(self, root, text=text, padx=padx, pady=pady)
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)


"""
    Custom label
"""


class NavigationLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.anchor(tkinter.CENTER)


class InformationLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.anchor(tkinter.CENTER)


class SearchLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.anchor(tkinter.CENTER)


class PlotLabel(Label):
    def __init__(self, root, column, row, columnspan=1, rowspan=1, padx=5, pady=5, text=None):
        Label.__init__(self, root, column=column, row=row,
                       columnspan=columnspan, rowspan=rowspan,
                       padx=padx, pady=pady,
                       text=text)
        self.anchor(tkinter.CENTER)
