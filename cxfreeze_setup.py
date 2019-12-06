from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.

includes = ['./draftman2.glade']

buildOptions = dict(packages = ['gi'], include_files = includes, excludes = [])

import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('draftman2.py', base=base)
]

setup(name='Draftman2',
      version = '2.0b',
      description = 'foo',
      options = dict(build_exe = buildOptions),
      executables = executables)
