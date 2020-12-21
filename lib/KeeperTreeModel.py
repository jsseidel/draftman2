"""
KeeperTreeModel

This class represents the keeper tree model
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk, GdkPixbuf
from pathlib import Path, PurePath
import os
import yaml
import traceback

from lib.Project import Project

class KeeperTreeModel:

    def __init__(self):
        self._store = Gtk.TreeStore(GdkPixbuf.Pixbuf, str, str, bool, str, bool, int, int, int, int)

    def _get_icon_for_type_or_name(self, item_type, item_name):
        icon_size = 16
        if 'DRAFTMAN2_ICON_SIZE' in os.environ:
            icon_size = int(os.environ['DRAFTMAN2_ICON_SIZE'])

        if item_type == 'directory' and item_name == 'Trash':
            return GdkPixbuf.Pixbuf.new_from_file_at_size("icon/trash.svg", icon_size, icon_size)
        elif item_type == 'directory':
            return GdkPixbuf.Pixbuf.new_from_file_at_size("icon/directory.svg", icon_size, icon_size)
        elif item_type == 'file':
            return GdkPixbuf.Pixbuf.new_from_file_at_size("icon/file.svg", icon_size, icon_size)

        return GdkPixbuf.Pixbuf.new_from_file_at_size("icon/file.svg", icon_size, icon_size)

    def _add_item_list_to_store(self, parent_row, item_list):
        if item_list is not None:
            for item in item_list:
                contents_size = 0
                if 'contents' in item:
                    contents_size = len(item['contents'])

                init_expanded = False
                if 'expanded' in item:
                    init_expanded = item['expanded']

                parent = self._store.append(parent_row,
                        [self._get_icon_for_type_or_name(item['type'],
                            item['title']), item['type'], item['id'], init_expanded,
                            item['title'], item['compile'], 0, 0, 0, 0])

                if 'contents' in item:
                    self._add_item_list_to_store(parent, item['contents'])

    def clear(self):
        self._store.clear()

    def get_tree_store(self):
        return self._store

    def _find_last_child_of_iter(self, store, tree_iter):
        if tree_iter is not None:
            if store.iter_has_child(tree_iter):
                child_iter = store.iter_children(tree_iter)
                last_child_iter = child_iter
                while child_iter:
                    last_child_iter = child_iter
                    child_iter = store.iter_next(child_iter)

                return last_child_iter
            else:
                return None

        return tree_iter

    def insert_at(self, tree_iter, name, item_type, item_id, as_child):
        # If not inserting as a child, insert after the selected sibling
        if not as_child:
            return self._store.insert_after(None, tree_iter,
                [self._get_icon_for_type_or_name(item_type, name),
                    item_type, item_id, False, name, True, 0, 0, 0, 0])
        else:
            # Inserting as a child. We find the last sibling and insert after it.
            return self._store.insert_after(tree_iter, self._find_last_child_of_iter(self._store,
                tree_iter), [self._get_icon_for_type_or_name(item_type,
                    name), item_type, item_id, False, name, True, 0, 0, 0, 0])

    def remove(self, tree_iter):
        self._store.remove(tree_iter)

    def load_tree_store(self, project_path):
        rv = True
        reason = "OK"

        self.clear()

        try:
            with open(("%s/keeper.yaml" % project_path), "r") as stream:
                keeper = yaml.safe_load(stream)
                self._add_item_list_to_store(None, keeper['keeper'])

        except Exception as e:
            rv = False
            reason = str(e)
            traceback.print_exc()

        return (rv, reason)
