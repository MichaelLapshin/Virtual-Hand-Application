import tkinter

from scripts import General, Warnings, Parameters, Constants
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock, SearchBlock, \
    DataInfoBlock, ProgressBar
from scripts.frontend.pages import GenericPage

TITLE_MODEL_INFORMATION = "Selected Model Information"


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_TRAINING_PROCESSES)

        # Weights
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=3)
        self.rowconfigure(1, weight=1)

        # Search space
        self.queue_search_frame = SearchBlock.ModelTrainingSearchFrame(
            self, column=0, row=0, queue_fetch_function=ClientConnection.get_model_training_queue,
            title="Queue", multi_select=False,
            select_change_command= self.queue_selected_entry_update_command)

        self.complete_search_frame = SearchBlock.ModelTrainingSearchFrame(
            self, column=1, row=0, queue_fetch_function=ClientConnection.get_model_complete_queue,
            title="Complete", multi_select=False,
            select_change_command= self.complete_selected_entry_update_command)
        self.clear_button = SearchButton(
            self.complete_search_frame.button_frame, column=0, row=0, text="Clear", command=self.clear_complete_list)

        # Info frame
        self.info_frame = DataInfoBlock.ModelInfo(
            self, column=2, row=0, title="Model Information",
            general_options_data={"Name": False, "ID_Owner": False, "Date_Created": False,
                                  "Permission": False, "Rating": False, "ID_Dataset": False, "Frames_Shift": False},
            right_options_data={"Num_Training_Frames": False, "Learning_Rate": False,
                                "Batch_Size": False, "Num_Epochs": False,
                                "Layer_Types": False, "Num_Layers": False, "Num_Nodes_Per_Layer": False},
            right_column_title="Training Information")

        self.progress_bar = ProgressBar.Frame(self.info_frame, column=0, row=3, columnspan=2, metric_text=" Epochs")

        # Prediction Preview frame
        self.prediction_preview_block = PredictionPreviewBlock.Frame(self, column=0, row=1, columnspan=3)

    def update_colour(self):
        super().update_colour()
        self.queue_search_frame.update_colour()
        self.complete_search_frame.update_colour()
        self.clear_button.update_colour()
        self.info_frame.update_colour()
        self.prediction_preview_block.update_colour()

    def update_content(self):
        super().update_content()
        self.queue_search_frame.update_content()
        self.complete_search_frame.update_content()
        self.clear_button.update_content()
        self.info_frame.update_content()
        self.prediction_preview_block.update_content()

    def destroy(self):
        super().destroy()

    def selected_entry_update_command(self, search_frame):
        # Obtains the data
        selected_index = search_frame.scroll_block.get_selected_main()
        data_at_index = search_frame.get_index_data(selected_index)

        # Prepares the entries
        entries = {}
        for i in range(0, len(Constants.MODEL_ENTRY_TRANSFER_DATA)):
            entries[Constants.MODEL_ENTRY_TRANSFER_DATA[i]] = data_at_index[i]
        owner_name = ClientConnection.get_user_name_of(entries.get("ID_Owner"))

        # Updates the info frame
        self.info_frame.update_entries(entries=entries, owner_name=owner_name)

        # Loads in the prediction and error images
        selected_model_id = search_frame.get_selected_main_id()
        self.prediction_preview_block.image_frame.load_new_images(model_id=selected_model_id)
        self.prediction_preview_block.button_frame.update_image_state()

    def clear_complete_list(self):
        ClientConnection.clear_worker_complete_queue()
        self.complete_search_frame.search_button_command()

    def queue_selected_entry_update_command(self):
        self.selected_entry_update_command(search_frame=self.queue_search_frame)
        self.complete_search_frame.scroll_block.unselect_main()

    def complete_selected_entry_update_command(self):
        self.selected_entry_update_command(search_frame=self.complete_search_frame)
        self.queue_search_frame.scroll_block.unselect_main()
