import tkinter
from PIL import ImageTk, Image
from tkinter import messagebox
from tkinter import filedialog

from scripts import General
from scripts.frontend import Constants, User

from scripts.frontend.custom_widgets.CustomButtons import NavigationButton
from scripts.frontend.custom_widgets.CustomEntry import NavigationEntry
from scripts.frontend.custom_widgets.CustomLabels import NavigationLabel

# Navigation constants
TITLE_MODELS = "Models"
TITLE_DATASETS = "Datasets"
TITLE_TRAINING_PROCESSES = "Training Processes"
TITLE_MODEL_PROCESSES = "Model Processes"
TITLE_HOW_TO = "How to"
TITLE_PROJECT_INFORMATION = "Project Information"
TITLE_ACCOUNT = "Account"
TITLE_SETTINGS = "Settings"

# Navigation variables
current_page = None
page_map = {}


def add_page_map(name, page):
    page_map[name] = page


def select_new_page(new_page_name):
    global current_page, page_map

    # Asserts that the page exists
    assert new_page_name is not None
    assert page_map.get(new_page_name) is not None

    # Replaces old page with the new
    new_page = page_map.get(new_page_name)
    if current_page is not None:
        current_page.grid_remove()
    new_page.grid()
    current_page = new_page

    return current_page


class NavigationBar(tkinter.Frame):

    def __init__(self, root, column, row, columnspan=1, rowspan=1):
        tkinter.Frame.__init__(self, root)
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)

        """
            Navigation Bar configurations
        """
        self.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour20))
        self.config(bd=1, relief=tkinter.RIDGE)
        self.grid(padx=5, pady=5)

        """
            Navigation buttons
        """
        self.button_Models = NavigationButton(
            self,
            column=0, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_MODELS, command=lambda: select_new_page(TITLE_MODELS))

        self.button_Datasets = NavigationButton(
            self,
            column=1, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_DATASETS, command=lambda: select_new_page(TITLE_DATASETS))

        self.button_TrainingProcesses = NavigationButton(
            self,
            column=2, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_TRAINING_PROCESSES, command=lambda: select_new_page(TITLE_TRAINING_PROCESSES))

        self.button_ModelProcesses = NavigationButton(
            self,
            column=3, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_MODEL_PROCESSES, command=lambda: select_new_page(TITLE_MODEL_PROCESSES))

        self.button_HowTo = NavigationButton(
            self,
            column=4, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_HOW_TO, command=lambda: select_new_page(TITLE_HOW_TO))

        self.button_ProjectInformation = NavigationButton(
            self,
            column=5, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_PROJECT_INFORMATION, command=lambda: select_new_page(TITLE_PROJECT_INFORMATION))

        self.button_Account = NavigationButton(
            self,
            column=6, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_ACCOUNT, command=lambda: select_new_page(TITLE_ACCOUNT))

        self.button_Settings = NavigationButton(
            self,
            column=7, row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=TITLE_SETTINGS, command=lambda: select_new_page(TITLE_SETTINGS))




    def destroy(self):
        # Destroys navigation buttons
        self.button_Models.destroy()
        self.button_Datasets.destroy()
        self.button_TrainingProcesses.destroy()
        self.button_ModelProcesses.destroy()
        self.button_HowTo.destroy()
        self.button_ProjectInformation.destroy()
        self.button_Settings.destroy()

        # Destroys the frame
        super().destroy()
