"""
AddItemDialog

This class presents the user with a dialog to add items to the keeper
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AddItemDialog:
    def __init__(self, builder, something_selected):
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('dialogAddItem')
        self._entry_add = builder.get_object('entryAddItem')
        self._checkbox_add_at_root = builder.get_object('addItemAtRoot')
        self._entry_add.set_activates_default(True)

        # If nothing is selected, we must force adding to root checkbox by
        # selecting it and then disabling it
        self._checkbox_add_at_root.set_sensitive(something_selected)
        self._checkbox_add_at_root.set_active(not something_selected)

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
        # Give focus to the text box
        self._entry_add.grab_focus_without_selecting()
        response = self._dialog.run()
        item_name = ''
        if response == Gtk.ResponseType.OK:
            item_name = self._entry_add.get_text()

        self._dialog.hide()

        return (response, item_name, self._checkbox_add_at_root.get_active())

