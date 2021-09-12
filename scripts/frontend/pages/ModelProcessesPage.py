import base64
import tkinter

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.backend.connection import API_Helper
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.logic import ModelConnectionServer
from scripts.frontend.page_components import ScrollBlock, InformationBlock, SensorsBufferBlock, SearchBlock, \
    DataInfoBlock, ProgressBar
from scripts.frontend.pages import GenericPage

TITLE_MODEL_INFORMATION = "Selected Model Information"

model_processes_page = None


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

            """
                Additional information
            """
            # Fill in data for the information block
            # self.info_block.add_info(0, 0, Client.get_name())
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

            self.info_block.set_label_colour(Parameters.COLOUR_BRAVO)
            self.info_block.set_frame_colour(Parameters.COLOUR_BRAVO)
            self.info_block.update_colour()

            self.button_frame.config(bg=General.washed_colour_hex(Parameters.COLOUR_ALPHA, Parameters.ColourGrad_B))
            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODEL_PROCESSES)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)

        # Search space
        self.search_frame = SearchBlock.ModelSearchFrame(
            self, column=0, row=0, rowspan=2,
            title="Available Models", select_change_command=self.selected_change_command)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.info_frame = DataInfoBlock.ModelInfo(self, column=1, row=0, title="Model Information",
                                                  general_options_data={"Name": False, "ID_Owner": False,
                                                                        "Date_Created": False,
                                                                        "Permission": False, "Rating": False,
                                                                        "ID_Dataset": False, "Frames_Shift": False},
                                                  right_options_data={"Num_Training_Frames": False,
                                                                      "Learning_Rate": False,
                                                                      "Batch_Size": False, "Num_Epochs": False,
                                                                      "Layer_Types": False, "Num_Layers": False,
                                                                      "Num_Nodes_Per_Layer": False},
                                                  right_column_title="Training Information")

        # Create buttons
        self.button_frame = GenericPage.Frame(self, column=1, row=1, columnspan=1, rowspan=1)
        self.start_server_button = \
            InformationButton(self.button_frame, column=0, row=0,
                              text="Start Server", command=self.start_server_command)
        self.stop_server_button = \
            InformationButton(self.button_frame, column=1, row=0, text="Stop Server", command=self.stop_server_command)
        self.progress_bar = ProgressBar.Frame(
            self.button_frame, column=2, row=0, columnspan=2,
            metric_text=" Loaded Finger Models", max_count=Constants.NUM_FINGERS * Constants.NUM_LIMBS_PER_FINGER)

        self.start_server_button.disable()
        self.stop_server_button.disable()

        # Prediction Preview frame
        self.prediction_preview_block = SensorsBufferBlock.Frame(self, column=0, row=2, columnspan=2)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.info_frame.update_colour()
        self.button_frame.update_colour()
        self.start_server_button.update_colour()
        self.stop_server_button.update_colour()
        self.progress_bar.update_colour()
        self.prediction_preview_block.update_colour()

        # Progress bar
        self.progress_bar.set_background_colour(
            General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))
        self.progress_bar.set_progress_colour(
            General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_F))

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()
        self.info_frame.update_content()
        self.button_frame.update_content()
        self.start_server_button.update_content()
        self.stop_server_button.update_content()
        self.progress_bar.update_content()
        self.prediction_preview_block.update_content()

    def destroy(self):
        self.search_frame.destroy()
        self.info_frame.destroy()
        self.button_frame.destroy()
        self.start_server_button.destroy()
        self.stop_server_button.destroy()
        self.progress_bar.destroy()
        self.prediction_preview_block.destroy()
        super().destroy()

    def selected_change_command(self):
        if self.search_frame.scroll_block.is_selected_main():
            self.start_server_button.enable()
        else:
            self.start_server_button.disable()
            self.stop_server_button.disable()

    def start_server_command(self):
        self.progress_bar.set_count(0)
        self.progress_bar.set_metric_text(" Models Downloaded.   Status: Fetching models from the server...")

        # Loads the models into the AppData-Client\temp-models folder
        model_id = self.search_frame.get_selected_main_id()
        model_encoded_str_dir = ClientConnection.fetch_model_encoded_str_dir(model_id)

        # Saves the model # TODO, FINISH THIS!
        Log.debug("Model encoded string: " + str(model_encoded_str_dir))
        if model_encoded_str_dir is not None:
            API_Helper.decode_string_directory(Parameters.PROJECT_PATH + Constants.TEMP_MODEL_PATH,
                                               model_encoded_str_dir)

        self.progress_bar.set_metric_text(" Models Downloaded.   Status: Saving the models locally...")

        #
        # self.server.connect(
        #     models_dir_path=Parameters.PROJECT_PATH + Constants.TEMP_MODEL_PATH + str(model_id) + Constants.MODEL_EXT,
        #     progress_bar=self.progress_bar)

        Warnings.not_complete()
        self.start_server_button.disable()
        self.stop_server_button.enable()

    def stop_server_command(self):
        Warnings.not_complete()

        self.start_server_button.enable()
        self.stop_server_button.disable()
