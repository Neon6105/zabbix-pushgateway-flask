from os import listdir
from os.path import isfile, join  # basename, dirname

plugins_dir = "plugins"  # or basename(dirname(__file__))
# List of plugins to skip. __init__.py is always skipped.
skip_plugins = ("__template", "file")

# Get *.py files except tuple(skip_plugins), and remove the .py extension.
modules = [f[:-3] for f in listdir(plugins_dir)
           if isfile(join(plugins_dir, f)) and
           f.endswith(".py") and
           f != "__init__.py" and
           f[:-3] not in skip_plugins
           ]

for module in modules:
  __import__(f"{plugins_dir}.{module}")
