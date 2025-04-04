# from _config import getvar
from flask import Blueprint, request
from os.path import basename
from plugins.localcache import readlocalcache, writelocalcache
from plugins.zabbix import ZabbixObject
import time

''' Default
Provide basic pseudo-universal JSON reader at /default
'''

plugin_name = basename(__file__)[:-3]
host_key = "host"
plugin_prefix = ""
skip_keys = (host_key, )
time_keys = ("time", "when", "clock", "timestamp")

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
    # determine time:
    for _key in time_keys:
      _val = str(posted.get(_key, None))
      if _val:
        if "." in _val:
          clock, ns = _val.split(".")
        else:
          try:
            clock = int(_val)
            ns = 0
          except ValueError:
            pass
    if not clock and not ns:
      clock, ns = str(time.time()).split(".")
    # Loop through each JSON item. Special processing is recommended.
    for _key, _val in posted.items():
      if _key in skip_keys or _key in time_keys:
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
