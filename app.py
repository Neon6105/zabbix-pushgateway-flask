import profiles
from flask import Flask
from outputs.zabbix import blueprint as zabbix_blueprint
from outputs.cache import blueprint as cache_blueprint

app = Flask(__name__)

app.register_blueprint(zabbix_blueprint)
app.register_blueprint(cache_blueprint)

failed_profiles = 0
for profile in profiles.modules:
  try:
    app.register_blueprint(getattr(profiles, profile).blueprint)
  except AttributeError:
    # TODO: error handling
    print(f"\033[93mWARNING: Flask Blueprint not found for profile '{profile}'. Profile not loaded.\033[0m")
    failed_profiles = failed_profiles + 1
  else:
    # TODO: post-blueprint success tasks
    pass
  finally:
    # TODO: Per-module finally clause (not needed?)
    pass
print(f" * Profiles: {len(profiles.modules)} ({failed_profiles} not loaded)")

if __name__ == "__main__":
  app.run()
