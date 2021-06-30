import tkinter

from scripts import Warnings
from scripts.frontend.pages import \
    GenericPage, ModelsPage, DatasetsPage, TrainingProcessesPage, \
    ModelProcessesPage, HowToPage, ProjectInformationPage, AccountPage, SettingsPage

from scripts.frontend import \
    Constants, Parameters, \
    Navigation, ClientConnection, User

# App constants
APP_TITLE = "Virtual-Hand"
APP_ICON = "images\\virtualhand_icons\\virtualhand_icon_YuG_1.ico"

# Created the window
root = tkinter.Tk()
root.title(APP_TITLE)
root.iconbitmap(default=APP_ICON)
root.geometry(Parameters.default_resolution)

# client_conn = ClientConnection()

# Template frame for the pages to use
frame_window = GenericPage.BaseFrame(
    root=root,
    column=0, row=1,
    columnspan=Constants.MAX_SPAN, rowspan=Constants.MAX_SPAN)
frame_window.grid()

# Creates and adds the pages
Navigation.add_page_map(Navigation.TITLE_MODELS, ModelsPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_DATASETS, DatasetsPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_TRAINING_PROCESSES, TrainingProcessesPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_MODEL_PROCESSES, ModelProcessesPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_HOW_TO, HowToPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_PROJECT_INFORMATION, ProjectInformationPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_ACCOUNT, AccountPage.Frame(root, base_frame=frame_window))
Navigation.add_page_map(Navigation.TITLE_SETTINGS, SettingsPage.Frame(root, base_frame=frame_window))

# Destroys reference frame
frame_window.destroy()

# Starts at the Account page by default
Navigation.select_new_page(Navigation.TITLE_ACCOUNT)

# Creates the navigation bar and links them to the page
navig_bar = Navigation.NavigationBar(root, column=0, row=0, columnspan=Constants.MAX_SPAN, rowspan=1)

root.mainloop()
