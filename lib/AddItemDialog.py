"""
AddItemDialog

This class presents the user with a dialog to add items to the keeper
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddItemDialog:
    def __init__(self, builder):
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('dialogAddItem')
        self._entry_add = builder.get_object('entryAddItem')
        self._entry_add.set_activates_default(True)

        # Make OK button the default
        self._dialog.set_default_response(Gtk.ResponseType.OK)
        okButton = self._dialog.get_widget_for_response(response_id=Gtk.ResponseType.OK)
        # Enter key should trigger the default action
        okButton.set_can_default(True)
        okButton.grab_default()

    def run(self):
        self._dialog.set_transient_for(self._app_window)
        self._dialog.set_modal(True)
        self._entry_add.set_text('')
        response = self._dialog.run()
        item_name = ''
        if response == Gtk.ResponseType.OK:
            item_name = self._entry_add.get_text()

        self._dialog.hide()

        return (response, item_name)

