import tkinter

from scripts.frontend import User
from scripts.frontend.page_components import ScrollBlock, InformationBlock
from scripts.frontend.pages.GenericPage import BaseFrame

TITLE_MODEL_INFORMATION = "Model Information"


class Frame(BaseFrame):

    def __init__(self, root, base_frame=None):
        BaseFrame.__init__(self, root=root, base_frame=base_frame)

        # Weights
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        # Scrolling frame with the models
        self.scroll_models_block = ScrollBlock.Frame(self, selectable_items=True)
        self.scroll_models_block.grid(column=0, row=0)
        self.scroll_models_block.grid(columnspan=1, rowspan=1)

        # Information frame
        self.info_block = InformationBlock.Frame(self, title=TITLE_MODEL_INFORMATION, num_columns=2, num_rows=3)

        # Fill in data for the information block
        self.info_block.add_info(0, 0, User.name())
        self.info_block.add_info(0, 2, "Hello \n\n\n\n\n\n\n Hi")
        self.info_block.add_info(1, 0, "hello world!")
        self.info_block.add_info(1, 2, "Yes, this is the one! \n oh yeah!")
        self.info_block.add_info(0, 1, "This is another test \n to check out \n what this type of stuff\n can do.")

        self.info_block.grid(column=1, row=0, columnspan=1, rowspan=1)

    def destroy(self):
        super().destroy()
