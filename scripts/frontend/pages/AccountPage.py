import tkinter

from scripts import General
from scripts.frontend import User, Constants, Navigation
from scripts.frontend.custom_widgets.CustomButtons import AccountButton
from scripts.frontend.custom_widgets.CustomEntry import InformationEntry
from scripts.frontend.custom_widgets.CustomLabels import LoginLabel
from scripts.frontend.pages import GenericPage

# Account constants
STATUS_LOGGED_IN = "Status: Logged in"
STATUS_LOGGED_OUT = "Status: Logged out"
STATUS_FAILED_LOGIN = "Status: Log-in failed"
LOGIN_TEXT = "Log in"
LOGOUT_TEXT = "Log out"

USERNAME_ENTRY = "Username: "
PASSWORD_ENTRY = "Password: "


class Frame(GenericPage.NavigationFrame):

    def __init__(self, root, base_frame=None):
        GenericPage.NavigationFrame.__init__(self, root=root, base_frame=base_frame,
                                   page_title=Navigation.TITLE_ACCOUNT)

        """
            Frame configurations
        """

        """
            Login/Logout buttons & labels
        """

        self.input_username = tkinter.StringVar()
        self.input_password = tkinter.StringVar()

        # Logged is as labels
        self.label_status = LoginLabel(
            self, text=STATUS_LOGGED_OUT,
            column=0, row=0,
            columnspan=2, rowspan=1)

        # Credentials entry field
        self.label_logged_as = LoginLabel(
            self, text=USERNAME_ENTRY,
            column=0, row=1,
            columnspan=1, rowspan=1)

        self.entry_username = InformationEntry(
            self, textvariable=self.input_username,
            column=1, row=1,
            columnspan=1, rowspan=1,
            width=16)

        self.label_logged_as = LoginLabel(
            self, text=PASSWORD_ENTRY,
            column=0, row=2,
            columnspan=1, rowspan=1)

        self.entry_password = InformationEntry(
            self, textvariable=self.input_password,
            column=1, row=2,
            columnspan=1, rowspan=1,
            width=16)

        # Log in button
        self.button_UserLogin = AccountButton(
            self, command=self.login_button_function,
            text=LOGIN_TEXT,
            column=0, row=3,
            columnspan=1, rowspan=1)

        # Log out button
        self.button_UserLogout = AccountButton(
            self, command=self.logout_button_function,
            text=LOGOUT_TEXT,
            column=1, row=3,
            columnspan=1, rowspan=1)

        self.login_button_enabling_update()

    def logout_button_function(self):
        User.logout()
        self.login_button_enabling_update()

    def login_button_function(self):
        User.login(self.input_username.get(), self.input_password.get())
        self.login_button_enabling_update()

        # Update the labels
        if User.is_logged_in() is False:
            self.label_status.config(text=STATUS_FAILED_LOGIN)

    def login_button_enabling_update(self):
        if User.is_logged_in() is True:
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

    def destroy(self):
        # Destroys login widgets
        self.entry_username.destroy()
        self.entry_password.destroy()
        self.button_UserLogin.destroy()
        self.button_UserLogout.destroy()

        super().destroy()
