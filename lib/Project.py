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

class Project:
    def __validate_project(self, path):
        p = Path(path)
        if not p.exists() or not p.is_dir():
            return (False, "%s either doesn't exist or isn't a directory." % path)

        # Now, we look for all the items we expect to find in a draftman2
        # project.
        must_haves = ['draft.txt', 'draft', 'notes.md', 'trash']
        for item in must_haves:
            q = p / item
            if not q.exists():
                return (False, "%s doesn't exist." % item)

        return (True, "OK")

    def __init__(self):
        self.name = ""
        self.project_path = ""
        self.notes_path= ""
        self.draft_path = ""
        self.draft_master = ""
        self.backups_path = ""
        self.is_loaded = False

    def __str__(self):
        return ("name=%s\nproject=%s\nnotes=%s\ndraft=%s\n"
                "draftmaster=%s\nbackups=%s\n" % (self.name, self.project_path,
                    self.notes_path, self.draft_path, self.draft_master,
                    self.backups_path))

    def open(self, path):
        (rv, reason) = self.__validate_project(path)
        if not rv:
            return (rv, reason)

        p = PurePath(path)
        self.name = p.name
        self.project_path = p
        self.notes_path = p / 'notes.md'
        self.draft_path = p / 'draft'
        self.draft_master = p / 'draft.txt'
        self.backups_path = p
        self.is_loaded = True

        print(str(self))

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
            proj_piece = project_dir / 'draft'
            proj_piece.mkdir()
            proj_piece = project_dir / 'trash'
            proj_piece.mkdir()

            proj_piece = project_dir / 'draft.txt'
            with open(str(proj_piece), "w") as f:
                f.write("% THIS IS A DRAFTMAN2 PROJECT FILE. IT CONTAINS THE\n"
                    "% INTERNAL DRAFT DATABASE. YOU MAY EDIT THIS FILE WHEN\n"
                    "% DRAFTMAN2 IS NOT RUNNING. OTHERWISE YOUR CHANGES MAY\n"
                    "% BE OVERWRITTEN.\n")

            proj_piece = project_dir / 'notes.md'
            with open(str(proj_piece), "w") as f:
                f.write("# %s notes\n" % name)
                f.write("\nHappy writing.\n")

            return (True, "OK")
        except Exception as e:
            return (False, "Something went wrong creating %s:\n%s" % (str(project_dir), str(e)))

    def choose_new_project(self, builder):
        app_window = builder.get_object('appWindow')
        entry_project_name = builder.get_object('entryProjectName')
        dialog = builder.get_object('fileChooserProjectDirectory')
        dialog.set_default_size(800, 400)
        dialog.set_transient_for(app_window)
        dialog.set_modal(True)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            (rv, reason) = self.new(dialog.get_filename(), entry_project_name.get_text())
            if not rv:
                m = Message()
                m.warning(app_window, "Unable to create project", reason)

        dialog.destroy()

        return "OK"

    def choose_project_directory(self, app_window):
        dialog = Gtk.FileChooserDialog(
                "Select project directory", app_window,
            Gtk.FileChooserAction.SELECT_FOLDER,
            (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
             "Select", Gtk.ResponseType.OK))
        dialog.set_default_size(800, 400)

        response = dialog.run()
        rv = ""
        if response == Gtk.ResponseType.OK:
            rv = dialog.get_filename()

        dialog.destroy()

        return rv

