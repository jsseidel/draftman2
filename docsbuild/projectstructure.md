# Project Structure

Draftman2 projects have the following structure:

```
Project Directory/
+--keeper
|   +-- <stripped file name 1>-YYYYMMDD_HHMMSS.md
|   +-- <stripped file name 2>-YYYYMMDD_HHMMSS.md
|   +-- <etc>
+--keeper.yaml
+--notes
    +-- <stripped file name 1>-YYYYMMDD_HHMMSS.md
    +-- <stripped file name 2>-YYYYMMDD_HHMMSS.md
    +-- <stripped folder name 1>-YYYYMMDD_HHMMSS.md
    +-- <etc>
    +-- trash-0.md
```

The time stamp is generated only once, when the file is created.

Every Draftman2 file has an associated file in "keeper" and "notes." Folder names are internal, but have an associated file in "notes."

File and folder names are created like this:

```
<lowercase name with punctuation stripped>-<YYYYMMDD_HHMMSS>.md
```

This structure makes all the file names unique, even if they have the same name. 

## `keeper.yaml`

`keeper.yaml` is a YAML file that acts as the project database. It looks like this:

```
project:
  editor: '/usr/bin/gedit'
  editorArgs: ''
  backupPath: '/home/att/backups'
  backupOnStart: False
  includeTitlesCompile: False
  includeDirectoryTitlesCompile: True
  includeTextCompile: False
  includeTextEntryCompile: ''
  skipFirst: False

keeper:
  - type: 'file'
    title: 'My File 1'
    id: '20191204_102120'
    compile: True
  - type: 'directory'
    title: 'My File 1'
    id: '20191204_102120'
    compile: True
    contents:
      - type: 'file'
        title: 'My Sub File 1'
        id: '20191204_102120'
        compile: True
  - type: 'file'
    title: 'My File 1'
    id: '20191204_102120'
    compile: True
     contents:
      - type: 'file'
        title: 'My Sub File 2'
        id: '20191204_102125'
        compile: True
```

Project preferences are stored at the top and the directories and files are stored on the bottom.

