# Project

## Add file...

Add a file underneath the selected row.

## Add folder...

Add a folder underneath the selected row.

## Add file at root...

Add a new file to the project root.

## Add folder at root...

Add a new folder to the project root.

## Edit...

Edit the currently selected file using the editor defined in *Project->Preferences...*

## Delete...

Delete the files associated with the selected row. Note that the delete is recursive, so deleting a folder will also delete everything inside the folder.

## Compile...

Produces a single Markup file containing all the files marked for inclusion in the chosen oirectory.

## Create backup

Generates a zip archive of the project directory and puts it in the backups directory defined in *Project->Preferences...*

## Refresh file list/word counts

Recalculates the word and scene counts in the Keeper.

## Preferences...

### Application

Select the application Draftman2 should launch when you want to edit a file. The application must take at least one argument: the name of the file to edit.

### Arguments

Any additional arguments required to launch the editor successfully. For example, to support a gvim writing configuration, you might choose something like the following as an argument to `gvim`:

```
-u /home/mylogin/.vimrc_for_writing_only
```

### Include folder titles

Draftman2 will output the titles of folders using an appropriate heading level. For example, if a folder named 'My folder' is contained within a folder at the root folder, Draftman would output:

```
## My folder
```

### Include file titles

Similar to folder titles, Draftman2 will output file titles, using a heading level determined by the number of parent folders. 

### Include text with files

Draftman2 will place the provided arbitrary text at the top of every included file in the compilation.

This is useful if you like to use scene separators like `* * *` or `~~~`.

If you do not want to include the text after a heading, click the 'And skip first' checkbox. Then you'll end up with:

```
# Some heading

Some text.
```

Instead of:

```
# Some heading

* * *

Some text.
```

### Backup automatically upon startup

Draftman2 will create a backup of your currently loaded project in the directory specified (see next item).

### Directory

The directory to store your Draftman2 backups. This defaults to the project directory itself when the project is created.

