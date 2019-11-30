"""
KeeperTreeModel

This class represents the keeper tree model
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from pathlib import Path, PurePath
import yaml
import traceback

from lib.Project import Project

class KeeperTreeModel:

    def __init__(self):
        self.__store = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, str, bool, int, int, int, int)

    def __get_icon_for_type(self, item_type, contents_size):
        if item_type == 'directory':
            return Gtk.IconTheme.get_default().load_icon("gtk-directory", 24, 0)
        elif item_type == 'file':
            return Gtk.IconTheme.get_default().load_icon("gtk-file", 24, 0)
        elif item_type == 'trash' and contents_size == 0:
            return Gtk.IconTheme.get_default().load_icon("gnome-stock-trash", 24, 0)
        elif item_type == 'trash' and contents_size > 0:
            return Gtk.IconTheme.get_default().load_icon("gnome-stock-trash-full", 24, 0)

        return Gtk.IconTheme.get_default().load_icon("gtk-file", 24, 0)

    def __add_item_list_to_store(self, parent_row, item_list):
        for item in item_list:
            contents_size = 0
            if item['type'] == 'directory' or item['type'] == 'trash':
                contents_size = len(item['contents'])

            parent = self.__store.append(parent_row,
                [self.__get_icon_for_type(item['type'], contents_size),
                    item['type'], item['title'], item['compile'], 0, 0, 0, 0])

            if item['type'] == 'directory' or item['type'] == 'trash':
                self.__add_item_list_to_store(parent, item['contents'])

    def clear(self):
        self.__store.clear()

    def get_tree_store(self):
        return self.__store

    def insert_at(self, tree_iter, name, item_type, as_child):
        # If not inserting as a child, insert after the selected sibling
        if not as_child:
            self.__store.insert_after(None, tree_iter, [self.__get_icon_for_type(item_type, 0), item_type, name, True, 0, 0, 0, 0])
        else:
            # Inserting as a child, so we'll leave the sibling empty
            self.__store.insert_after(tree_iter, None, [self.__get_icon_for_type(item_type, 0), item_type, name, True, 0, 0, 0, 0])


    def load_tree_store(self, project_path):
        rv = True
        reason = "OK"

        self.clear()

        try:
            yaml_str = ""
            with open(("%s/keeper.yaml" % project_path), "r") as stream:
                draftmaster = yaml.safe_load(stream)
                self.__add_item_list_to_store(None, draftmaster['keeper'])

        except Exception as e:
            rv = False
            reason = str(e)
            traceback.print_exc()

        return (rv, reason)
