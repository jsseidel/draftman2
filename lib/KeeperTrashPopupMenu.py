"""
KeeperTrashPopupMenu

This class controls how the popup menu appears in the treeview
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class KeeperTrashPopupMenu:

    def __init__(self):
        self._popup = Gtk.Menu()
        self._menuItemDeleteAll = Gtk.MenuItem('Empty...')
        self._popup.append(self._menuItemDeleteAll)

    def enable(b):
        self._popup.set_sensitive(False)

    def get_menu(self, has_children):
        self._menuItemDeleteAll.set_sensitive(has_children)
        return self._popup

    def connect_delete_all(self, del_all_func):
        self._menuItemDeleteAll.connect("activate", del_all_func)
