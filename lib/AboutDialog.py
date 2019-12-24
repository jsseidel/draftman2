"""
AboutDialog

This class presents the user with an about dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AboutDialog:
    def __init__(self, builder):
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('dialogAbout')
        # Make OK button the default
        self._dialog.set_default_response(Gtk.ResponseType.OK)
        okButton = builder.get_object("fileChooserButtonOK")
        # Enter key should trigger the default action
        okButton.set_can_default(True)
        okButton.grab_default()


    def run(self):
        self._dialog.set_transient_for(self._app_window)
        self._dialog.set_modal(True)
        response = self._dialog.run()
        self._dialog.hide()

