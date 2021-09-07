import tkinter

from scripts import General, Warnings, Parameters, Constants
from scripts.frontend import Navigation, ClientConnection
from scripts.frontend.custom_widgets.CustomButtons import InformationButton, SearchButton
from scripts.frontend.custom_widgets.CustomLabels import SearchLabel
from scripts.frontend.custom_widgets.CustomOptionMenu import SortOptionMenu
from scripts.frontend.logic import ProgressBarUpdater
from scripts.frontend.page_components import ScrollBlock, InformationBlock, PredictionPreviewBlock, SearchBlock, \
    DataInfoBlock, ProgressBar
from scripts.frontend.pages import GenericPage, ModelsPage
from scripts.logic import Worker

TITLE_MODEL_INFORMATION = "Selected Model Information"

training_processes_page = None


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
            select_change_command=self.queue_selected_entry_update_command)
        self.new_button = SearchButton(
            self.queue_search_frame.button_frame, column=0, row=0, text="New", command=self.new_model_button_command)

        self.complete_search_frame = SearchBlock.ModelTrainingSearchFrame(
            self, column=1, row=0, queue_fetch_function=ClientConnection.get_model_complete_queue,
            title="Complete", multi_select=False,
            select_change_command=self.complete_selected_entry_update_command)
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
        self.new_button.update_colour()
        self.complete_search_frame.update_colour()
        self.clear_button.update_colour()
        self.info_frame.update_colour()
        self.progress_bar.update_colour()
        self.prediction_preview_block.update_colour()

    def update_content(self):
        super().update_content()
        self.queue_search_frame.update_content()
        self.new_button.update_content()
        self.complete_search_frame.update_content()
        self.clear_button.update_content()
        self.info_frame.update_content()
        self.prediction_preview_block.update_content()

        # Progress bar
        self.progress_bar.set_background_colour(
            General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_C))
        self.progress_bar.set_progress_colour(
            General.washed_colour_hex(Constants.COLOUR_GREEN, Parameters.ColourGrad_F))

        self.progress_bar.update_content()

    def destroy(self):
        self.queue_search_frame.destroy()
        self.new_button.destroy()
        self.complete_search_frame.destroy()
        self.clear_button.destroy()
        self.info_frame.destroy()
        self.prediction_preview_block.destroy()
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

    def new_model_button_command(self):
        Navigation.navig_bar.select_new_page(Navigation.TITLE_MODELS)
        ModelsPage.models_page._switch_to_frame(ModelsPage.models_page.new_frame)

    def clear_complete_list(self):
        ClientConnection.clear_worker_complete_queue()
        self.complete_search_frame.search_button_command()
        self.prediction_preview_block.image_frame.clear_images()
        self.info_frame.clear_info_frame()
        self.progress_bar.clear()

    def queue_selected_entry_update_command(self):
        # Updates progress bar
        ProgressBarUpdater.remove_all_progress_bar_jobs()
        Worker.worker.add_task(job=ProgressBarUpdater.JobUpdateProgressBar(
            job_id=self.queue_search_frame.get_job_id_of_selected_main(), progress_bar_obj=self.progress_bar))

        self.selected_entry_update_command(search_frame=self.queue_search_frame)
        self.complete_search_frame.scroll_block.unselect_main()

        # Clears the images (because the images won't be loaded at this point)
        self.prediction_preview_block.image_frame.clear_images()

    def complete_selected_entry_update_command(self):
        # Updates progress bar
        ProgressBarUpdater.remove_all_progress_bar_jobs()
        Worker.worker.add_task(job=ProgressBarUpdater.JobUpdateProgressBar(
            job_id=self.complete_search_frame.get_job_id_of_selected_main(), progress_bar_obj=self.progress_bar))

        self.selected_entry_update_command(search_frame=self.complete_search_frame)
        self.queue_search_frame.scroll_block.unselect_main()

        # Loads in the prediction and error images
        selected_model_id = self.complete_search_frame.get_selected_main_id()
        if selected_model_id is not None:
            self.prediction_preview_block.image_frame.load_new_images(model_id=selected_model_id)
            self.prediction_preview_block.button_frame.update_image_state()
