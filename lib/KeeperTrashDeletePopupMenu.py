"""
KeeperTrashDeletePopupMenu

This class controls how the popup menu appears in the treeview
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class KeeperTrashDeletePopupMenu:

    def __init__(self):
        self._popup = Gtk.Menu()
        self._menuItemDeleteAll = Gtk.MenuItem('Delete...')
        self._popup.append(self._menuItemDeleteAll)

    def enable(b):
        self._popup.set_sensitive(False)

    def get_menu(self):
        self._menuItemDeleteAll.set_sensitive(True)
        return self._popup

    def connect_delete_all(self, del_all_func):
        self._menuItemDeleteAll.connect("activate", del_all_func)
