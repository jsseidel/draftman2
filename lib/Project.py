"""
Project

This class represents a draftman2 project and maintains state about the project
for the lifetime of the running draftman2 instance.
"""

from pathlib import Path

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
        self.backups_path = ""
        self.is_loaded = False

    def open(self, path):
        p = Path(path)
        (rv, reason) = self.__validate_project(path)
        if not rv:
            return (rv, reason)

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
        except:
            return (False, "Something went wrong creating %s." % str(project_dir))

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
        except:
            return (False, "Something went wrong creating %s." % str(project_dir))

