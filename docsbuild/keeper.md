# Keeper

## Introduction

The Keeper (short for Trapper Keeper, like the old notebooks some of us used in the 80's) is a tree-like view of all the files and folders that make up your writing project. Just how you use it is up to you, but the concepts are similar to those you are already familiar with:

1. Files represent text.
2. Folders hold text files.
3. A 'trashcan' holds files you may or may not want to eventually delete.

## The view

The Keeper presents your project's files and folders in rows. Draftman2 projects are linear. If you imagine a Draftman2 project as a single text file, items at the top of the view would appear at the top of the file and items at the bottom would appear at the end of the file.

### Columns

#### Type

An icon designates what type of object the row represents:

1. A file icon represents a text file in your project. (Files can contain other files -- see Advanced/Project Structure for more information.)
2. A folder icon represents a folder in your project. Folders contain files and other folders.
3. A trashcan icon is created whenever you create a new folder with the name "Trash." Trash folders can only be deleted by copying them into another Trash folder and emptying with a right click. You can permanently delete items in a Trash folder by right-clicking them and confirming.

#### Name

The name of the file or folder. Double-click in the name to rename a file.

#### Inc

The *Inc* check boxes indicate that the file or folder should be included when you Compile a Draftman2 project. See the [Compiling a Project](#compiling-a-project) section for more information about compiling a project to a single file.

#### Scenes/Running

Scenes tells you how many 'scenes' are in a file or a folder represented by that row. Scenes, in Draftman2 parlance, indicate either a count of Markdown headers in a text file (i.e. lines beginning with `#`) or the file itself as a single scene. Because you might not use headers in a file, a file that contains no headers is counted as having one scene, even empty files. See the [Project Organization](#project-organization) section for more information.

The scene count next to a folder indicates the total number of scenes found within the folder. If you have a folder that contains five files with one scene per file, Scenes would be 5 at the folder row. If you open the folder, each file would show 1 scene at its row.

The Running column next to the Scenes column indicates how many *total* scenes that have been found *as of and including that row* for all included (*Inc* is checked) items above.

#### Words/Running

The Words and associated Running column are identical to the Scenes/Running columns, except they count words instead of scenes.

Similar to scenes, only included (*Inc* is checked) files are counted as part of a total count.

## Rows

You can take specific action on rows by selecting them and right-clicking. Further, you can reorder rows by clicking and dragging.

You can de-select all rows by clicking in white space below all rows. This also refreshes the scene and word counts.

## Status

Below the rows, there are several status items and a couple of buttons:

### Words

The total words of all included objects in your project.

### Scenes

The total number of included scenes in your project

### Avg words/file

The average number of words per included file in your project. This can be used to predict your project's overall length if you have an idea of how many scenes your project will contain.

### Update counts

After editing a file outside of Draftman2, click Update counts to update the number of words and scenes in the Keeper.

### Expand all

Click Expand all to open all folders in the Keeper

### Collapse all

Click Collapse all to close all folders in the Keeper
