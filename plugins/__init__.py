from _config import getvar
from os import listdir
from os.path import isfile, join  # basename, dirname
import json

plugins_dir = "plugins"  # or basename(dirname(__file__))

try:
  with open("plugins.json", "r") as f:
    conf = json.load(f)
except FileNotFoundError:
  conf = dict()
finally:
  skip_plugins = getvar("ZPG_SKIP_PLUGINS", default=("template", ))

# Get *.py files except tuple(skip_plugins), and remove the .py extension.
modules = [f[:-3] for f in listdir(plugins_dir)
           if isfile(join(plugins_dir, f)) and
           f.endswith(".py") and
           f != "__init__.py" and
           f[:-3] not in skip_plugins
           ]

for module in modules:
  __import__(f"{plugins_dir}.{module}")
