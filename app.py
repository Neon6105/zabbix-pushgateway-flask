import plugins
from flask import Flask

app = Flask(__name__)

failed_plugins = 0
for plugin in plugins.modules:
  try:
    app.register_blueprint(getattr(plugins, plugin).blueprint)
  except AttributeError:
    # TODO: error handling
    print(f"\033[93mWARNING: Flask Blueprint not found for plugin '{plugin}'. Plugin not loaded.\033[0m")
    failed_plugins = failed_plugins + 1
  else:
    # TODO: post-blueprint success tasks
    pass
  finally:
    # TODO: Per-module finally clause (not needed?)
    pass
print(f" * Plugins: {len(plugins.modules)} ({failed_plugins} not loaded)")

if __name__ == "__main__":
  app.run()
