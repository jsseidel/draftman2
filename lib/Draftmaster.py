"""
Draftmaster

This class handles the opening and parsing of the draft.txt file into a
treeview model.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path, PurePath
import yaml
import traceback

class Draftmaster:

    def __add_directory_to_store(self, store, parent_row, item):
        parent = store.append(parent_row, [item['title']])
        self.__add_directory_to_store(store, parent, item['contents'])

    def get_tree_store(self, path):
        rv = True
        reason = "OK"

        store = Gtk.TreeStore(str)

        try:
            yaml_str = ""
            with open(path, "r") as stream:
                draftmaster = yaml.safe_load(stream)
                for item in draftmaster['draft']:
                    if item['type'] == 'file':
                        store.append(None, [item['title']])
                    else:
                        self.__add_directory_to_store(store, None, item)

        except Exception as e:
            rv = False
            reason = str(e)
            traceback.print_exc()

        return (rv, reason, store)
