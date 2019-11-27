"""
AppWindowHandlerRouter

This class catches all signals and routes them to the appropriate hander
classes.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class AppWindowHandlerRouter:
    # Handle the simpler stuff here
    def onDestroy(self, *args):
        Gtk.main_quit()

    def onQuit(self, *args):
        Gtk.main_quit()
