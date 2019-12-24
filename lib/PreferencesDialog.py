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
        self._app_window = builder.get_object('appWindow')
        self._dialog = builder.get_object('dialogPreferences')
        self._dialog.set_transient_for(self._app_window)
        self._entry_editor = builder.get_object('entryEditor')
        self._entry_editor_args = builder.get_object('entryEditorArgs')
        self._entry_backup_path = builder.get_object('entryBackupPath')
        self._checkbox_backup_on_start = builder.get_object('checkboxBackupOnStart')
        self._checkbox_include_text = builder.get_object('checkboxIncludeText')
        self._entry_include_text = builder.get_object('entryIncludeText')
        self._checkbox_skip_first = builder.get_object('checkboxSkipFirst')
        self._checkbox_include_titles = builder.get_object('checkboxIncludeTitles')
        self._checkbox_include_directory_titles = builder.get_object('checkboxIncludeDirectoryTitles')
        self._button_browse_editor = builder.get_object('buttonBrowseEditor')
        self._button_browse_backup = builder.get_object('buttonBrowseBackup')

        # We need signals for the buttons to get file names
        self._button_browse_editor.connect("clicked", self._on_choose_editor)
        self._button_browse_backup.connect("clicked", self._on_choose_backup_path)
        self._checkbox_include_text.connect("clicked", self._on_checkbox_include_text)

        self._entry_include_text.set_sensitive(self._checkbox_include_text.get_active())

        # Populate the fields
        self._entry_editor.set_text(project.editor())
        self._entry_editor_args.set_text(project.editor_args())
        self._entry_backup_path.set_text(str(project.backup_path()))
        self._checkbox_backup_on_start.set_active(project.backup_on_start())
        self._checkbox_include_text.set_active(project.include_text())
        entry_text = project.include_text_entry()
        if entry_text is None:
            entry_text = ''
        self._checkbox_skip_first.set_active(project.skip_first())
        self._entry_include_text.set_text(entry_text)
        self._checkbox_include_titles.set_active(project.include_titles())
        self._checkbox_include_directory_titles.set_active(project.include_directory_titles())

        self._checkbox_skip_first.set_sensitive(self._checkbox_include_text.get_active())

    def _on_checkbox_include_text(self, *args):
        self._entry_include_text.set_sensitive(self._checkbox_include_text.get_active())
        self._checkbox_skip_first.set_sensitive(self._checkbox_include_text.get_active())

    def _on_choose_editor(self, *args):
        (rv, filename) = self._get_file_name("Choose an editor",
                Gtk.FileChooserAction.OPEN)
        if rv == Gtk.ResponseType.OK:
            self._entry_editor.set_text(filename)

    def _on_choose_backup_path(self, *args):
        (rv, filename) = self._get_file_name("Choose a backup path",
                Gtk.FileChooserAction.SELECT_FOLDER)
        if rv == Gtk.ResponseType.OK:
            self._entry_backup_path.set_text(filename)

    def _get_file_name(self, title, action):
        dialog = Gtk.FileChooserDialog( title, self._app_window, action,
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
        response = self._dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            pass

        self._dialog.hide()

        return (response, self._entry_editor.get_text(),
                self._entry_editor_args.get_text(),
                self._entry_backup_path.get_text(),
                self._checkbox_backup_on_start.get_active(),
                self._checkbox_include_text.get_active(),
                self._entry_include_text.get_text(),
                self._checkbox_skip_first.get_active(),
                self._checkbox_include_titles.get_active(),
                self._checkbox_include_directory_titles.get_active())
