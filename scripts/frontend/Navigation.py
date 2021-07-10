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


class NavigationBar(tkinter.Frame):

    def __init__(self, root, column, row, columnspan=1, rowspan=1):
        tkinter.Frame.__init__(self, root)

        # Navigation variables
        self.current_page = None
        self.buttons_page_map = {}

        """
            Navigation Bar configurations
        """
        self.config(bg=General.washed_colour_hex(Constants.BASE_BLUE_COLOUR, Constants.Colour20))
        self.config(bd=1, relief=tkinter.RIDGE)

        # Grid configurations
        self.grid(column=column, row=row, columnspan=columnspan, rowspan=rowspan)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

    def add_page(self, page):
        # Configures column eight
        self.columnconfigure(self.num_buttons(), weight=1)

        new_button = NavigationButton(
            self,
            column=self.num_buttons(), row=0,
            columnspan=1, rowspan=Constants.MAX_SPAN,
            text=page.get_page_title(),
            command=lambda: self.select_new_page(page.get_page_title()))
        page.grid_remove()

        self.buttons_page_map[new_button] = page

    def select_new_page(self, new_page_name):
        # Asserts that the page exists
        assert new_page_name is not None

        # Sets old page button back to blue
        if self.current_page is not None:
            for b in self.buttons_page_map.keys():
                if b.cget("text") == self.current_page.get_page_title():
                    b.config(bg=NavigationButton.UNSELECTED_COLOUR)

        # Sets current page button to green
        for b in self.buttons_page_map.keys():
            if b.cget("text") == new_page_name:
                b.config(bg=NavigationButton.SELECTED_COLOUR)

        # Replaces old page with the new
        new_page = None
        for p in self.buttons_page_map.values():
            if p.get_page_title() == new_page_name:
                new_page = p;

        assert new_page is not None

        # Hides the old page, shows the new page
        if self.current_page is not None:
            self.current_page.grid_remove()
        new_page.grid()
        self.current_page = new_page

        return self.current_page

    def num_buttons(self):
        return len(self.buttons_page_map)

    def destroy(self):
        # Destroys navigation buttons
        for b in self.buttons_page_map.keys():
            self.buttons_page_map.get(b).destroy()
            b.destroy()

        # Destroys the frame
        super().destroy()
