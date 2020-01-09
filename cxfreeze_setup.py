from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

includes = ['./draftman2.glade',
           ('./icon/draftman2.png', 'icon/draftman2.png'),
           ('./icon/draftman2_sm.png', 'icon/draftman2_sm.png'),
           ('./icon/file.svg', 'icon/file.svg'),
           ('./icon/directory.svg', 'icon/directory.svg'),
           ('./icon/trash.svg', 'icon/trash.svg'),
           ('./Draftman2 Tutorial/', 'Draftman2 Tutorial'),
           './draftman2_run']

buildOptions = dict(packages = ['gi'], include_files = includes, excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('draftman2.py', base=base)
]

setup(name='Draftman2',
      version = '2.0.2',
      description = 'foo',
      options = dict(build_exe = buildOptions),
      executables = executables)
