"""
AddItemDialog

This class presents the user with a dialog to add items to the keeper
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddItemDialog:
    def __init__(self, builder):
        self.__app_window = builder.get_object('appWindow')
        self.__dialog = builder.get_object('dialogAddItem')
        self.__entry_add = builder.get_object('entryAddItem')
        self.__radio_button_file = builder.get_object('radioButtonFile')
        self.__radio_button_directory = builder.get_object('radioButtonDirectory')
        self.__checkbox_is_child = builder.get_object('checkboxIsChild')

    def run(self):
        self.__dialog.set_transient_for(self.__app_window)
        self.__dialog.set_modal(True)
        response = self.__dialog.run()
        item_name = ''
        item_type = ''
        is_child = False
        if response == Gtk.ResponseType.OK:
            item_type = 'file'
            if self.__radio_button_directory.get_active():
                item_type = 'directory'

            item_name = self.__entry_add.get_text()
            is_child = self.__checkbox_is_child.get_active()

        self.__dialog.hide()

        return (response, item_name, item_type, is_child)

