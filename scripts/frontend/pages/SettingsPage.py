import tkinter

from scripts.frontend.pages import GenericPage

class Frame(GenericPage.Frame):

    def __init__(self, root, base_frame=None):
        GenericPage.Frame.__init__(self, root=root, base_frame=base_frame)

    def destroy(self):
        super().destroy()