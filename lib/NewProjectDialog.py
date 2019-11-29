"""
NewProjectDialog

This class presents the user with a new project dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NewProjectDialog:
    def __init__(self, app_window, entry_project_name, dialog):
        self.__app_window = app_window
        self.__entry_project_name = entry_project_name
        self.__dialog = dialog

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

