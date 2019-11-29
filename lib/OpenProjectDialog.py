"""
OpenProjectDialog

This class presents the user with an open project dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class OpenProjectDialog:
    def __init__(self, app_window):
        self.__app_window = app_window

    def run(self):
        dialog = Gtk.FileChooserDialog(
                "Select project directory", self.__app_window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()

        return (response, filename)
