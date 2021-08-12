import tkinter

from scripts import General, Warnings, Parameters, Constants
from scripts.frontend import  Navigation
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock
from scripts.frontend.pages import GenericPage

TITLE_SELECTED_MODEL_INFORMATION = "Selected Model Information"
TITLE_SELECTED_DATABASE_INFORMATION = "Selected Database Information"
TITLE_NEW_MODEL_INFORMATION = "New Model Information"


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)
        self.grid(padx=0, pady=0, sticky=tkinter.NSEW)
        self.config(bd=0, relief=None)

        # Weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # Frames
        self.view_frame = ViewFrame(self, base_frame=base_frame)
        self.new_frame = NewFrame(self, base_frame=base_frame)
        self.view_frame.grid(row=0)
        self.new_frame.grid(row=0)

        # Swt switch frame functions
        self.view_frame.set_switch_to_new_frame(lambda: self._switch_to_frame(self.new_frame))
        self.new_frame.set_switch_to_view_frame(lambda: self._switch_to_frame(self.view_frame))

        # Default view the new frame
        self._switch_to_frame(self.view_frame)

    def _switch_to_frame(self, frame):
        self.view_frame.grid_remove()
        self.new_frame.grid_remove()

        # Set and switch display to current frame
        self.current_frame = frame
        self.current_frame.grid()

    def update_colour(self):
        super().update_colour()
        self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_A))
        self.view_frame.update_colour()
        self.new_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.view_frame.update_content()
        self.new_frame.update_content()


class ViewFrame(GenericPage.NavigationFrame):
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
            self.info_block = InformationBlock.Frame(self, title=TITLE_SELECTED_MODEL_INFORMATION,
                                                     num_columns=2, num_rows=2)

            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            self.info_block.set_font(0, 0, 0)
            self.info_block.set_font(1, 0, 0)

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

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    class SearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
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

        def update_colour(self):
            super().update_colour()
            self.scroll_models_block.update_colour()
            self.button_frame.update_colour()

            self.new_button.update_colour()
            self.search_button.update_colour()
            self.sort_label.update_colour()
            self.sort_option_menu.update_colour()

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.button_search_frame.config(bg=self.button_frame.cget("bg"))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def update_content(self):
            super().update_content()
            self.scroll_models_block.update_content()

        def set_switch_frame_command(self, command):
            self.new_button.config(command=command)

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = ViewFrame.SearchFrame(self, column=0, row=0)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.info_frame = ViewFrame.InfoFrame(self, column=1, row=0)

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=1, columnspan=2)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.info_frame.update_colour()
        self.prediction_preview_block.update_colour()

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()

    def destroy(self):
        super().destroy()

    def set_switch_to_new_frame(self, command):
        self.search_frame.set_switch_frame_command(command=command)


class NewFrame(GenericPage.NavigationFrame):
    class DatasetInfoFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self,
                                       root,
                                       column=column, row=row,
                                       columnspan=columnspan, rowspan=rowspan)
            self.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure weights
            self.columnconfigure(0, weight=1)
            self.rowconfigure(0, weight=1)

            # Information frame
            self.info_block = InformationBlock.Frame(self, title=TITLE_SELECTED_DATABASE_INFORMATION,
                                                     num_columns=2, num_rows=2)
            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            self.info_block.set_font(0, 0, 0)
            self.info_block.set_font(1, 0, 0)

            """
                Additional information
            """
            # Fill in data for the information block
            # self.info_block.add_info(0, 0, User.get_name())
            self.info_block.add_info(1, 0, "hello world!")
            self.info_block.add_info(0, 1, "This is another test \n to check out \n what this type of stuff\n can do.")

        def update_colour(self):
            super().update_colour()
            self.info_block.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.info_block.set_label_colour(Parameters.COLOUR_BRAVO)
            self.info_block.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    class NewModelInfoFrame(GenericPage.Frame):

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
            self.info_block = InformationBlock.Frame(self, title=TITLE_SELECTED_DATABASE_INFORMATION,
                                                     num_columns=2, num_rows=2)
            self.info_block.config()
            self.info_block.grid(column=0, row=0)
            self.info_block.grid(columnspan=1, rowspan=1)

            self.info_block.set_font(0, 0, 0)
            self.info_block.set_font(1, 0, 0)

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

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    class SearchFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root)
            self.grid(column=column, row=row)
            self.grid(columnspan=columnspan, rowspan=rowspan)
            self.grid(sticky=tkinter.NS)

            # Configure weights
            self.rowconfigure(2, weight=1)
            self.columnconfigure(0, weight=1)

            # Select Dataset title
            self.select_dataset_label = CustomLabels.TitleLabel(self, column=0, row=0, text="Select Datasets")

            # Scroll block
            self.scroll_models_block = ScrollBlock.Frame(self, selectable_items=True)
            self.scroll_models_block.grid(column=0, row=2)
            self.scroll_models_block.grid(columnspan=1, rowspan=1)

            # Buttons frame
            self.button_frame = GenericPage.Frame(self,
                                                  column=0, row=1,
                                                  columnspan=1, rowspan=1)
            self.button_frame.config(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)

            # Configure button frame weights
            self.button_frame.rowconfigure(0, weight=1)
            self.button_frame.rowconfigure(1, weight=1)
            self.button_frame.columnconfigure(0, weight=1)
            self.button_frame.columnconfigure(1, weight=1)

            # Search buttons & widgets
            self.cancel_button = SearchButton(self.button_frame, column=0, row=0, text="Cancel",
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

        def update_colour(self):
            super().update_colour()
            self.scroll_models_block.update_colour()
            self.button_frame.update_colour()

            self.select_dataset_label.update_colour()
            self.cancel_button.update_colour()
            self.search_button.update_colour()
            self.sort_label.update_colour()
            self.sort_option_menu.update_colour()

            self.cancel_button.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))
            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.button_search_frame.config(bg=self.button_frame.cget("bg"))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def update_content(self):
            super().update_content()

            self.scroll_models_block.update_content()

        def set_switch_frame_command(self, command):
            self.cancel_button.config(command=command)

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODELS)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = NewFrame.SearchFrame(self, column=0, row=0, rowspan=2)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.database_info_frame = NewFrame.DatasetInfoFrame(self, column=1, row=0)
        self.new_model_info_frame = NewFrame.NewModelInfoFrame(self, column=1, row=1)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.database_info_frame.update_colour()
        self.new_model_info_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()
        self.database_info_frame.update_content()
        self.new_model_info_frame.update_content()

    def destroy(self):
        self.search_frame.update_content()
        self.database_info_frame.update_content()
        self.new_model_info_frame.update_content()
        super().destroy()

    def set_switch_to_view_frame(self, command):
        self.search_frame.set_switch_frame_command(command=command)
