from flask import Blueprint, request
from os.path import basename
from outputs import Zabbix, readcache, writecache
import time

'''Query String
All data is posted to the HTTP Query String; no payloads are processed.
'''

plugin_name = basename(__file__)[:-3]
host_key = "host"
key_prefix = f"{plugin_name}."
skip_key = (host_key, )

blueprint = Blueprint(f"{plugin_name}", __name__)


@blueprint.route(f"/{plugin_name}", methods=["POST", "GET"])
def translate():
  host = request.args.get(host_key)
  if request.method == "POST":
    zbx = Zabbix()
    query_string = request.query_string.decode("utf-8")
    clock, ns = str(time.time()).split(".")
    if not host:
      return zbx.no_host(host_key, query_string)
    for _key, _val in request.args.items():
      # Skip the host's name; we already know it
      if _key in skip_key:
        continue
      zbx.add_param(host, key_prefix, _key, str(_val), clock, ns)
    json_out, result = zbx.push()
    qs = request.query_string.decode("utf-8")
    writecache(plugin_name, host, qs, None, json_out, result.json())
    return result.content
  # else it's a GET request
  host = request.args.get("host")
  return readcache(plugin_name, host)
# -- end translate()
