from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': []}

base = 'gui'

executables = [
    Executable('gui.py', base=base)
]

setup(name='dev-activity-cx-freeze',
      version = '1.0',
      description = 'Development activity statistics build with cxfreeze',
      options = {'build_exe': build_options},
      executables = executables)
