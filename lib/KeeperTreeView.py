"""
KeeperTreeView

This class maintains the app's keeper tree view.
"""
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re

from lib.AddItemDialog import AddItemDialog
from lib.KeeperTreeModel import KeeperTreeModel
from lib.KeeperPopupMenu import KeeperPopupMenu
from lib.Message import Message
from lib.KeeperFileOpsLinux import KeeperFileOpsLinux
from pathlib import Path, PurePath

class KeeperTreeView:
    COL_PIXBUF=0
    COL_TYPE=1
    COL_ID=2
    COL_TITLE=3
    COL_COMPILE=4
    COL_SCENES=5
    COL_SCENES_RUNNING=6
    COL_WORDS=7
    COL_WORDS_RUNNING=8

    def __init__(self, builder, project):
        self.__app_window = builder.get_object('appWindow')
        self.__project = project
        self.__treeview = builder.get_object('treeViewKeeper')
        self.__tree_model = KeeperTreeModel()
        self.__builder = builder

        # We use this to save our last selected row so we can save notes
        # before we show another row's notes
        self.__last_sel = None

        # Note that when adding columns, the "text" attribute is an index into
        # the tree model list. Attributes names match the available properties
        # of the class.

        # The icon representing the kind of item
        col_icon = Gtk.TreeViewColumn('Type', Gtk.CellRendererPixbuf(),
                pixbuf=KeeperTreeView.COL_PIXBUF)
        col_icon.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_icon.set_resizable(False)
        col_icon.set_reorderable(False)
        self.__treeview.append_column(col_icon)

        # A hidden type column
        col_type = Gtk.TreeViewColumn('Type', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_TYPE)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        col_type.set_visible(False)
        self.__treeview.append_column(col_type)

        # A hidden id column
        col_type = Gtk.TreeViewColumn('ID', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_ID)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        col_type.set_visible(False)
        self.__treeview.append_column(col_type)

        # The title of the item
        col_title = Gtk.TreeViewColumn('Title', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_TITLE)
        col_title.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_title.set_resizable(True)
        col_title.set_reorderable(False)
        self.__treeview.append_column(col_title)

        # Add checkbox column for including in compiles
        toggle_renderer = Gtk.CellRendererToggle()
        col_include = Gtk.TreeViewColumn('Inc', toggle_renderer,
                active=KeeperTreeView.COL_COMPILE)
        col_include.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_include.set_resizable(False)
        col_include.set_reorderable(False)
        toggle_renderer.connect("toggled", self.__on_compile_cell_toggled)
        self.__treeview.append_column(col_include)

        # Number of scenes in an item
        col_scenes = Gtk.TreeViewColumn('Scenes', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_SCENES)
        col_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_scenes.set_resizable(True)
        col_scenes.set_reorderable(False)
        self.__treeview.append_column(col_scenes)

        # Running count of the number of scenes in the project
        col_running_scenes = Gtk.TreeViewColumn('Running',
                Gtk.CellRendererText(), text=KeeperTreeView.COL_SCENES_RUNNING)
        col_running_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_scenes.set_resizable(True)
        col_running_scenes.set_reorderable(False)
        self.__treeview.append_column(col_running_scenes)

        # The number of words in the item
        col_words = Gtk.TreeViewColumn('Words', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_WORDS)
        col_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_words.set_resizable(True)
        col_words.set_reorderable(False)
        self.__treeview.append_column(col_words)

        # Running count of the number of words in the project
        col_running_words = Gtk.TreeViewColumn('Running',
                Gtk.CellRendererText(), text=KeeperTreeView.COL_WORDS_RUNNING)
        col_running_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_words.set_resizable(True)
        col_running_words.set_reorderable(False)
        self.__treeview.append_column(col_running_words)

        # Connect signals
        select = self.__treeview.get_selection()
        select.connect("changed", self.__on_tree_selection_changed)

        self.__treeview.connect("drag-end", self.__on_row_moved)
        self.__treeview.connect("button-press-event", self.__on_button_pressed)

        # A popover menu for right clicks in treeview
        self.__popup = KeeperPopupMenu()
        self.__popup.connect_add(self.on_add_file, self.on_add_directory)
        self.__popup.connect_delete(self.on_delete)
        self.__popup.connect_edit(self.on_edit_file)

    def refresh(self):
        if not self.__project.is_loaded():
            return

        (is_ok, reason) = self.__tree_model.load_tree_store(self.__project.project_path())
        if not is_ok:
            m = Message()
            m.error(self.__app_window, 'Keeper error', 'Could not refresh '
                    'Keeper:\n\n%s' % reason)
            return

        # Set treestore
        self.__treeview.set_model(self.__tree_model.get_tree_store())
        self.__treeview.set_cursor(0)

    def add_item(self, name, item_type, item_id, as_child):
        (model, tree_iter) = self.__treeview.get_selection().get_selected()
        self.__tree_model.insert_at(tree_iter, name, item_type, item_id, as_child)
        self.save()

    def remove_item(self, tree_iter):
        self.__tree_model.remove(tree_iter)
        self.save()

    def iter_to_project_path(self, tree_iter):
        item_id = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_ID]
        item_name = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_TITLE]
        return ("%s/%s" % (self.__project.keeper_path(),
            self.__file_name(item_name, item_id)))

    def iter_to_notes_path(self, tree_iter):
        item_id = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_ID]
        item_name = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_TITLE]
        return ("%s/%s" % (self.__project.notes_path(),
            self.__file_name(item_name, item_id)))

    def __tree_to_yaml(self, store, tree_iter, indent, out_str=""):
        while tree_iter is not None:
            item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
            item_id = store[tree_iter][KeeperTreeView.COL_ID]
            item_title = store[tree_iter][KeeperTreeView.COL_TITLE]
            item_compile = store[tree_iter][KeeperTreeView.COL_COMPILE]

            out_str = out_str + "%s- type: '%s'\n" % (indent, item_type)
            out_str = out_str + "%s  title: '%s'\n" % (indent, item_title)
            out_str = out_str + "%s  id: '%s'\n" % (indent, item_id)
            out_str = out_str + '%s  compile: %s\n' % (indent, item_compile)
            if store.iter_has_child(tree_iter):
                out_str = out_str + '%s  contents:\n' % indent
                child_iter = store.iter_children(tree_iter)
                out_str = self.__tree_to_yaml(store, child_iter, indent + "  ", out_str)
            elif item_type == 'directory':
                out_str = out_str + '%s  contents: []\n' % indent

            tree_iter = store.iter_next(tree_iter)

        return out_str

    def save(self):
        if self.__project.is_loaded():
            store = self.__tree_model.get_tree_store()
            tree_iter = store.get_iter_first()
            keeper_str = "project:\nkeeper:\n%s\n" % self.__tree_to_yaml(store, tree_iter, "  ")
            with open(self.__project.keeper_yaml(), "w") as f:
                f.write(keeper_str)

    ###
    ##
    ## Helper functions
    ##
    ###
    def __set_compile_cells(self, store, tree_iter, new_value):
        while tree_iter is not None:
            store[tree_iter][KeeperTreeView.COL_COMPILE] = new_value
            if store.iter_has_child(tree_iter):
                child_iter = store.iter_children(tree_iter)
                self.__set_compile_cells(store, child_iter, new_value)
            tree_iter = store.iter_next(tree_iter)

    def __strip_name(self, name):
        name = name.strip()
        name = re.sub('[^0-9a-zA-Z]+', '', name.lower())
        return name

    def __file_name(self, item_name, item_id):
        return "%s-%s.md" % (self.__strip_name(item_name), item_id)

    def __save_notes(self, store, tree_iter):
        item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
        text_view_notes = self.__builder.get_object('textViewNotes')
        text_view_buffer = text_view_notes.get_buffer()
        item_id = store[tree_iter][KeeperTreeView.COL_ID]
        item_name = store[tree_iter][KeeperTreeView.COL_TITLE]
        path = Path("%s/notes/%s" % (self.__project.project_path(),
            self.__file_name(item_name, item_id)))
        start_iter = text_view_buffer.get_start_iter()
        end_iter = text_view_buffer.get_end_iter()
        with open(str(path), "w") as f:
            f.write(text_view_buffer.get_text(start_iter, end_iter, True))

    def __show_notes(self, store, tree_iter):
        item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
        text_view_notes = self.__builder.get_object('textViewNotes')
        text_view_buffer = text_view_notes.get_buffer()
        item_id = store[tree_iter][KeeperTreeView.COL_ID]
        item_name = store[tree_iter][KeeperTreeView.COL_TITLE]
        path = Path("%s/notes/%s" % (self.__project.project_path(),
            self.__file_name(item_name, item_id)))
        with open(str(path), "r") as f:
            text_view_buffer.set_text(f.read())

    ###
    ##
    ## Signal handler functions
    ##
    ###
    def __on_tree_selection_changed(self, selection):
        if self.__last_sel is not None:
            (store, tree_iter) = self.__last_sel
            self.__save_notes(store, tree_iter)

        (store, tree_iter) = selection.get_selected()
        if tree_iter is not None:
            text_view_notes = self.__builder.get_object('textViewNotes')
            self.__show_notes(store, tree_iter)
            self.__last_sel = selection.get_selected()
            text_view_notes.set_sensitive(True)
        else:
            text_view_notes = self.__builder.get_object('textViewNotes')
            text_view_buffer = text_view_notes.get_buffer()
            text_view_buffer.set_text('')
            self.__last_sel = None
            text_view_notes.set_sensitive(False)

    def __on_compile_cell_toggled(self, widget, path):
        store = self.__tree_model.get_tree_store()
        new_value = not store[path][KeeperTreeView.COL_COMPILE]

        # Now this item and all children should be set to new value
        store[path][KeeperTreeView.COL_COMPILE] = new_value
        tree_iter = store.get_iter(path)
        self.__set_compile_cells(store, store.iter_children(tree_iter), new_value)

    def __on_row_moved(self, widget, context):
        self.save()

    def __on_button_pressed(self, widget, event):
        # right click
        if event.button == 3:
            info = self.__treeview.get_path_at_pos(event.x, event.y)
            if info != None:
                (path, col, cell_x, cell_y) = info
                self.__treeview.grab_focus()
                self.__treeview.set_cursor(path, col, 0)

                selection = self.__treeview.get_selection()
                (model, tree_iter) = selection.get_selected()
                item_type = model[tree_iter][KeeperTreeView.COL_TYPE]

                menu = self.__popup.get_menu_for_type(item_type)
                menu.show_all()
                menu.popup_at_pointer(event)
            else:
                select = self.__treeview.get_selection().unselect_all()
                menu = self.__popup.get_menu_for_type(None)
                menu.show_all()
                menu.popup_at_pointer(event)
        elif event.button == 1:
            info = self.__treeview.get_path_at_pos(event.x, event.y)
            if info == None:
                select = self.__treeview.get_selection().unselect_all()

    # These are not private because our App uses them to handle the
    # app menu signals
    def on_add_file(self, *args):
        aid = AddItemDialog(self.__builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%d%m_%H%M%S')
            selection = self.__treeview.get_selection()
            (model, tree_iter) = selection.get_selected()
            (rv, reason) = self.__project.write_new_file(name, self.__file_name(name,
                item_id))
            (rv, reason) = self.__project.write_new_note(name, self.__file_name(name,
                item_id))
            if rv:
                self.add_item(name, 'file', item_id, True)
            else:
                m = Message()
                m.error(self.__app_window, 'Keeper error', 'Could not add'
                        'file:\n\n%s' % reason)

    def on_add_directory(self, *args):
        aid = AddItemDialog(self.__builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%d%m_%H%M%S')
            selection = self.__treeview.get_selection()
            (model, tree_iter) = selection.get_selected()
            (rv, reason) = self.__project.write_new_note(name,
                    self.__file_name(name, item_id))
            if rv:
                self.add_item(name, 'directory', item_id, True)
            else:
                m = Message()
                m.error(self.__app_window, 'Keeper error', 'Could not add'
                        'directory note:\n\n%s' % reason)

    def on_edit_file(self, *args):
        print('Edit file')

    def __delete_list(self, tree_iter):
        store = self.__tree_model.get_tree_store()
        item_type = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_TYPE]
        if item_type == 'file':
            path = self.iter_to_project_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self.__app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))
            path = self.iter_to_notes_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self.__app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))
        elif item_type == 'directory':
            path = self.iter_to_notes_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self.__app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))

        if store.iter_has_child(tree_iter):
            child_iter = store.iter_children(tree_iter)
            while child_iter is not None:
                self.__delete_list(child_iter)
                child_iter = store.iter_next(child_iter)

    def on_delete(self, *args):
        selection = self.__treeview.get_selection()
        (model, tree_iter) = selection.get_selected()
        self.__last_sel = None
        if tree_iter is not None:
            path = self.iter_to_project_path(tree_iter)
            item_name = self.__tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_TITLE]
            m = Message()
            if m.confirm(self.__app_window, 'Confirm', 'Are you sure you want '
                    'to permenantly delete %s?' % item_name):
                self.__delete_list(tree_iter)
                self.remove_item(tree_iter)
        else:
            m = Message()
            m.error(self.__app_window, 'Keeper error', 'Nothing to delete.'
                    ' Please report.')

