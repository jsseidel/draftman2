"""
OpenProjectDialog

This class presents the user with an open project dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class PreferencesDialog:
    def __init__(self, builder, project):
        # Get pointers to the various widgets
        self.__app_window = builder.get_object('appWindow')
        self.__dialog = builder.get_object('dialogPreferences')
        self.__dialog.set_transient_for(self.__app_window)
        self.__entry_editor = builder.get_object('entryEditor')
        self.__entry_editor_args = builder.get_object('entryEditorArgs')
        self.__entry_backup_path = builder.get_object('entryBackupPath')
        self.__checkbox_backup_on_start = builder.get_object('checkboxBackupOnStart')
        self.__checkbox_include_text = builder.get_object('checkboxIncludeText')
        self.__entry_include_text = builder.get_object('entryIncludeText')
        self.__checkbox_skip_first = builder.get_object('checkboxSkipFirst')
        self.__checkbox_include_titles = builder.get_object('checkboxIncludeTitles')
        self.__checkbox_include_directory_titles = builder.get_object('checkboxIncludeDirectoryTitles')
        self.__button_browse_editor = builder.get_object('buttonBrowseEditor')
        self.__button_browse_backup = builder.get_object('buttonBrowseBackup')

        # We need signals for the buttons to get file names
        self.__button_browse_editor.connect("clicked", self.__on_choose_editor)
        self.__button_browse_backup.connect("clicked", self.__on_choose_backup_path)
        self.__checkbox_include_text.connect("clicked", self.__on_checkbox_include_text)

        self.__entry_include_text.set_sensitive(self.__checkbox_include_text.get_active())

        # Populate the fields
        self.__entry_editor.set_text(project.editor())
        self.__entry_editor_args.set_text(project.editor_args())
        self.__entry_backup_path.set_text(str(project.backup_path()))
        self.__checkbox_backup_on_start.set_active(project.backup_on_start())
        self.__checkbox_include_text.set_active(project.include_text())
        entry_text = project.include_text_entry()
        if entry_text is None:
            entry_text = ''
        self.__checkbox_skip_first.set_active(project.skip_first())
        self.__entry_include_text.set_text(entry_text)
        self.__checkbox_include_titles.set_active(project.include_titles())
        self.__checkbox_include_directory_titles.set_active(project.include_directory_titles())

    def __on_checkbox_include_text(self, *args):
        self.__entry_include_text.set_sensitive(self.__checkbox_include_text.get_active())

    def __on_choose_editor(self, *args):
        (rv, filename) = self.__get_file_name("Choose an editor",
                Gtk.FileChooserAction.OPEN)
        if rv == Gtk.ResponseType.OK:
            self.__entry_editor.set_text(filename)

    def __on_choose_backup_path(self, *args):
        (rv, filename) = self.__get_file_name("Choose a backup path",
                Gtk.FileChooserAction.SELECT_FOLDER)
        if rv == Gtk.ResponseType.OK:
            self.__entry_backup_path.set_text(filename)

    def __get_file_name(self, title, action):
        dialog = Gtk.FileChooserDialog( title, self.__app_window, action,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select",
                    Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()

        return (response, filename)

    def run(self):
        response = self.__dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            pass

        self.__dialog.hide()

        return (response, self.__entry_editor.get_text(),
                self.__entry_editor_args.get_text(),
                self.__entry_backup_path.get_text(),
                self.__checkbox_backup_on_start.get_active(),
                self.__checkbox_include_text.get_active(),
                self.__entry_include_text.get_text(),
                self.__checkbox_skip_first.get_active(),
                self.__checkbox_include_titles.get_active(),
                self.__checkbox_include_directory_titles.get_active())
