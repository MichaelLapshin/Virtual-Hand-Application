import tkinter

from scripts import General, Warnings
from scripts.frontend import User, Constants, Navigation
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock
from scripts.frontend.pages import GenericPage

TITLE_MODEL_INFORMATION = "Selected Model Information"


class Frame(GenericPage.NavigationFrame):
    class InfoFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self,
                                       root,
                                       column=column, row=row,
                                       columnspan=columnspan, rowspan=rowspan)
            self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=0)

            # Information frame
            self.info_block = InformationBlock.Frame(self, title=TITLE_MODEL_INFORMATION,
                                                     num_columns=2, num_rows=2,
                                                     frame_colour=Constants.COLOUR_ALPHA,
                                                     label_colour=Constants.COLOUR_BRAVO)
            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            # Buttons Frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=1,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)
            self.button_frame.columnconfigure(2, weight=3)
            self.button_frame.columnconfigure(3, weight=3)
            self.button_frame.columnconfigure(4, weight=1)

            # Create buttons
            self.favourite_button = \
                InformationButton(self.button_frame, column=0, row=0, text="Favourite", command=Warnings.not_complete)
            self.duplicate_button = \
                InformationButton(self.button_frame, column=1, row=0, text="Duplicate", command=Warnings.not_complete)
            self.process_button = \
                InformationButton(self.button_frame, column=2, row=0, text="Process:", command=Warnings.not_complete)
            self.game_engine_button = \
                InformationButton(self.button_frame, column=3, row=0, text="Connection:", command=Warnings.not_complete)
            self.delete_button = \
                InformationButton(self.button_frame, column=4, row=0, text="Delete", command=Warnings.not_complete)

            """
                Additional information
            """
            # Fill in data for the information block
            self.info_block.add_info(0, 0, User.name())
            self.info_block.add_info(1, 0, "hello world!")
            self.info_block.add_info(0, 1, "This is another test \n to check out \n what this type of stuff\n can do.")

        def update_colour(self):
            super().update_colour()
            self.button_frame.update_colour()
            self.favourite_button.update_colour()
            self.duplicate_button.update_colour()
            self.process_button.update_colour()
            self.game_engine_button.update_colour()
            self.delete_button.update_colour()

            self.info_block.set_frame_colour(Constants.COLOUR_BRAVO)
            self.info_block.set_label_colour(Constants.COLOUR_BRAVO)
            self.info_block.update_colour()

            self.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_B))
            self.button_frame.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_B))

    class QueueSearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(sticky=tkinter.NSEW)

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
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)

            # Search buttons & widgets
            self.new_button = SearchButton(self.button_frame, column=0, row=0, text="New",
                                           command=Warnings.not_complete)
            self.search_button = SearchButton(self.button_frame, column=1, row=0, text="Search",
                                              command=Warnings.not_complete)

            # Sorting
            self.button_search_frame = tkinter.Frame(self.button_frame)
            self.button_search_frame.grid(column=0, row=1, columnspan=2, sticky=tkinter.NSEW)
            self.button_search_frame.columnconfigure(1, weight=1)

            self.sort_label = SearchLabel(self.button_search_frame, column=0, row=0, text="Sort by:")
            self.sort_option_menu = SortOptionMenu(self.button_search_frame, column=1, row=0)
            self.sort_option_menu.grid(sticky=tkinter.NSEW)

        def update_content(self):
            self.scroll_models_block.update_content()

        def update_colour(self):
            super().update_colour()
            self.scroll_models_block.update_colour()
            self.button_frame.update_colour()
            self.new_button.update_colour()
            self.search_button.update_colour()
            # self.button_search_frame.update_colour()
            self.sort_label.update_colour()
            self.sort_option_menu.update_colour()

            self.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_B))
            self.button_search_frame.config(bg=self.button_frame.cget("bg"))
            self.button_frame.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_B))

    class CompleteSearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(sticky=tkinter.NSEW)

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
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)

            # Search buttons & widgets
            self.new_button = SearchButton(self.button_frame, column=0, row=0, text="Clear",
                                           command=Warnings.not_complete)
            self.search_button = SearchButton(self.button_frame, column=1, row=0, text="Search",
                                              command=Warnings.not_complete)

            # Sorting
            self.button_search_frame = tkinter.Frame(self.button_frame)
            self.button_search_frame.grid(column=0, row=1, columnspan=2, sticky=tkinter.NSEW)
            self.button_search_frame.columnconfigure(1, weight=1)

            self.sort_label = SearchLabel(self.button_search_frame, column=0, row=0, text="Sort by:")
            self.sort_option_menu = SortOptionMenu(self.button_search_frame, column=1, row=0)
            self.sort_option_menu.grid(sticky=tkinter.NSEW)

        def update_content(self):
            self.scroll_models_block.update_content()

        def update_colour(self):
            super().update_colour()
            self.scroll_models_block.update_colour()
            self.button_frame.update_colour()
            self.new_button.update_colour()
            self.search_button.update_colour()
            # self.button_search_frame.update_colour()
            self.sort_label.update_colour()
            self.sort_option_menu.update_colour()

            self.button_frame.config(bg=General.washed_colour_hex(Constants.COLOUR_ALPHA, Constants.ColourGrad_B))
            self.button_search_frame.config(bg=self.button_frame.cget("bg"))
            self.config(bg=General.washed_colour_hex(Constants.COLOUR_BRAVO, Constants.ColourGrad_B))

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_TRAINING_PROCESSES)

        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)

        # Search space
        self.queue_search_frame = Frame.QueueSearchFrame(self, column=0, row=0)
        self.complete_search_frame = Frame.CompleteSearchFrame(self, column=1, row=0)

        # Info frame
        self.info_frame = Frame.InfoFrame(self, column=2, row=0)

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=1, columnspan=3)

    def update_colour(self):
        super().update_colour()
        self.queue_search_frame.update_colour()
        self.complete_search_frame.update_colour()
        self.info_frame.update_colour()
        self.prediction_preview_block.update_colour()

    def update_content(self):
        self.queue_search_frame.update_content()
        self.complete_search_frame.update_content()

    def destroy(self):
        super().destroy()
