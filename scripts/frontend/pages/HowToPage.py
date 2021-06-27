import tkinter

from scripts.frontend.pages.GenericPage import BaseFrame

class Frame(BaseFrame):

    def __init__(self, root, base_frame=None):
        BaseFrame.__init__(self, root=root, base_frame=base_frame)

    def destroy(self):
        super().destroy()
