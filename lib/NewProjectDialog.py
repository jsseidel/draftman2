"""
NewProjectDialog

This class presents the user with a new project dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NewProjectDialog:
    def __init__(self, builder):
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('fileChooserProjectDirectory')
        self._entry_project_name = builder.get_object('entryProjectName')
        self._entry_project_name.set_activates_default(True)

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
        project_name = ""
        project_directory = ""
        if response == Gtk.ResponseType.OK:
            project_directory = self._dialog.get_filename()
            project_name = self._entry_project_name.get_text()

        self._dialog.hide()

        return (response, project_name, project_directory)

