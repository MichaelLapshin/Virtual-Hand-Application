import tkinter
import threading
import time

from scripts import Warnings
from scripts.frontend import Constants
from scripts.frontend.pages import \
    GenericPage, ModelsPage, DatasetsPage, TrainingProcessesPage, \
    ModelProcessesPage, HowToPage, ProjectInformationPage, AccountPage, SettingsPage

from scripts.frontend import \
    Constants, Parameters, \
    Navigation, ClientConnection, User

"""
    Process client app/connection constants
"""

# App constants
APP_TITLE = "Virtual-Hand"
APP_ICON = "images\\virtualhand_icons\\virtualhand_icon_YuG_1.ico"

# Process User Constants File
Parameters.process_file_parameters()

"""
    Client connection to the server
"""

# client_conn = ClientConnection()

"""
    Client-Side GUI
"""

# Created the window
root = tkinter.Tk()
root.title(APP_TITLE)
root.iconbitmap(default=APP_ICON)
root.geometry(Constants.default_resolution)
root.tk.call('tk', 'scaling', Constants.GUI_Scale)
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

# Creates the navigation bar and links them to the page
navig_bar = Navigation.NavigationBar(root, column=0, row=0, columnspan=1, rowspan=1)

# Template frame for the pages to use
frame_window = GenericPage.Frame(
    root=root,
    column=0, row=1,
    columnspan=1, rowspan=1)
frame_window.grid()

# Creates and adds the pages
navig_bar.add_page(ModelsPage.BaseFrame(root, base_frame=frame_window))
navig_bar.add_page(DatasetsPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(TrainingProcessesPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(ModelProcessesPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(HowToPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(ProjectInformationPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(AccountPage.Frame(root, base_frame=frame_window))
navig_bar.add_page(SettingsPage.Frame(root, base_frame=frame_window, navig_bar=navig_bar))

# Destroys reference frame
frame_window.destroy()

# Starts at the Account page by default
navig_bar.select_new_page(Navigation.TITLE_ACCOUNT)
navig_bar.update_colour()


class UpdateThread(threading.Thread):
    """
        Thread for updating the GUI
    """

    def __init__(self, navig_bar):
        threading.Thread.__init__(self)
        self.navig_bar = navig_bar
        self.running = True

    def run(self):
        while self.running:
            self.navig_bar.update_content()

            time.sleep(Parameters.UPDATE_DELAY_MS / 1000.0)

    def stop(self):
        self.running = False


updater = UpdateThread(navig_bar=navig_bar)
updater.start()

# Starts the GUI
root.mainloop()

# Ending functions
updater.stop()

print("The client application has ended.")
