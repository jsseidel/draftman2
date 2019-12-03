"""
NewProjectDialog

This class presents the user with a new project dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NewProjectDialog:
    def __init__(self, builder):
        self.__app_window = builder.get_object('appWindow')
        self.__dialog = builder.get_object('fileChooserProjectDirectory')
        self.__entry_project_name = builder.get_object('entryProjectName')
        self.__entry_project_name.set_activates_default(True)

        # Make OK button the default
        self.__dialog.set_default_response(Gtk.ResponseType.OK)
        okButton = builder.get_object("fileChooserButtonOK")
        # Enter key should trigger the default action
        okButton.set_can_default(True)
        okButton.grab_default()

    def run(self):
        self.__dialog.set_default_size(800, 400)
        self.__dialog.set_transient_for(self.__app_window)
        self.__dialog.set_modal(True)
        response = self.__dialog.run()
        project_name = ""
        project_directory = ""
        if response == Gtk.ResponseType.OK:
            project_directory = self.__dialog.get_filename()
            project_name = self.__entry_project_name.get_text()

        self.__dialog.hide()

        return (response, project_name, project_directory)

