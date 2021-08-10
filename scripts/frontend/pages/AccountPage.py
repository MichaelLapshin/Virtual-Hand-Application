import tkinter

import requests

from scripts import General, Parameters, Constants, InputConstraints, Log
from scripts.frontend import User, Navigation
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.CustomButtons import AccountButton
from scripts.frontend.custom_widgets.CustomEntries import AccountEntry
from scripts.frontend.custom_widgets.CustomLabels import AccountLabel
from scripts.frontend.pages import GenericPage

# Account constants
STATUS_LOGGED_IN = "Status: Logged in"
STATUS_LOGGED_OUT = "Status: Logged out"
STATUS_FAILED_LOGIN = "Status: Log-in failed"
LOGIN_TEXT = "Log in"
LOGOUT_TEXT = "Log out"
CREATE_USER_TEXT = "Create user"
DELETE_USER_TEXT = "Delete user"

USERNAME_ENTRY = "Username:"
PASSWORD_ENTRY = "Password:"
VERIFY_PASSWORD_ENTRY = "Verify Password:"


class Frame(GenericPage.NavigationFrame):
    class LoginFrame(GenericPage.Frame):

        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Logged is as labels
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text="Log-in Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

            # Labels and Entries
            self.label_status = AccountLabel(
                self, text=STATUS_LOGGED_OUT,
                column=0, row=1,
                columnspan=2, rowspan=1)

            # Credentials entry field
            self.label_logged_as_username = AccountLabel(
                self, text=USERNAME_ENTRY,
                column=0, row=2,
                columnspan=1, rowspan=1)

            self.entry_username = AccountEntry(
                self,
                column=1, row=2,
                columnspan=1, rowspan=1,
                width=16)

            self.label_logged_as_password = AccountLabel(
                self, text=PASSWORD_ENTRY,
                column=0, row=3,
                columnspan=1, rowspan=1)

            self.entry_password = AccountEntry(
                self,
                column=1, row=3,
                columnspan=1, rowspan=1,
                width=16)

            # Log in button
            self.button_UserLogin = AccountButton(
                self, command=self.login_button_function,
                text=LOGIN_TEXT,
                column=0, row=4,
                columnspan=1, rowspan=1)

            # Log out button
            self.button_UserLogout = AccountButton(
                self, command=self.logout_button_function,
                text=LOGOUT_TEXT,
                column=1, row=4,
                columnspan=1, rowspan=1)

            self.login_button_enabling_update(reset_login=True)

        def logout_button_function(self):
            User.logout()
            self.login_button_enabling_update()

        def login_button_function(self):
            User.login(self.input_username.get(), self.input_password.get())
            self.login_button_enabling_update()

            # Update the labels
            if User.is_logged_in() is False:
                self.label_status.config(text=STATUS_FAILED_LOGIN)

        def login_button_enabling_update(self, reset_login=False):
            if (reset_login is False) and (User.is_logged_in() is True):
                # Disable/enable buttons
                self.entry_username.disable()
                self.entry_password.disable()
                self.button_UserLogin.disable()
                self.button_UserLogout.enable()

                # Update the labels
                self.label_status.config(text=STATUS_LOGGED_IN)

            else:
                # Disable/enable buttons
                self.entry_username.enable()
                self.entry_password.enable()
                self.button_UserLogin.enable()
                self.button_UserLogout.disable()

                # Update the labels
                self.label_status.config(text=STATUS_LOGGED_OUT)

        def update_colour(self):
            super().update_colour()
            self.title.update_colour()
            self.label_status.update_colour()
            self.label_logged_as_username.update_colour()
            self.entry_username.update_colour()
            self.label_logged_as_password.update_colour()
            self.entry_password.update_colour()
            self.button_UserLogin.update_colour()
            self.button_UserLogout.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def destroy(self):
            # Destroys login widgets
            self.entry_username.destroy()
            self.entry_password.destroy()
            self.button_UserLogin.destroy()
            self.button_UserLogout.destroy()

            super().destroy()

    class UserManagerFrame(GenericPage.Frame):
        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Title
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text="Account Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

            # Credentials entry field
            self.label_logged_as_username = AccountLabel(
                self, text=USERNAME_ENTRY,
                column=0, row=2,
                columnspan=1, rowspan=1)

            self.entry_username = AccountEntry(
                self,
                column=1, row=2,
                columnspan=1, rowspan=1,
                width=16)

            self.label_logged_as_password = AccountLabel(
                self, text=PASSWORD_ENTRY,
                column=0, row=3,
                columnspan=1, rowspan=1)

            self.entry_password = AccountEntry(
                self,
                column=1, row=3,
                columnspan=1, rowspan=1,
                width=16)

            self.label_logged_as_verify_password = AccountLabel(
                self, text=VERIFY_PASSWORD_ENTRY,
                column=0, row=4,
                columnspan=1, rowspan=1)

            self.entry_verify_password = AccountEntry(
                self,
                column=1, row=4,
                columnspan=1, rowspan=1,
                width=16)

            # Edit account buttons
            self.create_user_button = AccountButton(
                self, command=self.create_user,
                text=CREATE_USER_TEXT,
                column=0, row=5,
                columnspan=1, rowspan=1)

            self.delete_user_button = AccountButton(
                self, command=self.delete_user,
                text=DELETE_USER_TEXT,
                column=1, row=5,
                columnspan=1, rowspan=1)

        def update_colour(self):
            super().update_colour()
            self.title.update_colour()
            self.label_logged_as_username.update_colour()
            self.entry_username.update_colour()
            self.label_logged_as_password.update_colour()
            self.entry_password.update_colour()
            self.label_logged_as_verify_password.update_colour()
            self.entry_verify_password.update_colour()
            self.create_user_button.update_colour()
            self.delete_user_button.update_colour()

            self.config(bg=General.washed_colour_hex(Parameters.COLOUR_BRAVO, Parameters.ColourGrad_B))

        def destroy(self):
            # Destroys widgets

            super().destroy()

        def create_user(self):
            Log.info("Attempting to create a new user.")

            # Obtains inputs
            username = self.entry_username.get()
            password = self.entry_password.get()
            verify_password = self.entry_verify_password.get()

            if password == verify_password:

                # Assert user name
                can_create = True
                can_create &= InputConstraints.assert_string_non_empty("Username", username)
                can_create &= InputConstraints.assert_string_non_empty("Password", password)

                # Logic for creating the user
                if can_create is True:

                    is_created = requests.get(
                        Constants.SERVER_IP_ADDRESS + "/account/create?user_name=" + username + "&password=" + password)

                    if is_created is True:
                        pass
                    else:
                        pass
                else:
                    InputConstraints.warn("Could not create the user. Input constraints were not met.")
            else:
                Log.info("Password and verify password do not match!")
                InputConstraints.warn("The password verification does not match the original.")

        def delete_user(self):
            Log.info("Attempting to delete a new user.")

            # Obtains inputs
            username = self.entry_username.get()
            password = self.entry_password.get()
            verify_password = self.entry_verify_password.get()

            if password == verify_password:
                # Assert user name
                can_delete = True
                can_delete &= InputConstraints.assert_string_non_empty("Username", username)
                can_delete &= InputConstraints.assert_string_non_empty("Password", password)

                # Logic for creating the user
                if can_delete is True:

                    is_deleted = requests.get(
                        Constants.SERVER_IP_ADDRESS + "/account/delete?user_name=" + username + "&password=" + password)

                    if is_deleted is True:
                        pass
                    else:
                        pass
                else:
                    InputConstraints.warn("Could not delete the user. Input constraints were not met.")

            else:
                Log.info("Password and verify password do not match!")
                InputConstraints.warn("The password verification does not match the original.")

    class ServerManagerFrame(GenericPage.Frame):
        def __init__(self, root, column, row, columnspan=1, rowspan=1):
            GenericPage.Frame.__init__(self, root=root, column=column, row=row, columnspan=columnspan, rowspan=rowspan)

            # Create login frame
            self.config(bd=2)
            self.grid(sticky=tkinter.N)

            # Title
            self.title = CustomLabels.TitleLabel(self, column=0, row=0, columnspan=2, text="Server Management")
            self.title.grid(padx=Constants.STANDARD_SPACING)

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                             page_title=Navigation.TITLE_ACCOUNT)

        # Weight configurations
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        # Frames
        self.server_manager_frame = Frame.ServerManagerFrame(self, column=0, row=0)
        self.login_frame = Frame.LoginFrame(self, column=1, row=0)
        self.user_manager_frame = Frame.UserManagerFrame(self, column=2, row=0)

    def update_colour(self):
        super().update_colour()
        self.server_manager_frame.update_colour()
        self.login_frame.update_colour()
        self.user_manager_frame.update_colour()

    def update_content(self):
        super().update_content()
        self.server_manager_frame.update_content()
        self.login_frame.update_content()
        self.user_manager_frame.update_content()

    def destroy(self):
        self.server_manager_frame.destroy()
        self.login_frame.destroy()
        self.user_manager_frame.destroy()
        super().destroy()
