import tkinter
import tkinter.tix

from scripts import Warnings, Constants
from scripts.frontend.custom_widgets import CustomLabels
from scripts.frontend.custom_widgets.WidgetInterface import WidgetInterface


class Frame(tkinter.Frame, WidgetInterface):
    _selected = "Number of Selected Items: "

    def __init__(self, root, multi_select=False, select_change_command=None):
        tkinter.Frame.__init__(self, root)
        self.grid(padx=Constants.STANDARD_SPACING, pady=Constants.STANDARD_SPACING)
        self.grid(sticky=tkinter.NSEW)

        # Selection logic
        self.selected_index_listbox = -1
        self.selected_index_sorted_listbox = -1
        self.select_change_command = select_change_command

        # Configures weights
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)
        self.columnconfigure(3, weight=0)

        # Creates the scroll bar
        self.scrollbar = tkinter.Scrollbar(self, orient=tkinter.VERTICAL)
        self.scrollbar.grid(column=3, row=0)
        self.scrollbar.grid(columnspan=1, rowspan=1)
        self.scrollbar.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.scrollbar.grid(sticky=tkinter.NS)

        # Initializes the list box
        self.listbox = tkinter.Listbox(self, selectmode=tkinter.SINGLE,
                                       yscrollcommand=self.listbox_scroll, exportselection=False)
        self.listbox.grid(column=2, row=0)
        self.listbox.grid(columnspan=1, rowspan=1)
        self.listbox.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.listbox.grid(sticky=tkinter.NSEW)

        # Initializes the listbox that displays the sorted data values
        self.sorted_listbox = tkinter.Listbox(self, selectmode=tkinter.SINGLE, width=3,
                                              yscrollcommand=self.sorted_listbox_scroll, exportselection=True)
        self.sorted_listbox.grid(column=1, row=0)
        self.sorted_listbox.grid(columnspan=1, rowspan=1)
        self.sorted_listbox.grid(padx=Constants.SHORT_SPACING, pady=Constants.SHORT_SPACING)
        self.sorted_listbox.grid(sticky=tkinter.NS)

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

    def update_content(self):
        super().update_content()

        # Selection Activation
        selection_changed = False
        if self.listbox.size() > 0:  # TODO, add a function that will trigger upon select change

            if len(self.listbox.curselection()) > 0 and self.selected_index_listbox != self.listbox.curselection()[0]:
                self.selected_index_listbox = self.listbox.curselection()[0]
                self.sorted_listbox.selection_clear(0, tkinter.END)
                self.sorted_listbox.selection_set(self.selected_index_listbox)
                self.selected_index_sorted_listbox = self.selected_index_listbox
                selection_changed = True

            elif len(self.sorted_listbox.curselection()) > 0 and \
                    self.selected_index_sorted_listbox != self.sorted_listbox.curselection()[0]:
                self.selected_index_sorted_listbox = self.sorted_listbox.curselection()[0]
                self.listbox.selection_clear(0, tkinter.END)
                self.listbox.selection_set(self.selected_index_sorted_listbox)
                self.selected_index_listbox = self.selected_index_sorted_listbox
                selection_changed = True

        if (selection_changed is True) and (self.select_change_command is not None):
            self.select_change_command()

        # Selected Count
        if self.num_selected() != 0:
            self.selected_count_label.config(text=Frame._selected + str(self.num_selected()))
            self.selected_count_label.grid()
        else:
            self.selected_count_label.grid_remove()

    # Synchronous scrolling of both list boxes
    def scroll(self, *args):
        self.listbox.yview(*args)
        self.selectbox.yview(*args)

    def listbox_scroll(self, *args):
        if (self.selectbox is not None) and (self.listbox.yview() != self.selectbox.yview()):
            self.selectbox.yview_moveto(args[0])
        if self.listbox.yview() != self.sorted_listbox.yview():
            self.sorted_listbox.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def sorted_listbox_scroll(self, *args):
        if (self.selectbox is not None) and (self.sorted_listbox.yview() != self.selectbox.yview()):
            self.selectbox.yview_moveto(args[0])
        if self.sorted_listbox.yview() != self.listbox.yview():
            self.listbox.yview_moveto(args[0])
        self.scrollbar.set(*args)

    def selectbox_scroll(self, *args):
        if self.selectbox.yview() != self.listbox.yview():
            self.listbox.yview_moveto(args[0])
        if self.selectbox.yview() != self.sorted_listbox.yview():
            self.sorted_listbox.yview_moveto(args[0])
        self.scrollbar.set(*args)

    # More functionality methods
    def get_selected_multi(self):
        if self.multi_select is True:
            return self.selectbox.curselection()
        else:
            return ()

    def get_selected_main(self):
        if self.is_selected_main():
            return self.listbox.curselection()[0]
        else:
            return None

    def is_selected_main(self):
        return len(self.listbox.curselection()) > 0

    def num_selected(self):
        return len(self.get_selected_multi())

    def add_to_list(self, item_display_name, item_display_sorted, index=tkinter.END):
        # Computes the index
        if index == tkinter.END:
            index = self.listbox.size()

        # Adds the item to the index
        self.listbox.insert(index, item_display_name)
        self.sorted_listbox.insert(index, str(item_display_sorted))
        if self.selectbox is not None:
            self.selectbox.insert(index, " " + str(index))
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

    def replace_list(self, new_list, new_sorted_list):
        assert len(new_list) == len(new_sorted_list)

        # Sets the appropriate width of the sorted column
        max_width = 1
        for item in new_sorted_list:
            if len(str(item)) > max_width:
                max_width = len(item)
        self.sorted_listbox.config(width=max_width)

        # Removes all items
        self.listbox.delete(0, tkinter.END)
        self.sorted_listbox.delete(0, tkinter.END)
        if self.multi_select is True:
            self.selectbox.delete(0, tkinter.END)

        # Deletes and re-adds the items
        for index in range(0, len(new_list)):
            self.add_to_list(new_list[index], new_sorted_list[index])

        # Resets select index
        self.selected_index_listbox = -1
        self.selected_index_sorted_listbox = -1
        return True
