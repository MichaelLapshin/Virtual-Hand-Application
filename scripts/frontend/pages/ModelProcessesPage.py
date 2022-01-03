import base64
import socketserver
import tkinter

from scripts import General, Warnings, Parameters, Constants, Log
from scripts.backend.connection import API_Helper
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.logic import ModelConnectionServer
from scripts.frontend.page_components import ScrollBlock, InformationBlock, SensorsBufferBlock, SearchBlock, \
    DataInfoBlock, ProgressBar
from scripts.frontend.pages import GenericPage, ModelsPage

TITLE_MODEL_INFORMATION = "Selected Model Information"

model_processes_page = None


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_MODEL_PROCESSES)
        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(2, weight=1)

        # Search space
        self.search_frame = SearchBlock.ModelSearchFrame(
            self, column=0, row=0, rowspan=2,
            title="Available Models", select_change_command=self.selected_change_command)
        self.new_button = SearchButton(
            self.search_frame.button_frame, column=0, row=0, text="New", command=self.new_model_button_command)
        self.search_frame.grid(sticky=tkinter.NSEW)

        # Info frame
        self.info_frame = DataInfoBlock.ModelInfo(self, column=1, row=0, columnspan=2, title="Model Information",
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

        # Creating the server object
        self.server = ModelConnectionServer.ModelServer()

        # Create buttons
        self.button_frame = GenericPage.Frame(self, column=1, row=1, columnspan=1, rowspan=1)
        self.button_frame.columnconfigure(3, weight=1)

        self.zero_sensors_button = InformationButton(self.button_frame, column=0, row=0, text="Zero the Sensors",
                                                     command=self.server.zero_sensors)

        self.start_server_button = InformationButton(self.button_frame, column=1, row=0, text="Start Server",
                                                     command=self.start_server_command)
        self.stop_server_button = \
            InformationButton(self.button_frame, column=2, row=0, text="Stop Server", command=self.stop_server_command)
        self.progress_bar = ProgressBar.Frame(
            self.button_frame, column=3, row=0, columnspan=1, metric_text=" Loaded Finger Models", max_count=10)

        self.start_server_button.disable()
        self.stop_server_button.disable()
        self.zero_sensors_button.disable()

        # Prediction Preview frame
        self.sensor_buffer_block = SensorsBufferBlock.Frame(self, column=0, row=2, columnspan=3)

    def update_colour(self):
        super().update_colour()
        self.search_frame.update_colour()
        self.new_button.update_colour()
        self.info_frame.update_colour()
        self.button_frame.update_colour()
        self.zero_sensors_button.update_colour()
        self.start_server_button.update_colour()
        self.stop_server_button.update_colour()
        self.progress_bar.update_colour()
        self.sensor_buffer_block.update_colour()

        # Progress bar
        self.progress_bar.set_background_colour(
            General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))
        self.progress_bar.set_progress_colour(
            General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_F))

    def update_content(self):
        super().update_content()
        self.search_frame.update_content()
        self.new_button.update_content()
        self.info_frame.update_content()
        self.button_frame.update_content()
        self.zero_sensors_button.update_content()
        self.start_server_button.update_content()
        self.stop_server_button.update_content()
        self.progress_bar.update_content()
        self.sensor_buffer_block.update_content()

    def destroy(self):
        self.search_frame.destroy()
        self.new_button.destroy()
        self.info_frame.destroy()
        self.button_frame.destroy()
        self.zero_sensors_button.destroy()
        self.start_server_button.destroy()
        self.stop_server_button.destroy()
        self.progress_bar.destroy()
        self.sensor_buffer_block.destroy()
        super().destroy()

    def new_model_button_command(self):
        Navigation.navig_bar.select_new_page(Navigation.TITLE_MODELS)
        ModelsPage.models_page._switch_to_frame(ModelsPage.models_page.new_frame)

    def selected_change_command(self):
        if self.search_frame.scroll_block.is_selected_main():
            # Enables the start-server button
            self.start_server_button.enable()

            # Fills in the model information
            # Obtains the data
            selected_index = self.search_frame.scroll_block.get_selected_main()
            data_at_index = self.search_frame.get_index_data(selected_index)

            # Prepares the entries
            entries = {}
            for i in range(0, len(Constants.MODEL_ENTRY_TRANSFER_DATA)):
                entries[Constants.MODEL_ENTRY_TRANSFER_DATA[i]] = data_at_index[i]
            owner_name = ClientConnection.get_user_name_of(entries.get("ID_Owner"))

            # Updates the info frame
            self.info_frame.update_entries(entries=entries, owner_name=owner_name)
        else:
            self.start_server_button.disable()
            self.stop_server_button.disable()
            self.zero_sensors_button.disable()

    def start_server_command(self):
        Log.info("Starting the model server.")

        self.progress_bar.set_count(0)
        self.progress_bar.set_metric_text(" Model Downloading.   Status: Fetching model from the server...")

        # Loads the models into the AppData-Client\temp-models folder
        model_id = self.search_frame.get_selected_main_id()
        model_encoded_str_dir = ClientConnection.fetch_model_encoded_str_dir(model_id)

        # Crops the first line of model_encoded to not create a new directory
        model_encoded_str_dir = model_encoded_str_dir[1::]
        model_encoded_str_dir = model_encoded_str_dir[model_encoded_str_dir.index("#")::]

        self.progress_bar.add_count(1)
        self.progress_bar.set_metric_text(" Model Downloading.   Status: Saving the model locally...")

        # Saves the model
        Log.debug("Obtained the model encoded string.")
        if model_encoded_str_dir is not None:
            API_Helper.decode_string_directory(Parameters.PROJECT_PATH + Constants.TEMP_MODEL_PATH,
                                               model_encoded_str_dir)
        Log.debug("Decoded and saved the model locally.")

        # Server loads
        Log.debug("Starting to load the model into the model server.")
        connect_success = self.server.connect_model(
            models_dir_path=Parameters.PROJECT_PATH + Constants.TEMP_MODEL_PATH,
            progress_bar=self.progress_bar)

        # Starts serving clients until it is stopped
        if connect_success:
            self.server.serve_forever()
            Log.debug("Starting the model server.")

            # GUI Button control
            self.start_server_button.disable()
            self.stop_server_button.enable()
            self.zero_sensors_button.enable()

            self.progress_bar.set_count(10)
        else:
            self.progress_bar.set_count(-1)
            self.progress_bar.set_metric_text(" Failed to start the server. Unable to connect to the hand controller.")

    def stop_server_command(self):
        Log.info("Stopping the model server.")
        if self.server.is_running():
            self.server.disconnect_model()
            self.server.shutdown()

        # GUI Button control
        self.start_server_button.enable()
        self.stop_server_button.disable()
        self.zero_sensors_button.disable()
