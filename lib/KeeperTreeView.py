"""
KeeperTreeView

This class maintains the app's keeper tree view.
"""
from datetime import datetime
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
import re
import os
import subprocess
import sys

from lib.counts import word_count, scene_count
from lib.AddItemDialog import AddItemDialog
from lib.KeeperTreeModel import KeeperTreeModel
from lib.KeeperPopupMenu import KeeperPopupMenu
from lib.Message import Message
from lib.KeeperFileOpsLinux import KeeperFileOpsLinux
from pathlib import Path, PurePath, PurePosixPath

class KeeperTreeView:
    COL_PIXBUF=0
    COL_TYPE=1
    COL_ID=2
    COL_INIT_EXPAND=3
    COL_NAME=4
    COL_COMPILE=5
    COL_SCENES=6
    COL_SCENES_RUNNING=7
    COL_WORDS=8
    COL_WORDS_RUNNING=9

    def __init__(self, builder, project):
        self._app_window = builder.get_object('appWindow')
        self._project = project
        self._treeview = builder.get_object('treeViewKeeper')
        indent = 0
        if 'DRAFTMAN2_TREE_INDENT' in os.environ:
            indent = int(os.environ['DRAFTMAN2_TREE_INDENT'])
        self._treeview.set_level_indentation(indent)
        self._tree_model = KeeperTreeModel()
        self._builder = builder
        self._label_status1 = builder.get_object('labelStatus1')
        self._label_status2 = builder.get_object('labelStatus2')
        self._label_status3 = builder.get_object('labelStatus3')
        self._text_view_notes = self._builder.get_object('textViewNotes')

        m = Message()
        m.warning(self._app_window, 'Warning BETA', 'Draftman2 is currently in'
                ' beta. This means that some things might break. If you choose to'
                ' use Draftman2 in beta, back up your projects frequently.')

        # We use this to save our last selected row so we can save notes
        # before we show another row's notes
        self._last_sel = None

        # Note that when adding columns, the text/pizbuf/etc attributes are an
        # index into the tree model list. Attributes names match the available
        # properties of the class.

        # The icon representing the kind of item
        col_icon = Gtk.TreeViewColumn('Type', Gtk.CellRendererPixbuf(),
                pixbuf=KeeperTreeView.COL_PIXBUF)
        col_icon.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_icon.set_resizable(False)
        col_icon.set_reorderable(False)
        self._treeview.append_column(col_icon)

        # A hidden type column
        col_type = Gtk.TreeViewColumn('Type', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_TYPE)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        col_type.set_visible(False)
        self._treeview.append_column(col_type)

        # A hidden id column
        col_type = Gtk.TreeViewColumn('ID', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_ID)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        col_type.set_visible(False)
        self._treeview.append_column(col_type)

        # A hidden initial expansion column
        col_type = Gtk.TreeViewColumn('INIT_EXPAND', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_INIT_EXPAND)
        col_type.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_type.set_resizable(False)
        col_type.set_reorderable(False)
        col_type.set_visible(False)
        self._treeview.append_column(col_type)

        # The title of the item
        title_cell = Gtk.CellRendererText()
        title_cell.set_property("editable", True)
        title_cell.connect("edited", self._on_name_changed)
        col_title = Gtk.TreeViewColumn('Name', title_cell,
                text=KeeperTreeView.COL_NAME)
        col_title.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_title.set_resizable(True)
        col_title.set_reorderable(False)
        self._treeview.append_column(col_title)

        # Add checkbox column for including in compiles
        toggle_renderer = Gtk.CellRendererToggle()
        col_include = Gtk.TreeViewColumn('Inc', toggle_renderer,
                active=KeeperTreeView.COL_COMPILE)
        col_include.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_include.set_resizable(False)
        col_include.set_reorderable(False)
        toggle_renderer.connect("toggled", self._on_compile_cell_toggled)
        self._treeview.append_column(col_include)

        # Number of scenes in an item
        col_scenes = Gtk.TreeViewColumn('Scenes', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_SCENES)
        col_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_scenes.set_resizable(True)
        col_scenes.set_reorderable(False)
        self._treeview.append_column(col_scenes)

        # Running count of the number of scenes in the project
        col_running_scenes = Gtk.TreeViewColumn('Running',
                Gtk.CellRendererText(), text=KeeperTreeView.COL_SCENES_RUNNING)
        col_running_scenes.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_scenes.set_resizable(True)
        col_running_scenes.set_reorderable(False)
        self._treeview.append_column(col_running_scenes)

        # The number of words in the item
        col_words = Gtk.TreeViewColumn('Words', Gtk.CellRendererText(),
                text=KeeperTreeView.COL_WORDS)
        col_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_words.set_resizable(True)
        col_words.set_reorderable(False)
        self._treeview.append_column(col_words)

        # Running count of the number of words in the project
        col_running_words = Gtk.TreeViewColumn('Running',
                Gtk.CellRendererText(), text=KeeperTreeView.COL_WORDS_RUNNING)
        col_running_words.set_sizing(Gtk.TreeViewColumnSizing.AUTOSIZE)
        col_running_words.set_resizable(True)
        col_running_words.set_reorderable(False)
        self._treeview.append_column(col_running_words)

        # Connect signals
        select = self._treeview.get_selection()
        select.connect("changed", self._on_tree_selection_changed)

        self._treeview.connect("drag-begin", self._on_row_started_move)
        self._treeview.connect("drag-end", self._on_row_moved)
        self._treeview.connect("button-press-event", self._on_button_pressed)
        self._treeview.connect("row-activated", self._on_row_activated)

        # A popover menu for right clicks in treeview
        self._popup = KeeperPopupMenu()
        self._popup.connect_add(self.on_add_file, self.on_add_directory)
        self._popup.connect_delete(self.on_delete)
        self._popup.connect_delete_all(self.on_delete_all)
        self._popup.connect_edit(self.on_edit_file)

        # Set labels
        self._label_status1.set_label("Words: 0")
        self._label_status2.set_label("Scenes: 0")
        self._label_status3.set_label("Avg Words/File: 0")

        self.sanity_check_editor()

        self.enable_items()

    def sanity_check_editor(self):
        # Sanity check the editor
        p = Path(self._project.editor())
        if self._project.is_loaded() and not p.exists():
            m = Message()
            m.info(self._app_window, 'No editor', 'It seems that the %s editor'
                    ' does not exist on your system. To choose a new editor,'
                    ' please select Project->Preferences...\n' %
                    self._project.editor())
            return False

        return True

    def enable_items(self):
        l = self._project.is_loaded()
        (model, tree_iter) = self._treeview.get_selection().get_selected()
        item_type = None
        if model is not None and tree_iter is not None:
            item_type = model[tree_iter][KeeperTreeView.COL_TYPE]

        self._treeview.set_sensitive(l)
        self._text_view_notes.set_sensitive(l)
        self._builder.get_object('buttonExpandAll').set_sensitive(l)
        self._builder.get_object('buttonCollapseAll').set_sensitive(l)
        self._builder.get_object('buttonUpdateCounts').set_sensitive(l)

        # Menus
        self._builder.get_object('menuAddFile').set_sensitive(l)
        self._builder.get_object('menuAddFileAtRoot').set_sensitive(l)
        self._builder.get_object('menuAddDirectoryAtRoot').set_sensitive(l)
        self._builder.get_object('menuCompile').set_sensitive(l)
        self._builder.get_object('menuBackup').set_sensitive(l)
        self._builder.get_object('menuRefresh').set_sensitive(l)
        self._builder.get_object('menuPreferences').set_sensitive(l)

        b = (l and (item_type == 'directory' or item_type == None))
        self._builder.get_object('menuAddDirectory').set_sensitive(b)
        b = (l and item_type == 'file')
        self._builder.get_object('menuEdit').set_sensitive(b)
        b = (l and item_type != None)
        self._builder.get_object('menuDelete').set_sensitive(b)

    def refresh(self):
        if not self._project.is_loaded():
            return

        (is_ok, reason) = self._tree_model.load_tree_store(self._project.project_path())
        if not is_ok:
            m = Message()
            m.error(self._app_window, 'Keeper error', 'Could not refresh '
                    'Keeper:\n\n%s' % reason)
            sys.exit(1)
            return

        # Set treestore
        self._treeview.set_model(self._tree_model.get_tree_store())
        self._treeview.set_cursor(0)
        self._last_sel = self._treeview.get_selection().get_selected()
        self.update_word_counts()

        if self._project.backup_on_start():
            dt = datetime.now()
            ts = dt.strftime('%Y%m%d_%H%M%S')
            p = Path(self._project.backup_path())
            filename = '%s-%s%s' % (self._project.name(), ts, '.zip')
            p = p / filename
            self.backup(str(p))

        # Do auto expansion of rows
        store = self._tree_model.get_tree_store()
        tree_iter = store.get_iter_first()
        self._auto_expand(store, tree_iter)

    def _auto_expand(self, store, tree_iter):
        while tree_iter is not None:
            expanded = store[tree_iter][KeeperTreeView.COL_INIT_EXPAND]
            if expanded:
                path = store.get_path(tree_iter)
                self._treeview.expand_row(path, False)

            if store.iter_has_child(tree_iter):
                self._auto_expand(store, store.iter_children(tree_iter))

            tree_iter = store.iter_next(tree_iter)

    def add_item(self, name, item_type, item_id, as_child):
        (model, tree_iter) = self._treeview.get_selection().get_selected()
        self._tree_model.insert_at(tree_iter, name, item_type, item_id,
                as_child)
        self.save()

    def remove_item(self, tree_iter):
        self._tree_model.remove(tree_iter)
        self.save()

    def iter_to_project_path(self, tree_iter):
        item_id = self._tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_ID]
        item_name = self._tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_NAME]
        return ("%s/%s" % (self._project.keeper_path(),
            self._file_name(item_name, item_id)))

    def iter_to_notes_path(self, tree_iter):
        item_id = self._tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_ID]
        item_name = self._tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_NAME]
        return ("%s/%s" % (self._project.notes_path(),
            self._file_name(item_name, item_id)))

    def _tree_to_yaml(self, store, tree_iter, indent, out_str=""):
        while tree_iter is not None:
            item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
            item_id = store[tree_iter][KeeperTreeView.COL_ID]
            item_title = store[tree_iter][KeeperTreeView.COL_NAME]
            item_compile = store[tree_iter][KeeperTreeView.COL_COMPILE]

            out_str = out_str + "%s- type: '%s'\n" % (indent, item_type)
            out_str = out_str + "%s  title: '%s'\n" % (indent, item_title)
            out_str = out_str + "%s  id: '%s'\n" % (indent, item_id)
            out_str = out_str + '%s  compile: %s\n' % (indent, item_compile)
            if store.iter_has_child(tree_iter):
                out_str = out_str + '%s  expanded: %s\n' % (indent,
                        self._treeview.row_expanded(store.get_path(tree_iter)))
                out_str = out_str + '%s  contents:\n' % indent
                child_iter = store.iter_children(tree_iter)
                out_str = self._tree_to_yaml(store, child_iter, indent + "  ", out_str)
            elif item_type == 'directory':
                out_str = out_str + '%s  contents: []\n' % indent

            tree_iter = store.iter_next(tree_iter)

        return out_str

    def _project_settings_to_yaml(self):
        yaml = "  editor: '%s'\n" % self._project.editor()
        yaml = "%s  editorArgs: '%s'\n" % (yaml, self._project.editor_args())
        yaml = "%s  backupPath: '%s'\n" % (yaml, self._project.backup_path())
        yaml = "%s  backupOnStart: %s\n" % (yaml, self._project.backup_on_start())
        yaml = "%s  includeTitlesCompile: %s\n" % (yaml, self._project.include_titles())
        yaml = "%s  includeDirectoryTitlesCompile: %s\n" % (yaml,
                self._project.include_directory_titles())
        yaml = "%s  includeTextCompile: %s\n" % (yaml, self._project.include_text())
        yaml = "%s  includeTextEntryCompile: '%s'\n" % (yaml,
                self._project.include_text_entry())
        yaml = "%s  skipFirst: %s\n" % (yaml, self._project.skip_first())
        yaml = "%s  appWindow:\n" % yaml
        yaml = "%s    width: %d\n" % (yaml, self._project.app_window_state.w)
        yaml = "%s    height: %d\n" % (yaml, self._project.app_window_state.h)
        yaml = "%s    pane: %d\n" % (yaml, self._project.app_window_state.pane)
        yaml = "%s    maximized: %s\n" % (yaml, self._project.app_window_state.maximized)
        yaml = "%s    fullscreen: %s\n" % (yaml, self._project.app_window_state.fullscreen)
        return yaml

    def save(self):
        if self._project.is_loaded():
            self._save_last_sel()
            store = self._tree_model.get_tree_store()
            tree_iter = store.get_iter_first()
            keeper_yaml = self._tree_to_yaml(store, tree_iter, "  ")
            keeper_str = ("project:\n%s\nkeeper:\n%s\n" %
                    (self._project_settings_to_yaml(), keeper_yaml))
            with open(self._project.keeper_yaml(), "w") as f:
                f.write(keeper_str)

    def _update_word_count_tree(self, store, tree_iter, words_running, scenes_running, files_running):
        while tree_iter is not None:
            item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
            item_name = store[tree_iter][KeeperTreeView.COL_NAME]
            item_id = store[tree_iter][KeeperTreeView.COL_ID]
            item_compile = store[tree_iter][KeeperTreeView.COL_COMPILE]

            if item_type == 'file':
                files_running += 1
                path = Path("%s/keeper/%s" % (self._project.project_path(),
                    self._file_name(item_name, item_id)))
                (rv, reason, words) = word_count(str(path))
                if not rv:
                    print("WARNING: internal error in word count: %s " % reason)

                if item_compile:
                    words_running += words

                store[tree_iter][KeeperTreeView.COL_WORDS] = int(words)
                store[tree_iter][KeeperTreeView.COL_WORDS_RUNNING] = int(words_running)

                (rv, reason, scenes) = scene_count(str(path))
                if not rv:
                    print("WARNING: internal error in scene count: %s " % reason)

                if item_compile:
                    scenes_running += scenes

                store[tree_iter][KeeperTreeView.COL_SCENES] = int(scenes)
                store[tree_iter][KeeperTreeView.COL_SCENES_RUNNING] = int(scenes_running)

            elif item_type == 'directory' or store.iter_has_child(tree_iter):
                child_iter = store.iter_children(tree_iter)
                (dir_words, dir_scenes, dir_files) = self._update_word_count_tree(store,
                        child_iter, 0, 0, 0)
                if item_compile:
                    words_running += dir_words
                    scenes_running += dir_scenes
                    files_running += dir_files
                store[tree_iter][KeeperTreeView.COL_WORDS] = int(dir_words)
                store[tree_iter][KeeperTreeView.COL_WORDS_RUNNING] = int(words_running)
                store[tree_iter][KeeperTreeView.COL_SCENES] = int(dir_scenes)
                store[tree_iter][KeeperTreeView.COL_SCENES_RUNNING] = int(scenes_running)

            tree_iter = store.iter_next(tree_iter)

        return (words_running, scenes_running, files_running)

    def update_word_counts(self):
        if self._project.is_loaded():
            store = self._tree_model.get_tree_store()
            tree_iter = store.get_iter_first()
            (total_words, total_scenes, total_files) = self._update_word_count_tree(store, tree_iter, 0, 0, 0)
            self._label_status1.set_label("Words: %d" % total_words)
            self._label_status2.set_label("Scenes: %d" % total_scenes)
            avg = 0
            if total_files > 0:
                avg = int(total_words/total_files)
            self._label_status3.set_label("Avg Words/File: %d" % avg)

    def expand_all(self):
        self._treeview.expand_all()

    def collapse_all(self):
        self._treeview.collapse_all()

    def _do_compile(self, store, tree_iter, out_str):
        first = self._project.skip_first()
        while tree_iter is not None:
            item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
            item_name = store[tree_iter][KeeperTreeView.COL_NAME]
            item_id = store[tree_iter][KeeperTreeView.COL_ID]
            item_compile = store[tree_iter][KeeperTreeView.COL_COMPILE]
            heading_level = self._num_parents(store, tree_iter, 1)

            if item_compile:
                path = Path("%s/keeper/%s" % (self._project.project_path(),
                self._file_name(item_name, item_id)))
                if path.exists():
                    with open(str(path), "r") as f:
                        f_contents = f.read().strip()

                    title = ''
                    if self._project.include_titles():
                        title = '%s %s\n\n' % ('#'*heading_level, item_name)

                    text = ''
                    if not first and self._project.include_text():
                        text = '%s\n\n' % self._project.include_text_entry()

                    out_str = "%s%s%s%s\n\n" % (out_str, title, text, f_contents)

                if store.iter_has_child(tree_iter):
                    child_iter = store.iter_children(tree_iter)
                    title = ''
                    if self._project.include_directory_titles():
                        title = '%s %s\n\n' % ('#'*heading_level, item_name)
                    out_str = "%s%s" % (out_str, title)
                    child_out_str = self._do_compile(store, child_iter, '')
                    out_str = "%s%s" % (out_str, child_out_str)

            first = False
            tree_iter = store.iter_next(tree_iter)

        return out_str

    def compile(self, path):
        store = self._tree_model.get_tree_store()
        tree_iter = store.get_iter_first()
        m = Message()

        p = Path(path)
        go_ahead = True
        if p.exists():
            rv = m.confirm(self._app_window, "Replace?", "%s exists. Replace it?" % path)
            go_head = (rv == Gtk.ResponseType.YES)

        if go_ahead:
            out_str = self._do_compile(store, tree_iter, "")
            with open(path, "w") as f:
                f.write(out_str)
            m.info(self._app_window, "File created", "%s created." % path)

    def backup(self, path):
        p = PurePath(self._project.project_path())
        old_dir = os.getcwd()
        os.chdir(str(p.parent))
        result = subprocess.run(['zip', '-r', path, self._project.name()])
        m = Message()
        if result.returncode != 0:
            m.error(self._app_window, 'Error creating backup', result.stderr)
        else:
            m.info(self._app_window, 'Backup created', '%s created successfully' % path)
        os.chdir(old_dir)

    ###
    ##
    ## Helper functions
    ##
    ###
    def clear_all(self):
        self._tree_model.clear()

    def _set_compile_cells(self, store, tree_iter, new_value):
        while tree_iter is not None:
            store[tree_iter][KeeperTreeView.COL_COMPILE] = new_value
            if store.iter_has_child(tree_iter):
                child_iter = store.iter_children(tree_iter)
                self._set_compile_cells(store, child_iter, new_value)
            tree_iter = store.iter_next(tree_iter)

        self.update_word_counts()

    def _strip_name(self, name):
        name = name.strip()
        name = re.sub('[^0-9a-zA-Z]+', '', name.lower())
        return name

    def _file_name(self, item_name, item_id):
        return "%s-%s.md" % (self._strip_name(item_name), item_id)

    def _save_notes(self, store, tree_iter):
        if tree_iter is not None:
            item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
            text_view_buffer = self._text_view_notes.get_buffer()
            item_id = store[tree_iter][KeeperTreeView.COL_ID]
            item_name = store[tree_iter][KeeperTreeView.COL_NAME]
            if item_name is None:
                return
            path = Path("%s/notes/%s" % (self._project.project_path(),
                self._file_name(item_name, item_id)))
            start_iter = text_view_buffer.get_start_iter()
            end_iter = text_view_buffer.get_end_iter()
            with open(str(path), "w") as f:
                f.write(text_view_buffer.get_text(start_iter, end_iter, True))

    def _save_last_sel(self):
        if self._last_sel is not None:
            (store, tree_iter) = self._last_sel
            self._save_notes(store, tree_iter)

    def _show_notes(self, store, tree_iter):
        item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
        text_view_buffer = self._text_view_notes.get_buffer()
        item_id = store[tree_iter][KeeperTreeView.COL_ID]
        item_name = store[tree_iter][KeeperTreeView.COL_NAME]
        path = Path("%s/notes/%s" % (self._project.project_path(),
            self._file_name(item_name, item_id)))
        with open(str(path), "r") as f:
            text_view_buffer.set_text(f.read())

    def _do_edit_selected(self):
        if not self.sanity_check_editor():
            return
        selection = self._treeview.get_selection()
        (model, tree_iter) = selection.get_selected()
        item_id = model[tree_iter][KeeperTreeView.COL_ID]
        item_name = model[tree_iter][KeeperTreeView.COL_NAME]
        path = Path("%s/keeper/%s" % (self._project.project_path(),
            self._file_name(item_name, item_id)))
        if self._project.editor_args() != '':
            popen_list = [self._project.editor()]
            for arg in self._project.editor_args().split():
                popen_list.append(arg)
            popen_list.append(path)
            subprocess.Popen(popen_list)
        else:
            subprocess.Popen([self._project.editor(), path])

    def _num_parents(self, store, tree_iter, n):
        if store.iter_parent(tree_iter) == None:
            return n
        return self._num_parents(store, store.iter_parent(tree_iter), n+1)

    ###
    ##
    ## Signal handler functions
    ##
    ###
    def _on_name_changed(self, cell_renderer_text, path, new_name):
        store = self._tree_model.get_tree_store()
        old_name = store[path][KeeperTreeView.COL_NAME]
        item_id = store[path][KeeperTreeView.COL_ID]
        item_type = store[path][KeeperTreeView.COL_TYPE]
        store[path][KeeperTreeView.COL_NAME] = str(new_name)
        p_proj = Path(self._project.project_path())

        # Update keeper file if a file
        if item_type == 'file':
            p_src = p_proj / 'keeper' / self._file_name(old_name, item_id)
            p_dst = p_proj / 'keeper' / self._file_name(new_name, item_id)

            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.move(str(p_src), str(p_dst))
            if not rv:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Unable to update'
                        ' keeper files:\n\n%s' % reason)

        # Update notes file
        p_src = p_proj / 'notes' / self._file_name(old_name, item_id)
        p_dst = p_proj / 'notes' / self._file_name(new_name, item_id)

        fops = KeeperFileOpsLinux()
        (rv, reason) = fops.move(str(p_src), str(p_dst))
        if not rv:
            m = Message()
            m.error(self._app_window, 'Keeper error', 'Unable to update'
                    ' keeper files:\n\n%s' % reason)

    def _on_tree_selection_changed(self, selection):
        self._save_last_sel()
        self.enable_items()
        (store, tree_iter) = selection.get_selected()

        if tree_iter is not None:
            self._show_notes(store, tree_iter)
            self._last_sel = selection.get_selected()
            self._text_view_notes.set_sensitive(True)
        else:
            text_view_buffer = self._text_view_notes.get_buffer()
            text_view_buffer.set_text('')
            self._last_sel = None
            self._text_view_notes.set_sensitive(False)

    def _on_compile_cell_toggled(self, widget, path):
        store = self._tree_model.get_tree_store()
        new_value = not store[path][KeeperTreeView.COL_COMPILE]

        # Now this item and all children should be set to new value
        store[path][KeeperTreeView.COL_COMPILE] = new_value
        tree_iter = store.get_iter(path)
        self._set_compile_cells(store, store.iter_children(tree_iter), new_value)

    def _on_row_started_move(self, widget, context):
        self._save_last_sel()

    def _on_row_moved(self, widget, context):
        self.update_word_counts()
        self.save()

    def _on_button_pressed(self, widget, event):
        # right click
        if event.button == 3 and self._project.is_loaded():
            info = self._treeview.get_path_at_pos(event.x, event.y)
            if info != None:
                (path, col, cell_x, cell_y) = info
                self._treeview.grab_focus()
                self._treeview.set_cursor(path, col, 0)

                selection = self._treeview.get_selection()
                (model, tree_iter) = selection.get_selected()
                item_type = model[tree_iter][KeeperTreeView.COL_TYPE]
                has_children = model.iter_has_child(tree_iter)

                menu = self._popup.get_menu_for_type(item_type, has_children)
                menu.show_all()
                menu.popup_at_pointer(event)
            else:
                select = self._treeview.get_selection().unselect_all()
                menu = self._popup.get_menu_for_type(None, False)
                menu.show_all()
                menu.popup_at_pointer(event)
        elif event.button == 1:
            info = self._treeview.get_path_at_pos(event.x, event.y)
            selection = self._treeview.get_selection()
            if info == None:
                self._save_last_sel()
                self._treeview.get_selection().unselect_all()
                self._last_sel = None
                self.update_word_counts()

    # These are not private because our App uses them to handle the
    # app menu signals
    def on_add_file(self, *args):
        aid = AddItemDialog(self._builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%m%d_%H%M%S')
            selection = self._treeview.get_selection()
            (model, tree_iter) = selection.get_selected()
            (rv, reason) = self._project.write_new_file(name, self._file_name(name,
                item_id))
            (rv, reason) = self._project.write_new_note(name, self._file_name(name,
                item_id))
            if rv:
                self.add_item(name, 'file', item_id, True)
            else:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not add'
                        'file:\n\n%s' % reason)

            self.update_word_counts()

    def on_add_file_at_root(self, *args):
        aid = AddItemDialog(self._builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%m%d_%H%M%S')
            (rv, reason) = self._project.write_new_file(name, self._file_name(name,
                item_id))
            (rv, reason) = self._project.write_new_note(name, self._file_name(name,
                item_id))
            if rv:
                self._tree_model.insert_at(None, name, 'file', item_id, False)
                self.save()
            else:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not add'
                        'file:\n\n%s' % reason)

            self.update_word_counts()

    def on_add_directory(self, *args):
        aid = AddItemDialog(self._builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%m%d_%H%M%S')
            selection = self._treeview.get_selection()
            (model, tree_iter) = selection.get_selected()
            (rv, reason) = self._project.write_new_note(name,
                    self._file_name(name, item_id))
            if rv:
                self.add_item(name, 'directory', item_id, True)
            else:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not add'
                        'directory note:\n\n%s' % reason)

    def on_add_directory_at_root(self, *args):
        aid = AddItemDialog(self._builder)
        (response, name) = aid.run()
        if response == Gtk.ResponseType.OK:
            dt = datetime.now()
            item_id = dt.strftime('%Y%m%d_%H%M%S')
            (rv, reason) = self._project.write_new_note(name,
                    self._file_name(name, item_id))
            if rv:
                self._tree_model.insert_at(None, name, 'directory', item_id, False)
                self.save()
            else:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not add'
                        'directory note:\n\n%s' % reason)

    def _on_row_activated(self, tree_view, path, column):
        store = self._tree_model.get_tree_store()
        if store[path][KeeperTreeView.COL_TYPE] == 'file':
            self._do_edit_selected()

    def on_edit_file(self, *args):
        self._do_edit_selected()

    def _delete_self_and_child_files(self, tree_iter):
        store = self._tree_model.get_tree_store()
        item_type = store[tree_iter][KeeperTreeView.COL_TYPE]
        if item_type == 'file':
            path = self.iter_to_project_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))
            path = self.iter_to_notes_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))
        elif item_type == 'directory':
            path = self.iter_to_notes_path(tree_iter)
            fops = KeeperFileOpsLinux()
            (rv, reason) = fops.delete(path)
            if not rv:
                m = Message()
                m.error(self._app_window, 'Keeper error', 'Could not delete'
                        ' %s:\n%s\n' % (path, reason))

        if store.iter_has_child(tree_iter):
            child_iter = store.iter_children(tree_iter)
            while child_iter is not None:
                self._delete_self_and_child_files(child_iter)
                child_iter = store.iter_next(child_iter)

    def _delete_child_files(self, tree_iter):
        store = self._tree_model.get_tree_store()
        if store.iter_has_child(tree_iter):
            child_iter = store.iter_children(tree_iter)
            while child_iter is not None:
                self._delete_self_and_child_files(child_iter)
                child_iter = store.iter_next(child_iter)

    def on_delete(self, *args):
        selection = self._treeview.get_selection()
        (model, tree_iter) = selection.get_selected()
        self._last_sel = None
        if tree_iter is not None:
            path = self.iter_to_project_path(tree_iter)
            item_name = self._tree_model.get_tree_store()[tree_iter][KeeperTreeView.COL_NAME]
            m = Message()
            if m.confirm(self._app_window, 'Confirm', 'Are you sure you want '
                    'to permenantly delete %s?' % item_name):
                self._delete_self_and_child_files(tree_iter)
                self.remove_item(tree_iter)
        else:
            m = Message()
            m.error(self._app_window, 'Keeper error', 'Nothing to delete.'
                    ' Please report.')

        self.update_word_counts()

    def on_delete_all(self, *args):
        selection = self._treeview.get_selection()
        (model, tree_iter) = selection.get_selected()
        self._last_sel = None
        if tree_iter is not None:
            path = self.iter_to_project_path(tree_iter)
            item_name = model[tree_iter][KeeperTreeView.COL_NAME]
            m = Message()
            if m.confirm(self._app_window, 'Confirm', 'Are you sure you want '
                    'to permenantly delete everything in %s?' % item_name):
                self._delete_child_files(tree_iter)
                paths = []
                child_iter = model.iter_children(tree_iter)
                while child_iter is not None:
                    paths.append(model.get_path(child_iter))
                    child_iter = model.iter_next(child_iter)

                for p in reversed(paths):
                    itr = model.get_iter(p)
                    model.remove(itr)
        else:
            m = Message()
            m.error(self._app_window, 'Keeper error', 'Nothing to delete.'
                    ' Please report.')

        self.update_word_counts()

