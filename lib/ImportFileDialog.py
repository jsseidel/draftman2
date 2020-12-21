"""
ImportFileDialog

This class presents the user with an open file dialog for importing
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ImportFileDialog:
    def __init__(self, builder, something_selected):
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('importFileChooser')
        self._checkbox_import_at_root = builder.get_object('checkboxImportFileAtRoot')

        # If nothing is selected, we must force adding to root checkbox by
        # selecting it and then disabling it
        self._checkbox_import_at_root.set_sensitive(something_selected)
        self._checkbox_import_at_root.set_active(not something_selected)

        # Make OK button the default
        self._dialog.set_default_response(Gtk.ResponseType.OK)
        okButton = builder.get_object("fileChooserButtonOK")
        # Enter key should trigger the default action
        okButton.set_can_default(True)
        okButton.grab_default()

    def run(self):
        self._dialog.set_default_size(800, 400)
        self._dialog.set_transient_for(self._app_window)
        self._dialog.set_modal(True)
        response = self._dialog.run()
        file_name = ""
        import_at_root = False
        if response == Gtk.ResponseType.OK:
            file_name = self._dialog.get_filename()
            import_at_root = self._checkbox_import_at_root.get_active()
        self._dialog.hide()

        return (response, file_name, import_at_root)

