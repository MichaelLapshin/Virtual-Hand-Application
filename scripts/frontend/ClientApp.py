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
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# client_conn = ClientConnection()

# Creates the navigation bar and links them to the page
navig_bar = Navigation.NavigationBar(root, column=0, row=0, columnspan=Constants.MAX_SPAN, rowspan=1)

# Template frame for the pages to use
frame_window = GenericPage.Frame(
    root=root,
    column=0, row=1,
    columnspan=Constants.MAX_SPAN, rowspan=Constants.MAX_SPAN)
frame_window.grid()

# Creates and adds the pages
navig_bar.add_page(ModelsPage.BaseFrame(root, base_frame=frame_window))
navig_bar.add_page(DatasetsPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(TrainingProcessesPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(ModelProcessesPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(HowToPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(ProjectInformationPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(AccountPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(SettingsPage.Frame(root, base_frame=frame_window))

# Destroys reference frame
frame_window.destroy()

# Starts at the Account page by default
navig_bar.select_new_page(Navigation.TITLE_ACCOUNT)



root.mainloop()
