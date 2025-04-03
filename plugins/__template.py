from flask import Blueprint, request
from os.path import basename
from zabbix import ZabbixObject
import time

''' Template
A breif description of what this plugin is supposed to do.
'''

# Edit this line to set a manual name for this plugin. Not recomended.
plugin_name = basename(__file__)[:-3]
# Whick key contains the host's name. Also used to set host via query string.
host_key = "host"
# Prefix all keys with this value. Set plugin_prefix = "" to disable.
plugin_prefix = f"{plugin_name}."
# Tuple of keys to ignore. Always ignore the host_key.
skip_keys = (host_key, )

''' Editing below this line should not be necessary for normal operation. '''

# Publish a Flask Blueprint for this plugin (used in app.py)
blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["POST", "GET"])
def translate():
  if request.method == "POST":
    zbx = ZabbixObject()
    posted = request.get_json()
    # Determine Zabbix {HOST.NAME}. Query String first, then JSON[host_key].
    if request.args.get(host_key):
      host = request.args.get(host_key)
    else:
      host = posted.get(host_key, None)
    # Host is still undetermined: fail.
    if not host:
      zbx.no_host(host_key)
    # Loop through each JSON item. Special processing is recommended.
    clock, ns = str(time.time()).split(".")
    for _key, _val in posted.items():
      if _key in skip_keys:
        continue
      zbx.add_param(host, plugin_prefix, _key, _val, clock, ns)
    # Publish the data to Zabbix API using the ZabbixObject.
    zbx.push()
    return f"{plugin_name} Blueprint [POST]"  # TODO: return meaningful data.
  # else it's a GET request
  return f"{plugin_name} Blueprint [GET]"  # TODO: Return last posted value.
# -- end translate()
