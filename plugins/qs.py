from flask import Blueprint, request
from os.path import basename
from zabbix import ZabbixObject
import time

'''Query String
All data is posted to the HTTP Query String; no payloads are processed.
'''

plugin_name = basename(__file__)[:-3]
host_key = "host"
key_prefix = f"{plugin_name}."


blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["POST", "GET"])
def translate():
  host = request.args.get(host_key)
  if request.method == "POST":
    zbx = ZabbixObject()
    query_string = request.query_string.decode("utf-8")
    clock, ns = str(time.time()).split(".")
    if not host:
      return zbx.no_host(host_key, query_string)
    for _key, _val in request.args.items():
      # Skip the host's name; we already know it
      if _key == host_key:
        continue
      zbx.add_param(host, key_prefix, _key, str(_val), clock, ns)
    zbx.push()
    return f"{plugin_name} Blueprint [POST]"  # TODO: return meaningful data.
  # else it's a GET request
  return f"{plugin_name} Blueprint [GET]"  # TODO: Return last posted value.
# -- end translate()
