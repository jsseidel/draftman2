"""
AppWindowState

This class keeps track of the window state from run to run.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class AppWindowState:

    def __init__(self):
        self.w = -1
        self.h = -1
        self.pane = -1
        self.maximized = False
        self.fullscreen = False

    def is_valid(self):
        return (self.w != -1 and self.h != -1 and self.pane != -1)

    def __str__(self):
        return "W=%d, H=%d, P=%d, M=%s, F=%s" % (self.w, self.w, self.pane,
                self.maximized, self.fullscreen)
