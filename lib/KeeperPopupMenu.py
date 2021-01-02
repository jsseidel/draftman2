"""
KeeperPopupMenu

This class controls how the popup menu appears in the treeview
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class KeeperPopupMenu:

    def __init__(self):
        self._popup = Gtk.Menu()
        self._menuItemAddFile = Gtk.MenuItem('Add file...')
        self._menuItemEditFile = Gtk.MenuItem('Edit...')
        self._menuItemCopy = Gtk.MenuItem('Copy')
        self._menuItemPaste = Gtk.MenuItem('Paste')
        self._menuItemAddDirectory = Gtk.MenuItem('Add folder...')
        self._menuItemDelete = Gtk.MenuItem('Delete...')

        self._popup.append(self._menuItemAddFile)
        self._popup.append(self._menuItemEditFile)
        self._popup.append(self._menuItemCopy)
        self._popup.append(self._menuItemPaste)
        self._popup.append(Gtk.SeparatorMenuItem())
        self._popup.append(self._menuItemAddDirectory)
        self._popup.append(Gtk.SeparatorMenuItem())
        self._popup.append(self._menuItemDelete)

    def enable(b):
        self._popup.set_sensitive(False)

    def get_menu_for_type(self, item_type, has_children, has_sel, can_paste, is_in_trash):
        if item_type == 'file':
            self._menuItemAddFile.set_sensitive(True)
            self._menuItemEditFile.set_sensitive(True)
            self._menuItemCopy.set_sensitive(True)
            self._menuItemPaste.set_sensitive(has_sel and can_paste)
            self._menuItemAddDirectory.set_sensitive(False)
            self._menuItemDelete.set_sensitive(not is_in_trash)
        elif item_type == 'directory':
            self._menuItemAddFile.set_sensitive(True)
            self._menuItemEditFile.set_sensitive(False)
            self._menuItemCopy.set_sensitive(True)
            self._menuItemPaste.set_sensitive(has_sel and can_paste)
            self._menuItemAddDirectory.set_sensitive(True)
            self._menuItemDelete.set_sensitive(not is_in_trash)
        else:
            self._menuItemAddFile.set_sensitive(True)
            self._menuItemEditFile.set_sensitive(False)
            self._menuItemCopy.set_sensitive(False)
            self._menuItemPaste.set_sensitive(has_sel and can_paste)
            self._menuItemAddDirectory.set_sensitive(True)
            self._menuItemDelete.set_sensitive(False)

        return self._popup

    def connect_add(self, add_file_func, add_directory_func):
        self._menuItemAddFile.connect("activate", add_file_func)
        self._menuItemAddDirectory.connect("activate", add_directory_func)

    def connect_edit(self, edit_file_func):
        self._menuItemEditFile.connect("activate", edit_file_func)

    def connect_copy(self, copy_func):
        self._menuItemCopy.connect("activate", copy_func)

    def connect_paste(self, paste_func):
        self._menuItemPaste.connect("activate", paste_func)

    def connect_delete(self, del_func):
        self._menuItemDelete.connect("activate", del_func)
