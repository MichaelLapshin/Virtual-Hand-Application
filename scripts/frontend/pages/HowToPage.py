import tkinter

from scripts.frontend.page_components import InformationBlock
from  scripts.frontend.pages import GenericPage

class Frame(GenericPage.Frame):

    def __init__(self, root, base_frame=None):
        GenericPage.Frame.__init__(self, root=root, base_frame=base_frame)
        self.grid(sticky=tkinter.EW)

        # Creates the info block
        self.info_block = InformationBlock.Frame(self, num_columns=4, num_rows=4, title="How to...")
        self.columnconfigure(0, weight=1)

        # First row titles
        self.info_block.add_info(column=0, row=0, text="View a Model")
        self.info_block.add_info(column=1, row=0, text="Create a Model")
        self.info_block.add_info(column=2, row=0, text="View a Dataset")
        self.info_block.add_info(column=3, row=0, text="Create a Dataset")

        # Seconds row titles
        self.info_block.add_info(column=0, row=2, text="")
        self.info_block.add_info(column=1, row=2, text="")
        self.info_block.add_info(column=2, row=2, text="View a Training Process")
        self.info_block.add_info(column=3, row=2, text="View a Model Process")

    def destroy(self):
        super().destroy()
