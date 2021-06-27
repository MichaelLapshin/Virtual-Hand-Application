import tkinter


class BaseFrame(tkinter.Frame):

    def __init__(self, root, column=0, row=0, columnspan=1, rowspan=1, base_frame=None):
        tkinter.Frame.__init__(self, root)

        if base_frame is not None:
            # Uses base_face dimensions
            self.grid(column=base_frame.grid_info()["column"], row=base_frame.grid_info()["row"],
                      columnspan=base_frame.grid_info()["columnspan"], rowspan=base_frame.grid_info()["rowspan"])
        else:
            # Uses input (or default) dimensions
            self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        self.grid_remove()
