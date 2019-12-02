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
        self.__entry_add.set_activates_default(True)

        # Make OK button the default
        self.__dialog.set_default_response(Gtk.ResponseType.OK)
        okButton = self.__dialog.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        # Enter key should trigger the default action
        okButton.set_can_default(True)
        okButton.grab_default()

    def run(self):
        self.__dialog.set_transient_for(self.__app_window)
        self.__dialog.set_modal(True)
        self.__entry_add.set_text('')
        response = self.__dialog.run()
        item_name = ''
        if response == Gtk.ResponseType.OK:
            item_name = self.__entry_add.get_text()

        self.__dialog.hide()

        return (response, item_name)

