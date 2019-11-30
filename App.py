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
from lib.AddItemDialog import AddItemDialog
from lib.KeeperTreeView import KeeperTreeView
from lib.Message import Message

class App:

    def __init__(self):
        # Use a builder to create our objects from the glade
        # file.
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file('%s/draftman2.glade' %
                os.path.dirname(os.path.realpath(__file__)))
        self.__builder.connect_signals(self)
        self.__app_window = self.__builder.get_object("appWindow")
        self.__keeper_treeview = self.__builder.get_object("treeViewKeeper")
        self.__project = Project()
        self.__keeper_treeview = KeeperTreeView(self.__app_window,
                self.__project, self.__keeper_treeview)

        self.__app_window.show_all()
        Gtk.main()

    # User closed the appwindow
    def onDestroy(self, *args):
        self.__keeper_treeview.save()
        Gtk.main_quit()

    # MENU Handlers
    #
    #

    # User selected Quit
    def onQuit(self, *args):
        self.__keeper_treeview.save()
        Gtk.main_quit()

    # User selected Add or clicked add button
    def onAdd(self, button):
        self.__doAddItem()

    def onAdd(self, *args):
        self.__doAddItem()

    def __doAddItem(self):
        aid = AddItemDialog(self.__builder)
        (response, name, item_type, is_child) = aid.run()
        if response == Gtk.ResponseType.OK:
            self.__keeper_treeview.add_item(name, item_type, is_child)
            self.__keeper_treeview.refresh()

    # User selected New
    def onNew(self, *args):
        npd = NewProjectDialog(self.__builder)
        (response, project_name, project_directory) = npd.run()
        if response == Gtk.ResponseType.OK:
            (rv, reason) = self.__project.new(project_directory, project_name)
            if not rv:
                m = Message()
                m.error(self.__app_window, "Cannot create project", "Cannot create project directory, %s:\n\n%s\n" % (project_directory, reason))
                return

            self.__keeper_treeview.refresh()

    # User selected Open
    def onOpen(self, *args):
        opd = OpenProjectDialog(self.__builder)
        (response, project_directory) = opd.run()
        if response == Gtk.ResponseType.OK:
            (rv, reason) = self.__project.open(project_directory)
            if not rv:
                m = Message()
                m.error(self.__app_window, "Cannot open project", "Cannot open project directory, %s:\n\n%s\n" % (project_directory, reason))
                return

            self.__keeper_treeview.refresh()
