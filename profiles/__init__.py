from os import listdir
from os.path import isfile, join, basename, dirname

profiles_dir = basename(dirname(__file__))  # or just "profiles"
skip_profiles = ("template", )

# Get *.py files except tuple(skip_profiles), and remove the .py extension.
modules = [f[:-3] for f in listdir(profiles_dir)
           if isfile(join(profiles_dir, f)) and
           f.endswith(".py") and
           f != "__init__.py" and
           f[:-3] not in skip_profiles
           ]

for module in modules:
  __import__(f"{profiles_dir}.{module}")
