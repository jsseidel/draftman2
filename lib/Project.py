"""
Project

This class represents a draftman2 project and maintains state about the project
for the lifetime of the running draftman2 instance.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path, PurePath
from lib.AppWindowState import AppWindowState
from lib.Message import Message
import re
import sys
import yaml

DEFAULT_NEW_PROJECT="""project:
keeper:
  - type: 'directory'
    id: '0'
    title: 'Trash'
    compile: False
    contents: []
"""

class Project:
    def __init__(self):
        self._name = ""
        self._project_path = ""
        self._keeper_path = ""
        self._notes_path = ""
        self._keeper_yaml = ""
        self._backup_path = ""
        self._backup_on_start = False
        self._editor = '/usr/bin/gedit'
        self._editor_args = ''
        self._include_titles = False
        self._include_directory_titles = False
        self._is_loaded = False
        self._include_text = False
        self._include_text_entry = ''
        self._skip_first = False
        self.app_window_state = AppWindowState()

    def _validate_project(self, path):
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return (False, "%s either doesn't exist or isn't a directory." %
                    path)

        # Now, we look for all the items we expect to find in a draftman2
        # project (which isn't much).
        must_haves = ['keeper.yaml', 'keeper', 'notes']
        for item in must_haves:
            q = p / item
            if not q.exists():
                return (False, "%s doesn't exist." % item)

        return (True, "OK")

    def _load_prefs(self, path):
        keeper = ""
        with open(("%s/keeper.yaml" % self._project_path), "r") as stream:
            keeper = yaml.safe_load(stream)

        project = keeper['project']
        if project is not None:
            if 'editor' in project:
                self._editor = project['editor']

            if 'editorArgs' in project:
                self._editor_args = project['editorArgs']

            if 'backupPath' in project:
                self._backup_path = project['backupPath']

            if 'backupOnStart' in project:
                self._backup_on_start = project['backupOnStart']

            if 'includeTextCompile' in project:
                self._include_text = project['includeTextCompile']

            if 'includeTextEntryCompile' in project:
                self._include_text_entry = project['includeTextEntryCompile']

            if 'skipFirst' in project:
                self._skip_first = project['skipFirst']

            if 'includeTitlesCompile' in project:
                self._include_titles = project['includeTitlesCompile']

            if 'includeDirectoryTitlesCompile' in project:
                self._include_directory_titles = project['includeDirectoryTitlesCompile']
            if 'appWindow' in project:
                appWindowYaml = project['appWindow']
                self.app_window_state.w = appWindowYaml['width']
                self.app_window_state.h = appWindowYaml['height']
                self.app_window_state.pane = appWindowYaml['pane']
                self.app_window_state.maximized = appWindowYaml['maximized']
                self.app_window_state.fullscreen = appWindowYaml['fullscreen']

    def name(self):
        return self._name

    def is_loaded(self):
        return self._is_loaded

    def project_path(self):
        return self._project_path

    def notes_path(self):
        return self._notes_path

    def keeper_yaml(self):
        return self._keeper_yaml

    def keeper_path(self):
        return self._keeper_path

    def backup_path(self):
        return self._backup_path

    def backup_on_start(self):
        return self._backup_on_start

    def editor(self):
        return self._editor

    def editor_args(self):
        return self._editor_args

    def include_titles(self):
        return self._include_titles

    def include_directory_titles(self):
        return self._include_directory_titles

    def include_text(self):
        return self._include_text

    def include_text_entry(self):
        return self._include_text_entry

    def skip_first(self):
        return self._skip_first

    def set_editor(self, editor):
        self._editor = editor

    def set_editor_args(self, editor_args):
        self._editor_args = editor_args

    def set_backup_path(self, backup_path):
        self._backup_path= backup_path

    def set_backup_on_start(self, backup_on_start):
        self._backup_on_start= backup_on_start

    def set_include_titles(self, include_titles):
        self._include_titles = include_titles

    def set_include_directory_titles(self, include_titles):
        self._include_directory_titles = include_titles

    def set_include_text(self, include_text):
        self._include_text = include_text

    def set_include_text_entry(self, include_text_entry):
        self._include_text_entry = include_text_entry

    def set_skip_first(self, skip_first):
        self._skip_first = skip_first

    def open(self, path):
        (rv, reason) = self._validate_project(path)
        if not rv:
            return (rv, reason)

        p = PurePath(path)
        self._name = p.name
        self._project_path = p
        self._keeper_path = p / 'keeper'
        self._keeper_yaml = p / 'keeper.yaml'
        self._notes_path = p / 'notes'
        self._backup_path = p
        self._backup_on_start = False
        self._editor = '/usr/bin/gedit'
        self._editor_args = ''
        self._is_loaded = True
        self._include_titles = False
        self._include_text = False
        self._include_text_entry = ''
        self._skip_first = False

        self._load_prefs(str(self._keeper_yaml))

        return (True, "OK")

    def new(self, path, name):
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return (False, "Either %s doesn't exist or isn't a directory." % path)

        project_dir = p / name

        # Create a new project directory at path
        try:
            project_dir.mkdir()
        except FileExistsError:
            return (False, "%s already exists." % str(project_dir))
        except Exception as e:
            return (False, "Something went wrong creating %s:\n%s" % (str(project_dir), str(e)))

        # Create the other parts of the project
        try:
            proj_piece = project_dir / 'keeper'
            proj_piece.mkdir()

            proj_piece = project_dir / 'notes'
            proj_piece.mkdir()

            proj_piece = project_dir / 'notes' / 'trash-0.md'
            with open(str(proj_piece), "w") as f:
                f.write("# Trash notes\n\n")

            proj_piece = project_dir / 'keeper.yaml'
            with open(str(proj_piece), "w") as f:
                f.write(DEFAULT_NEW_PROJECT)

            p = PurePath(project_dir)
            self._name = p.name
            self._project_path = p
            self._keeper_path = p / 'keeper'
            self._keeper_yaml = p / 'keeper.yaml'
            self._notes_path = p / 'notes'
            self._backup_path = p
            self._backup_on_start = False
            self._editor = '/usr/bin/gedit'
            self._editor_args = ''
            self._is_loaded = True
            self._include_titles = False
            self._include_directory_titles = False
            self._include_text = False
            self._include_text_entry = ''
            self._skip_first = False

            return (True, "OK")
        except Exception as e:
            return (False, "Something went wrong creating %s:\n%s" % (str(project_dir), str(e)))

    def write_new_file(self, title, file_name):
        rv = True
        reason = "OK"
        try:
            p = Path(self._keeper_path)
            with open(str(p / ("%s" % file_name)), "w") as f:
                f.write("Happy writing!\n\n")
        except Exception as e:
            rv = False
            reason = str(e)

        return (rv, reason)

    def write_new_note(self, title, file_name):
        rv = True
        reason = "OK"
        try:
            p = Path(self._notes_path)
            with open(str(p / ("%s" % file_name)), "w") as f:
                f.write("# %s notes\n\nKeep track of notes here\n\n" % title)
        except Exception as e:
            rv = False
            reason = str(e)

        return (rv, reason)

