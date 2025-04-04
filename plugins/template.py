# from _config import getvar
from flask import Blueprint, request
from os.path import basename
from plugins.localcache import readlocalcache, writelocalcache
from plugins.zabbix import ZabbixObject
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
    datadict, result = zbx.push()
    qs = request.query_string.decode("utf-8")
    writelocalcache(plugin_name, host, qs, posted, datadict, result.json())
    return result.content
  # else it's a GET request
  host = request.args.get("host")  # Universal: {app_url}/{plugin_name}?host=
  return readlocalcache(plugin_name, host)
# -- end translate()
