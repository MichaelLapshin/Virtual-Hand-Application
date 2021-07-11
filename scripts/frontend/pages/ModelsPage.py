import tkinter

from scripts import General
from scripts.frontend import User, Constants, Navigation
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock
from scripts.frontend.pages import GenericPage

TITLE_MODEL_INFORMATION = "Selected Model Information"


class BaseFrame(GenericPage.NavigationFrame):
    class InfoFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self,
                                       root,
                                       column=column, row=row,
                                       columnspan=columnspan, rowspan=rowspan)
            self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour20))
            self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=0)

            # Information frame
            self.info_block = InformationBlock.Frame(self, title=TITLE_MODEL_INFORMATION,
                                                     num_columns=2, num_rows=2)
            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            # Buttons Frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=1,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour20))
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=3)
            self.button_frame.columnconfigure(3, weight=3)
            self.button_frame.columnconfigure(4, weight=1)

            # Create buttons
            self.favourite_button = \
                InformationButton(self.button_frame, column=0, row=0, text="Favourite", command=None)
            self.duplicate_button = \
                InformationButton(self.button_frame, column=1, row=0, text="Duplicate", command=None)
            self.process_button = \
                InformationButton(self.button_frame, column=2, row=0, text="Process:", command=None)
            self.game_engine_button = \
                InformationButton(self.button_frame, column=3, row=0, text="Connection:", command=None)
            self.delete_button = \
                InformationButton(self.button_frame, column=4, row=0, text="Delete", command=None)

            """
                Additional information
            """
            # Fill in data for the information block
            self.info_block.add_info(0, 0, User.name())
            self.info_block.add_info(1, 0, "hello world!")
            self.info_block.add_info(0, 1, "This is another test \n to check out \n what this type of stuff\n can do.")

    class SearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
            self.config(bg=General.washed_colour_hex(Constants.BASE_GREEN_COLOUR, Constants.Colour20))
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(sticky=tkinter.NS)

            # Configure weights
            self.rowconfigure(1, weight=1)
            self.columnconfigure(0, weight=1)

            # Scroll block
            self.scroll_models_block = ScrollBlock.Frame(self, selectable_items=True)
            self.scroll_models_block.grid(column=0, row=1)
            self.scroll_models_block.grid(columnspan=1, rowspan=1)

            # Buttons frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=0,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour20))
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)

            # Search buttons & widgets
            self.new_button = SearchButton(self.button_frame, column=0, row=0, text="New", command=None)
            self.search_button = SearchButton(self.button_frame, column=1, row=0, text="Search", command=None)

            # Sorting
            self.button_search_frame = tkinter.Frame(self.button_frame, bg=self.button_frame.cget("bg"))
            self.button_search_frame.grid(column=0, row=1, columnspan=2, sticky=tkinter.NSEW)
            self.button_search_frame.columnconfigure(1, weight=1)

            self.sort_label = SearchLabel(self.button_search_frame, column=0, row=0, text="Sort by:")
            self.sort_option_menu = SortOptionMenu(self.button_search_frame, column=1, row=0)
            self.sort_option_menu.grid(sticky=tkinter.NSEW)

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)

        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = BaseFrame.SearchFrame(self, column=0, row=0)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.info_frame = BaseFrame.InfoFrame(self, column=1, row=0)

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=1, columnspan=2)

    def destroy(self):
        super().destroy()


class NewFrame(GenericPage.Frame):
    def __init__(self, root, base_frame=None):
        GenericPage.Frame.__init__(self, root=root, base_frame=base_frame)

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

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=1, columnspan=2)

    def destroy(self):
        super().destroy()
