"""
Draftmaster

This class handles the opening and parsing of the draft.txt file into a
treeview model.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path, PurePath

class Draftmaster:

    def __parse_line(self, line):
        line = line.strip()
        a = line.split('|')
        p = PurePath(a[0])
        title = a[1]
        in_compile = True if a[2] == "1" else False
        return (list(p.parts), title, in_compile)

    def __add_tree_row(self, store, parent_row, pieces, title, in_compile):
        if len(pieces) == 1:
            parent = store.append(parent_row, [title])
        else:
            parent = store.append(parent_row, [pieces[0]])
            pieces = pieces[1:]
            self.__add_tree_row(store, parent, pieces, title, in_compile)


    def get_tree_store(self, path):
        rv = True
        reason = "OK"

        store = Gtk.TreeStore(str)
        rows = []

        try:
            with open(path, "r") as f:
                for line in f.readlines():
                    # Ignore comments, or lines that start with '%'
                    if line[0] == '%':
                        continue

                    # Lines are made up of a relative path, a title, and a 0 or
                    # 1 to indicate that the file should or should not be
                    # included in a compile
                    (path_pieces, title, in_compile) = self.__parse_line(line)

                    # Use a recursive function to add the tree rows
                    self.__add_tree_row(store, None, path_pieces, title, in_compile)

        except Exception as e:
            rv = False
            reason = str(e)

        return (rv, reason, store)
