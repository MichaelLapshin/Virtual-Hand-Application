import tkinter

from scripts import General, Warnings, Parameters, Constants
from scripts.frontend import Navigation
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock, SearchBlock
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
                                                     num_columns=2, num_rows=2)
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
            # self.info_block.add_info(0, 0, User.get_name())
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

            self.info_block.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.info_block.set_label_colour(Parameters.COLOUR_BRAVO)
            self.info_block.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))
            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_TRAINING_PROCESSES)

        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)

        # Search space
        # self.queue_search_frame = Frame.QueueSearchFrame(self, column=0, row=0)
        # self.complete_search_frame = Frame.CompleteSearchFrame(self, column=1, row=0)

        self.queue_search_frame = SearchBlock.ModelSearchFrame(self, column=0, row=0, title="Queue")
        self.complete_search_frame = SearchBlock.ModelSearchFrame(self, column=1, row=0, title="Complete")

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
        super().update_content()
        self.queue_search_frame.update_content()
        self.complete_search_frame.update_content()

    def destroy(self):
        super().destroy()
