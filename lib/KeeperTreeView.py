"""
KeeperTreeView

This class maintains the app's keeper tree view.
"""
import enum
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

from lib.KeeperTreeModel import KeeperTreeModel
from lib.Message import Message

class KeeperTreeView:
    def __init__(self, app_window, project, treeview):
        self.app_window = app_window
        self.project = project
        self.treeview = treeview
        self.tree_model = KeeperTreeModel()

        # Note that when adding columns, the "text" attribute is an index into
        # the tree model list. Attributes names match the available properties
        # of the class.

        # The icon representing the kind of item
        col_type = Gtk.TreeViewColumn('Type', Gtk.CellRendererPixbuf(), pixbuf=0)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        self.treeview.append_column(col_type)

        # The title of the item
        col_title = Gtk.TreeViewColumn('Title', Gtk.CellRendererText(), text=1)
        col_title.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_title.set_resizable(True)
        col_title.set_reorderable(False)
        self.treeview.append_column(col_title)

        # Add checkbox column for including in compilees
        toggle_renderer = Gtk.CellRendererToggle()
        col_include = Gtk.TreeViewColumn('Inc', toggle_renderer, active=2)
        col_include.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_include.set_resizable(False)
        col_include.set_reorderable(False)
        toggle_renderer.connect("toggled", self.__on_compile_cell_toggled)
        self.treeview.append_column(col_include)

        # Number of scenes in an item
        col_scenes = Gtk.TreeViewColumn('Scenes', Gtk.CellRendererText(), text=3)
        col_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_scenes.set_resizable(True)
        col_scenes.set_reorderable(False)
        self.treeview.append_column(col_scenes)

        # Running count of the number of scenes in the project
        col_running_scenes = Gtk.TreeViewColumn('Running', Gtk.CellRendererText(), text=4)
        col_running_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_scenes.set_resizable(True)
        col_running_scenes.set_reorderable(False)
        self.treeview.append_column(col_running_scenes)

        # The number of words in the item
        col_words = Gtk.TreeViewColumn('Words', Gtk.CellRendererText(), text=5)
        col_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_words.set_resizable(True)
        col_words.set_reorderable(False)
        self.treeview.append_column(col_words)

        # Running count of the number of words in the project
        col_running_words = Gtk.TreeViewColumn('Running', Gtk.CellRendererText(), text=6)
        col_running_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_words.set_resizable(True)
        col_running_words.set_reorderable(False)
        self.treeview.append_column(col_running_words)

        # Connect signals
        select = self.treeview.get_selection()
        select.connect("changed", self.__on_tree_selection_changed)

    def refresh(self):
        if not self.project.is_loaded:
            return

        (is_ok, reason) = self.tree_model.load_tree_store(self.project.project_path)
        if not is_ok:
            m = Message()
            m.error(self.app_window, 'Keeper error', 'Could not refresh '
                    'Keeper:\n\n%s' % reason)
            return

        # Set treestore
        self.treeview.set_model(self.tree_model.get_tree_store())
        self.treeview.set_cursor(0)

    ###
    ##
    ## Helper functions
    ##
    ###
    def __set_compile_cells(self, store, tree_iter, new_value):
        while tree_iter is not None:
            store[tree_iter][2] = new_value
            if store.iter_has_child(tree_iter):
                child_iter = store.iter_children(tree_iter)
                self.__set_compile_cells(store, child_iter, new_value)
            tree_iter = store.iter_next(tree_iter)


    def __iter_to_project_path(self, store, tree_iter, path):
        parent_iter = store.iter_parent(tree_iter)
        if parent_iter is not None:
            parent_path = self.__iter_to_project_path(store, parent_iter, store[parent_iter][1])
            return ("%s/%s" % (parent_path, path))

        return path

    ###
    ##
    ## Signal handler functions
    ##
    ###
    def __on_tree_selection_changed(self, selection):
        (model, tree_iter) = selection.get_selected()
        if tree_iter is not None:
            print("You selected", model[tree_iter][1])
            store = self.tree_model.get_tree_store()
            print("path=%s" % self.__iter_to_project_path(store, tree_iter, model[tree_iter][1]))

    def __on_compile_cell_toggled(self, widget, path):
        store = self.tree_model.get_tree_store()
        new_value = not store[path][2]

        # Now this item and all children should be set to new value
        store[path][2] = new_value
        tree_iter = store.get_iter(path)
        self.__set_compile_cells(store, store.iter_children(tree_iter), new_value)

