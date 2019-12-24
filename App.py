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
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file('draftman2.glade')
        self.__builder.connect_signals(self)
        self.__app_window = self.__builder.get_object("appWindow")
        self.__pane = self.__builder.get_object("pane")
        self.__keeper_treeview = self.__builder.get_object("treeViewKeeper")
        self.__project = Project()

        # Signals
        self.__app_window.connect("size-allocate", self.__on_size_allocate)
        self.__app_window.connect("window-state-event", self.__on_window_state_event)
        self.__pane.connect("notify::position", self.__on_pane_position)

        draftman2rc = Path.home() / '.draftman2rc'
        if draftman2rc.exists():
            last_project = ''
            with draftman2rc.open() as f:
                last_project = f.read().strip()
            p = Path(last_project)
            if p.exists():
                self.__project.open(str(p))
                if self.__project.app_window_state.is_valid():
                    if self.__project.app_window_state.maximized:
                        self.__app_window.maximize()
                    else:
                        self.__app_window.resize(self.__project.app_window_state.w,
                                self.__project.app_window_state.h)
                    self.__pane.set_position(self.__project.app_window_state.pane)

        self.__keeper_treeview = KeeperTreeView(self.__builder, self.__project)
        self.__keeper_treeview.refresh()
        self.__app_window.show_all()
        Gtk.main()

    def save_last(self):
        if self.__project.project_path() != "":
            draftman2rc = Path.home() / '.draftman2rc'
            with draftman2rc.open("w") as f:
                f.write(str(self.__project.project_path()))

    # User closed the appwindow
    def onDestroy(self, *args):
        self.save_last()
        self.__keeper_treeview.save()
        Gtk.main_quit()

    # Signal handlers
    #
    #
    def __on_size_allocate(self, widget, allocation):
        (self.__project.app_window_state.w, self.__project.app_window_state.h) = self.__app_window.get_size()

    def __on_pane_position(self, widget, gparam):
        self.__project.app_window_state.pane = widget.get_property(gparam.name)

    def __on_window_state_event(self, widget, event):
        self.__project.app_window_state.maximized = (event.new_window_state & Gdk.WindowState.MAXIMIZED) != 0
        self.__project.app_window_state.fullscreen = (event.new_window_state & Gdk.WindowState.FULLSCREEN) != 0

    # Menu and Button Handlers
    #
    #

    # User selected Quit
    def onQuit(self, *args):
        self.save_last()
        self.__keeper_treeview.save()
        Gtk.main_quit()

    # User selected add file
    def onAddFile(self, *args):
        self.__keeper_treeview.on_add_file(args)

    # User selected add file at root
    def onAddFileAtRoot(self, *args):
        self.__keeper_treeview.on_add_file_at_root(args)

    # User selected add directory
    def onAddDirectory(self, *args):
        self.__keeper_treeview.on_add_directory(args)

    # User selected add root directory
    def onAddDirectoryAtRoot(self, *args):
        self.__keeper_treeview.on_add_directory_at_root(args)

    # User selected edit file
    def onEditFile(self, *args):
        self.__keeper_treeview.on_edit_file(args)

    # User selected delete
    def onDelete(self, *args):
        self.__keeper_treeview.on_delete(args)


    # User selected New
    def onNew(self, *args):
        npd = NewProjectDialog(self.__builder)
        (response, project_name, project_directory) = npd.run()
        if response == Gtk.ResponseType.OK:
            if self.__project.is_loaded():
                self.save_last()
                self.__keeper_treeview.save()
                self.__keeper_treeview.clear_all()

            (rv, reason) = self.__project.new(project_directory, project_name)
            if not rv:
                m = Message()
                m.error(self.__app_window, 'Cannot create project', 'Cannot'
                        ' create project directory, %s:\n\n%s\n' %
                        (project_directory, reason))
                return

            self.__keeper_treeview.refresh()
            self.__keeper_treeview.enable_items()

    # User selected Open
    def onOpen(self, *args):
        opd = OpenProjectDialog(self.__builder)
        (response, project_directory) = opd.run()
        if response == Gtk.ResponseType.OK:
            if self.__project.is_loaded():
                self.save_last()
                self.__keeper_treeview.save()
                self.__keeper_treeview.clear_all()

            (rv, reason) = self.__project.open(project_directory)
            if not rv:
                m = Message()
                m.error(self.__app_window, 'Cannot open project', 'Cannot open '
                        ' project directory, %s:\n\n%s\n' % (project_directory,
                        reason))
                return

            self.__keeper_treeview.refresh()
            self.__keeper_treeview.enable_items()

    # Expand all
    def onExpandAll(self, *args):
        self.__keeper_treeview.expand_all()

    # Collapse all
    def onCollapseAll(self, *args):
        self.__keeper_treeview.collapse_all()

    # Update word/scene counts
    def onUpdateWordCounts(self, *args):
        self.__keeper_treeview.update_word_counts()

    # User selected About
    def onAbout(self, *args):
        ad = AboutDialog(self.__builder)
        ad.run()

    # User selected Preferences
    def onPreferences(self, *args):
        pd = PreferencesDialog(self.__builder, self.__project)
        (response, editor, editor_args, backup_path, backup_on_start,
                include_text, include_text_entry, skip_first, include_titles,
                include_directory_titles) = pd.run()
        if response == Gtk.ResponseType.OK:
            self.__project.set_editor(editor)
            self.__project.set_editor_args(editor_args)
            self.__project.set_backup_path(backup_path)
            self.__project.set_backup_on_start(backup_on_start)
            self.__project.set_include_text(include_text)
            self.__project.set_include_text_entry(include_text_entry)
            self.__project.set_skip_first(skip_first)
            self.__project.set_include_titles(include_titles)
            self.__project.set_include_directory_titles(include_directory_titles)

    # User selected Compile
    def onCompile(self, *args):
        dialog = Gtk.FileChooserDialog("Save compilation to folder",
                self.__app_window, Gtk.FileChooserAction.SELECT_FOLDER,
                (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select",
                    Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        filename = "NA"
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()

        dialog.destroy()

        p = Path(filename)
        fileName = '%s%s' % (self.__project.name(), '.md')
        p = p / fileName
        self.__keeper_treeview.compile(str(p))

    # User selected backup
    def onCreateBackup(self, *args):
        dt = datetime.now()
        ts = dt.strftime('%Y%m%d_%H%M%S')
        p = Path(self.__project.backup_path())
        filename = '%s-%s%s' % (self.__project.name(), ts, '.zip')
        p = p / filename
        self.__keeper_treeview.backup(str(p))

    # User selected create tutorial
    def onCreateTutorial(self, *args):
        m = Message()
        dialog = Gtk.FileChooserDialog("Save tutorial project to folder",
                self.__app_window, Gtk.FileChooserAction.SELECT_FOLDER,
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
                rv = m.confirm(self.__app_window, 'Overwrite?', '%s exists.'
                      ' Overwrite?' % str(tutorial_path))
                go_ahead == (response == Gtk.ResponseType.OK)

            if go_ahead:
                fops = KeeperFileOpsLinux()
                (rv, reason) = fops.copy_tutorial(tut_dir)
                if not rv:
                    m.error(self.__app_window, 'Error', 'Could not create'
                            ' tutorial: %s\n' % reason)
                else:
                    m.info(self.__app_window, 'Success', 'Created %s' %
                            str(tutorial_path))

                if self.__project.is_loaded():
                    self.save_last()
                    self.__keeper_treeview.save()
                    self.__keeper_treeview.clear_all()

                (rv, reason) = self.__project.open(str(tutorial_path))
                if not rv:
                    m = Message()
                    m.error(self.__app_window, 'Cannot open project', 'Cannot'
                            ' open project: %s:\n\n%s\n' % (str(tutorial_path),
                                reason))
                    return

                self.__keeper_treeview.refresh()
                self.__keeper_treeview.enable_items()


