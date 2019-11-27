"""
AppWindowSignalHandler

This class catches all signals and takes action. More complex actions are
routed to library functions and other classes. We try to keep things simple in
this class.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lib.Project import Project

class AppWindowSignalHandler:

    def __init__(self, project):
        self.project = project

    # User closed the appwindow
    def onDestroy(self, *args):
        Gtk.main_quit()

    # MENU
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
        print("Create a new project")

    # User selected Open
    def onOpen(self, *args):
        print("Open a project")
