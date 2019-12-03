"""
KeeperPopupMenu

This class controls how the popup menu appears in the treeview
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class KeeperPopupMenu:

    def __init__(self):
        self.__popup = Gtk.Menu()
        self.__menuItemAddFile = Gtk.MenuItem('Add file...')
        self.__menuItemEditFile = Gtk.MenuItem('Edit...')
        self.__menuItemAddDirectory = Gtk.MenuItem('Add directory...')
        self.__menuItemDelete = Gtk.MenuItem('Delete...')
        self.__menuItemDeleteAll = Gtk.MenuItem('Empty directory...')

        self.__popup.append(self.__menuItemAddFile)
        self.__popup.append(self.__menuItemEditFile)
        self.__popup.append(Gtk.SeparatorMenuItem())
        self.__popup.append(self.__menuItemAddDirectory)
        self.__popup.append(Gtk.SeparatorMenuItem())
        self.__popup.append(self.__menuItemDelete)
        self.__popup.append(self.__menuItemDeleteAll)

    def enable(b):
        self.__popup.set_sensitive(False)

    def get_menu_for_type(self, item_type):
        if item_type == 'file':
            self.__menuItemAddFile.set_sensitive(False)
            self.__menuItemEditFile.set_sensitive(True)
            self.__menuItemAddDirectory.set_sensitive(False)
            self.__menuItemDelete.set_sensitive(True)
            self.__menuItemDeleteAll.set_sensitive(True)
        elif item_type == 'directory':
            self.__menuItemAddFile.set_sensitive(True)
            self.__menuItemEditFile.set_sensitive(False)
            self.__menuItemAddDirectory.set_sensitive(True)
            self.__menuItemDelete.set_sensitive(True)
            self.__menuItemDeleteAll.set_sensitive(True)
        else:
            self.__menuItemAddFile.set_sensitive(True)
            self.__menuItemEditFile.set_sensitive(False)
            self.__menuItemAddDirectory.set_sensitive(True)
            self.__menuItemDelete.set_sensitive(False)
            self.__menuItemDeleteAll.set_sensitive(False)

        return self.__popup

    def connect_add(self, add_file_func, add_directory_func):
        self.__menuItemAddFile.connect("activate", add_file_func)
        self.__menuItemAddDirectory.connect("activate", add_directory_func)

    def connect_edit(self, edit_file_func):
        self.__menuItemEditFile.connect("activate", edit_file_func)

    def connect_delete(self, del_func):
        self.__menuItemDelete.connect("activate", del_func)

    def connect_delete_all(self, del_all_func):
        self.__menuItemDeleteAll.connect("activate", del_all_func)
