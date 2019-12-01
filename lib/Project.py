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
import re
import sys
import time

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
        self.__name = ""
        self.__project_path = ""
        self.__keeper_path = ""
        self.__keeper_yaml = ""
        self.__backups_path = ""
        self.__is_loaded = False

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


    def is_loaded(self):
        return self.__is_loaded

    def project_path(self):
        return self.__project_path

    def keeper_yaml(self):
        return self.__keeper_yaml

    def keeper_path(self):
        return self.__keeper_path

    def open(self, path):
        (rv, reason) = self.__validate_project(path)
        if not rv:
            return (rv, reason)

        p = PurePath(path)
        self.__name = p.name
        self.__project_path = p
        self.__keeper_path = p / 'keeper'
        self.__keeper_yaml = p / 'keeper.yaml'
        self.__backups_path = p
        self.__is_loaded = True

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
            self.__name = p.name
            self.__project_path = p
            self.__keeper_path = p / 'keeper'
            self.__keeper_yaml = p / 'keeper.yaml'
            self.__backups_path = p
            self.__is_loaded = True

            return (True, "OK")
        except Exception as e:
            return (False, "Something went wrong creating %s:\n%s" % (str(project_dir), str(e)))

    def write_new_file(self, name):
        rv = True
        reason = "OK"
        try:
            p = Path(self.__keeper_path)
            with open(str(p / ("%s" % name)), "w") as f:
                f.write("# %s\n\nHappy writing!\n\n" % name)
        except Exception as e:
            rv = False
            reason = str(e)

        return (rv, reason)

