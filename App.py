"""
App

This class is responsible for routing gtk signals and maintaining the
consistency of the state of the running instance of draftman.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

import os

from lib.Project import Project
from lib.NewProjectDialog import NewProjectDialog
from lib.OpenProjectDialog import OpenProjectDialog
from lib.KeeperTreeView import KeeperTreeView
from lib.Message import Message

class App:

    def __init__(self):
        # Use a builder to create our objects from the glade
        # file.
        self.builder = Gtk.Builder()
        self.builder.add_from_file('%s/draftman2.glade' %
                os.path.dirname(os.path.realpath(__file__)))
        self.builder.connect_signals(self)
        self.app_window = self.builder.get_object("appWindow")
        self.keeper_treeview = self.builder.get_object("treeViewKeeper")
        self.project = Project()

        self.keeper_treeview = KeeperTreeView(self.app_window, self.project, self.keeper_treeview)

        self.app_window.show_all()
        Gtk.main()

    # User closed the appwindow
    def onDestroy(self, *args):
        Gtk.main_quit()

    # MENU Handlers
    #
    #

    # User selected Quit
    def onQuit(self, *args):
        Gtk.main_quit()

    # User selected Add
    def onAdd(self, *args):
        print("Add a file to a project")

    # User selected New
    def onNew(self, *args):
        np = NewProjectDialog(self.app_window,
                self.builder.get_object('entryProjectName'),
                self.builder.get_object('fileChooserProjectDirectory'))
        (response, project_name, project_directory) = np.run()
        if response == Gtk.ResponseType.OK:
            (rv, reason) = self.project.new(project_directory, project_name)
            if not rv:
                m = Message()
                m.error(self.app_window, "Cannot create project", "Cannot create project directory, %s:\n\n%s\n" % (project_directory, reason))
                return

            self.keeper_treeview.refresh()

    # User selected Open
    def onOpen(self, *args):
        op = OpenProjectDialog(self.app_window)
        (response, project_directory) = op.run()
        if response == Gtk.ResponseType.OK:
            (rv, reason) = self.project.open(project_directory)
            if not rv:
                m = Message()
                m.error(self.app_window, "Cannot open project", "Cannot open project directory, %s:\n\n%s\n" % (project_directory, reason))
                return

            self.keeper_treeview.refresh()
            self.keeper_treeview.save()
