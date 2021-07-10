import tkinter

from scripts.frontend import Navigation
from scripts.frontend.pages import GenericPage


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_DATASETS)

    def destroy(self):
        super().destroy()
