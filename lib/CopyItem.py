"""
CopyItem

This class holds information about an object the user has copied.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class CopyItem:
    def __init__(self):
        self.clear()

    def clear(self):
        self._copied_tree_iter = None

    def get(self):
        return self._copied_tree_iter

    def set(self, iter_to_copy):
        self._copied_tree_iter = iter_to_copy

    def has_sel(self):
        return self._copied_tree_iter is not None
