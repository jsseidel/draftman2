"""
KeeperPopupMenu

This class controls how the popup menu appears in the treeview
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class KeeperPopupMenu:

    def __init__(self):
        self.__dpopup = Gtk.Menu()
        self.__menuItemAddFile = Gtk.MenuItem('Add file...')
        self.__menuItemEditFile = Gtk.MenuItem('Edit...')
        self.__menuItemAddDirectory = Gtk.MenuItem('Add directory...')
        self.__menuItemDelete = Gtk.MenuItem('Delete ...')

        self.__dpopup.append(self.__menuItemAddFile)
        self.__dpopup.append(self.__menuItemAddDirectory)
        self.__dpopup.append(self.__menuItemDelete)

        self.__fpopup = Gtk.Menu()
        self.__fpopup.append(self.__menuItemEditFile)
        self.__fpopup.append(self.__menuItemDelete)

        self.__npopup = Gtk.Menu()
        self.__npopup.append(self.__menuItemAddFile)
        self.__npopup.append(self.__menuItemAddDirectory)

    def get_menu_for_type(self, item_type):
        if item_type == 'file':
            return self.__fpopup
        elif item_type == 'directory' or item_type == 'trash':
            return self.__dpopup

        return self.__npopup

    def connect_add(self, add_file_func, add_directory_func):
        self.__menuItemAddFile.connect("activate", add_file_func)
        self.__menuItemAddDirectory.connect("activate", add_directory_func)

    def connect_edit(self, edit_file_func):
        self.__menuItemEditFile.connect("activate", edit_file_func)

    def connect_delete(self, del_func):
        self.__menuItemDelete.connect("activate", del_func)
