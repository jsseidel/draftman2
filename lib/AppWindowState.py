"""
AppWindowState

This class keeps track of the window state from run to run.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GLib

class AppWindowState:

    def __init__(self):
        self._app_width = -1
        self._app_height = -1
        self._pane_position = -1

    def set_width_height(self, w, h):
        self._app_width = w
        self._app_height = h

    def set_pane_position(self, p):
        self._pane_position = p

    def load_keyfile(self):
        self._app_width = 920
        self._app_height = 1414
        self._pane_position = 700
        return (self._app_width, self._app_height, self._pane_position)

    def save_keyfile(self):
        print(self)

    def __str__(self):
        return "W=%d, H=%d, P=%d" % (self._app_width, self._app_height,
            self._pane_position)
