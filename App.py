"""
App

This class is responsible for routing gtk signals and maintaining the
consistency of the state of the running instance of draftman.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

import os

from datetime import datetime
from lib.AppWindowState import AppWindowState
from lib.KeeperFileOpsLinux import KeeperFileOpsLinux
from lib.Project import Project
from lib.PreferencesDialog import PreferencesDialog
from lib.NewProjectDialog import NewProjectDialog
from lib.OpenProjectDialog import OpenProjectDialog
from lib.AboutDialog import AboutDialog
from lib.KeeperTreeView import KeeperTreeView
from lib.Message import Message
from pathlib import Path

class App:

    def __init__(self):
        # Use a builder to create our objects from the glade
        # file.
        self._builder = Gtk.Builder()
        self._builder.add_from_file('draftman2.glade')
        self._builder.connect_signals(self)
        self._app_window = self._builder.get_object("appWindow")
        self._pane = self._builder.get_object("pane")
        self._keeper_treeview = self._builder.get_object("treeViewKeeper")
        self._project = Project()

        # Signals
        self._app_window.connect("size-allocate", self._on_size_allocate)
        self._app_window.connect("window-state-event", self._on_window_state_event)
        self._pane.connect("notify::position", self._on_pane_position)

        draftman2rc = Path.home() / '.draftman2rc'
        if draftman2rc.exists():
            last_project = ''
            with draftman2rc.open() as f:
                last_project = f.read().strip()
            p = Path(last_project)
            if p.exists():
                self._project.open(str(p))
                if self._project.app_window_state.is_valid():
                    if self._project.app_window_state.maximized:
                        self._app_window.maximize()
                    else:
                        self._app_window.resize(self._project.app_window_state.w,
                                self._project.app_window_state.h)
                    self._pane.set_position(self._project.app_window_state.pane)

        self._keeper_treeview = KeeperTreeView(self._builder, self._project)
        self._keeper_treeview.refresh()
        self._set_window_title()
        self._app_window.show_all()
        Gtk.main()

    def _set_window_title(self):
        title = "Draftman2"
        if self._project.name() != '':
            title = '%s: %s' % (title, self._project.name())
        self._app_window.set_title(title)

    def _clear_window_title(self):
        self._app_window.set_title('')

    def save_last(self):
        if self._project.project_path() != "":
            draftman2rc = Path.home() / '.draftman2rc'
            with draftman2rc.open("w") as f:
                f.write(str(self._project.project_path()))

    # User closed the appwindow
    def onDestroy(self, *args):
        self.save_last()
        self._keeper_treeview.save()
        Gtk.main_quit()

    # Signal handlers
    #
    #
    def _on_size_allocate(self, widget, allocation):
        (self._project.app_window_state.w, self._project.app_window_state.h) = self._app_window.get_size()

    def _on_pane_position(self, widget, gparam):
        self._project.app_window_state.pane = widget.get_property(gparam.name)

    def _on_window_state_event(self, widget, event):
        self._project.app_window_state.maximized = (event.new_window_state & Gdk.WindowState.MAXIMIZED) != 0
        self._project.app_window_state.fullscreen = (event.new_window_state & Gdk.WindowState.FULLSCREEN) != 0

    # Menu and Button Handlers
    #
    #

    # User selected Quit
    def onQuit(self, *args):
        self.save_last()
        self._keeper_treeview.save()
        Gtk.main_quit()

    # User selected add file
    def onAddFile(self, *args):
        self._keeper_treeview.on_add_file(args)

    # User selected add file at root
    def onAddFileAtRoot(self, *args):
        self._keeper_treeview.on_add_file_at_root(args)

    # User selected import file
    def onImportMarkdownFile(self, *args):
        self._keeper_treeview.on_import_file(args)

    # User selected add directory
    def onAddDirectory(self, *args):
        self._keeper_treeview.on_add_directory(args)

    # User selected edit file
    def onEditFile(self, *args):
        self._keeper_treeview.on_edit_file(args)

    # User selected copy
    def onCopy(self, *args):
        self._keeper_treeview.on_copy(args)

    # User selected paste
    def onPaste(self, *args):
        self._keeper_treeview.on_paste(args)

    # User selected delete
    def onDelete(self, *args):
        self._keeper_treeview.on_delete(args)


    # User selected New
    def onNew(self, *args):
        npd = NewProjectDialog(self._builder)
        (response, project_name, project_directory) = npd.run()
        if response == Gtk.ResponseType.OK:
            if self._project.is_loaded():
                self.save_last()
                self._keeper_treeview.save()
                self._keeper_treeview.clear_all()
                self._clear_window_title()

            (rv, reason) = self._project.new(project_directory, project_name)
            if not rv:
                m = Message()
                m.error(self._app_window, 'Cannot create project', 'Cannot'
                        ' create project directory, %s:\n\n%s\n' %
                        (project_directory, reason))
                return

            self._set_window_title()
            self._keeper_treeview.refresh()
            self._keeper_treeview.enable_items()

    # User selected Open
    def onOpen(self, *args):
        opd = OpenProjectDialog(self._builder)
        (response, project_directory) = opd.run()
        if response == Gtk.ResponseType.OK:
            if self._project.is_loaded():
                self.save_last()
                self._keeper_treeview.save()
                self._keeper_treeview.clear_all()
                self._clear_window_title()

            (rv, reason) = self._project.open(project_directory)
            if not rv:
                m = Message()
                m.error(self._app_window, 'Cannot open project', 'Cannot open '
                        ' project directory, %s:\n\n%s\n' % (project_directory,
                        reason))
                return

            self._set_window_title()
            self._keeper_treeview.refresh()
            self._keeper_treeview.enable_items()

    # Expand all
    def onExpandAll(self, *args):
        self._keeper_treeview.expand_all()

    # Collapse all
    def onCollapseAll(self, *args):
        self._keeper_treeview.collapse_all()

    # Update word/scene counts
    def onUpdateWordCounts(self, *args):
        self._keeper_treeview.update_word_counts()

    # User selected About
    def onAbout(self, *args):
        ad = AboutDialog(self._builder)
        ad.run()

    # User selected Preferences
    def onPreferences(self, *args):
        pd = PreferencesDialog(self._builder, self._project)
        (response, editor, editor_args, backup_path, backup_on_start,
                include_text, include_text_entry, skip_first, include_titles,
                include_directory_titles) = pd.run()
        if response == Gtk.ResponseType.OK:
            self._project.set_editor(editor)
            self._project.set_editor_args(editor_args)
            self._project.set_backup_path(backup_path)
            self._project.set_backup_on_start(backup_on_start)
            self._project.set_include_text(include_text)
            self._project.set_include_text_entry(include_text_entry)
            self._project.set_skip_first(skip_first)
            self._project.set_include_titles(include_titles)
            self._project.set_include_directory_titles(include_directory_titles)

    # User selected Compile
    def onCompile(self, *args):
        dialog = Gtk.FileChooserDialog("Save compilation to folder",
                self._app_window, Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select",
                    Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()

        p = Path(filename)
        fileName = '%s%s' % (self._project.name(), '.md')
        p = p / fileName
        self._keeper_treeview.compile(str(p))

    # User selected backup
    def onCreateBackup(self, *args):
        dt = datetime.now()
        ts = dt.strftime('%Y%m%d_%H%M%S')
        p = Path(self._project.backup_path())
        filename = '%s-%s%s' % (self._project.name(), ts, '.zip')
        p = p / filename
        self._keeper_treeview.backup(str(p))

    # User selected create tutorial
    def onCreateTutorial(self, *args):
        m = Message()
        dialog = Gtk.FileChooserDialog("Save tutorial project to folder",
                self._app_window, Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select",
                    Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        tut_dir = dialog.get_filename()

        dialog.destroy()

        tutorial_path = Path(tut_dir)
        tutorial_path = tutorial_path / 'Draftman2 Tutorial'

        if response == Gtk.ResponseType.OK:
            go_ahead = True
            if tutorial_path.exists():
                rv = m.confirm(self._app_window, 'Overwrite?', '%s exists.'
                      ' Overwrite?' % str(tutorial_path))
                go_ahead == (response == Gtk.ResponseType.OK)

            if go_ahead:
                fops = KeeperFileOpsLinux()
                (rv, reason) = fops.copy_tutorial(tut_dir)
                if not rv:
                    m.error(self._app_window, 'Error', 'Could not create'
                            ' tutorial: %s\n' % reason)
                else:
                    m.info(self._app_window, 'Success', 'Created %s' %
                            str(tutorial_path))

                if self._project.is_loaded():
                    self.save_last()
                    self._keeper_treeview.save()
                    self._keeper_treeview.clear_all()

                (rv, reason) = self._project.open(str(tutorial_path))
                if not rv:
                    m = Message()
                    m.error(self._app_window, 'Cannot open project', 'Cannot'
                            ' open project: %s:\n\n%s\n' % (str(tutorial_path),
                                reason))
                    return

                self._keeper_treeview.refresh()
                self._keeper_treeview.enable_items()
                if self._project.app_window_state.is_valid():
                    if self._project.app_window_state.maximized:
                        self._app_window.maximize()
                    else:
                        self._app_window.resize(self._project.app_window_state.w,
                                self._project.app_window_state.h)
                    self._pane.set_position(self._project.app_window_state.pane)


