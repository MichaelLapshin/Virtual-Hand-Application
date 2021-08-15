import tkinter
import tkinter.tix

from scripts import Warnings, Constants
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class Frame(tkinter.Frame, WidgetInterface):
    _selected = "Number of Selected Items: "

    def __init__(self, root, multi_select=False):
        tkinter.Frame.__init__(self, root)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

        # Configures weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=0)

        # Creates the scroll bar
        self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.scrollbar.grid(column=2, row=0)
        self.scrollbar.grid(columnspan=1, rowspan=1)
        self.scrollbar.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.scrollbar.grid(sticky=tkinter.NS)

        # Initializes the list box
        self.listbox = tkinter.Listbox(self, selectmode=tkinter.SINGLE,
                                       yscrollcommand=self.listbox_scroll, exportselection=False)
        self.listbox.grid(column=1, row=0)
        self.listbox.grid(columnspan=1, rowspan=1)
        self.listbox.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.listbox.grid(sticky=tkinter.NSEW)

        # Creates selectable scroll bar
        self.multi_select = multi_select
        self.selectbox = None
        if multi_select is True:
            self.selectbox = tkinter.Listbox(
                self, width=2, exportselection=False,
                selectmode=tkinter.MULTIPLE, yscrollcommand=self.selectbox_scroll)
            self.selectbox.grid(column=0, row=0)
            self.selectbox.grid(columnspan=1, rowspan=1)
            self.selectbox.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
            self.selectbox.grid(sticky=tkinter.NS)

        # Links the scrollbar to the listbox (so you can move listbox view with the scrollbar)
        self.scrollbar.config(command=self.listbox.yview)
        if multi_select is True:
            self.scrollbar.config(command=self.scroll)

        # Selected count
        self.selected_count_label = self.selected_count_label = CustomLabels.SearchLabel(
            self,
            column=0, row=2,
            columnspan=3,
            text=Frame._selected + str(self.num_selected()))
        self.selected_count_label.grid_remove()

    def update_colour(self):
        super().update_colour()
        self.selected_count_label.update_colour()

    # Synchronous scrolling of both list boxes
    def scroll(self, *args):
        self.listbox.yview(*args)
        self.selectbox.yview(*args)

    def listbox_scroll(self, *args):
        if (self.selectbox is not None) and (self.listbox.yview() != self.selectbox.yview()):
            self.selectbox.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def selectbox_scroll(self, *args):
        if self.listbox.yview() != self.selectbox.yview():
            self.listbox.yview_moveto(args[0])
        self.scrollbar.set(*args)

    # More functionality methods
    def update_content(self):
        super().update_content()
        # Selected Count
        if self.num_selected() != 0:
            self.selected_count_label.config(text=Frame._selected + str(self.num_selected()))
            self.selected_count_label.grid()
        else:
            self.selected_count_label.grid_remove()

    def get_selected(self):
        if self.multi_select is True:
            return self.selectbox.curselection()
        else:
            return self.listbox.curselection()

    def num_selected(self):
        return len(self.get_selected())

    def add_to_list(self, item_display_name, index=tkinter.END):
        # Computes the index
        if index == tkinter.END:
            index = self.listbox.size()

        # Adds the item to the index
        self.listbox.insert(index, item_display_name)
        if self.selectbox is not None:
            self.selectbox.insert(index, str(index))
        return True

    def remove_from_list(self, item_display_name):
        # Find the index of the item
        found = False
        index = 0
        for index in range(0, self.listbox.size()):
            if self.listbox.index(index) == item_display_name:
                found = True
                break

        # Removes the item
        if found is True:
            # Removes the item at index
            self.listbox.delete(index)
            self.replace_list(self.listbox.get(0, tkinter.END))
            return True
        else:
            Warnings.not_to_reach()
            return False

    def replace_list(self, new_list):
        # Removes all items
        self.listbox.delete(0, tkinter.END)
        if self.multi_select is True:
            self.selectbox.delete(0, tkinter.END)

        # Deletes and re-adds the items
        for item in new_list:
            self.add_to_list(item)
        return True
