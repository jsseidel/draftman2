"""
Project

This class represents a draftman2 project and maintains state about the project
for the lifetime of the running draftman2 instance.
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from pathlib import Path, PurePath
from lib.Message import Message
import sys

DEFAULT_NEW_PROJECT="""project:
keeper:
  - type: 'trash'
    path: 'trash'
    title: 'Trash'
    compile: False
    contents: []
"""

class Project:
    def __init__(self):
        self.name = ""
        self.project_path = ""
        self.keeper_path = ""
        self.keeper_yaml = ""
        self.backups_path = ""
        self.is_loaded = False

    def __validate_project(self, path):
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return (False, "%s either doesn't exist or isn't a directory." %
                    path)

        # Now, we look for all the items we expect to find in a draftman2
        # project (which isn't much).
        must_haves = ['keeper.yaml', 'keeper']
        for item in must_haves:
            q = p / item
            if not q.exists():
                return (False, "%s doesn't exist." % item)

        return (True, "OK")

    def __str__(self):
        return ("name=%s\nproject=%s\nkeeper=%s\n"
                "keeper_yaml=%s\nbackups=%s\n" % (self.name, self.project_path,
                    self.keeper_path, self.keeper_yaml, self.backups_path))

    def open(self, path):
        (rv, reason) = self.__validate_project(path)
        if not rv:
            return (rv, reason)

        p = PurePath(path)
        self.name = p.name
        self.project_path = p
        self.keeper_path = p / 'keeper'
        self.keeper_yaml = p / 'keeper.yaml'
        self.backups_path = p
        self.is_loaded = True

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

            proj_piece = project_dir / 'keeper' / 'Trash'
            proj_piece.mkdir()

            proj_piece = project_dir / 'keeper.yaml'
            with open(str(proj_piece), "w") as f:
                f.write(DEFAULT_NEW_PROJECT)

            p = PurePath(project_dir)
            self.name = p.name
            self.project_path = p
            self.keeper_path = p / 'keeper'
            self.keeper_yaml = p / 'keeper.yaml'
            self.backups_path = p
            self.is_loaded = True

            return (True, "OK")
        except Exception as e:
            return (False, "Something went wrong creating %s:\n%s" % (str(project_dir), str(e)))


