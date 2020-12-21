"""
ImportFileDialog

This class presents the user with an open file dialog for importing
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ImportFileDialog:
    def __init__(self, builder):
        self._app_window = builder.get_object('appWindow')

    def run(self):
        dialog = Gtk.FileChooserDialog(
                "Select file to import", self._app_window,
            Gtk.FileChooserAction.OPEN,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()

        return (response, filename)
